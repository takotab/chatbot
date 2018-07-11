import numpy as np
import pytest
import random
import string
import requests
# from entity_rec.match import match_text
# use python3 -m pytest tests/ to test

def test_interface():
    url = 'http://' + 'localhost:8080'
    response = requests.get(url)
    assert response.status_code == 200

def test_start(id_ = '25468eee'):
    """
    
    """
    response_content = interact(id_, 'e')

    assert "Waterstand doorgeven" in response_content
    assert "Watergebruik analyse" in response_content
    assert "Factuur inzien" in response_content
    assert "Adreswijziging" in response_content

def interact(id_, msg):
    id_ = '__id__' + id_
    url = 'http://' + 'localhost:8080'
    response = requests.get(url + '/get',params={"msg":msg + id_})
    assert response.status_code == 200
    return str(response.content, 'utf-8')

testdata = [
    ("tako Tabak",False),
    ("Melis Schaap",True),
    ("Bert Schaap",True),
    ("Jan Schaap",True),
]


@pytest.mark.parametrize("naam,is_in_sys", testdata)
def test_waterstand_doorgeven(naam,is_in_sys):
    N = 4
    id_ = ''.join(random.choice(string.ascii_uppercase + string.digits)
                      for _ in range(N))
    test_start(id_ = id_)
    response_content = interact(id_, "waterstand doorgeven")

    # assert "Wat is" in response_content
    # assert "naam" in response_content


    response_content = interact(id_, "Mijn naam is " + naam)
    assert naam.lower() in str(response_content).lower()

    if is_in_sys:
        assert "Dit klopt allemaal?" in response_content
        assert "gevonden in het systeem" in response_content
    else:
        assert "Ik kan je niet vinden in het systeem als" in response_content
        return
    
    response_content = interact(id_, "Jazeker ")

    assert "de waterstand?" in response_content


    waterstand = str(np.random.randint(1000))
    response_content = interact(id_, "Mijn waterstand is " + waterstand)


    assert waterstand in response_content
    assert "klopt, dat?"

    response_content = interact(id_, "Jazeker dat klopt ")
    print(response_content)
    assert 'de waterstand is doorgegeven' in response_content





    



    