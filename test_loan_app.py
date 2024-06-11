import pytest
from loan_app import app


@pytest.fixture()
def client():
    return app.test_client()

def test_pinger(client):
    resp = client.get("/ping")
    assert resp.status_code == 200

def test_json_check(client):
    resp = client.get("/json")
    assert resp.status_code == 200
    assert resp.json == {'message': "Hi I am json!"}

def test_predict(client):
    test_data = {
        "ApplicantIncome": 1000000,
        "Credit_History": 1.0,
        "LoanAmount": 12000,
        "Married": "No",
        "Gender": "Male"
        }
    
    resp = client.post("/predict", json = test_data)

    assert resp.status_code == 200
    assert resp.json == {'Your_Loan_Application_is': "Rejected"}
