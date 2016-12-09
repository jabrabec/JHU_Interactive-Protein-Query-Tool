#!/usr/bin/perl -wT

## ref: http://www.sitepoint.com/uploading-files-cgi-perl-2/

use strict;
use CGI;
use CGI::Carp qw ( fatalsToBrowser );
use File::Basename;
use Config::IniFiles;
use HTML::Template;

# my $cgi = CGI->new();
my $tmpl = HTML::Template->new(filename => 'tmpl/upload.tmpl');

## limit genbank file upload size to 15mb
$CGI::POST_MAX = 1024 * 15360;


## process uploaded file
my $safe_filename_characters = "a-zA-Z0-9_.-";
my $upload_dir = "/var/www/jbrabec1/FinalProject/temp";
# my $query = new CGI;
my $query = CGI->new();
my $filename = $query->param("fileselect");
if ( !$filename ) {
    print $query->header ( );
    print "There was a problem uploading your file (try a smaller file).";
    exit;
    }
my ( $name, $path, $extension ) = fileparse ( $filename, '\..*' );
$filename = $name . $extension;
$filename =~ tr/ /_/;
$filename =~ s/[^$safe_filename_characters]//g;
if ( $filename =~ /^([$safe_filename_characters]+)$/ ) {
    $filename = $1;
    }
else {
    die "Filename contains invalid characters";
    }
my $upload_filehandle = $query->upload("fileselect");
open ( UPLOADFILE, ">$upload_dir/$filename" ) or die "$!";
binmode UPLOADFILE; ## may not be necessary to include
while ( <$upload_filehandle> ) {
    print UPLOADFILE;
    }
close UPLOADFILE;


## load gbk file into database
my $cfg = Config::IniFiles->new( -file => "settings.ini" ) || die "failed to read INI file: $!";
my $user = $cfg->val('database', 'user');
my $database = $cfg->val('database', 'name');
my $password = $cfg->val('database', 'pass');

## ref: http://www.boards.ie/vbulletin/showpost.php?p=55944778&postcount=3
## Set PATH and remove some environment variables for running in taint mode.
$ENV{ 'PATH' } = '/bin:/usr/bin:/usr/local/bin';
delete @ENV{ 'IFS', 'CDPATH', 'ENV', 'BASH_ENV' };
my $cfg = Config::IniFiles->new( -file => "settings.ini" ) || die "failed to read INI file: $!";
my $user = $cfg->val('database', 'user');
my $database = $cfg->val('database', 'name');
my $password = $cfg->val('database', 'pass');
system("perl load_gbk.pl -i /var/www/jbrabec1/FinalProject/temp/$filename -d $database -u $user -p $password");

## clean-up file after it has been imported into db
system("rm -f /var/www/jbrabec1/FinalProject/temp/$filename");

## parameters that will be passed to upload.tmpl
$tmpl->param( PAGE_TITLE => 'Thanks for uploading you file to the custom protein database!' );
$tmpl->param( UPLOADED_FILE => $filename );

print $query->header('text/html');
print $tmpl->output;
