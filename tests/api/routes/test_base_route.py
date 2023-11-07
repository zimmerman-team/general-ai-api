from manage import app

HEADERS = {
    "Authorization": "ZIMMERMAN"
}


def test_base_route():
    # Return a 200 OK response as JSON
    print("test base route - headers: ", HEADERS)
    response = app.test_client().get("/", headers=HEADERS)
    print("response - ", response)
    assert response.status_code == 200
    assert response.json["result"] == "Welcome to the Zimmerman General AI API! Consult the documentation for the API endpoints."
