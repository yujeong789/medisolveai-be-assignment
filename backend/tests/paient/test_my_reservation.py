def test_read_my_reservation_success(client):
    payload = {
        "patient_name": "홍길동",
        "phone": "010-1234-5678"
    }

    response = client.post("/api/v1/patient/my", json=payload)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_my_reservation_empty(client):
    payload = {
        "patient_name": "없는사람",
        "phone": "010-0000-0000"
    }

    response = client.post("/api/v1/patient/my", json=payload)
    assert response.status_code == 200
    assert response.json() == []
