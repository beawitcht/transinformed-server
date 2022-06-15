from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SelectField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, Optional, AnyOf


class InputForm(FlaskForm):
    countries = SelectField("Country", choices=['England'], validators=[
        DataRequired(), AnyOf(['England', 'Northern Ireland', 'Scotland', 'Wales'], message="Please select a country")])
    self_med = BooleanField("I am self medicating")
    self_med_likely = BooleanField("I am likely to start self medicating")
    formal_diagnosis = BooleanField("I have a formal Diagnosis")
    hrt_recommendation = BooleanField("I have a letter of recommendation for HRT")
    shared_care = BooleanField("I want a shared care agreement with my GP")
    bridging_desired = BooleanField("I would like a bridging prescription")
    name = StringField("First Name", validators=[Optional()])
    email = EmailField("Email", validators=[Optional(), Email()])
    phone = StringField("Phone Number", validators=[Optional()])
    docx = SubmitField("Generate Docx")
    pdf = SubmitField("Generate PDF")
    captcha = RecaptchaField()
