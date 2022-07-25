from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SelectField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, Optional, AnyOf
from pathlib import Path
import ast
path = Path(__file__).parent.resolve()
# import options for GICs
with open(path / 'GICs.txt') as f:
    gicOptions = f.read()
# convert options to list of tuples
gicOptions = ast.literal_eval(gicOptions)

# import options for Private HRT providers
with open(path / 'private_services.txt') as f:
    privateServices = f.read()
serviceOptions = ast.literal_eval(privateServices)


class InputForm(FlaskForm):
    countries = SelectField("Country", choices=['England', 'Northern Ireland', 'Scotland', 'Wales'], validators=[
        DataRequired(), AnyOf(['England', 'Northern Ireland', 'Scotland', 'Wales'], message="Please select a country")])
    self_med = BooleanField("I am self medicating")
    self_med_likely = BooleanField("I am likely to start self medicating")
    private_prescription = BooleanField("I hold a private prescription")
    foreign_prescription = BooleanField("I hold a foreign prescription")
    formal_diagnosis = BooleanField("I have a formal Diagnosis")
    hrt_recommendation = BooleanField("I have a letter of recommendation for HRT")
    shared_care = BooleanField("I want a shared care agreement with my GP")
    bridging_desired = BooleanField("I would like a bridging prescription")
    gic_referral = BooleanField("I would like to be referred to a GIC")
    chosen_gic = SelectField("Chosen GIC", choices=gicOptions, validate_choice=False)
    chosen_private_care = SelectField("Chosen Private Care", choices=serviceOptions, validate_choice=False)
    immigration_care = BooleanField("I am an immigrant looking to continue my care in the UK")
    immigration_letter = BooleanField("I have a letter from my previous HRT healthcare provider")
    name = StringField("First Name", validators=[Optional()])
    email = EmailField("Email", validators=[Optional(), Email()])
    phone = StringField("Phone Number", validators=[Optional()])
    docx = SubmitField("Generate Docx")
    pdf = SubmitField("Generate PDF")
    captcha = RecaptchaField()
