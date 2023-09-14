from flask import Blueprint, render_template, request, send_file
from main import cache, limiter
from forms.input_form import InputForm
from docproc.populate_doc import generate_document
import requests, json, os

api_key = os.getenv('PDF_API_KEY')
pdf_limit = os.getenv('PDF_LIMIT')
core_bp = Blueprint('core', __name__)

@core_bp.route("/", methods=['GET', 'POST'])
# Don't limit GET requests or docx generation
@limiter.limit(pdf_limit, exempt_when=lambda: request.method != 'POST' or request.form.get('docx'))
@cache.cached(timeout=60 * 60 * 24 * 7, unless=lambda: request.method == 'POST')
def home():
    api_data = json.loads(requests.get(f"https://v2.convertapi.com/user?Secret={api_key}").text)
    try:
        seconds_left = api_data['SecondsLeft']
    except KeyError:
        seconds_left = 0

    # check if api limit reached
    if int(seconds_left) < 10:
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
            return send_file(file, download_name=f"myhealthcareguide.{filetype}")
        except file.getvalue() is None:
            if filetype == "pdf":
                return ("PDF download limit reached, please download .docx version")
            else:
                return ("An error occured, please try again later")

    return render_template("index.html", form=form, pdf_available=pdf_available)


@core_bp.route("/about", methods=['GET'])
@cache.cached(timeout=60 * 60 * 24 * 7)
def about():
    return render_template("about.html")


@core_bp.route("/resources", methods=['GET'])
@cache.cached(timeout=60 * 60 * 24 * 7)
def resources():
    return render_template("resources.html")

@core_bp.route("/sources", methods=['GET'])
@cache.cached(timeout=60 * 60 * 24 * 7)
def sources():
    return render_template("sources.html")

