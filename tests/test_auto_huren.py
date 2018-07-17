import numpy as np
import pytest
import random
import string
import requests
from tests import Conversation, test_start

testdata = [
    ("aantal passagiers"),
    ("jaartal"),
    ]

@pytest.mark.parametrize("keuze_opties",testdata)
def test_auto_kiezen(keuze_opties, return_state = False):
    conver = test_start()

    response_content = conver.interact("Auto huren")

    assert "Op welke manier wilt u" in response_content, conver

    response_content = conver.interact(keuze_opties)
    if keuze_opties == "aantal passagiers":
        assert "Met hoeveel passagiers" in response_content, conver

        if return_state:
            return conver

    elif keuze_opties == "jaartal":
        assert "Hoe nieuw wilt u uw auto" in response_content, conver

    if return_state:
         return conver


aantal_passagiers_data = [
    ("1","kleine auto"),
    ("1-2","kleine auto's"),
    ("3-5","grote auto's"),
    ("3-5","grote auto")
    ]

@pytest.mark.parametrize("aantal, resp",aantal_passagiers_data)
def test_aantal_passagiers(aantal, resp):
    conver = test_auto_kiezen("aantal passagiers",return_state = True)
    response_content = conver.interact(aantal)

    assert resp in response_content, conver




jaartal_data = [
    ("vóór 2000","oude auto's"),
    ("vóór 2000","oude auto"),
    ("na 2000", "nieuwe auto's"),
    ("na 2000", "nieuwe auto")
    ]

@pytest.mark.parametrize("aantal, resp",jaartal_data)
def test_jaartal(aantal, resp):
    conver = test_auto_kiezen("jaartal",return_state = True)
    response_content = conver.interact(aantal)
    assert resp in response_content, conver