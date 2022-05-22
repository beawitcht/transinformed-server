from flask import Flask, render_template, request, send_file
from docproc.populate_doc import generate_document

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/test_submit", methods=["POST"])
def test_submit():
    if request.method == 'POST':
        file = generate_document(request.form.to_dict())
        return send_file(file, as_attachment=True, attachment_filename='out.docx')

    else:
        return "Error"

if __name__ == '__main__':
    app.run(debug=True)