# 베이스 이미지
FROM python:3.11

# 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 설치 (mysql, postgres 대비)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# uv 설치
RUN pip install --no-cache-dir uv

# 의존성 파일 복사
COPY pyproject.toml uv.lock ./

# 의존성 설치 (prod 기준)
RUN uv sync --frozen

# 애플리케이션 코드 복사
COPY app ./app

# 기본 실행 포트 (compose에서 override)
EXPOSE 8000

# 기본 실행 명령 (compose에서 override)
CMD ["uv", "run", "uvicorn", "app.gateway.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Alembic 설정 복사
COPY alembic.ini ./alembic.ini
COPY alembic ./alembic