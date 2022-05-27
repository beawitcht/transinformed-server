from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SelectField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, Optional, AnyOf


class InputForm(FlaskForm):
    countries = SelectField("Country", choices=['England', 'Northern Ireland', 'Scotland', 'Wales'], validators=[
        DataRequired(), AnyOf(['England', 'Northern Ireland', 'Scotland', 'Wales'], message="Please select a country")])
    self_med = BooleanField("I am self medicating")
    formal_diagnosis = BooleanField("I have a formal Diagnosis")
    shared_care = BooleanField("I want a shared care agreement with my GP")
    name = StringField("First Name", validators=[Optional()])
    surname = StringField("Last Name", validators=[Optional()])
    email = EmailField("Email", validators=[Optional(), Email()])
    phone = StringField("Phone Number", validators=[Optional()])
    docx = SubmitField("Generate Docx")
    pdf = SubmitField("Generate PDF")
    captcha = RecaptchaField()
