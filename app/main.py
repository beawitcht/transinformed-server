from flask import Flask, render_template, request, send_file
from docproc.populate_doc import generate_document
import requests
import os
import json

api_key = os.getenv('PDF_API_KEY')

app = Flask(__name__)


@app.route("/")
def index():
    seconds_left = json.loads(requests.get(
        f"https://v2.convertapi.com/user?Secret={api_key}").text)['SecondsLeft']

    if int(seconds_left) < 50:
        pdf_available = False
    else:
        pdf_available = True
    return render_template("index.html", pdf_available=pdf_available)


@app.route("/test_submit", methods=["POST"])
def test_submit():
    if request.method == 'POST':
        filetype = request.form['filetype']
        file = generate_document(request.form.to_dict(), filetype)
        try:
            return send_file(file, download_name=f"transgpguide.{filetype}")
        except:
            if filetype == "pdf":
                return ("An error occured, PDF downloads may be maxxed out, please download the .docx version")
            else:
                return ("An error occured, please try again later")


if __name__ == '__main__':
    app.run(debug=True)
