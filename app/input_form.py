from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SelectField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, Optional, AnyOf
from pathlib import Path
from custom_form_elements import CustomSelect
import ast
path = Path(__file__).parent.resolve()
# import options for GICs
with open(path / 'GICs.txt') as f:
    gic_options = f.read()
# change NaN's to Unkown
gic_options = gic_options.replace('nan', 'Unknown')
# convert options to list of tuples
gic_options = ast.literal_eval(gic_options)
gic_options.insert(0,("0", "Select a country to see GICs"))
gic_options.insert(1,("1", "I don't have a preferred clinic"))

# import options for Private HRT providers
with open(path / 'private_services.txt') as f:
    private_services = f.read()
service_options = ast.literal_eval(private_services)
service_options.insert(0,"I haven't chosen a provider yet")


class InputForm(FlaskForm):
    countries = SelectField("Country", choices=['Choose...','England', 'Northern Ireland', 'Scotland', 'Wales'], validators=[
        DataRequired(), AnyOf(['England', 'Northern Ireland', 'Scotland', 'Wales'], message="Please select a country")])
    self_med = BooleanField("I am self medicating")
    self_med_likely = BooleanField("I am likely to start self medicating")
    no_self_med = BooleanField("I am not currently or likely to start self medicating")
    no_fixed_address = BooleanField("I do not have any proof of address")
    no_id_proof = BooleanField("I do not have any proof of identification")
    private_prescription = BooleanField("I have a private prescription for HRT")
    foreign_prescription = BooleanField("I have been prescribed HRT outside of the UK")
    formal_diagnosis = BooleanField("I have a formal diagnosis")
    hrt_recommendation = BooleanField("I have a letter of recommendation for HRT")
    no_doc = BooleanField("I do not have any of these documents")
    shared_care = BooleanField("I need a shared care agreement")
    bridging_desired = BooleanField("I need a bridging prescription (select medication status)")
    gic_referral = BooleanField("I need a referral to a Gender Identity Clinic")
    chosen_gic = SelectField("Chosen GIC", choices=gic_options, validate_choice=False, widget=CustomSelect())
    chosen_private_care = SelectField("My chosen private provider", choices=service_options, validate_choice=False)
    immigration_care = BooleanField("I am an immigrant looking to continue my care in the UK")
    immigration_letter = BooleanField("I have a letter from my previous HRT healthcare provider")
    blood_testing = BooleanField("I need regular blood testing and monitoring")
    name = StringField("Name", validators=[Optional()])
    pronouns = StringField("Pronouns", validators=[Optional()])
    email = EmailField("Email", validators=[Optional(), Email()])
    phone = StringField("Phone Number", validators=[Optional()])
    docx = SubmitField("Generate Docx")
    pdf = SubmitField("Generate PDF")
    captcha = RecaptchaField()
