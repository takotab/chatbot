from . import match_text

def test_match_text():
    results = [('Jazeker',0),
    ('Nee',1),
    ("Jazeker dat klopt",0),
    ('Nee dat klopt niet',1),
    ("Neen dat is niet mijn naam mijn naam is tako",1)]
    for result in results:
        check(result)
    
def check(results):
    value = results[0]
    options = ["Jazeker","Neen"]
    best = match_text(value,options)
    assert best["choice"] == results[1]

