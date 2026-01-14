# 🏥 피부과 예약 관리 시스템 백엔드 API  
메디솔브 AI 백엔드 과제 레포지토리입니다.

---

## 📖 과제 개요

본 과제는 **메디솔브 AI 백엔드 개발자 채용을 위한 기술 과제**입니다.  

피부과 예약 관리 시스템의 백엔드 API를 설계하고 구현하는 과제로,  
마이크로서비스 아키텍처를 간소화한 형태로 구성했습니다.

- Gateway API
- Patient API
- Admin API

---

## 📁 제출 항목 구성

### 1. 소스 코드
- FastAPI 기반 백엔드 소스 코드
- Gateway / Patient / Admin API 분리
- Router / Service / Repository 계층 분리 구조로 구현

---

### 2. 데이터베이스 마이그레이션 파일
- Alembic을 사용한 데이터베이스 스키마 관리
```
    docker-compose run --rm gateway uv run alembic revision --autogenerate -m "create clinic tables"
    docker-compose run --rm gateway uv run alembic upgrade head
```
---

### 3. 테스트 데이터셋 SQL 파일
- 피부과 예약 관리 시스템 더미 데이터 삽입용 SQL 파일
- 의사, 진료 항목, 환자, 예약 관련 초기 데이터 포함

---

### 4. Docker 관련 파일
- docker-compose.yml
- Dockerfile (필요 서비스에 한해 구성)

---

## 🧾 프로젝트 설명

- 피부과 예약 관리 도메인을 기반으로 한 REST API 백엔드 프로젝트
- 진료과 / 의사 / 환자 / 예약 / 시술 정보 관리 기능 구현
- 운영 환경과 테스트 환경을 분리하여 안정적인 개발 구조 구성
- 테스트 환경에서는 SQLite in-memory DB를 사용하여 테스트 독립성 확보

---

## ▶️ 실행 방법

### 1. 환경 설정

#### 필수 환경
- Docker Desktop (v20.10 이상)
- Docker Compose (v2 이상)
- Python 3.11
- MySQL

---

### 2. 환경 변수 설정

#### `.env` (개발 / 운영 환경)

    ENV=development
    DEBUG=true

    DB_HOST=db
    DB_PORT=3306
    DB_USER=yujeong
    DB_PASSWORD=zUQEGMFiMpTg4FyrXJaq
    DB_NAME=medisolve

#### `.env.test` (테스트 환경)

    ENV=test
    DEBUG=false

    DATABASE_URL=sqlite+pysqlite:///:memory:

---

### 3. Docker Compose 실행

    docker-compose up --build -d

---

### 4. 테스트 실행

    docker-compose run --rm gateway uv run pytest

---

### 5. API 문서 접근 (Swagger)

- Gateway API: http://localhost:8000/docs
- Patient API: http://localhost:8001/docs
- Admin API: http://localhost:8002/docs

---

## 🤖 AI 활용 방식

- 사용한 AI: ChatGPT
- 다음과 같은 목적으로 활용

  - 파일 및 디렉토리 구조 설계 검증
  - Docker 연결 및 컨테이너 실행 오류 해결
  - Router ↔ Service 간 인수 전달 방식 검증
  - Service / Repository 계층 분리 구조 검토
  - uv 실행 환경에 따른 명령어 변경 검증
  - 모델 설계 이후 더미 데이터 작성
  - 서비스 로직 오류 발생 시 원인 분석 및 개선
  - README.md 작성

> AI는 설계 검증과 문제 해결을 위한 보조 도구로 활용했습니다.

---

