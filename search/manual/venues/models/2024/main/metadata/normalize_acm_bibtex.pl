#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use BibTeX::Parser;
use Text::CSV;
use Unicode::Normalize qw(NFC);
use Digest::SHA qw(sha256_hex);
use Getopt::Long qw(GetOptions);

my %arg;
GetOptions(map { ($_ . '=s' => \$arg{$_}) } qw(raw bib output audit normalized-at source-manifest metadata-source-id run-reason previous-normalization-timestamp)) or die "Invalid arguments\n";
for my $key (qw(raw bib output audit normalized-at source-manifest metadata-source-id run-reason previous-normalization-timestamp)) { die "Missing --$key\n" unless defined $arg{$key}; }
die "BibTeX::Parser version mismatch: " . ($BibTeX::Parser::VERSION // 'undefined') . "\n" unless ($BibTeX::Parser::VERSION // '') eq '1.05';

my @columns = qw(ManualSearchID ManualSearchUnitID SourceOrdinal InventorySourceID MetadataSourceID TitleRaw TitleNormalized AuthorsRaw AuthorsNormalized DOIRaw DOINormalized VenueRaw VenueNormalized YearRaw YearNormalized VolumeTrackIssue PublisherRecordURL MetadataSourceURL Publisher PublisherAddress ISBN Pages NumPages PublicationLocation Series AbstractRaw AbstractAvailability AbstractSourceURL AuthorKeywordsRaw AuthorKeywordsAvailability FullTextURL RetrievedAt NormalizedAt InventoryConflict CrossrefSnapshotPath PDFStatus PDFSHA256 Notes);
my $csv = Text::CSV->new({binary => 1, eol => "\n"}) or die "Text::CSV init failed\n";
sub file_sha { my ($path) = @_; open my $fh, '<:raw', $path or die "$path: $!\n"; local $/; return sha256_hex(<$fh>); }
sub clean { my ($s) = @_; $s //= ''; $s = NFC($s); $s =~ s/\s+/ /g; $s =~ s/^\s+|\s+$//g; return $s; }
sub doi { my ($s) = @_; $s = clean($s); $s =~ s!^(?:doi:\s*|https?://(?:dx\.)?doi\.org/)!!i; return lc $s; }
sub fail { die "Invariant failed: $_[0]\n"; }
sub read_csv {
    my ($path) = @_; open my $fh, '<:encoding(UTF-8)', $path or die "$path: $!\n";
    my $header = $csv->getline($fh) or die "CSV header unreadable: $path\n";
    my @rows; while (my $row = $csv->getline($fh)) { push @rows, $row; }
    die "CSV parse error in $path: " . $csv->error_diag . "\n" if !$csv->eof;
    return ($header, \@rows);
}

my $raw_sha_before = file_sha($arg{raw});
my ($manifest_header, $manifest_rows) = read_csv($arg{'source-manifest'});
my %mi = map { $manifest_header->[$_] => $_ } 0 .. $#$manifest_header;
my ($manifest_row) = grep { $_->[$mi{SourceID}] eq $arg{'metadata-source-id'} } @$manifest_rows;
fail('metadata source absent from manifest') unless $manifest_row;
my $manifest_bib_sha = $manifest_row->[$mi{SHA256}] // '';
fail('manifest metadata SHA256 is empty') unless length $manifest_bib_sha;
my $actual_bib_sha = file_sha($arg{bib});
fail('BibTeX SHA256 differs from manifest') unless $actual_bib_sha eq $manifest_bib_sha;

my ($raw_header, $raw_rows) = read_csv($arg{raw});
my %ri = map { $raw_header->[$_] => $_ } 0 .. $#$raw_header;
my @raw = map {
    my $row = $_;
    +{ map { $raw_header->[$_] => $row->[$_] } 0 .. $#$raw_header }
} @$raw_rows;
fail('RawRows') unless @raw == 27;
my @articles = grep { length $_->{DOIRaw} } @raw;
fail('RawArticleRows') unless @articles == 26;

open my $bib_fh, '<:encoding(UTF-8)', $arg{bib} or die "$arg{bib}: $!\n";
my $parser = BibTeX::Parser->new($bib_fh);
my (%bib, %raw_doi, %raw_dup, %bib_types);
my ($bib_count, $parse_failures, $bib_dups) = (0, 0, 0);
for my $row (@articles) { my $key = doi($row->{DOIRaw}); $raw_dup{$key}++ if exists $raw_doi{$key}; $raw_doi{$key} = $row; }
fail('DuplicateRawDOI') if keys %raw_dup;
while (my $entry = $parser->next) {
    $bib_count++; if (!$entry->parse_ok) { $parse_failures++; fail("BibTeX parse_ok entry $bib_count"); }
    my $type = lc($entry->type // ''); $bib_types{$type}++; fail("incompatible BibTeX entry type $type") unless $type eq 'inproceedings';
    my $key = doi($entry->field('doi')); fail("empty BibTeX DOI entry $bib_count") unless length $key;
    $bib_dups++ if exists $bib{$key}; fail("duplicate BibTeX DOI $key") if exists $bib{$key};
    my @authors = map { clean(join ' ', grep { defined && length } @$_) } $entry->cleaned_author;
    $bib{$key} = {
      title=>clean($entry->cleaned_field('title')), authors=>join('; ',@authors), booktitle=>clean($entry->cleaned_field('booktitle')),
      year=>clean($entry->field('year')), url=>clean($entry->field('url')), publisher=>clean($entry->cleaned_field('publisher')),
      address=>clean($entry->cleaned_field('address')), isbn=>clean($entry->field('isbn')), pages=>clean($entry->field('pages')),
      numpages=>clean($entry->field('numpages')), location=>clean($entry->cleaned_field('location')), series=>clean($entry->field('series')),
      has_abstract=>length(clean($entry->field('abstract')))?1:0, has_keywords=>length(clean($entry->field('keywords')))?1:0,
      author_count=>scalar @authors, author_raw=>$entry->field('author')//'',
    };
}
fail('BibTeXEntryCount') unless $bib_count == 26;
my @raw_only = grep { !exists $bib{$_} } keys %raw_doi; my @bib_only = grep { !exists $raw_doi{$_} } keys %bib;
fail('DOI set equality') if @raw_only || @bib_only;

my ($title_mismatch,$truncation,$authors_completed,$anomalies,$abstracts,$keywords,$keywords_missing)=(0,0,0,0,0,0,0);
open my $out, '>:encoding(UTF-8)', $arg{output} or die "$arg{output}: $!\n";
$csv->print($out, \@columns) or die "CSV header write failed: " . $csv->error_diag . "\n";
for my $r (@raw) {
    my %n = map { $_ => '' } @columns;
    for my $field (qw(ManualSearchID ManualSearchUnitID SourceOrdinal InventorySourceID TitleRaw AuthorsRaw DOIRaw VenueRaw YearRaw RetrievedAt)) { $n{$field}=$r->{$field}; }
    $n{VolumeTrackIssue}=$r->{VolumeTrackIssueRaw}; $n{PublisherRecordURL}=$r->{PublisherRecordURLRaw}; $n{NormalizedAt}=$arg{'normalized-at'}; $n{InventoryConflict}='false';
    if (!length $r->{DOIRaw}) {
      $n{TitleNormalized}=clean($r->{TitleRaw}); $n{VenueNormalized}=clean($r->{VenueRaw}); $n{YearNormalized}=clean($r->{YearRaw}); $n{AbstractAvailability}='NOT_APPLICABLE'; $n{AuthorKeywordsAvailability}='NOT_APPLICABLE'; $n{Notes}='No publisher BibTeX entry exists for the front-matter item; normalized row derives only from the raw membership record.';
    } else {
      my $key=doi($r->{DOIRaw}); my $b=$bib{$key}; $title_mismatch++ if clean($r->{TitleRaw}) ne $b->{title}; fail("Unexpected title mismatch $key") if clean($r->{TitleRaw}) ne $b->{title};
      $n{MetadataSourceID}=$arg{'metadata-source-id'}; $n{TitleNormalized}=$b->{title}; $n{AuthorsNormalized}=$b->{authors}; $n{DOINormalized}=$key; $n{VenueNormalized}=$b->{booktitle}; $n{YearNormalized}=$b->{year}; $n{MetadataSourceURL}=$b->{url};
      @n{qw(Publisher PublisherAddress ISBN Pages NumPages PublicationLocation Series)}=@$b{qw(publisher address isbn pages numpages location series)};
      $n{AbstractAvailability}=$b->{has_abstract}?'AVAILABLE_CONTROLLED_NOT_REDISTRIBUTED':'NOT_REPORTED_BY_SOURCE'; $n{AbstractSourceURL}=$b->{url}; $n{AuthorKeywordsAvailability}=$b->{has_keywords}?'AVAILABLE_CONTROLLED_NOT_REDISTRIBUTED':'NOT_REPORTED_BY_SOURCE'; $abstracts+=$b->{has_abstract}; $keywords+=$b->{has_keywords}; $keywords_missing+=!$b->{has_keywords};
      if ($r->{Notes}=~/interface indicated (\d+) additional author/) { $truncation++; my $visible=scalar grep{length}split /,/,($r->{AuthorsRaw}//''); my $expected=$visible+$1; fail("author completion $r->{ManualSearchID}") unless $b->{author_count}==$expected; $authors_completed++; }
      if ($b->{authors}=~/Â/) { $anomalies++; $n{Notes}='Publisher BibTeX deterministic decoding yields a source-level author encoding anomaly; no external correction was applied.'; }
    }
    $csv->print($out,[map{$n{$_}}@columns]) or die "CSV row write failed: " . $csv->error_diag . "\n";
}
close $out or die "CSV close failed: $!\n";
my $raw_sha_after=file_sha($arg{raw}); fail('raw inventory changed during normalization') unless $raw_sha_before eq $raw_sha_after;
my $normalized_sha=file_sha($arg{output});
my ($nh,$nr)=read_csv($arg{output}); fail('normalized header') unless join("\x1F",@$nh) eq join("\x1F",@columns); fail('NormalizedRows') unless @$nr==27; my $cols_ok=!grep { @$_ != @columns } @$nr; fail('NormalizedCSVColumnCount') unless $cols_ok;
my %ni=map{$nh->[$_]=>$_}0..$#$nh; my($set,$seq,$ord,$source,$rawcopy)=(1,1,1,1,1); my%ids; for my$i(0..$#raw){my$r=$raw[$i];my$n=$nr->[$i];$ids{$n->[$ni{ManualSearchID}]}++;$set=0 unless exists $r->{ManualSearchID};$seq=0 unless $r->{ManualSearchID}eq$n->[$ni{ManualSearchID}];$ord=0 unless $r->{SourceOrdinal}eq$n->[$ni{SourceOrdinal}];$source=0 unless $r->{InventorySourceID}eq$n->[$ni{InventorySourceID}];for my$f(qw(ManualSearchID ManualSearchUnitID SourceOrdinal InventorySourceID TitleRaw AuthorsRaw DOIRaw VenueRaw YearRaw RetrievedAt)){$rawcopy=0 unless($r->{$f}//'')eq($n->[$ni{$f}]//'')}}$set=0 unless keys(%ids)==27&&!grep{$ids{$_}!=1}keys%ids;
my $count=sub{my($f,$v)=@_;scalar grep{($_->[$ni{$f}]//'')eq$v}@$nr};
my $normalized_doi_count=scalar grep{length($_->[$ni{DOINormalized}]//'')}@$nr;
my %normalized_dois=map{($_->[$ni{DOINormalized}]//'')=>1}grep{length($_->[$ni{DOINormalized}]//'')}@$nr;
fail('NormalizedDOICount') unless $normalized_doi_count==26;
fail('UniqueNormalizedDOICount') unless keys(%normalized_dois)==26;
for my$pair ([MetadataSourceID=>$arg{'metadata-source-id'},26],[AbstractAvailability=>'AVAILABLE_CONTROLLED_NOT_REDISTRIBUTED',26],[AbstractAvailability=>'NOT_APPLICABLE',1],[AuthorKeywordsAvailability=>'AVAILABLE_CONTROLLED_NOT_REDISTRIBUTED',24],[AuthorKeywordsAvailability=>'NOT_REPORTED_BY_SOURCE',2],[AuthorKeywordsAvailability=>'NOT_APPLICABLE',1]){fail("normalized enum $pair->[0]")unless$count->(@$pair[0,1])==$pair->[2]}
for my$f(qw(AbstractRaw AuthorKeywordsRaw FullTextURL CrossrefSnapshotPath PDFSHA256)){fail("populated $f")if$count->($f,'')!=27}fail('InventoryConflictTrue')if$count->('InventoryConflict','true');
open my $audit,'>:encoding(UTF-8)',$arg{audit} or die "$arg{audit}: $!\n"; print $audit "# MODELS 2024 Main normalization audit\n\n";
my @a=(['AmendmentID','A001'],['NormalizationSchemaVersion',1],['NormalizationRunReason',$arg{'run-reason'}],['PreviousNormalizationTimestamp',$arg{'previous-normalization-timestamp'}],['NormalizationTimestamp',$arg{'normalized-at'}],['RawInventorySHA256Before',$raw_sha_before],['RawInventorySHA256After',$raw_sha_after],['RawInventoryByteIdentical',$raw_sha_before eq $raw_sha_after?'true':'false'],['ManifestBibTeXSHA256',$manifest_bib_sha],['ActualBibTeXSHA256',$actual_bib_sha],['BibTeXSHA256Match',$actual_bib_sha eq $manifest_bib_sha?'true':'false'],['NormalizedInventorySHA256',$normalized_sha],['BibTeXParserVersion',$BibTeX::Parser::VERSION],['TextCSVVersion',$Text::CSV::VERSION],['UnicodeNormalizeVersion',$Unicode::Normalize::VERSION],['DigestSHAVersion',$Digest::SHA::VERSION],['GetoptLongVersion',$Getopt::Long::VERSION],['BibTeXParseFailureCount',$parse_failures],['BibTeXEntryTypeCounts',join(', ',map{"$_=$bib_types{$_}"}sort keys%bib_types)],['RawRows',scalar@raw],['RawResearchArticleRows',scalar@articles],['RawFrontMatterRows',1],['NormalizedRows',scalar@$nr],['NormalizedResearchArticleRows',26],['NormalizedFrontMatterRows',1],['BibTeXEntryCount',$bib_count],['MatchedByDOI',scalar@articles],['RawOnlyDOICount',scalar@raw_only],['BibTeXOnlyDOICount',scalar@bib_only],['DuplicateRawDOICount',scalar keys%raw_dup],['DuplicateBibTeXDOICount',$bib_dups],['UnexpectedTitleMismatchCount',$title_mismatch],['UnexpectedDOIMismatchCount',0],['ManualSearchIDSetEqual',$set?'true':'false'],['ManualSearchIDSequenceEqual',$seq?'true':'false'],['SourceOrdinalSequenceEqual',$ord?'true':'false'],['InventorySourceIDPreserved',$source?'true':'false'],['RawFieldCopyEquality',$rawcopy?'true':'false'],['NormalizedCSVParseOK','true'],['NormalizedCSVColumnCount',scalar@columns],['ResearchArticleMetadataSourceIDCount',$count->('MetadataSourceID',$arg{'metadata-source-id'})],['FrontMatterMetadataSourceIDBlankCount',$count->('MetadataSourceID','')],['NormalizedDOICount',$normalized_doi_count],['UniqueNormalizedDOICount',scalar keys%normalized_dois],['RawAuthorTruncationCount',$truncation],['AuthorsCompletedFromMetadataCount',$authors_completed],['MetadataEncodingAnomalyCount',$anomalies],['AbstractAvailableControlledCount',$abstracts],['AbstractPersistedPublicCount',0],['AbstractRawPopulatedCount',$count->('AbstractRaw','')==27?0:-1],['KeywordsAvailableControlledCount',$keywords],['KeywordsNotReportedCount',$keywords_missing],['KeywordsPersistedPublicCount',0],['AuthorKeywordsRawPopulatedCount',$count->('AuthorKeywordsRaw','')==27?0:-1],['FullTextURLPopulatedCount',$count->('FullTextURL','')==27?0:-1],['CrossrefSnapshotPathPopulatedCount',$count->('CrossrefSnapshotPath','')==27?0:-1],['PDFSHA256PopulatedCount',$count->('PDFSHA256','')==27?0:-1],['InventoryConflictTrueCount',$count->('InventoryConflict','true')],['CrossrefUsed','false'],['FullTextRetrieved','false'],['InventoryConflictCount',0],['PrimaryInventorySourceID','SRC-MODELS-2024-MAIN-ACM-TOC-HUMAN-20260811'],['MetadataSourceID',$arg{'metadata-source-id'}],['NormalizationScript','normalize_acm_bibtex.pl'],); print $audit join('',map{"- $_->[0]: $_->[1]\n"}@a);
print $audit "\n## Metadata representation review\n\n| ManualSearchID | Field | RawValue | MetadataNormalizedValue | SourceBibTeXFragment | Action |\n| --- | --- | --- | --- | --- | --- |\n| MS-MODELS-2024-MAIN-0012 | AuthorsNormalized | MaÂngeles Moraga | $bib{'10.1145/3640310.3674099'}->{authors} | Ma{\\^A}ngeles Moraga | Preserved deterministic publisher representation; queued for metadata review, not an identity correction. |\n";
