from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SelectField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, Optional, AnyOf
from pathlib import Path
from custom_form_elements import CustomSelect
import json
path = Path(__file__).parent.resolve()
# import options for GICs
with open(path / 'GICs.json') as f:
    gic_options = json.loads(f.read())

# convert from JSON to list of tuples - show nan as Unknown for wait times
gic_options = gic_options["GICs"]
gic_options = [(country, clinic.replace('nan', 'Unknown')) for country, clinic in gic_options]
# change NaN's to Unknown

gic_options.insert(0,("0", "Select a country and service to see GICs"))
gic_options.insert(1,("1", "I don't have a preferred clinic"))

# import options for Private HRT providers
with open(path / 'private_services.json') as f:
    private_services = json.loads(f.read())
service_options = private_services["Private Services"]
service_options.insert(0,"I haven't chosen a provider yet")


class InputForm(FlaskForm):
    countries = SelectField("Country", choices=['Choose...','England', 'Northern Ireland', 'Scotland', 'Wales'], validators=[
        DataRequired(), AnyOf(['England', 'Northern Ireland', 'Scotland', 'Wales'], message="Please select a country")])
    services = SelectField("Services", choices=['Choose...','Adult (17+)', 'Youth (≤16)'], validators=[
        DataRequired(), AnyOf(['Adult (17+)', 'Youth (≤16)'], message="Please select adult or youth services")])
    self_med = BooleanField("I am self medicating")
    self_med_likely = BooleanField("I am likely to start self medicating")
    no_self_med = BooleanField("I am not currently or likely to start self medicating")
    under_16 = BooleanField("I am 15 or under")
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
    slt_referral = BooleanField("I need a referral to a Speech & Language Therapist")
    passport_letter = BooleanField("I need a letter to update the gender marker on my passport")
    grc_letter = BooleanField("I need a report for my Gender Recognition Certificate (GRC) application")
    nhs_record_gender = BooleanField("I need to update my NHS records to reflect my gender")
    nhs_record_name = BooleanField("I need to update my NHS records to reflect my name")
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
