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

my ($input, $entries_output, $summary_output, $expected_year, $expected_venue);
GetOptions(
    'input=s'          => \$input,
    'entries-output=s' => \$entries_output,
    'summary-output=s' => \$summary_output,
    'expected-year=s'  => \$expected_year,
    'expected-venue=s' => \$expected_venue,
) or die "Invalid arguments\n";
die "Missing --input\n" unless defined $input;
die "Missing --entries-output\n" unless defined $entries_output;
die "Missing --summary-output\n" unless defined $summary_output;
die "Missing --expected-year\n" unless defined $expected_year;
die "Missing --expected-venue\n" unless defined $expected_venue;

sub clean {
    my ($value) = @_;
    $value //= '';
    $value = NFC($value);
    $value =~ s/\x{a0}/ /g;
    $value =~ s/\s+/ /g;
    $value =~ s/^\s+|\s+$//g;
    return $value;
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
die "Expected venue not observable in controlled HTML\n"
    unless $page_text =~ /\Q$expected_venue\E/i || $document_title =~ /\Q$expected_venue\E/i;
die "Expected year not observable in controlled HTML\n" unless $page_text =~ /\b\Q$expected_year\E\b/;

my ($canonical_node) = $tree->look_down(
    sub { lc($_[0]->tag // '') eq 'link' && lc($_[0]->attr('rel') // '') eq 'canonical' }
);
my $canonical_url = $canonical_node ? clean($canonical_node->attr('href')) : '';
my @anchors = $tree->look_down(_tag => 'a');
my @technical_program_links = grep {
    clean($_->as_text) =~ /technical\s+program/i || clean($_->attr('href')) =~ /technicalprogram/i
} @anchors;
my @accepted_links = grep { clean($_->as_text) =~ /accepted\s+papers/i } @anchors;
my @publisher_record_links = grep {
    clean($_->attr('href')) =~ m{(?:PublicationsDetail\.aspx|doi\.org/)}i
} @anchors;
my @citation_titles = $tree->look_down(
    sub { lc($_[0]->tag // '') eq 'meta' && lc($_[0]->attr('name') // '') eq 'citation_title' }
);

my $item_count = scalar(@publisher_record_links) + scalar(@citation_titles);
my $granularity = $item_count ? 'UNRESOLVED' : 'EVENT_LEVEL';
my $completeness = $item_count ? 'UNRESOLVED' : 'LANDING_PAGE_ONLY';

my @columns = qw(EntryOrdinal Title Authors Locator Section);
my $csv = Text::CSV->new({binary => 1, eol => "\n"}) or die "Cannot initialize Text::CSV\n";
open my $out, '>:encoding(UTF-8)', $entries_output or die "Cannot write $entries_output: $!\n";
$csv->print($out, \@columns) or die "Cannot write CSV header\n";
close $out or die "Cannot close $entries_output: $!\n";

my $summary = {
    SourceFilename => ($input =~ m{([^/]+)$} ? $1 : $input),
    SHA256 => $source_sha256, Platform => 'SCITEVENTS',
    DocumentTitle => $document_title, CanonicalURL => $canonical_url,
    EvidenceRole => 'VENUE_CROSSCHECK', CrosscheckGranularity => $granularity,
    HTMLCompletenessStatus => $completeness,
    LocallyMaterializedPaperItemCount => $item_count,
    TechnicalProgramLinkCount => scalar(@technical_program_links),
    AcceptedPapersLinkCount => scalar(@accepted_links),
    RemoteJavaScriptExecuted => JSON::PP::false,
    HTMLTreeBuilderVersion => $HTML::TreeBuilder::VERSION,
    TextCSVVersion => $Text::CSV::VERSION,
};
open my $summary_fh, '>:encoding(UTF-8)', $summary_output
    or die "Cannot write $summary_output: $!\n";
print {$summary_fh} JSON::PP->new->canonical(1)->pretty(1)->encode($summary);
close $summary_fh or die "Cannot close $summary_output: $!\n";
$tree->delete;
