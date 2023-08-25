from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import BooleanField, SubmitField, HiddenField
from wtforms.validators import DataRequired

class UploadForm(FlaskForm):
    upload = FileField("Please upload your file here (docx or pdf):", validators=[FileRequired(), FileAllowed(['docx', 'pdf'], 'Ensure file is docx or pdf only')])
    submit = SubmitField("Upload file")
    id = HiddenField("id")

class PurchaseForm(FlaskForm):
    document_ready = BooleanField("I have generated and reviewed my document ahead of purchase, and I understand that 24 hours after purchase, I will no longer be able to modify the document", validators=[DataRequired()])
    data_ready = BooleanField("I understand that my file will be stored for 30 days to ensure that the document is delivered succesfully and without defect", validators=[DataRequired()])
    third_party_consent = BooleanField("I understand that my payment and details will be processed by Stripe, and my address and document will be shared with our printing fullfilment provider", validators=[DataRequired()])
    submit = SubmitField("Buy £14.99")