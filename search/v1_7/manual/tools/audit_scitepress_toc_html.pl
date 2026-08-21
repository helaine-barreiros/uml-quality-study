#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use Digest::SHA qw(sha256_hex);
use Encode qw(decode FB_CROAK);
use Getopt::Long qw(GetOptions);
use HTML::TreeBuilder;
use JSON::PP;
use Text::CSV;
use Unicode::Normalize qw(NFC);

my ($input, $entries_output, $summary_output, $expected_year, $expected_count);
GetOptions(
    'input=s'          => \$input,
    'entries-output=s' => \$entries_output,
    'summary-output=s' => \$summary_output,
    'expected-year=s'  => \$expected_year,
    'expected-count=i' => \$expected_count,
) or die "Invalid arguments\n";
die "Missing --input\n" unless defined $input;
die "Missing --entries-output\n" unless defined $entries_output;
die "Missing --summary-output\n" unless defined $summary_output;
die "Missing --expected-year\n" unless defined $expected_year;

sub clean {
    my ($value) = @_;
    $value //= '';
    $value = NFC($value);
    $value =~ s/\x{a0}/ /g;
    $value =~ s/\s+/ /g;
    $value =~ s/^\s+|\s+$//g;
    return $value;
}

sub has_class {
    my ($element, $wanted) = @_;
    return 0 unless ref $element;
    return ($element->attr('class') // '') =~ /(?:^|\s)\Q$wanted\E(?:\s|$)/;
}

open my $fh, '<:raw', $input or die "Cannot read $input: $!\n";
my $bytes = do { local $/; <$fh> };
close $fh or die "Cannot close $input: $!\n";
my $source_sha256 = sha256_hex($bytes);
my $html = eval { decode('UTF-8', $bytes, FB_CROAK) };
$html = decode('Windows-1252', $bytes) unless defined $html;
my $tree = HTML::TreeBuilder->new;
$tree->parse_content($html);

my ($title_node) = $tree->look_down(_tag => 'title');
my $document_title = clean($title_node ? $title_node->as_text : '');
my $page_text = clean($tree->as_text);
die "Expected year not observable in controlled HTML\n" unless $page_text =~ /\b\Q$expected_year\E\b/;
die "Not a SCITEPRESS proceedings details page\n"
    unless $html =~ /ProceedingsDetails\.aspx/i && $page_text =~ /MODELSWARD/i;

my ($canonical_node) = $tree->look_down(
    sub { lc($_[0]->tag // '') eq 'link' && lc($_[0]->attr('rel') // '') eq 'canonical' }
);
my $canonical_url = $canonical_node ? clean($canonical_node->attr('href')) : '';
if (!length $canonical_url && $html =~ m{https://www\.scitepress\.org/ProceedingsDetails\.aspx\?[^"'<>\s]+}i) {
    $canonical_url = $&;
    $canonical_url =~ s/&amp;/&/g;
}
my ($isbn) = $page_text =~ /ISBN:\s*([0-9-]{10,20})/i;
$isbn = clean($isbn // '');

my ($pane) = $tree->look_down(id => 'ContentPlaceHolder1_ProceedingsDetailsPage_ProceedingsDetailsSummary_panePapers');
die "Missing local SCITEPRESS papers pane\n" unless $pane;
my @title_nodes = $pane->look_down(sub { has_class($_[0], 'ProceedingIndexPaperTitle') });
my @items;
for my $title_container (@title_nodes) {
    my ($title_link) = $title_container->look_down(sub { has_class($_[0], 'LabelSearchPublicationTitle') });
    next unless $title_link;
    my $title = clean($title_link->as_text);
    my $record = $title_container->parent;
    my ($pages_node) = $record->look_down(sub { has_class($_[0], 'ProceedingsIndexPages') });
    my $pages = clean($pages_node ? $pages_node->as_text : '');
    $pages =~ s/^P\.\s*//i;
    my @authors;
    for my $author_node ($record->look_down(sub {
        has_class($_[0], 'PublicationsDetailNormal')
            && (($_[0]->attr('id') // '') =~ /LabelAuthor_/)
    })) {
        my $author = clean($author_node->as_text);
        push @authors, $author if length $author;
    }
    my ($doi_node) = $record->look_down(sub { has_class($_[0], 'ProceedingsIndexDoi') });
    my $doi = clean($doi_node ? $doi_node->as_text : '');
    $doi =~ s!^(?:DOI:\s*|https?://(?:dx\.)?doi\.org/)!!i;
    push @items, {
        ItemType => 'paper', Title => $title, Authors => join('; ', @authors),
        DOI => lc($doi), Year => $expected_year, Pages => $pages,
        Locator => clean($title_link->attr('href')), Section => '', IsEditorial => 'false',
    };
}

my %doi_counts;
$doi_counts{$_->{DOI}}++ for grep { length $_->{DOI} } @items;
my $duplicate_dois = scalar grep { $doi_counts{$_} > 1 } keys %doi_counts;
my $incomplete_items = scalar grep { !length($_->{Title}) || !length($_->{Locator}) } @items;
my ($page_size_select) = $pane->look_down(
    sub { lc($_[0]->tag // '') eq 'select' && (($_[0]->attr('id') // '') =~ /DropDownListProceedings$/) }
);
my $selected_page_size = '';
if ($page_size_select) {
    my ($selected) = $page_size_select->look_down(sub {
        lc($_[0]->tag // '') eq 'option' && defined($_[0]->attr('selected'))
    });
    $selected_page_size = clean($selected ? $selected->as_text : '');
}
my $count_matches = defined($expected_count) ? scalar(@items) == $expected_count : 0;
my $complete = defined($expected_count) && $count_matches && !$duplicate_dois && !$incomplete_items;

my @columns = qw(EntryOrdinal ItemType Title Authors DOI Year Pages Locator Section IsEditorial);
my $csv = Text::CSV->new({binary => 1, eol => "\n"}) or die "Cannot initialize Text::CSV\n";
open my $out, '>:encoding(UTF-8)', $entries_output or die "Cannot write $entries_output: $!\n";
$csv->print($out, \@columns) or die "Cannot write CSV header\n";
for my $index (0 .. $#items) {
    my $item = $items[$index];
    $csv->print($out, [$index + 1, @{$item}{qw(ItemType Title Authors DOI Year Pages Locator Section IsEditorial)}])
        or die "Cannot write CSV item " . ($index + 1) . "\n";
}
close $out or die "Cannot close $entries_output: $!\n";

my $summary = {
    SourceFilename => ($input =~ m{([^/]+)$} ? $1 : $input), SHA256 => $source_sha256,
    Platform => 'SCITEPRESS', DocumentTitle => $document_title, CanonicalURL => $canonical_url,
    ISBN => $isbn, ExtractedItemCount => scalar(@items), ExpectedItemCount => $expected_count,
    ResearchItemCount => scalar(@items), EditorialItemCount => 0,
    DuplicateDOICount => $duplicate_dois, IncompleteItemCount => $incomplete_items,
    SelectedPageSize => $selected_page_size, CountMatchesExpected => $count_matches ? JSON::PP::true : JSON::PP::false,
    HTMLCompletenessStatus => $complete ? 'COMPLETE_TOC' : 'PARTIAL_TOC',
    HTMLTreeBuilderVersion => $HTML::TreeBuilder::VERSION, TextCSVVersion => $Text::CSV::VERSION,
};
open my $summary_fh, '>:encoding(UTF-8)', $summary_output or die "Cannot write $summary_output: $!\n";
print {$summary_fh} JSON::PP->new->canonical(1)->pretty(1)->encode($summary);
close $summary_fh or die "Cannot close $summary_output: $!\n";
$tree->delete;
