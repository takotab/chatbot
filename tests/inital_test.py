import numpy as np
import pytest
import requests
from tests import Conversation
# from entity_rec.match import match_text
# use python3 -m pytest tests/ to test

def test_interface():
    url = 'http://' + 'localhost:8080'
    response = requests.get(url)
    assert response.status_code == 200

def test_start(conver = None):
    """
    
    """
    if conver is None:
        conver = Conversation()
    response_content = conver.interact( 'e')

    assert "Waterstand doorgeven" in response_content
    assert "Watergebruik analyse" in response_content
    assert "Factuur inzien" in response_content
    assert "Adreswijziging" in response_content
    # assert "Wie ben jij?" in response_content
    return conver

testdata_confirmation = [
    ("Ja", True),
    ("Jazeker", True),
    ("Inderdaad", True),
    ("Jazeker dat klopt.", True),
    ("Jazeker", True),
    ("Nee", False),
    ("neen", False),
    ("Dit klopt niet.", False),
]

@pytest.mark.parametrize("confirmes_msg,boolean", testdata_confirmation)
def test_confirmation(confirmes_msg,boolean):
    """
    :param confirmes_msg: The messege that is used to confirm the request
    :return: If the chatbot understands the reply
    """
    # TODO: make other test to add extra confirmation
    conver = test_start()

    response_content = conver.interact( "waterstand doorgeven")

    response_content = conver.interact( "Mijn naam is Bert Schaap.")
    # assert naam.lower() in str(response_content).lower()

    response_content = conver.interact(confirmes_msg)
    if boolean:
        assert "de waterstand?" in response_content, conver
    else:
        assert "excuses" in response_content, conver

testdata = [
    ("tako Tabak",False),
    ("Melis Schaap",True),
    ("Bert Schaap",True),
    ("Jan Schaap",True),
]

@pytest.mark.parametrize("naam,is_in_sys", testdata)
def test_waterstand_doorgeven(naam,is_in_sys):
    conver = test_start()
    
    response_content = conver.interact( "waterstand doorgeven")

    # assert "Wat is" in response_content
    # assert "naam" in response_content


    response_content = conver.interact( "Mijn naam is " + naam)
    assert naam.lower() in str(response_content).lower()

    if is_in_sys:
        assert "Dit klopt allemaal?" in response_content ,conver
        assert "gevonden in het systeem" in response_content , conver
    else:
        assert "Ik kan je niet vinden in het systeem als" in response_content
        return

    response_content = conver.interact( "Jazeker ")

    assert "de waterstand?" in response_content, conver


    waterstand = str(np.random.randint(1000))
    response_content = conver.interact( "Mijn waterstand is " + waterstand)


    assert waterstand in response_content , conver
    assert "klopt, dat?"

    response_content = conver.interact( "Jazeker dat klopt ")
    print(response_content)
    assert 'de waterstand is doorgegeven' in response_content, conver



@pytest.mark.parametrize("naam,is_in_sys", testdata)
def test_waterstand_analyse(naam,is_in_sys):
    conver = test_start()

    if not is_in_sys:
        return

    #NOTE: not a full setentence
    response_content = conver.interact( "watergebruik analyseren")

    assert "helpen met administrative handelingen" in response_content, conver
    
    response_content = conver.interact( "Ik heet " + naam)

    assert naam in response_content, conver
    assert "klopt" in response_content, conver

    #NOTE: this is not a full response but just repeated the word must be test more thorough
    # will probally fail these tests
    response_content = conver.interact( "Jazeker ")

    assert "De waterstand is" in response_content, conver
    assert "dan normaal" in response_content, conver

    assert "Ik laat u weer zien wat ik allemaal voor u kan doen." in response_content, conver










    



    