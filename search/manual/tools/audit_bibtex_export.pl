#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use BibTeX::Parser;
use Text::CSV;
use Unicode::Normalize qw(NFC);
use Digest::SHA qw(sha256_hex);
use Getopt::Long qw(GetOptions);
use JSON::PP;

my ($input, $entries_output, $summary_output);
GetOptions(
    'input=s'           => \$input,
    'entries-output=s'  => \$entries_output,
    'summary-output=s'  => \$summary_output,
) or die "Invalid arguments\n";
die "Missing --input\n" unless defined $input;
die "Missing --entries-output\n" unless defined $entries_output;
die "Missing --summary-output\n" unless defined $summary_output;
die "BibTeX::Parser version mismatch\n"
    unless ($BibTeX::Parser::VERSION // '') eq '1.05';

sub sha256_file {
    my ($path) = @_;
    open my $fh, '<:raw', $path or die "Cannot read $path: $!\n";
    my $sha = Digest::SHA->new(256);
    $sha->addfile($fh);
    return $sha->hexdigest;
}

sub clean {
    my ($value) = @_;
    $value //= '';
    $value = NFC($value);
    $value =~ s/\s+/ /g;
    $value =~ s/^\s+|\s+$//g;
    return $value;
}

sub normalized_doi {
    my ($value) = @_;
    $value = clean($value);
    $value =~ s!^(?:doi:\s*|https?://(?:dx\.)?doi\.org/)!!i;
    return lc $value;
}

sub grouped_values {
    my ($counts) = @_;
    return [map { +{value => $_, count => $counts->{$_}} } sort keys %$counts];
}

my @columns = qw(
    SourceFilename EntryOrdinal BibTeXKey BibTeXType DOI Title Authors Year Booktitle
    Series ISBN Publisher Location Pages NumPages URL AbstractAvailability
    KeywordsAvailability ParseStatus Notes
);
my $csv = Text::CSV->new({binary => 1, eol => "\n"})
    or die "Cannot initialize Text::CSV\n";
open my $out, '>:encoding(UTF-8)', $entries_output
    or die "Cannot write $entries_output: $!\n";
$csv->print($out, \@columns) or die "Cannot write CSV header\n";

open my $bib_raw, '<:raw', $input or die "Cannot read $input: $!\n";
my $bib_bytes = do { local $/; <$bib_raw> };
close $bib_raw or die "Cannot close $input: $!\n";
# Some publisher bulk exports concatenate otherwise valid entries as `}@TYPE`
# without a separating line break.  BibTeX::Parser 1.05 stops after the first
# such entry.  Insert only the missing lexical boundary, then still require the
# proper parser to parse and validate every entry.
my $entry_boundary_insertions = ($bib_bytes =~ s/\}\s*\@(?=[A-Za-z])/\}\n\@/g);
open my $bib, '<:encoding(UTF-8)', \$bib_bytes
    or die "Cannot open in-memory BibTeX: $!\n";
my $parser = BibTeX::Parser->new($bib);
my (%types, %dois, %titles, %years, %booktitles, %series, %isbns, %publishers, %locations);
my ($entries, $parse_failures, $missing_doi, $missing_title, $missing_authors) = (0, 0, 0, 0, 0);
my ($abstract_available, $keywords_available) = (0, 0);

