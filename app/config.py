from pydantic_settings import BaseSettings

class Settings(BaseSettings) :
    MONGO_URL : str
    REDIS_URL : str
    BASE_URL : str
    RATE_LIMIT : int = 20

    class Config :
        env_file = ".env"

settings = Settings()