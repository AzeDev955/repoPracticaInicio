from app import app as flask_app


def test_home_ok():
    flask_app.testing = True
    client = flask_app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
