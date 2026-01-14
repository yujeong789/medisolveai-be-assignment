def test_get_doctors_success(client, db_session):
    """
    정상 케이스: 의사 목록 조회
    """
    from app.common.models import Doctor

    db_session.query(Doctor).delete()
    db_session.commit()
    
    doctor1 = Doctor(doctor_name="임윤아", department="피부과")
    doctor2 = Doctor(doctor_name="김세정", department="레이저")

    db_session.add_all([doctor1, doctor2])
    db_session.commit()
    db_session.refresh(doctor1)
    db_session.refresh(doctor2)

    response = client.get("/api/v1/patient/doctors")
    print(f"\n[DEBUG] API Response: {response}") # 데이터 구조 확인용
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)



def test_get_doctors_empty_by_department(client, db_session):
    """
    예외 케이스: 존재하지 않는 진료과 필터
    """

    from app.common.models import Doctor

    doctor1 = Doctor(doctor_name="임윤아", department="피부과")
    doctor2 = Doctor(doctor_name="김세정", department="레이저")

    db_session.add_all([doctor1, doctor2])
    db_session.commit()
    
    response = client.get("/api/v1/patient/doctors?department=정형외과")

    assert response.status_code == 200
    assert response.json() == []