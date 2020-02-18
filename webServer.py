#!/usr/bin/python
import time
import sys
import smtplib
import re

from Bio import ExPASy
from Bio import SwissProt
from Bio import SeqIO

import numpy as np

import urllib

from flask import Flask, redirect, url_for, render_template, request, flash
from forms import UniprotForm, FastaForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bioinformatics' #Config for web server to accept form input

# ------------------------------------- End of Imports -------------------------------

# ------------------------------------- Web Server Start -------------------------------
@app.route("/uniprot", methods=["POST", "GET"])
def uniprot():
	form = UniprotForm() # Sets the web page to use the form from forms.py so it uses a Uniprot input as opposed to the FASTA one
	if form.is_submitted(): # Checks to see if the user has pressed submit
		userSubmissionForm = (request.form.to_dict()) # Sets the form as a dictionary
		userSubmission = userSubmissionForm["UAC"] # Gets the UAC key from the dictionary which is the user input as the second key is the submit button
		print ("User input is " + userSubmission) # Prints the user submission to the terminal

		accession_number = userSubmission # Declares and sets the Accession number to the UAC key


		MatchCounter = 0 # Declares and sets a match counter to 0 which will later be sent to the next web page at the end of the code block

		d_UniprotResults = {"Motif":"Position"} # Creates a new dictionary for the results with the column headings of Motif and position
		d_Email = {"Motif":"Position"}# Creates a new dictionary for the email results with the column headings of Motif and position
# ------------------------------------- Uniprot Code Start -------------------------------

#Validation checks

# Error Handling - Tries the user input and if the input is invalid and yields a 404 error then the page refreshes
		if len(userSubmission) == 0: #If the user has submitted blank text then the page is refreshed with a banner message indicating so
			flash("Input is required")
			return redirect(request.url)

		try: #Try loop for if the user has entered an invalid input
			handle = ExPASy.get_sprot_raw(userSubmission) # Checks the Uniprot server for the accession code
		except urllib.error.HTTPError as err: # If a URL error occurs then...
			if err.code == 404: # If the code is 404 then prints to console page not found
				flash("Uniprot input is invalid")
				print ("Error 404 - Page not Found")
				return redirect(request.url) # Due to the error code the page is then refreshed so that the user can retry input
			else:
				pass

		record = SwissProt.read(handle) # Reads the data from the server and saves to a variable

		print(record)
		handle.close() # Closes the handle - Good practice

		print(record.entry_name) # Prints the entry + organism name to console (debug purposes)
		print(record.organism)

		Description = record.entry_name + " " + record.organism # Identiying information for the description of the input is saved for sending to the email and webpage results.

		dna = record.sequence # sets the sequence to a new variable

		sequence = re.finditer(r"([^P][^PKRHW][VLSWFNQ][ILTYWFN][FIY][^PKRH])", dna) # Regular expression to search the sequence for motifs that consist of 6 characters then saves the found motifs to a vairable.

		for matches in sequence: # For every match in the sequence variable the following loop is executed.
			print(matches.group(1)) # Prints the current motif to the terminal

			run_start = matches.start() # Saves the beginning motif identifier to a variable
			run_end = matches.end() # Saves the end motif identifier to a variable
			print("Region from " + str(run_start+1) + " to " + str(run_end+1)) # Prints the region of the current motif to the terminal

			d_UniprotResults.update({matches.group(1):("Region from " + str(run_start+1) + " to " + str(run_end+1))}) # In the same dictionary the current motif is saved as the key and the region where it is located is saved as the value - The +1 is due to all values in programming starting at 0 as opposed to 1 elsewhere.
			d_Email.update({matches.group(1):("Region from " + str(run_start+1) + " to " + str(run_end+1))})
			MatchCounter =  MatchCounter + 1 # Iterates the matchCounter variable so that the user can know how many motifs were found.
# ------------------------------------- Uniprot Code End   -------------------------------
		UACresult = d_UniprotResults # Sets a vairbale to hold the results
		noResultCounter = "" # This vairbale is initialised as a placeholder for if no motifs are found
		if MatchCounter == 0: # If there are no matches then this message is set
			noResultCounter = "No matched motifs were found"

		if userSubmissionForm["email"] != "":
			send_mail(d_Email, MatchCounter, userSubmissionForm["email"], accession_number + " - " + Description)

		return render_template("uniprotresults.html", result=UACresult, recordD=accession_number + " - " + Description, matches=MatchCounter, noResult=noResultCounter) # Returns the motif + position, the amount of matched motifs that were found and the placeholder message if there are no matches
	return render_template("uniprot.html", form=form) # else returns the same webpage/refreshes

# ------------------------------------- Uniprot Page End -------------------------------
@app.route("/")#Renders index page
def home():
	return render_template("index.html")
@app.route("/about")#Renders about page
def about():
	return render_template("about.html")

