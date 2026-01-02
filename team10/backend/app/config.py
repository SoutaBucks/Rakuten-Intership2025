
# backend/app/config.py
from __future__ import annotations
from typing import List, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # ========= DB =========
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "1234"
    DB_NAME: str = "safetravel"
    # 互換用：明示指定なければ上の値から組み立てる
    DATABASE_URL: Optional[str] = None

    # ========= API =========
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "safetravel API"

    # ========= CORS =========
    # .env で "http://localhost:5173,http://127.0.0.1:5173" のようにカンマ区切り可
    BACKEND_CORS_ORIGINS: List[str] = Field(default_factory=lambda: ["*"])

    # ========= Logging =========
    LOG_LEVEL: str = "INFO"

    # ========= Mail (追加) =========
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None         # 送信元 Gmail アドレス
    SMTP_PASS: Optional[str] = None         # Gmail アプリパスワード（16桁）
    SENDER_NAME: str = "SafeTravel"
    REPLY_TO: Optional[str] = None          # 返信先（任意）

    # ========= Front URL (追加) =========
    PUBLIC_BASE_URL: str = "http://localhost:5173"

    # pydantic-settings 設定
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",   # .env に余計なキーがあっても無視して起動
    )

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors(cls, v):
        # カンマ区切り → リスト に変換（既にリストならそのまま）
        if isinstance(v, str):
            parts = [s.strip() for s in v.split(",") if s.strip()]
            return parts if parts else ["*"]
        return v

    @field_validator("DATABASE_URL", mode="after")
    def build_db_url(cls, v, info):
        # DATABASE_URL 未指定 → 単項目から生成
        if v and isinstance(v, str) and v.strip():
            return v
        data = info.data
        user = data.get("DB_USER")
        pwd = data.get("DB_PASSWORD")
        host = data.get("DB_HOST")
        port = data.get("DB_PORT")
        name = data.get("DB_NAME")
        return f"postgresql://{user}:{pwd}@{host}:{port}/{name}"


settings = Settings()