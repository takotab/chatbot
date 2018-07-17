import numpy as np
import pytest
import random
import string
import requests
from inital_test import test_start
from tests import Conversation

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


    response_content = conver.interact(id_, "Auto huren")

    assert "Op welke manier wilt u" in response_content

    response_content = conver.interact(id_, "aantal passagiers")

    assert "Met hoeveel" in response_content

    response_content = conver.interact(id_, "1-2")

    assert "We hebben deze opties aan kleine auto's" in response_content

    response_content = conver.interact(id_, "opel corsa")

    assert "Het kiezen van een auto is niet gelukt" in response_content


