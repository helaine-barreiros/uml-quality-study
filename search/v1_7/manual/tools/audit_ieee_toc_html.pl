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

my ($input, $entries_output, $summary_output);
GetOptions(
    'input=s'          => \$input,
    'entries-output=s' => \$entries_output,
    'summary-output=s' => \$summary_output,
) or die "Invalid arguments\n";
die "Missing --input\n" unless defined $input;
die "Missing --entries-output\n" unless defined $entries_output;
die "Missing --summary-output\n" unless defined $summary_output;

sub read_bytes {
    my ($path) = @_;
    open my $fh, '<:raw', $path or die "Cannot read $path: $!\n";
    return do { local $/; <$fh> };
}

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
    my $class = $element->attr('class') // '';
    return $class =~ /(?:^|\s)\Q$wanted\E(?:\s|$)/;
}

sub first_ancestor_with_class {
    my ($element, $wanted) = @_;
    my $current = $element;
    while ($current) {
        return $current if has_class($current, $wanted);
        $current = $current->parent;
    }
    return;
}

my $bytes = read_bytes($input);
my $sha256 = sha256_hex($bytes);
my $html_text = eval { decode('UTF-8', $bytes, FB_CROAK) };
$html_text = decode('Windows-1252', $bytes) unless defined $html_text;
my $tree = HTML::TreeBuilder->new;
$tree->parse_content($html_text);

