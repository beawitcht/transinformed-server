from docxtpl import DocxTemplate
from io import BytesIO
import jinja2


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
    out = BytesIO()
    doc = DocxTemplate("/mnt/c/Users/broga/Documents/GitHub/tem/transinformer-frontend-server/app/docproc/templates/template_v0_1.docx")
    jinja_env = jinja2.Environment()
    jinja_env.filters['possessive'] = possessive
    doc.render(context, jinja_env)
    doc.save(out)
    out.seek(0)
    
    return out
