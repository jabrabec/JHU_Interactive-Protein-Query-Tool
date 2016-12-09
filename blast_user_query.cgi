#!/usr/bin/perl -w

use strict;
use Config::IniFiles;
use DBI;
use Bio::Tools::Run::StandAloneBlastPlus;
use Bio::Seq;
use CGI;
use CGI::Carp qw ( fatalsToBrowser );
use HTML::Template;


my $cgi = CGI->new();
my $tmpl = HTML::Template->new(filename => 'tmpl/blast.tmpl');


my $cfg = Config::IniFiles->new( -file => "settings.ini" ) || die "failed to read INI file: $!";
my $dsn = "DBI:mysql:database=" . $cfg->val('database', 'name') . 
                       ";host=" . $cfg->val('database', 'server') . ";";
my $dbh = DBI->connect($dsn, $cfg->val('database', 'user'), $cfg->val('database', 'pass'),
                       {RaiseError => 1, PrintError => 0});


## initialize an empty arrayref to store the search matches
my $matches = [];
## only return from polypeptides: organism common name, locus name, gene product, residue sequence
my $qry = qq{
	SELECT o.common_name, f.uniquename, product.value, f.residues
	FROM feature f
	JOIN cvterm polypeptide ON f.type_id=polypeptide.cvterm_id
	JOIN featureprop product ON f.feature_id=product.feature_id
	JOIN organism o ON f.organism_id=o.organism_id
	WHERE polypeptide.name = ?;
};
my $dsh = $dbh->prepare($qry);
$dsh->execute('polypeptide');

## Submit full query
while (my $row = $dsh->fetchrow_hashref) {
	## push the row to the match array
	push @$matches, $row;
	}

$dsh->finish;
$dbh->disconnect;

## create fasta-formatted file to be used as custom database for BLAST+
open (DBFILE, '>/var/www/jbrabec1/FinalProject/temp/customdb.faa'); 
my $fakeGIvalue = 0; # BLAST+ requires numeric value after >gi|
foreach my $dbhits ( @$matches ) {
	$fakeGIvalue++;
## mimic fasta format
	print DBFILE ">gi|$fakeGIvalue|ref|" .
	$$dbhits{uniquename} .
	"| " .
	$$dbhits{value} .
	" [" .
	$$dbhits{common_name} .
	"]\n" .
	$$dbhits{residues} .
	"\n";
}
close (DBFILE);

## pull query sequence from user form submission
my $querysequence = $cgi->param("blast_query");
# my $querysequence = "MRNPTLLQCFHWYYPEGGKLWPELAERADGFNDIGINMVWLPPAYKGASGGYSVGYDSYDLFDLGEFDQKGSIPTKYGDKAQLLAAIDALKRNDIAVLLDVVVNHKMGADEKEAIRVQRVNADDRTQIDEEIIECEGWTRYTFPARAGQYSQFIWDFKCFSGIDHIENPDEDGIFKIVNDYTGEGWNDQVDDELGNFDYLMGENIDFRNHAVTEEIKYWARWVMEQTQCDGFRLDAVKHIPAWFYKEWIEHVQEVAPKPLFIVAEYWSHEVDKLQTYIDQVEGKTMLFDAPLQMKFHEASRMGRDYDMTQIFTGTLVEADPFHAVTLVANHDTQPLQALEAPVEPWFKPLAYALILLRENGVPSVFYPDLYGAHYEDVGGDGQTYPIDMPIIEQLDELILARQRFAHGVQTLFFDHPNCIAFSRSGTDEFPGCVVVMSNGDDGEKTIHLGENYGNKTWRDFLGNRQERVVTDENGEATFFCNGGSVSVWVIEEVI";

## set BLAST+ program directory in PATH
# $ENV{ 'PATH' } = '/export/advcompbio/jbrabec1/ncbi-blast-2.2.28+/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games';
$ENV{ 'PATH' } = '/var/www/jbrabec1/FinalProject/ncbi-blast-2.2.28+/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games';

my $fac = Bio::Tools::Run::StandAloneBlastPlus->new(
	-db_name => '/var/www/jbrabec1/FinalProject/temp/customfasta',
	-db_data => '/var/www/jbrabec1/FinalProject/temp/customdb.faa',
	-overwrite => 1
	);

## run BLAST+ on query sequence
my $input = Bio::Seq->new(-id => "user_query",
                         -seq => $querysequence);

## output BLAST+ results to readable file
my $result = $fac->blastp( -query => $input,
							-outfile => '/var/www/jbrabec1/FinalProject/temp/blastp.out',
							-method_args => [ '-num_alignments' => 10 ]
);

## clean up BLAST+ DB
$fac->_register_temp_for_cleanup('customfasta');
$fac->cleanup;

## clean up fasta-formatted file
system("rm -f /var/www/jbrabec1/FinalProject/temp/customdb.faa");

## Set PATH and remove some environment variables for running in taint mode.
$ENV{ 'PATH' } = '/bin:/usr/bin:/usr/local/bin';
delete @ENV{ 'IFS', 'CDPATH', 'ENV', 'BASH_ENV' };

## convert blastp results to variable for tmpl access
# my $outputfile = "/var/www/jbrabec1/FinalProject/temp/blastp.out";
# my $blastresults = do {
#     local $/ = undef;
#     open my $fh, "<", $outputfile or die "could not open $outputfile: $!";
#     <$fh>;
# };

## convert blastp results to variable for tmpl access, preserving newlines
my $blastresults = 0;
open (OUTPUTFL, my $outputfile = "/var/www/jbrabec1/FinalProject/temp/blastp.out") or die "Can't open this file: $!";
while (<OUTPUTFL>) {
	$_ =~ s/\n/<br>/g; #preserve newlines as <br> in output
	$blastresults .= $_; #concatenate all lines into new source string
	}
close (OUTPUTFL) or die "Can't close $blastresults";

## clean up blastp.out file
system("rm -f /var/www/jbrabec1/FinalProject/temp/blastp.out");

## parameters that will be passed to upload.tmpl
$tmpl->param( PAGE_TITLE => 'Custom BLAST+ Results' );
$tmpl->param( QUERY_SEQ => $querysequence );
$tmpl->param( BLASTP_OUT => $blastresults );

print $cgi->header('text/html');
print $tmpl->output;
