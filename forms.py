from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField

class UniprotForm(FlaskForm):
	UAC = StringField("Uniprot Accession Code")
	submit = SubmitField("Submit")
	email = StringField("Email (Optional)")

class FastaForm(FlaskForm):
	FASTA = TextAreaField("Fasta")
	fastaSubmit = SubmitField("Submit")
	email = StringField("Email (Optional)")