from wsgiref.util import application_uri
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/test_submit", methods=["POST"])
def test_submit():
    if request.method == 'POST':
        return request.form
    else:
        return "Error"

if __name__ == '__main__':
    app.run(debug=True)