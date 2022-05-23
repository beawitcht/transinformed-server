from flask import Flask, render_template, request, send_file
from docproc.populate_doc import generate_document


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/test_submit", methods=["POST"])
def test_submit():
    if request.method == 'POST':
        docx = generate_document(request.form.to_dict())
        try:
            return send_file(docx, download_name='transgpguide.pdf')
        except:
            return ("An error occured, PDF downloads may be maxxed out, please download the .docx version")


if __name__ == '__main__':
    app.run(debug=True)
