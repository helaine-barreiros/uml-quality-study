#!/usr/bin/env perl
use strict;
use warnings;
use utf8;

use Digest::SHA qw(sha256_hex);
use Encode qw(decode);
use Getopt::Long qw(GetOptions);
use HTML::TreeBuilder;
use JSON::PP;
use Text::CSV;
use Unicode::Normalize qw(NFC);

my ($input, $entries_output, $audit_output, $unit_id, $year, $track);
GetOptions(
    'input=s'          => \$input,
    'entries-output=s' => \$entries_output,
    'audit-output=s'   => \$audit_output,
    'unit-id=s'        => \$unit_id,
    'year=s'           => \$year,
    'track=s'          => \$track,
) or die "Invalid arguments\n";
die "Required arguments are missing\n"
    unless $input && $entries_output && $audit_output && $unit_id && $year && $track;

open my $source_fh, '<:raw', $input or die "Cannot read $input: $!\n";
local $/;
my $bytes = <$source_fh>;
close $source_fh or die "Cannot close $input: $!\n";

my $tree = HTML::TreeBuilder->new;
$tree->parse_content(decode('UTF-8', $bytes, 1));

sub visible_text {
    my ($node) = @_;
    my $value = NFC($node ? $node->as_text : '');
    $value =~ s/\s+/ /g;
    $value =~ s/^\s+|\s+$//g;
    return $value;
}

