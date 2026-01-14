from sqlalchemy import text

def test_get_doctors_success(client, db_session):
    # 🔥 먼저 비운다
    db_session.execute(text("DELETE FROM doctors"))
    db_session.commit()

    # 그 다음 생성
    client.post(
        "/api/v1/admin/doctor",
        json={"doctor_name": "김의사", "department": "피부과"}
    )

    res = client.get("/api/v1/admin/doctor")

    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0]["doctor_name"] == "김의사"

def test_get_doctors_fail_empty_result(client):
    res = client.get("/api/v1/admin/doctor", params={"department": "정형외과"})

    assert res.status_code == 200
    assert res.json() == []

def test_create_doctor_success(client):
    res = client.post(
        "/api/v1/admin/doctor",
        json={"doctor_name": "김의사", "department": "피부과"}
    )

    assert res.status_code == 200
    assert res.json()["doctor_name"] == "김의사"

def test_create_doctor_fail_missing_field(client):
    res = client.post(
        "/api/v1/admin/doctor",
        json={"department": "피부과"}  # doctor_name 누락
    )

    assert res.status_code == 422

def test_update_doctor_success(client, db_session):
    db_session.execute(text("DELETE FROM doctors"))
    db_session.commit()

    create = client.post(
        "/api/v1/admin/doctor",
        json={"doctor_name": "김의사", "department": "피부과"}
    )
    doctor_id = create.json()["doctor_id"]

    res = client.patch(
        f"/api/v1/admin/doctor/{doctor_id}",
        json={"doctor_name": "김의사_수정"}
    )

    assert res.status_code == 200
    assert res.json()["doctor_name"] == "김의사_수정"

def test_update_doctor_fail_not_found(client, db_session):
    db_session.execute(text("DELETE FROM doctors"))
    db_session.commit()

    res = client.patch(
        "/api/v1/admin/doctor/999",
        json={"doctor_name": "없는의사"}
    )

    assert res.status_code == 404
    assert res.json()["detail"] == "해당 의사가 존재하지 않습니다."

def test_delete_doctor_success(client, db_session):
    db_session.execute(text("DELETE FROM doctors"))
    db_session.commit()

    create = client.post(
        "/api/v1/admin/doctor",
        json={"doctor_name": "김의사", "department": "피부과"}
    )
    doctor_id = create.json()["doctor_id"]

    res = client.delete(f"/api/v1/admin/doctor/{doctor_id}")
    assert res.status_code == 200

    list_res = client.get("/api/v1/admin/doctor")
    names = [d["doctor_name"] for d in list_res.json()]

    assert "김의사" not in names

def test_delete_doctor_fail_not_found(client, db_session):
    db_session.execute(text("DELETE FROM doctors"))
    db_session.commit()
    res = client.delete("/api/v1/admin/doctor/999")

    assert res.status_code == 404
    assert res.json()["detail"] == "해당 의사가 존재하지 않습니다."
