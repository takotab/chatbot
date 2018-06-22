import numpy as np
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

def test_sub():

    text = "hello mijn naam is Tako Tabak. Ik wil graag! dat dit gelijk blrijt werken 893"
    
    from . import sub_embedding
    subword = sub_embedding.add_subword(text)
    print(subword.shape)
    assert subword.shape == (17, 39)

def test_embedding():
    text = "hello mijn naam is Tako Tabak. Ik wil graag! dat dit gelijk blrijt werken 893"
    
    from . import embedding
    nederlands = embedding.language("NL")
    emb = nederlands.get_sentence_embedding(text)
    print(emb.shape)
    assert emb.shape == (17,300)

def test_sub_sentence():

    text = "hello mijn naam is Tako Tabak. Ik wil graag! dat dit gelijk blrijt werken 893"
    
    from . import sub_embedding

    subsentence = sub_embedding.add_subsentence(text)

    assert len(subsentence.shape) == 1

def test_chatbot():
    # from .chatbot import dialog
    # from . import procces_data
    from . import check_prep_files

    check_prep_files.init()

    text = "hello mijn naam is Tako Tabak. Ik wil graag! dat dit gelijk blrijt werken 893"
    
    from . import embedding
    nederlands = embedding.language("NL")
    emb = nederlands.get_sentence_embedding(text)
    print(emb.shape)
    from . import sub_embedding
    subword = sub_embedding.add_subword(text)
    emb = np.concatenate((emb,subword),axis = 1)

    assert emb.shape == (17,339)
    


