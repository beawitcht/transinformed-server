from flask import Flask, render_template, request, send_file
from flask_wtf import FlaskForm
from docproc.populate_doc import generate_document
from input_form import InputForm
import requests
import os
import json


api_key = os.getenv('PDF_API_KEY')

app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('RECAPTCHA_PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('RECAPTCHA_PRIVATE_KEY')


@app.route("/", methods=['GET', 'POST'])
def validation_test():
    api_data = json.loads(requests.get(f"https://v2.convertapi.com/user?Secret={api_key}").text)

    seconds_left = api_data['SecondsLeft']

    if int(seconds_left) < 50:
        pdf_available = False
    else:
        pdf_available = True

    form = InputForm()
    if form.validate_on_submit():
        if form.docx.data:
            filetype = "docx"
        elif form.pdf.data:
            filetype = "pdf"

        file = generate_document(form.data, filetype)

        try:
            return send_file(file, download_name=f"transgpguide.{filetype}")
        except file.getvalue() is None:
            if filetype == "pdf":
                return ("PDF downloads maxxed please download .docx version")
            else:
                return ("An error occured, please try again later")

    return render_template("index.html", form=form, pdf_available=pdf_available)


if __name__ == '__main__':
    app.run(debug=True)
