import numpy as np
import pytest
import random
import string
import requests
from tests import Conversation


def test_interface():
    url = 'http://' + 'localhost:8080'
    response = requests.get(url)
    assert response.status_code == 200


def test_start(id_='25468eee'):
    """

    """
    conver = Conversation()
    response_content = conver.interact(id_, 'e')

    assert "Waterstand doorgeven" in response_content
    assert "Watergebruik analyse" in response_content
    assert "Factuur inzien" in response_content
    assert "Adreswijziging" in response_content
    assert "Auto huren" in response_content

testdata = [
    ("aantal passagiers"),
    ("jaartal"),
]

@pytest.mark.parametrize("keuze_optie", testdata)
def test_auto_kiezen(keuze_optie):
    conver = Conversation()
    N = 4
    id_ = ''.join(random.choice(string.ascii_uppercase + string.digits)
                      for _ in range(N))
    test_start(id_ = id_)

    response_content = conver.interact(id_, "aantal passagiers")

    assert "Hoe nieuw wilt u" in response_content

    response_content = conver.interact(id_, "1-2")

    assert "We hebben deze opties aan kleine auto's" in response_content

    response_content = conver.interact(id_, "opel corsa")

    assert "Het kiezen van een auto is niet gelukt" in response_content


