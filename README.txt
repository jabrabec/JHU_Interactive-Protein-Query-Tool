**ABOUT**

The Interactive protein query tool provides an interface for the customized/curated analysis of whole proteomes of selected organisms. Users can perform the following tasks:
	1. Query the existing database for gene products (limited to polypeptides) of interest.
	2. Perform BLAST+ protein analysis on a desired sequence against only those proteins in the customized/curated database.
	3. Upload whole genomes in Genbank format into the database.

Source code has beeb made available via Blackboard under the AS410.712 final submission tool, in .tar.gz format.

Demo version is available here:
http://cloud-131-215.diagcomputing.org/jbrabec1/FinalProject/


**REQUIREMENTS**

System must have the following components installed in order to run this package:
	1. BLAST+ from NCBI:
	http://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download
	2. BioPerl-1.6.901:
	http://search.cpan.org/~cjfields/BioPerl-1.6.901/
	3. BioPerl-Run-1.006900:
	http://search.cpan.org/~cjfields/BioPerl-Run-1.006900/

Standard Perl toolkit modules such as CGI, HTML::Template, Config::IniFiles, must also be available.

The NCBI BLAST+ installation will require approximately 400mb installed, without attached databases. Recommended available memory is 1gb.


**USAGE INSTRUCTIONS**

1. To query the existing database:
	a. Enter a desired search term.
		i. If desired, select an option from the drop-down autopopulated list.
	b. Click "Submit gene product query."
	c. Results will display below.

2. To perform a BLAST+ protein analysis on a desired sequence against the custom database:
	a. Enter the desired protein sequence (amino acids only) into the search box.
	b. Click "Submit BLASTP query."
	c. Browser will display the BLASTP report output.

3. To upload genomes into the database:
	a. Click on "Choose Files" and select the appropriate file (.gb or .gbk format only) from desired local storage location.
	b. Click "Upload Files."
	c. Browser will display a confirmation message when file processing has been completed (this will take some time).


**DEMO DATA**

In order to examine how this tool works, the following example steps can be followed:
	1. Enter "amylase" into the gene product query search field and click submit. User may select an option from the drop-down menu or simply click "submit."
	2. From the resulting output, choose a gene product and copy its associated "Amino Acid Residues" output.
	3. Paste this sequence into the BLASTP query search field and click submit.
	4. To upload a file:
		a. Choose either "blank_test.gbk," which has been included in this package, or pick an actual genome to download from: ftp://ftp.ncbi.nih.gov/genomes/
			i. If using a real genome, click a desired organism from the NCBI FTP site and save its associated .gbk file to your local hard drive.
		b. On the Interactive protein query tool page, click on "Choose Files" and select the target .gbk file from step 4a.
		c. Click "Upload Files" and wait for file upload & processing confirmation.


**QUESTIONS**

Questions about this tool can be directed to Jennifer Brabec (jbrabec1@jhu.edu). 07May2013.