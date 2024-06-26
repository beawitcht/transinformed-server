from dotenv import load_dotenv
from docxtpl import DocxTemplate
from io import BytesIO
from pathlib import Path
import jinja2
import convertapi
import requests
import os


path = Path(__file__).parent.resolve()
env_path = Path(__file__).parents[1].resolve()
load_dotenv(env_path / '.env')

convertapi.api_secret = os.getenv('PDF_API_KEY')


def possessive(name):
    if name == '':
        return 'My'
    elif name.endswith('s'):
        return name + '\''
    else:
        return name + '\'s'

def remove_wait_times(name):
    return name.split('-', 1)[0]


def generate_document(context, filetype):
    docx = BytesIO()
    if context['under_16'] == True:
        doc = DocxTemplate(path / 'templates' / 'under_16_template.docx')
    else:
        doc = DocxTemplate(path / 'templates' / 'template_v1_0.docx')
    jinja_env = jinja2.Environment(autoescape=True)
    jinja_env.filters['possessive'] = possessive
    jinja_env.filters['format_gic'] = remove_wait_times
    # remove images if text context is empty
    if context['phone'] == '':
        doc.replace_media(path / 'images' / 'phone.png', path / 'images' / 'blank.png')
    if context['email'] == '':
        doc.replace_media(path / 'images' / 'email.png', path / 'images' / 'blank.png')

    doc.render(context, jinja_env)
    doc.save(docx)
    docx.seek(0)

    if filetype == "docx":
        return docx

    elif filetype == "pdf":
        # upload docx
        conv = convertapi.UploadIO(docx, 'myhealthcareguide.docx')

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

    else:
        return "Error: invalid filetype"
