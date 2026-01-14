USE medisolve;

-- 1. 의사 정보 (Doctor)
-- 바뀐 모델의 'is_active' 컬럼을 추가했습니다. (기본값 1/True)
INSERT INTO doctors (doctor_name, department, is_active) VALUES 
('김철수', '피부과', 1),
('이영희', '성형외과', 1),
('박지성', '일반가정의학과', 1);

-- 2. 진료 항목 (Treatment) - 기존과 동일
INSERT INTO treatments (treatment_name, duration_minutes, price, description) VALUES 
('기본 진료', 30, 15000, '일반 상담 및 진찰'),
('보톡스(이마)', 30, 50000, '이마 주름 개선 시술'),
('레이저 제모', 30, 100000, '겨드랑이/종아리 레이저 제모'),
('필러(코)', 30, 250000, '콧대 보충 필러 시술');

-- 3. 병원 운영 시간 (OperatingHour) - 기존과 동일
INSERT INTO operating_hours (day_of_week, open_time, close_time, break_start_time, break_end_time, is_opened) VALUES 
(0, '09:00:00', '18:00:00', '13:00:00', '14:00:00', 1),
(1, '09:00:00', '18:00:00', '13:00:00', '14:00:00', 1),
(2, '09:00:00', '18:00:00', '13:00:00', '14:00:00', 1),
(3, '09:00:00', '18:00:00', '13:00:00', '14:00:00', 1),
(4, '09:00:00', '18:00:00', '13:00:00', '14:00:00', 1),
(5, '09:00:00', '13:00:00', NULL, NULL, 1),
(6, '00:00:00', '00:00:00', NULL, NULL, 0);

-- 4. 병원 슬롯 설정 (HospitalSlot) - 기존과 동일
INSERT INTO hospital_slots (start_time, end_time, max_capacity) VALUES 
('09:00:00', '09:30:00', 2),
('09:30:00', '10:00:00', 2),
('10:00:00', '10:30:00', 3),
('10:30:00', '11:00:00', 3),
('14:00:00', '14:30:00', 3),
('14:30:00', '15:00:00', 3),
('15:00:00', '15:30:00', 3),
('15:30:00', '16:00:00', 3),
('16:00:00', '16:30:00', 3),
('16:30:00', '17:00:00', 2),
('17:00:00', '17:30:00', 2),
('17:30:00', '18:00:00', 2);

-- 5. 환자 정보 (Patient) - UniqueConstraint('_name_phone_uc') 준수
INSERT INTO patients (patient_id, patient_name, phone) VALUES 
('4f3e8f80-7b2a-4a1e-8f80-7b2a4a1e8f80', '홍길동', '010-1234-5678'),
('9d1c7b30-5a4e-4e8b-9d1c-7b305a4e4e8b', '성춘향', '010-9876-5432');

-- 6. 예약 정보 (Appointment)
-- status 값을 Enum 클래스에 정의된 한글 문자열 "확정"으로 변경했습니다.
INSERT INTO appointments (reservation_code, patient_id, doctor_id, treatment_id, start_time, end_time, status, is_first_visit, created_at) VALUES 
('A1B2C3', '4f3e8f80-7b2a-4a1e-8f80-7b2a4a1e8f80', 1, 2, '2026-01-20 10:00:00', '2026-01-20 10:30:00', 'CONFIRMED', 1, NOW());