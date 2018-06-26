import random
import string
import requests

# @pytest.mark.usefixtures('app')
def test_start(id_ = '25468eee'):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
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
    return str(response.content)

def test_waterstand_doorgeven():
    N = 4
    id_ = ''.join(random.choice(string.ascii_uppercase + string.digits)
                      for _ in range(N))
    test_start(id_ = id_)
    response_content = interact(id_, "waterstand doorgeven")

    assert "Wat is" in response_content
    assert "naam" in response_content


    