while (my $entry = $parser->next) {
    $entries++;
    my $parse_ok = $entry->parse_ok ? 1 : 0;
    $parse_failures++ unless $parse_ok;
    my $type = lc clean($entry->type);
    my $key = clean($entry->key);
    $types{$type}++;
    my $doi = normalized_doi($entry->field('doi'));
    my $title = defined($entry->field('title'))
        ? clean($entry->cleaned_field('title')) : '';
    my @authors = defined($entry->field('author'))
        ? map { clean(join ' ', grep { defined && length } @$_) } $entry->cleaned_author
        : ();
    @authors = grep { length } @authors;
    my $authors = join '; ', @authors;
    my %fields = (
        Year => clean($entry->field('year')),
        Booktitle => defined($entry->field('booktitle'))
            ? clean($entry->cleaned_field('booktitle')) : '',
        Series => defined($entry->field('series'))
            ? clean($entry->cleaned_field('series')) : '',
        ISBN => clean($entry->field('isbn')),
        Publisher => defined($entry->field('publisher'))
            ? clean($entry->cleaned_field('publisher')) : '',
        Location => defined($entry->field('location'))
            ? clean($entry->cleaned_field('location')) : '',
        Pages => clean($entry->field('pages')),
        NumPages => clean($entry->field('numpages')),
        URL => clean($entry->field('url')),
    );
    my $has_abstract = length(clean($entry->field('abstract'))) ? 1 : 0;
    my $has_keywords = length(clean($entry->field('keywords'))) ? 1 : 0;
    $abstract_available += $has_abstract;
    $keywords_available += $has_keywords;
    $missing_doi++ unless length $doi;
    $missing_title++ unless length $title;
    $missing_authors++ unless length $authors;
    $dois{$doi}++ if length $doi;
    $titles{$title}++ if length $title;
    $years{$fields{Year}}++ if length $fields{Year};
    $booktitles{$fields{Booktitle}}++ if length $fields{Booktitle};
    $series{$fields{Series}}++ if length $fields{Series};
    $isbns{$fields{ISBN}}++ if length $fields{ISBN};
    $publishers{$fields{Publisher}}++ if length $fields{Publisher};
    $locations{$fields{Location}}++ if length $fields{Location};
    my @row = (
        $input =~ m{([^/]+)$} ? $1 : $input,
        $entries, $key, $type, $doi, $title, $authors,
        @fields{qw(Year Booktitle Series ISBN Publisher Location Pages NumPages URL)},
        $has_abstract ? 'AVAILABLE_CONTROLLED_NOT_REDISTRIBUTED' : 'NOT_REPORTED_BY_SOURCE',
        $has_keywords ? 'AVAILABLE_CONTROLLED_NOT_REDISTRIBUTED' : 'NOT_REPORTED_BY_SOURCE',
        $parse_ok ? 'PARSE_OK' : 'PARSE_FAILED', '',
    );
    $csv->print($out, \@row) or die "Cannot write CSV row $entries\n";
}
close $out or die "Cannot close $entries_output: $!\n";

my $summary = {
    SourceFilename => ($input =~ m{([^/]+)$} ? $1 : $input),
    SHA256 => sha256_file($input), BibTeXParserVersion => $BibTeX::Parser::VERSION,
    EntryCount => $entries, ParseFailureCount => $parse_failures,
    LexicalEntryBoundaryInsertions => $entry_boundary_insertions,
    BibTeXTypeCounts => grouped_values(\%types),
    DOICount => scalar(keys %dois),
    DuplicateDOICount => scalar(grep { $dois{$_} > 1 } keys %dois),
    DuplicateTitleCount => scalar(grep { $titles{$_} > 1 } keys %titles),
    MissingDOICount => $missing_doi, MissingTitleCount => $missing_title,
    MissingAuthorsCount => $missing_authors,
    AbstractAvailableCount => $abstract_available,
    KeywordsAvailableCount => $keywords_available,
    ObservedYears => grouped_values(\%years), ObservedBooktitles => grouped_values(\%booktitles),
    ObservedSeries => grouped_values(\%series), ObservedISBNs => grouped_values(\%isbns),
    ObservedPublishers => grouped_values(\%publishers), ObservedLocations => grouped_values(\%locations),
};
open my $summary_fh, '>:encoding(UTF-8)', $summary_output
    or die "Cannot write $summary_output: $!\n";
print {$summary_fh} JSON::PP->new->canonical(1)->pretty(1)->encode($summary);
close $summary_fh or die "Cannot close $summary_output: $!\n";
die "BibTeX parse failures: $parse_failures\n" if $parse_failures;
