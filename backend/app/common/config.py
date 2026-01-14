from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import os

class Settings(BaseSettings):
    # 기본 환경
    APP_NAME: str = "메디솔브에이아이 주식회사 과제테스트"
    ENV: str = Field("development", alias="ENV") # 기본값 지정
    DEBUG: bool = Field(False, alias="DEBUG")

    # DB (공통)
    DB_HOST: str = Field("localhost", alias="DB_HOST")
    DB_PORT: int = Field(3306, alias="DB_PORT")
    DB_USER: str = Field("mysql", alias="DB_USER")
    DB_PASSWORD: str = Field("0000", alias="DB_PASSWORD")
    DB_NAME: str = Field("medisolve", alias="DB_NAME")
    DATABASE_URL: str | None = Field(None, alias="DATABASE_URL")

    # .env 설정
    model_config = SettingsConfigDict(
        env_file=".env.test" if os.getenv("ENV") == "test" else ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def database_url(self) -> str:
        """
        test 환경 : DATABASE_URL 사용 (sqlite)
        dev 환경 : mysql 설정 조합
        """
        if self.DATABASE_URL:
            return self.DATABASE_URL
        
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
    
settings = Settings()
