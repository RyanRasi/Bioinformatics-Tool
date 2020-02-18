# Bioinformatics-Tool
A Bioinformatics tool written with Flask that searches for motifs within a protein sequence and reports the results on the website and/or to the users email.
<br>
# Introduction

This piece of software is a bioinformatics tool that can search for sequence motifs in proteins. This can either be through a UniprotAccession Code or with FASTA format where upon the user is presented with results in a table through the web page as well as the option to have the results delivered via email like most other bioinformatic tools.This tool has been developed to detect regions of proteins that can form amyloid associations. This is vital as proteins and aggregates are associated with a wide range of diseases such as Alzheimer’s disease(Greenwald and Riek, 2010). There is debate as to whether the cause is of this is due to specific sequences and the properties of amino acids orwhether it isa trait of all proteins, nonetheless existing tools have been developed to predict by sequence. This is highly important due to “reliable identification of amyloid motifs in proteinshavinga great impact in thedevelopment of antiamyloidtherapeutics.”(Lopez de la Paz and Serrano, 2003)A pattern motif has been discovered by researchers that detects regions of proteins that can form amyloid associations. This pattern is...

> {P}1-{PKRHW}2-[VLSWFNQ]3-[ILTYWFN]4-[FIY]5-{PKRH}6
> (Prosite.expasy.org, 2019)

This bioinformatics tool uses this pattern which has been converted into a regular expression in python and is utilised to search for the motifs and the position ranges, which is then displayed in an easy to understand table. The python regular expression is...
> \[^P\]\[\^PKRHW][VLSWFNQ][ILTYWFN][FIY]\[\^PKRH]

The language used to implement this tool is Python and the libraries of Biopython, flask, form and smtplib supplement allow its functionality.

## Running The Tool

**Online Access**
This tool is accessible online at http://142.93.44.105:5000/uniprot
**Local Access**
Alternatively, you can run this web server locally. To do this, download the project folder and ensure you have Python 3 installed. To check if you have Python installed run “python --version” in the terminal, if the command is not found then please go to the python website to download it.Running a virtual environment is up to the user’s discretion to ensure that the dependencies of this project are isolated from the dependencies of other projects.This project depends on libraries which can be installed through the terminal in the project folder. The command to run is “pip install [The Library]” replacing [The Library] with each of the following one by one, “flask”, “wtforms”, “Flask-WTF”, “numpy”, “biopython”.
**Libraries to install**

 - [ ] flask
 - [ ] wtforms
 - [ ] Flask-WTF
 - [ ] numpy
 - [ ] biopython

Finally, the user can run this tool from the terminal of the project folder by executing “python webServer.py”.Access via localhost is provided with the web link “http://127.0.0.1:5000/”

## Input

The user has two different methods to input that can be used with this tool; “Uniprot Accession Code” or “FASTA” format. The user can access these webpages from the navbar at the top of the website.

**Accession Code**

On the Uniprot Accession Code page, the user is greeted with two text input fields, one for the Uniprot Accession Code and another for the users e-mail address which is optional. The user can input a Uniport Accession Code such as “P10636” and click submit without inputting their email if they choose to do so. The user input is validated against two factors, one if the text field for the Accession code is empty upon submission whereupon the page is refreshed with the banner message of “Input is required” and two, if the user input is for being an invalid Uniprot Accession code such as random text input which leads to a similar conclusion of the page being refreshed with a new banner message stating ”Uniprot input is invalid”.

**FASTA Format**

On the FASTA format page, the user is greeted with two input fields, one for the FASTA format text and another for the users e-mail address which is optional.The user can input a FASTA format such as...

>\>sp|P10997|IAPP_HUMAN Islet amyloid polypeptide OS=Homo sapiens OX=9606 GN=IAPP PE=1 SV=1MGILKLQVFLIVLSVALNHLKATPIESHQVEKRKCNTATCATQRLANFLVHSSNNFGAILSSTNVGSNTYGKRNAVEVLKREPLNYLPL

and click submit without inputting their email if they choose to do so.

## Output

The output is executed through a python script which returns a dictionary which is subsequently parsed into a table for the end user to see. The table has the description at the top which signifies the users input and additional identifiers such as the protein name and the organism. Below the description is an identifier to the number of matches found e.g. 3 matches were found) Under the identifier is the results table with two column headers being the motif name and the subsequent position of the motif. Whereupon all the matched motifs with their position identifiers will be listed underneath. Finally, underneath the results table is a section dedicated to helping the user understand the results.

If the user has entered in an e-mail address into the optional text field before they pressed submit then they should receive an e-mail from “bioinformaticsuniprotmotifs@gmail.com” detailing how many matches were found in the subject header and in the message box detailing the two outputs as seen in the webpage output; the description of the users input with identifiers such as the organism name and the results table with the motif and the position in columns with each subsequent data result in the rows that follow.

## Further Help

The about page which signifies how to use the tool is located at the top of the web page in the navbar and has useful information should the user get confused using the website and request a more efficient way of learning how to sue the tool as opposed to looking back at the user guide. The about page lists guides such as how to use the tool depending on your input choice of Uniprot Accession Code or FASTA format and explains how the python regular expression works.

## References

 - Greenwald, J. and Riek, R. (2010). Biology of Amyloid: Structure, Function, andRegulation.Structure, 18(10), pp.1244-1260.
 - Lopez de la Paz, M. andSerrano, L. (2003). Sequence determinants of amyloid fibril formation.Proceedings of the National Academy of Sciences, 101(1), pp.87-92.
 - Prosite.expasy.org. (2019).ScanProsite. [online] Available at: https://prosite.expasy.org/scanprosite/ [Accessed 15 Dec. 2019].
