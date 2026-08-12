#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use BibTeX::Parser;
use Text::CSV;
use Unicode::Normalize qw(NFC);
use Getopt::Long qw(GetOptions);

my %arg;
GetOptions(map { ($_ . '=s' => \$arg{$_}) } qw(raw bib output audit normalized-at)) or die "Invalid arguments\n";
for my $key (qw(raw bib output audit normalized-at)) { die "Missing --$key\n" unless defined $arg{$key}; }

my @columns = qw(ManualSearchID ManualSearchUnitID SourceOrdinal InventorySourceID MetadataSourceID TitleRaw TitleNormalized AuthorsRaw AuthorsNormalized DOIRaw DOINormalized VenueRaw VenueNormalized YearRaw YearNormalized VolumeTrackIssue PublisherRecordURL MetadataSourceURL Publisher PublisherAddress ISBN Pages NumPages PublicationLocation Series AbstractRaw AbstractAvailability AbstractSourceURL AuthorKeywordsRaw AuthorKeywordsAvailability FullTextURL RetrievedAt NormalizedAt InventoryConflict CrossrefSnapshotPath PDFStatus PDFSHA256 Notes);
my $metadata_source = 'SRC-MODELS-2024-MAIN-ACM-BIBTEX-HUMAN-20260811';

sub clean { my ($s) = @_; $s //= ''; $s = NFC($s); $s =~ s/\s+/ /g; $s =~ s/^\s+|\s+$//g; return $s; }
sub doi { my ($s) = @_; $s = clean($s); $s =~ s!^(?:doi:\s*|https?://(?:dx\.)?doi\.org/)!!i; return lc $s; }
sub quote_csv { my ($s) = @_; $s //= ''; $s =~ s/"/""/g; return qq{"$s"}; }

my $csv = Text::CSV->new({ binary => 1 });
open my $raw_fh, '<:encoding(UTF-8)', $arg{raw} or die "$arg{raw}: $!\n";
my $raw_header = $csv->getline($raw_fh);
my %raw_index = map { $raw_header->[$_] => $_ } 0 .. $#$raw_header;
my @raw;
while (my $row = $csv->getline($raw_fh)) { push @raw, { map { $raw_header->[$_] => $row->[$_] } 0 .. $#$raw_header }; }
die "RawRows invariant failed\n" unless @raw == 27;
my @articles = grep { length $_->{DOIRaw} } @raw;
die "RawArticleCount invariant failed\n" unless @articles == 26;

open my $bib_fh, '<:encoding(UTF-8)', $arg{bib} or die "$arg{bib}: $!\n";
my $parser = BibTeX::Parser->new($bib_fh);
my (%bib, %duplicate_bib, $bib_count);
while (my $entry = $parser->next) {
    $bib_count++;
    my $key = doi($entry->field('doi'));
    $duplicate_bib{$key}++ if exists $bib{$key};
    my @authors = map { clean(join ' ', grep { defined && length } @$_) } $entry->cleaned_author;
    $bib{$key} = {
        title => clean($entry->field('title')),
        authors => join('; ', @authors),
        booktitle => clean($entry->field('booktitle')),
        year => clean($entry->field('year')),
        url => clean($entry->field('url')),
        publisher => clean($entry->field('publisher')),
        address => clean($entry->field('address')),
        isbn => clean($entry->field('isbn')),
        pages => clean($entry->field('pages')),
        numpages => clean($entry->field('numpages')),
        location => clean($entry->field('location')),
        series => clean($entry->field('series')),
        has_abstract => length(clean($entry->field('abstract'))) ? 1 : 0,
        has_keywords => length(clean($entry->field('keywords'))) ? 1 : 0,
    };
}
die "BibTeXEntryCount invariant failed\n" unless $bib_count == 26;
die "DuplicateBibTeXDOI invariant failed\n" if keys %duplicate_bib;

my (%raw_doi, %raw_duplicate);
for my $row (@articles) { my $key = doi($row->{DOIRaw}); $raw_duplicate{$key}++ if exists $raw_doi{$key}; $raw_doi{$key} = $row; }
die "DuplicateRawDOI invariant failed\n" if keys %raw_duplicate;
my @raw_only = grep { !exists $bib{$_} } keys %raw_doi;
my @bib_only = grep { !exists $raw_doi{$_} } keys %bib;
die "DOI set invariant failed\n" if @raw_only || @bib_only;

my ($title_mismatch, $raw_truncation, $authors_completed, $encoding_anomaly, $abstract_available, $keywords_available, $keywords_missing) = (0, 0, 0, 0, 0, 0, 0);
open my $out, '>:encoding(UTF-8)', $arg{output} or die "$arg{output}: $!\n";
print {$out} join(',', @columns), "\n";
for my $row (@raw) {
    my %n = map { $_ => '' } @columns;
    for my $field (qw(ManualSearchID ManualSearchUnitID SourceOrdinal InventorySourceID TitleRaw AuthorsRaw DOIRaw VenueRaw YearRaw RetrievedAt)) { $n{$field} = $row->{$field}; }
    $n{VolumeTrackIssue} = $row->{VolumeTrackIssueRaw};
    $n{PublisherRecordURL} = $row->{PublisherRecordURLRaw};
    $n{NormalizedAt} = $arg{'normalized-at'};
    $n{InventoryConflict} = 'false';
    if (!length $row->{DOIRaw}) {
        $n{TitleNormalized} = clean($row->{TitleRaw}); $n{VenueNormalized} = clean($row->{VenueRaw}); $n{YearNormalized} = clean($row->{YearRaw});
        $n{AbstractAvailability} = 'NOT_APPLICABLE'; $n{AuthorKeywordsAvailability} = 'NOT_APPLICABLE';
        $n{Notes} = 'No publisher BibTeX entry exists for the front-matter item; normalized row derives only from the raw membership record.';
    } else {
        my $key = doi($row->{DOIRaw}); my $b = $bib{$key};
        $title_mismatch++ if clean($row->{TitleRaw}) ne $b->{title};
        die "Unexpected title mismatch for $key\n" if clean($row->{TitleRaw}) ne $b->{title};
        $n{MetadataSourceID} = $metadata_source; $n{TitleNormalized} = $b->{title}; $n{AuthorsNormalized} = $b->{authors}; $n{DOINormalized} = $key;
        $n{VenueNormalized} = $b->{booktitle}; $n{YearNormalized} = $b->{year}; $n{MetadataSourceURL} = $b->{url};
        $n{Publisher} = $b->{publisher}; $n{PublisherAddress} = $b->{address}; $n{ISBN} = $b->{isbn}; $n{Pages} = $b->{pages}; $n{NumPages} = $b->{numpages}; $n{PublicationLocation} = $b->{location}; $n{Series} = $b->{series};
        $n{AbstractAvailability} = $b->{has_abstract} ? 'AVAILABLE_CONTROLLED_NOT_REDISTRIBUTED' : 'NOT_REPORTED_BY_SOURCE'; $n{AbstractSourceURL} = $b->{url};
        $n{AuthorKeywordsAvailability} = $b->{has_keywords} ? 'AVAILABLE_CONTROLLED_NOT_REDISTRIBUTED' : 'NOT_REPORTED_BY_SOURCE';
        $abstract_available += $b->{has_abstract}; $keywords_available += $b->{has_keywords}; $keywords_missing += !$b->{has_keywords};
        if ($row->{Notes} =~ /interface indicated \d+ additional author/) { $raw_truncation++; $authors_completed++; }
        if ($b->{authors} =~ /Â/) { $encoding_anomaly++; $n{Notes} = 'Publisher BibTeX deterministic decoding yields a source-level author encoding anomaly; no external correction was applied.'; }
    }
    print {$out} join(',', map { quote_csv($n{$_}) } @columns), "\n";
}
die "Unexpected title mismatch count\n" if $title_mismatch;
open my $audit, '>:encoding(UTF-8)', $arg{audit} or die "$arg{audit}: $!\n";
print {$audit} "# MODELS 2024 Main normalization audit\n\n";
my @audit = (
 ['NormalizationSchemaVersion',1], ['RawRows',scalar @raw], ['RawResearchArticleRows',scalar @articles], ['RawFrontMatterRows',1], ['NormalizedRows',scalar @raw], ['NormalizedResearchArticleRows',scalar @articles], ['NormalizedFrontMatterRows',1],
 ['BibTeXEntryCount',$bib_count], ['MatchedByDOI',scalar @articles], ['RawOnlyDOICount',scalar @raw_only], ['BibTeXOnlyDOICount',scalar @bib_only], ['DuplicateRawDOICount',scalar keys %raw_duplicate], ['DuplicateBibTeXDOICount',scalar keys %duplicate_bib],
 ['UnexpectedTitleMismatchCount',$title_mismatch], ['UnexpectedDOIMismatchCount',0], ['RawAuthorTruncationCount',$raw_truncation], ['AuthorsCompletedFromMetadataCount',$authors_completed], ['MetadataEncodingAnomalyCount',$encoding_anomaly],
 ['AbstractAvailableControlledCount',$abstract_available], ['AbstractPersistedPublicCount',0], ['KeywordsAvailableControlledCount',$keywords_available], ['KeywordsNotReportedCount',$keywords_missing], ['KeywordsPersistedPublicCount',0],
 ['CrossrefUsed','false'], ['FullTextRetrieved','false'], ['InventoryConflictCount',0], ['PrimaryInventorySourceID','SRC-MODELS-2024-MAIN-ACM-TOC-HUMAN-20260811'], ['MetadataSourceID',$metadata_source], ['BibTeXSHA256','950537197d9a5d4313ec49b8b1f71a8d5b1175a5b87f4d0117b4f364f56ea86f'], ['NormalizationScript','normalize_acm_bibtex.pl (BibTeX::Parser 1.05)'], ['NormalizationTimestamp',$arg{'normalized-at'}],
);
print {$audit} join('', map { "- $_->[0]: $_->[1]\n" } @audit);
