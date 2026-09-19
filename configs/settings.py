from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # Application name used throughout the backend configuration.
    app_name: str = "Python Backend Training"

    # Database
    database_url: str

    # Enables or disables FastAPI debug mode.
    # Defaults to False so debug mode is not accidentally enabled.
    debug: bool = False

    admin_email: str
    admin_password: str

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30
    
    # Configuration for how Pydantic Settings loads environment variables.
    model_config = SettingsConfigDict(
        # Load values from the .env file in the project root.
        env_file=".env",
        # Ignore environment variables that are not defined
        # as fields in this Settings class.
        extra="ignore",
        env_file_encoding="utf-8",
    )


# Create one shared Settings instance for the entire application.
# Other modules should import this instance instead of creating
# their own Settings object.
settings = Settings()
