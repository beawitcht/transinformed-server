from populate_doc import possessive

def test_possessive():
    name_ending_s = possessive('Tas')
    name_not_ending_s = possessive('Bea')
    
    assert name_ending_s == 'Tas\'', 'Expected "Tas\'", got ' + name_ending_s
    assert name_not_ending_s == 'Bea\'s', 'Expected "Bea\'s", got ' + name_not_ending_s
    
    