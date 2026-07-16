from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Furniture Intake Agent"
    DEBUG: bool = False

    SUPABASE_URL: str
    SUPABASE_KEY: str

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"

    WHATSAPP_TOKEN: str = ""
    WHATSAPP_PHONE_NUMBER_ID: str = ""
    WHATSAPP_VERIFY_TOKEN: str = "furniture_intake_verify"

    TELEGRAM_BOT_TOKEN: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
