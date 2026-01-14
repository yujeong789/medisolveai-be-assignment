from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.common.config import settings

class Base(DeclarativeBase): 
    pass

DATABASE_URL = settings.database_url

engine_kwargs = {}

# test 환경 (sqlite)
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

# debug=true면 sql 로그 출력
engine = create_engine(
    DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True, # 연결 상태 확인
    pool_recycle=300, # 5분마다 연결 재생성
    **engine_kwargs,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# fast api 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()