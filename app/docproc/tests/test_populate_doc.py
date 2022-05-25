from app.docproc.populate_doc import possessive, generate_document


def test_possessive():
    name_ending_s = possessive('Tas')
    name_not_ending_s = possessive('Bea')

    assert name_ending_s == 'Tas\'', 'Expected "Tas\'", got ' + name_ending_s
    assert name_not_ending_s == 'Bea\'s', 'Expected "Bea\'s", got ' + name_not_ending_s


def test_generate_doc_docx():

    context = {
        'country': 'England',
        'formal_diagnosis': True,
        'name': 'Bea',
        'surname': '',
        'email': 'test123@test.com',
        'phone': '1234567890',
        'docx': True
    }
    docx = generate_document(context, 'docx')

    assert docx.getvalue() != b'', 'Expected data got' + len(docx.getvalue())
    assert docx is not None
