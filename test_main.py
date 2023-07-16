import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_payment_status():
    response = client.get("/getpaymentstatus")
    assert response.status_code == 200
    assert response.json() == {"data": 0 | 1}

def test_get_device_status():
    response = client.get("/getdevicestatus")
    assert response.status_code == 200
    assert response.json() == {"data": 0 | 1}

def test_paynow():
    response = client.put("/paynow/1")
    assert response.status_code == 200
    assert response.json() == {'status': 'success'}
    
def test_onoffdev():
    response1 = client.put("/onoffdev/1")
    assert response1.status_code == 200
    assert response1.json() == {'status': 'success'}
    
    response2 = client.put("/onoffdev/0")
    assert response2.status_code == 200
    assert response2.json() == {'status': 'success'}
    