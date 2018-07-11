import numpy as np
import pytest
import random
import string
import requests
from tests import Conversation
# from entity_rec.match import match_text
# use python3 -m pytest tests/ to test

def test_interface():
    url = 'http://' + 'localhost:8080'
    response = requests.get(url)
    assert response.status_code == 200

def test_start(id_ = '25468eee'):
    """
    
    """
    conver = Conversation()
    response_content = conver.interact(id_, 'e')

    assert "Waterstand doorgeven" in response_content
    assert "Watergebruik analyse" in response_content
    assert "Factuur inzien" in response_content
    assert "Adreswijziging" in response_content


testdata = [
    ("tako Tabak",False),
    ("Melis Schaap",True),
    ("Bert Schaap",True),
    ("Jan Schaap",True),
]


@pytest.mark.parametrize("naam,is_in_sys", testdata)
def test_waterstand_doorgeven(naam,is_in_sys):
    conver = Conversation()
    N = 4
    id_ = ''.join(random.choice(string.ascii_uppercase + string.digits)
                      for _ in range(N))
    test_start(id_ = id_)
    
    response_content = conver.interact(id_, "waterstand doorgeven")

    # assert "Wat is" in response_content
    # assert "naam" in response_content


    response_content = conver.interact(id_, "Mijn naam is " + naam)
    assert naam.lower() in str(response_content).lower()

    if is_in_sys:
        assert "Dit klopt allemaal?" in response_content ,conver
        assert "gevonden in het systeem" in response_content , conver
    else:
        assert "Ik kan je niet vinden in het systeem als" in response_content
        return
    
    response_content = conver.interact(id_, "Jazeker ")

    assert "de waterstand?" in response_content, conver


    waterstand = str(np.random.randint(1000))
    response_content = conver.interact(id_, "Mijn waterstand is " + waterstand)


    assert waterstand in response_content , conver
    assert "klopt, dat?"

    response_content = conver.interact(id_, "Jazeker dat klopt ")
    print(response_content)
    assert 'de waterstand is doorgegeven' in response_content, conver


@pytest.mark.parametrize("naam,is_in_sys", testdata)
def test_waterstand_analyse(naam,is_in_sys):
    conver = Conversation()

    N = 4
    id_ = ''.join(random.choice(string.ascii_uppercase + string.digits)
                      for _ in range(N))
    test_start(id_ = id_)

    if not is_in_sys:
        return

    #NOTE: not a full setentence
    response_content = conver.interact(id_, "watergebruik analyseren")

    assert "helpen met administrative handelingen" in response_content, conver
    
    response_content = conver.interact(id_, "Ik heet " + naam)

    assert naam in response_content, conver
    assert "klopt" in response_content, conver

    #NOTE: this is not a full response but just repeated the word must be test more thorough
    # will probally fail these tests
    response_content = conver.interact(id_, "Jazeker ")

    assert "De waterstand is" in response_content, conver
    assert "dan normaal" in response_content, conver

    assert "Ik laat u weer zien wat ik allemaal voor u kan doen." in response_content, conver










    



    