#!/usr/bin/env perl
use strict;
use warnings;
use Encode qw(decode);
use Getopt::Long qw(GetOptions);
use HTML::TreeBuilder;

my %arg;
GetOptions(
    'input=s'              => \$arg{input},
    'output=s'             => \$arg{output},
    'unit-id=s'            => \$arg{unit_id},
    'source-id=s'          => \$arg{source_id},
    'retrieved-at=s'       => \$arg{retrieved_at},
    'venue=s'              => \$arg{venue},
    'year=s'               => \$arg{year},
    'volume-track-issue=s' => \$arg{volume_track_issue},
    'method=s'             => \$arg{method},
) or die "Invalid arguments\n";

for my $key (qw(input output unit_id source_id retrieved_at venue year volume_track_issue method)) {
    die "Missing --$key\n" unless defined $arg{$key};
}

sub has_class {
    my ($node, $class) = @_;
    return 0 unless defined $node->attr('class');
    return $node->attr('class') =~ /(?:^|\s)\Q$class\E(?:\s|$)/;
}

sub visible_text {
    my ($node) = @_;
    return '' unless $node;
    my $text = $node->as_text;
    $text =~ s/\s+/ /g;
    $text =~ s/^\s+|\s+$//g;
    return $text;
}

sub csv_value {
    my ($value) = @_;
    $value //= '';
    $value =~ s/"/""/g;
    return '"' . $value . '"';
}

my $tree = HTML::TreeBuilder->new;
open my $input, '<:raw', $arg{input} or die "Cannot read $arg{input}: $!\n";
local $/;
my $html = decode('UTF-8', <$input>, 1);
close $input;
$tree->parse($html);
$tree->eof;

my @toc_nodes = $tree->look_down(sub {
    my ($node) = @_;
    return has_class($node, 'issue-downloads__item') || has_class($node, 'issue-item-container');
});

open my $out, '>:encoding(UTF-8)', $arg{output} or die "Cannot write $arg{output}: $!\n";
print {$out} join(',', qw(
    ManualSearchID ManualSearchUnitID SourceOrdinal InventorySourceID SourceRecordLocator
    TitleRaw AuthorsRaw DOIRaw VenueRaw YearRaw VolumeTrackIssueRaw PublisherRecordURLRaw
    RetrievedAt ExtractionMethod Notes
)), "\n";

my $ordinal = 0;
for my $node (@toc_nodes) {
    my ($title, $authors, $doi, $locator, $record_url, $notes) = ('', '', '', '', '', '');

    if (has_class($node, 'issue-downloads__item')) {
        my $link = $node->look_down(sub { $_[0]->tag eq 'a' });
        next unless $link;
        $title = $link->attr('title') // visible_text($link);
        $locator = $link->attr('href') // '';
        $record_url = $locator;
        $notes = 'Observed in ACM Proceeding Downloads.';
    }
    else {
        my $title_link = $node->look_down(sub {
            my ($candidate) = @_;
            return $candidate->tag eq 'a'
                && $candidate->parent
                && $candidate->parent->tag eq 'h3'
                && has_class($candidate->parent, 'issue-item__title');
        });
        die "TOC item without title link\n" unless $title_link;
        $title = visible_text($title_link);
        $locator = $title_link->attr('href') // '';
        $record_url = $locator;

        my $authors_list = $node->look_down(sub {
            my ($candidate) = @_;
            return $candidate->tag eq 'ul' && has_class($candidate, 'loa');
        });
        $authors = visible_text($authors_list) if $authors_list;
        if ($authors =~ /\+\s*(\d+)/) {
            $notes = "HTML author list truncated; interface indicated $1 additional author(s).";
        }

        my $doi_input = $node->look_down(sub {
            my ($candidate) = @_;
            return $candidate->tag eq 'input' && has_class($candidate, 'issue-Item__checkbox');
        });
        $doi = $doi_input->attr('name') // '' if $doi_input;

        my $type = $node->look_down(sub {
            my ($candidate) = @_;
            return has_class($candidate, 'issue-heading');
        });
        $notes = ($notes ? "$notes " : '') . 'ACM document type observed: ' . visible_text($type) if $type;
    }

    $ordinal++;
    my $id = sprintf('MS-MODELS-2024-MAIN-%04d', $ordinal);
    print {$out} join(',', map { csv_value($_) } (
        $id,
        $arg{unit_id},
        $ordinal,
        $arg{source_id},
        $locator,
        $title,
        $authors,
        $doi,
        $arg{venue},
        $arg{year},
        $arg{volume_track_issue},
        $record_url,
        $arg{retrieved_at},
        $arg{method},
        $notes,
    )), "\n";
}

die "No ACM TOC items found\n" unless $ordinal;
$tree->delete;