my ($title_element) = $tree->look_down(_tag => 'title');
my $document_title = clean($title_element ? $title_element->as_text : '');
my ($canonical_element) = $tree->look_down(
    sub {
        my $element = shift;
        return lc($element->tag // '') eq 'link'
            && lc($element->attr('rel') // '') eq 'canonical';
    }
);
my $canonical_url = $canonical_element ? clean($canonical_element->attr('href')) : '';

my $platform = '';
$platform = 'IEEE_XPLORE' if $canonical_url =~ m{ieeexplore\.ieee\.org}i;
$platform = 'IEEE_CSDL' if $canonical_url =~ m{computer\.org/csdl}i;

my @items;
if ($platform eq 'IEEE_XPLORE') {
    my @containers = $tree->look_down(
        sub { has_class($_[0], 'List-results-items') }
    );
    for my $container (@containers) {
        my ($desktop) = $container->look_down(
            sub { has_class($_[0], 'hide-mobile') }
        );
        $desktop //= $container;
        my ($heading) = $desktop->look_down(_tag => 'h2');
        next unless $heading;
        my ($title_link) = $heading->look_down(_tag => 'a');
        my $title = clean($heading->as_text);
        next unless length $title;
        my @authors;
        my @author_paragraphs = $desktop->look_down(
            sub { has_class($_[0], 'author') }
        );
        for my $paragraph (@author_paragraphs) {
            for my $anchor ($paragraph->look_down(_tag => 'a')) {
                my $href = $anchor->attr('href') // '';
                push @authors, clean($anchor->as_text) if $href =~ m{/author/};
            }
        }
        my $visible = clean($desktop->as_text);
        my ($year) = $visible =~ /Publication Year:\s*(\d{4})/;
        my ($start, $end) = $visible =~ /Page\(s\):\s*([^\s,]+)\s*-\s*([^\s,]+)/;
        push @items, {
            Title => $title,
            Authors => join('; ', @authors),
            Year => $year // '',
            Pages => defined($start) ? "$start-$end" : '',
            Locator => $title_link ? clean($title_link->attr('href')) : '',
        };
    }
} elsif ($platform eq 'IEEE_CSDL') {
    my @title_links = $tree->look_down(
        sub { lc($_[0]->tag // '') eq 'a' && has_class($_[0], 'article-title') }
    );
    for my $title_link (@title_links) {
        my $container = first_ancestor_with_class($title_link, 'article-list-item');
        next unless $container;
        my $title = clean($title_link->as_text);
        next unless length $title;
        my @authors;
        my @author_blocks = $container->look_down(
            sub { has_class($_[0], 'article-authors') }
        );
        for my $block (@author_blocks) {
            push @authors, map { clean($_->as_text) } $block->look_down(_tag => 'a');
        }
        my $visible = clean($container->as_text);
        my ($start, $end) = $visible =~ /pp\.\s*([^\s,]+)\s*-\s*([^\s,]+)/i;
        my ($year) = $document_title =~ /\b(20\d{2})\b/;
        push @items, {
            Title => $title,
            Authors => join('; ', grep { length } @authors),
            Year => $year // '',
            Pages => defined($start) ? "$start-$end" : '',
            Locator => clean($title_link->attr('href')),
        };
    }
}

my $page_text = clean($tree->as_text);
my ($shown_start, $shown_end, $reported_total);
if ($platform eq 'IEEE_XPLORE') {
    ($shown_start, $shown_end, $reported_total) =
        $page_text =~ /Showing\s+(\d+)\s*-\s*(\d+)\s+of\s+(\d+)/i;
} elsif ($platform eq 'IEEE_CSDL') {
    ($shown_end, $reported_total) =
        $page_text =~ /Showing\s+(\d+)\s+out\s+of\s+(\d+)/i;
    $shown_start = defined($shown_end) ? 1 : undef;
}
my $complete = @items
    && defined($reported_total)
    && $reported_total == scalar(@items)
    && (!defined($shown_start) || $shown_start == 1)
    && (!defined($shown_end) || $shown_end == $reported_total);

my ($proceedings_doi) = $bytes =~ m{https?://doi\.org/(10\.1109/[A-Za-z0-9_.()-]+)}i;
my ($isbn) = $page_text =~ /ISBN:\s*([0-9Xx-]{10,})/i;
my $proceedings_title = $document_title;
$proceedings_title =~ s/\s+-\s+(?:Conference )?Table of Contents.*$//i;
$proceedings_title =~ s/\s+\|\s+IEEE.*$//i;

my $csv = Text::CSV->new({binary => 1, eol => "\n"})
    or die "Cannot initialize Text::CSV\n";
open my $entries_fh, '>:encoding(UTF-8)', $entries_output
    or die "Cannot write $entries_output: $!\n";
my @columns = qw(EntryOrdinal Title Authors Year Pages Locator);
$csv->print($entries_fh, \@columns) or die "Cannot write CSV header\n";
for my $index (0 .. $#items) {
    my $item = $items[$index];
    $csv->print($entries_fh, [
        $index + 1, @{$item}{qw(Title Authors Year Pages Locator)}
    ]) or die "Cannot write CSV item " . ($index + 1) . "\n";
}
close $entries_fh or die "Cannot close $entries_output: $!\n";

my %title_counts;
$title_counts{$_->{Title}}++ for @items;
my $summary = {
    SourceFilename => ($input =~ m{([^/]+)$} ? $1 : $input),
    SHA256 => $sha256,
    Platform => $platform,
    DocumentTitle => $document_title,
    ProceedingsTitle => $proceedings_title,
    CanonicalURL => $canonical_url,
    ProceedingsDOI => $proceedings_doi // '',
    ISBN => $isbn // '',
    ExtractedItemCount => scalar(@items),
    ReportedItemCount => $reported_total // 0,
    ShowingStart => $shown_start // 0,
    ShowingEnd => $shown_end // 0,
    DuplicateTitleCount => scalar(grep { $title_counts{$_} > 1 } keys %title_counts),
    HTMLCompletenessStatus => $complete ? 'COMPLETE_TOC' : 'PARTIAL_TOC',
    HTMLTreeBuilderVersion => $HTML::TreeBuilder::VERSION,
    TextCSVVersion => $Text::CSV::VERSION,
};
open my $summary_fh, '>:encoding(UTF-8)', $summary_output
    or die "Cannot write $summary_output: $!\n";
print {$summary_fh} JSON::PP->new->canonical(1)->pretty(1)->encode($summary);
close $summary_fh or die "Cannot close $summary_output: $!\n";
$tree->delete;
die "Unsupported or incomplete IEEE TOC HTML\n" unless $complete;