@app.route("/fasta", methods=["POST", "GET"])
def fasta():
	form = FastaForm() # Sets the web page to use the form from forms.py so it uses a Uniprot input as opposed to the FASTA one
	if form.is_submitted(): # Checks to see if the user has pressed submit
		userSubmissionForm = (request.form.to_dict()) # Sets the form as a dictionary
		userSubmission = userSubmissionForm["FASTA"] # Gets the FASTA key from the dictionary which is the user input as the second key is the submit button

		#Validation checks
		       
		if len(userSubmission) == 0: #If user has entered nothing into the text field then the page is refreshed and a message loads indicating their error
			flash("Input is required")
			return redirect(request.url)

		print ("FASTA input is " + userSubmission) # Prints the user submission to the terminal

		
		f = open('fastaInput.fasta','w') #Creates and writes a FASTA file for the input data to be saved.
		f.write(userSubmission)
		f.close()

		record_iterator = SeqIO.parse("fastaInput.fasta", "fasta") #Parses the input with a FASTA identifier from the file that was created
		
		first_record = next(record_iterator)
		print(first_record.id)

		fasta_code = userSubmission.replace("\n", "")# Declares and sets the Accession number to the FASTA key
		fasta_code = fasta_code.replace(" ", "")
		fasta_code = fasta_code.replace("\r", "")

		MatchCounter = 0 # Declares and sets a match counter to 0 which will later be sent to the next web page at the end of the code block

		d_FastaResults = {"Fasta code":userSubmission} # Creates a new dictionary with the first key and value set as the Accession number for readability purposes
		d_Email = {"Motif":"Position"}
# ------------------------------------- FASTA Code Start -------------------------------

		sequence = re.finditer(r"([^P][^PKRHW][VLSWFNQ][ILTYWFN][FIY][^PKRH])", str(first_record.seq)) # Regular expression to search the sequence for motifs that consist of 6 characters then saves the found motifs to a vairable.

		for matches in sequence: # For every match in the sequence variable the following loop is executed.
			print(matches.group(1)) # Prints the current motif to the terminal

			run_start = matches.start() # Saves the beginning motif identifier to a variable
			run_end = matches.end() # Saves the end motif identifier to a variable
			print("Region from " + str(run_start+1) + " to " + str(run_end+1)) # Prints the region of the current motif to the terminal

			d_FastaResults.update({matches.group(1):("Region from " + str(run_start+1) + " to " + str(run_end+1))}) # In the same dictionary the current motif is saved as the key and the region where it is located is saved as the value - The +1 is due to all values in programming starting at 0 as opposed to 1 elsewhere.
			d_Email.update({matches.group(1):("Region from " + str(run_start+1) + " to " + str(run_end+1))})
			MatchCounter =  MatchCounter + 1 # Iterates the matchCounter variable so that the user can know how many motifs were found.
# ------------------------------------- FASTA Code End   -------------------------------
		FASTAresult = d_FastaResults # Sets a vairbale to hold the results
		noResultCounter = "" # This vairbale is initialised as a placeholder for if no motifs are found
		if MatchCounter == 0: # If there are no matches then this message is set
			noResultCounter = "No matched motifs were found"

		if userSubmissionForm["email"] != "":
			send_mail(d_Email, MatchCounter, userSubmissionForm["email"], first_record.description)

		return render_template("fastaresults.html", result=FASTAresult, recordD=first_record.description, matches=MatchCounter, noResult=noResultCounter) # Returns the motif + position, the amount of matched motifs that were found and the placeholder message if there are no matches
	return render_template("fasta.html", form=form) # else returns the same webpage/refreshes

# ------------------------------------- Uniprot Page End -------------------------------
#Send mail class
def send_mail(result, matches, toEmail, recordDescription):
	email = "bioinformaticsuniprotmotifs@gmail.com"
	email_password = "!Bioinformatics123"
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	#Server activation and communication.
	server.login(email, email_password)
	#Server login using details specified on lines 18 and 20.

	#Subject of email.
	subject = 'Your results are ready! ' + str(matches) + ' matches were found'
	#Body of email - concatenates variables usch as price and the URL of product.
	resultNewLines = str(result)
	chars = "{}\'\'"
	for c in chars:
		resultNewLines = resultNewLines.replace(c, "")

	body = "The input description is: \n" + recordDescription + '\n\n' + "Results: \n" + resultNewLines.replace(",", "\n")

	msg = f"Subject: {subject}\n\n{body}"
	#Sends the email and encodes it with UTF-8 so that it can support sending the pound sterling symbol.
	server.sendmail(
		email,  #From email address.
		toEmail,  #To email address.
		msg.encode("UTF-8") #UTF-8 Encoding.
	)   #Email is sent this way as it makes more sense for a sole person to send and recive emails from the same account with this parser.
	print('Email has been sent to ' + email)
	#Prints that the email has been sent in the terminal.
	#Quits the email server.
	server.quit()
if __name__ == "__main__":
	app.run(debug=True)