my ($title_node) = $tree->look_down(_tag => 'title');
my $document_title = visible_text($title_node);
my $observed_url = '';
for my $link ($tree->look_down(_tag => 'link')) {
    if (lc($link->attr('rel') // '') eq 'canonical' && ($link->attr('href') // '') ne '') {
        $observed_url = $link->attr('href');
        last;
    }
}
if (!$observed_url) {
    for my $meta ($tree->look_down(_tag => 'meta')) {
        if (lc($meta->attr('property') // '') eq 'og:url' && ($meta->attr('content') // '') ne '') {
            $observed_url = $meta->attr('content');
            last;
        }
    }
}

my @records;
my $layout = '';
my $raw_record_count = 0;
my $parse_failure_count = 0;

my @numbered_paragraphs = grep { visible_text($_) =~ /^\d+:/ } $tree->look_down(_tag => 'p');
if (@numbered_paragraphs) {
    $layout = 'ACCEPTED_PAPER_LIST';
    for my $paragraph (@numbered_paragraphs) {
        my $text = visible_text($paragraph);
        my ($authors, $paper_title) = ('', '');
        if ($text =~ /^\d+:\s*(.*?)\s+“(.*)”\s*$/s) {
            ($authors, $paper_title) = ($1, $2);
        }
        elsif ($text =~ /^\d+:\s*(.*?)\s+"(.*)"?\s*$/s) {
            ($authors, $paper_title) = ($1, $2);
            $paper_title =~ s/"$//;
        }
        else {
            $parse_failure_count++;
        }
        $authors =~ s/\s*,\s*/; /g;
        push @records, {
            Title       => NFC($paper_title),
            Authors     => NFC($authors),
            Track       => 'Accepted Papers',
            Locator     => '',
            RecordKind  => 'ACCEPTED_PAPER',
            ParseStatus => $paper_title ? 'PARSE_OK' : 'PARSE_UNRESOLVED',
            DisplayText => NFC($text),
        };
    }
}
else {
    $layout = 'PROGRAM_TRACK_PAGE';
    my @event_rows = $tree->look_down(sub { defined $_[0]->attr('data-slot-id') });
    $raw_record_count = scalar @event_rows;
    my %seen;
    for my $row (@event_rows) {
        my ($event_link) = $row->look_down(sub { defined $_[0]->attr('data-event-modal') });
        next unless $event_link;
        my $paper_title = visible_text($event_link);
        my ($track_node) = $row->look_down(sub {
            (($_[0]->attr('class') // '') =~ /(?:^|\s)prog-track(?:\s|$)/)
        });
        my ($performers_node) = $row->look_down(sub {
            (($_[0]->attr('class') // '') =~ /(?:^|\s)performers(?:\s|$)/)
        });
        my @authors;
        if ($performers_node) {
            @authors = map { visible_text($_) }
                grep { (($_->attr('href') // '') =~ m{/profile/}) }
                $performers_node->look_down(_tag => 'a');
        }
        my $authors = join('; ', @authors);
        my $record_track = visible_text($track_node);
        my $locator = $event_link->attr('href') // '';
        my $key = join("\x1e", $paper_title, $authors, $record_track);
        next if $seen{$key}++;
        push @records, {
            Title       => $paper_title,
            Authors     => $authors,
            Track       => $record_track,
            Locator     => $locator,
            RecordKind  => 'PROGRAM_EVENT',
            ParseStatus => $paper_title ? 'PARSE_OK' : 'PARSE_UNRESOLVED',
            DisplayText => $paper_title,
        };
        $parse_failure_count++ unless $paper_title;
    }
}
$raw_record_count ||= scalar @numbered_paragraphs;

if (!$observed_url) {
    for my $anchor ($tree->look_down(_tag => 'a')) {
        my $href = $anchor->attr('href') // '';
        next unless $href =~ m{^https://conf\.researchr\.org/(?:attending|track)/RE-\d{4}/};
        if (($layout eq 'ACCEPTED_PAPER_LIST' && $href =~ m{/Accepted#?$})
            || ($layout eq 'PROGRAM_TRACK_PAGE' && $href =~ m{(?:-|/)(?:Research-Papers|workshops)#?$}i)) {
            $href =~ s/#$//;
            $observed_url = $href;
            last;
        }
    }
}

my $granularity = $layout eq 'ACCEPTED_PAPER_LIST' ? 'ITEM_LEVEL' : 'SESSION_LEVEL';
my $csv = Text::CSV->new({binary => 1, eol => "\n"}) or die Text::CSV->error_diag;
open my $entries_fh, '>:encoding(UTF-8)', $entries_output
    or die "Cannot write $entries_output: $!\n";
my @header = qw(CrosscheckOrdinal Title Authors Track Locator RecordKind ParseStatus DisplayText);
$csv->say($entries_fh, \@header) or die $csv->error_diag;
my $ordinal = 0;
for my $record (@records) {
    $ordinal++;
    $csv->say($entries_fh, [ $ordinal, map { $record->{$_} } @header[1 .. $#header] ])
        or die $csv->error_diag;
}
close $entries_fh or die "Cannot close $entries_output: $!\n";

my %track_counts;
$track_counts{$_->{Track}}++ for @records;
my $audit = {
    SourceFilename          => $input =~ m{([^/]+)$} ? $1 : $input,
    SHA256                  => sha256_hex($bytes),
    SizeBytes               => length($bytes),
    ManualSearchUnitID      => $unit_id,
    DetectedYear            => $year,
    DetectedTrack           => $track,
    DocumentTitle           => $document_title,
    ObservedURL             => $observed_url,
    EvidenceRole            => 'VENUE_CROSSCHECK',
    CrosscheckGranularity   => $granularity,
    PageLayout              => $layout,
    RawRecordOccurrenceCount => $raw_record_count,
    ExtractedUniqueItemCount => scalar @records,
    DuplicateOccurrenceCount => $raw_record_count - scalar @records,
    ParseFailureCount       => $parse_failure_count,
    TrackCounts             => [ map { +{ value => $_, count => $track_counts{$_} } } sort keys %track_counts ],
    HTMLTreeBuilderVersion  => $HTML::TreeBuilder::VERSION,
    TextCSVVersion          => $Text::CSV::VERSION,
};
open my $audit_fh, '>:encoding(UTF-8)', $audit_output
    or die "Cannot write $audit_output: $!\n";
print {$audit_fh} JSON::PP->new->canonical->pretty->encode($audit);
close $audit_fh or die "Cannot close $audit_output: $!\n";
$tree->delete;

exit($parse_failure_count ? 2 : 0);
