from app.docproc.populate_doc import possessive, generate_document


# test that the name is using the correct possession form
def test_possessive():
    name_ending_s = possessive('Tas')
    name_not_ending_s = possessive('Bea')
    no_name = possessive('')

    assert name_ending_s == 'Tas\'', 'Expected "Tas\'", got ' + name_ending_s
    assert name_not_ending_s == 'Bea\'s', 'Expected "Bea\'s", got ' + name_not_ending_s
    assert no_name == 'My', 'Expected None, got ' + no_name


# test doc is returning data
def test_generate_doc_docx():

    context = {
        'countries': 'England',
        'self_med': True,
        'self_med_likely': False,
        'formal_diagnosis': True,
        'hrt_recommendation': False,
        'shared_care': False,
        'bridging_desired': False,
        'gic_referral': True,
        'chosen_gic': 'Leeds - Wait time (months): 44',
        'name': 'Bea',
        'email': 'test123@test.com',
        'phone': '1234567890',
        'docx': True,
        'pdf': False,
        'captcha': None
    }
    docx = generate_document(context, 'docx')

    assert docx.getvalue() != b'', 'Expected data got' + len(docx.getvalue())
    assert docx is not None
