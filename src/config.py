from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)

    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./sql_app.db"


settings = Settings()
