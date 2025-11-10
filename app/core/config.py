from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "FastAPI Jinja App"
    admin_email: str = "admin@example.com"
    items_per_page: int = 10
    session_secret_key: str = "super-secret-session-key"
    session_cookie_name: str = "credit_session"
    session_cookie_identifier: str = "credit-session"

    class Config:
        env_file = ".env"


settings = Settings()
