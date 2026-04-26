from pydantic import BaseSettings


class Settings(BaseSettings):
    # 🔹 DATABASE
    DATABASE_URL: str

    # 🔹 SECURITY
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # 🔹 EMAIL CONFIG
    EMAIL_USER: str
    EMAIL_PASSWORD: str
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587

    class Config:
        env_file = ".env"          # used for local development
        case_sensitive = True      # ensures correct variable matching


#  Create settings instance
settings = Settings()
