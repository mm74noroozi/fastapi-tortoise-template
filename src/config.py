from starlette.config import Config as Base
from decouple import config as read


class Config(Base):
    DEBUG: bool = read("DEBUG", cast=bool, default=False)
    SECRET_KEY: str = read("SECRET_KEY")
    ALGORITHM: str = read("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: str = read("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)
    DB_URL: str = read("DB_URL")
