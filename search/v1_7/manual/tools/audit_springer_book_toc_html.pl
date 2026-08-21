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

my ($input, $entries_output, $summary_output, $expected_year, $expected_metadata_count);
GetOptions(
    'input=s'                   => \$input,
    'entries-output=s'          => \$entries_output,
    'summary-output=s'          => \$summary_output,
    'expected-year=s'           => \$expected_year,
    'expected-metadata-count=i' => \$expected_metadata_count,
) or die "Invalid arguments\n";
die "Required arguments are missing\n"
    unless defined $input && defined $entries_output && defined $summary_output
        && defined $expected_year && defined $expected_metadata_count;

sub clean {
    my ($value) = @_;
    $value //= '';
    $value = NFC($value);
    $value =~ s/\x{a0}/ /g;
    $value =~ s/\x{fffd}/ /g;
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
die "Not a Springer book page\n"
    unless $document_title =~ /Springer/i && $page_text =~ /REFSQ/i;
die "Expected year not observable in controlled HTML\n"
    unless $page_text =~ /\b\Q$expected_year\E\b/;

my ($canonical_node) = $tree->look_down(sub {
    lc($_[0]->tag // '') eq 'link' && lc($_[0]->attr('rel') // '') eq 'canonical'
});
my $canonical_url = $canonical_node ? clean($canonical_node->attr('href')) : '';
my ($isbn) = $canonical_url =~ m{/book/10\.1007/(97[89]-[0-9-]+)$};
$isbn = clean($isbn // '');

my @cards = $tree->look_down(sub { has_class($_[0], 'app-card-open') });
my @items;
for my $card (@cards) {
    my ($heading) = $card->look_down(sub { has_class($_[0], 'app-card-open__heading') });
    next unless $heading;
    my $title = clean($heading->as_text);
    my $is_editorial = lc($title) eq 'front matter' ? 1 : 0;
    my ($title_link) = $heading->look_down(_tag => 'a');
    my $locator = clean($title_link ? $title_link->attr('href') : '');
    if (!$locator && $is_editorial) {
        my ($pdf_link) = $card->look_down(sub {
            lc($_[0]->tag // '') eq 'a' && has_class($_[0], 'c-pdf-chapter-download__link')
        });
        $locator = clean($pdf_link ? $pdf_link->attr('href') : '');
    }
    my $doi = '';
    $doi = lc($1) if $locator =~ m{/chapter/(10\.1007/[^?#]+)}i;
    my ($authors_node) = $card->look_down(sub { has_class($_[0], 'app-author-list') });
    my $authors = clean($authors_node ? $authors_node->as_text : '');
    $authors =~ s/\s*,\s*/; /g;
    my ($pages_node) = $card->look_down(sub {
        lc($_[0]->attr('data-test') // '') eq 'page-number'
    });
    my $pages = clean($pages_node ? $pages_node->as_text : '');
    $pages =~ s/^Pages\s+//i;
    push @items, {
        ItemType => $is_editorial ? 'editorial' : 'paper',
        Title => $title,
        Authors => $authors,
        DOI => $doi,
        Year => $expected_year,
        Pages => $pages,
        Locator => $locator,
        Section => '',
        IsEditorial => $is_editorial ? 'true' : 'false',
    };
}

my @next_links = $tree->look_down(sub {
    lc($_[0]->tag // '') eq 'a'
        && (lc($_[0]->attr('data-test') // '') eq 'next-page'
            || lc($_[0]->attr('aria-label') // '') =~ /^page\s+2$/)
});
my $has_uncaptured_pagination = @next_links ? 1 : 0;
my $research_count = scalar grep { $_->{IsEditorial} eq 'false' } @items;
my $editorial_count = scalar(@items) - $research_count;
my %doi_counts;
$doi_counts{$_->{DOI}}++ for grep { length $_->{DOI} } @items;
my $duplicate_dois = scalar grep { $doi_counts{$_} > 1 } keys %doi_counts;
my $incomplete_research = scalar grep {
    $_->{IsEditorial} eq 'false' && (!length($_->{Title}) || !length($_->{Locator}) || !length($_->{DOI}))
} @items;
my $count_matches = $research_count == $expected_metadata_count;
my $complete = !$has_uncaptured_pagination && $count_matches
    && !$duplicate_dois && !$incomplete_research;

my @columns = qw(EntryOrdinal ItemType Title Authors DOI Year Pages Locator Section IsEditorial);
my $csv = Text::CSV->new({binary => 1, eol => "\n"}) or die Text::CSV->error_diag;
open my $out, '>:encoding(UTF-8)', $entries_output or die "Cannot write $entries_output: $!\n";
$csv->say($out, \@columns) or die $csv->error_diag;
for my $index (0 .. $#items) {
    my $item = $items[$index];
    $csv->say($out, [$index + 1, @{$item}{qw(ItemType Title Authors DOI Year Pages Locator Section IsEditorial)}])
        or die $csv->error_diag;
}
close $out or die "Cannot close $entries_output: $!\n";

my $summary = {
    SourceFilename => ($input =~ m{([^/]+)$} ? $1 : $input),
    SHA256 => $source_sha256,
    Platform => 'Springer Nature Link',
    DocumentTitle => $document_title,
    CanonicalURL => $canonical_url,
    ISBN => $isbn,
    ExtractedItemCount => scalar(@items),
    ResearchItemCount => $research_count,
    EditorialItemCount => $editorial_count,
    ExpectedMetadataRecordCount => $expected_metadata_count,
    CountMatchesExpected => $count_matches ? JSON::PP::true : JSON::PP::false,
    DuplicateDOICount => $duplicate_dois,
    IncompleteResearchItemCount => $incomplete_research,
    HasUncapturedPagination => $has_uncaptured_pagination ? JSON::PP::true : JSON::PP::false,
    HTMLCompletenessStatus => $complete ? 'COMPLETE_TOC' : 'PARTIAL_TOC',
    HTMLTreeBuilderVersion => $HTML::TreeBuilder::VERSION,
    TextCSVVersion => $Text::CSV::VERSION,
};
open my $summary_fh, '>:encoding(UTF-8)', $summary_output
    or die "Cannot write $summary_output: $!\n";
print {$summary_fh} JSON::PP->new->canonical(1)->pretty(1)->encode($summary);
close $summary_fh or die "Cannot close $summary_output: $!\n";
$tree->delete;
