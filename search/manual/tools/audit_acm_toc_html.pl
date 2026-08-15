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

my ($input, $entries_output, $summary_output, $expected_year);
GetOptions(
    'input=s'          => \$input,
    'entries-output=s' => \$entries_output,
    'summary-output=s' => \$summary_output,
    'expected-year=s'  => \$expected_year,
) or die "Invalid arguments\n";
die "Missing --input\n" unless defined $input;
die "Missing --entries-output\n" unless defined $entries_output;
die "Missing --summary-output\n" unless defined $summary_output;
die "Missing --expected-year\n" unless defined $expected_year;

sub clean {
    my ($value) = @_;
    $value //= '';
    $value = NFC($value);
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

my ($canonical_node) = $tree->look_down(
    sub { lc($_[0]->tag // '') eq 'link' && lc($_[0]->attr('rel') // '') eq 'canonical' }
);
my $canonical_url = $canonical_node ? clean($canonical_node->attr('href')) : '';
my ($publication_doi_node) = $tree->look_down(
    sub { lc($_[0]->tag // '') eq 'meta' && lc($_[0]->attr('name') // '') eq 'publication_doi' }
);
my $proceedings_doi = $publication_doi_node ? clean($publication_doi_node->attr('content')) : '';
my ($title_node) = $tree->look_down(_tag => 'title');
my $document_title = clean($title_node ? $title_node->as_text : '');
my $page_text = clean($tree->as_text);
die "Expected year not observable in controlled HTML\n" unless $page_text =~ /\b\Q$expected_year\E\b/;
die "Not an ACM proceedings page\n"
    unless $canonical_url =~ m{/doi/proceedings/}i && length $proceedings_doi;

my ($toc) = $tree->look_down(id => 'tableOfContent');
die "Missing local ACM table of contents\n" unless $toc;
my @items;
my ($front_matter_link) = $tree->look_down(
    sub {
        lc($_[0]->tag // '') eq 'a'
            && (($_[0]->attr('title') // '') =~ /^Front matter\b/i)
    }
);
if ($front_matter_link) {
    push @items, {
        ItemType => 'front-matter',
        Title => clean($front_matter_link->attr('title') || $front_matter_link->as_text),
        Authors => '', DOI => '', Year => $expected_year, Pages => '',
        Locator => clean($front_matter_link->attr('href')), Section => 'Front matter',
        IsEditorial => 'true',
    };
}

for my $container ($toc->look_down(sub { has_class($_[0], 'issue-item-container') })) {
    my ($title_link) = $container->look_down(
        sub { lc($_[0]->tag // '') eq 'a' && has_class($_[0], 'issue-item__title') }
    );
    if (!$title_link) {
        my ($heading) = $container->look_down(sub { has_class($_[0], 'issue-item__title') });
        ($title_link) = $heading ? $heading->look_down(_tag => 'a') : ();
    }
    next unless $title_link;
    my $title = clean($title_link->as_text);
    next unless length $title;
    my ($type_node) = $container->look_down(sub { has_class($_[0], 'issue-heading') });
    my ($authors_node) = $container->look_down(
        sub { lc($_[0]->tag // '') eq 'ul' && lc($_[0]->attr('aria-label') // '') eq 'authors' }
    );
    my @authors;
    if ($authors_node) {
        for my $author_link ($authors_node->look_down(_tag => 'a')) {
            my $name = clean($author_link->attr('title') || $author_link->as_text);
            push @authors, $name if length $name;
        }
    }
    my ($doi_node) = $container->look_down(sub { has_class($_[0], 'issue-item__doi') });
    my $doi = clean($doi_node ? $doi_node->as_text : '');
    $doi =~ s!^https?://(?:doi-org[^/]*|doi\.org)/!!i;
    my $visible = clean($container->as_text);
    my ($pages) = $visible =~ /Pages?\s+([^\s]+(?:\s*[–-]\s*[^\s]+)?)/i;
    my $section = '';
    my $parent = $container->parent;
    while ($parent) {
        my ($section_node) = $parent->look_down(
            sub { has_class($_[0], 'section__title') && (($_[0]->attr('id') // '') =~ /^sec\d+$/) }
        );
        if ($section_node) { $section = clean($section_node->as_text); last; }
        $parent = $parent->parent;
    }
    push @items, {
        ItemType => lc clean($type_node ? $type_node->as_text : 'document'),
        Title => $title, Authors => join('; ', @authors), DOI => $doi,
        Year => $expected_year, Pages => clean($pages // ''),
        Locator => clean($title_link->attr('href')), Section => $section,
        IsEditorial => 'false',
    };
}

my @research = grep { $_->{IsEditorial} eq 'false' } @items;
my %doi_counts;
$doi_counts{$_->{DOI}}++ for grep { length $_->{DOI} } @research;
my @load_more_nodes = $toc->look_down(
    sub { clean($_[0]->as_text) =~ /^load more$/i || has_class($_[0], 'load-more') }
);
my $load_more = scalar @load_more_nodes;
my $incomplete_research = scalar grep {
    !length($_->{Title}) || !length($_->{DOI}) || !length($_->{Locator})
} @research;
my $duplicate_dois = scalar grep { $doi_counts{$_} > 1 } keys %doi_counts;
my $complete = @research && !$load_more && !$incomplete_research && !$duplicate_dois;

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
    SourceFilename => ($input =~ m{([^/]+)$} ? $1 : $input),
    SHA256 => $source_sha256, Platform => 'ACM_DL',
    DocumentTitle => $document_title, CanonicalURL => $canonical_url,
    ProceedingsDOI => $proceedings_doi, ExtractedItemCount => scalar(@items),
    ResearchItemCount => scalar(@research), EditorialItemCount => scalar(@items) - scalar(@research),
    DuplicateDOICount => scalar(grep { $doi_counts{$_} > 1 } keys %doi_counts),
    DynamicOrPaginationMarkerCount => $load_more,
    HTMLCompletenessStatus => $complete ? 'COMPLETE_TOC' : 'PARTIAL_TOC',
    HTMLTreeBuilderVersion => $HTML::TreeBuilder::VERSION,
    TextCSVVersion => $Text::CSV::VERSION,
};
open my $summary_fh, '>:encoding(UTF-8)', $summary_output
    or die "Cannot write $summary_output: $!\n";
print {$summary_fh} JSON::PP->new->canonical(1)->pretty(1)->encode($summary);
close $summary_fh or die "Cannot close $summary_output: $!\n";
$tree->delete;
die "Incomplete ACM TOC HTML\n" unless $complete;
