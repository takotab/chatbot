import pytest

@pytest.mark.usefixtures('app')
def test_watermeter_story(app):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    id = '__id__' + '938490abve'
    response = app.post('/get',
                                data=dict(msg='e' + id),
                                follow_redirects=True)
    assert response.status_code == 200
    print(response)
    assert b"Thanks for logging in, patkennedy79@gmail.com!" in response.data
    assert b"Welcome patkennedy79@gmail.com!" in response.data
    assert b"Flask User Management" in response.data
    assert b"Logout" in response.data
    assert b"Login" not in response.data
    assert b"Register" not in response.data
 
    """
    GIVEN a Flask application
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    # response = app.get('/logout', follow_redirects=True)
