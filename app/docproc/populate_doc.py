from docxtpl import DocxTemplate
from io import BytesIO
import jinja2
import convertapi
import requests
import os
from dotenv import load_dotenv

load_dotenv()

convertapi.api_secret = os.getenv('PDF_API_KEY')


def possessive(name):
    if name.endswith('s'):
        return name + '\''
    else:
        return name + '\'s'


def txt_to_var(txt):
    with open(f"templates/gender_journey/{txt}.txt", "r") as f:
        return f.read()

# formal_diagnosis = txt_to_var('formal_diagnosis')
# self_med = txt_to_var('self_med')


def generate_document(context):
    print(context)
    docx = BytesIO()
    doc = DocxTemplate(
        "/mnt/c/Users/broga/Documents/GitHub/tem/transinformer-frontend-server/app/docproc/templates/template_v0_1.docx")
    jinja_env = jinja2.Environment()
    jinja_env.filters['possessive'] = possessive
    doc.render(context, jinja_env)
    doc.save(docx)
    docx.seek(0)

    # upload docx
    conv = convertapi.UploadIO(docx, 'output.docx')

    # convert to pdf
    pdf = convertapi.convert('pdf', {'File': conv})

    # retrieve
    response_vars = vars(pdf)
    # get the URL of the converted document
    pdf_file = requests.get(
        response_vars['response']['Files'][0]['Url'], stream=True
    )

    # write to BytesIO for serving
    pdf_final = BytesIO(pdf_file.content)
    pdf_final.seek(0)
    return pdf_final
