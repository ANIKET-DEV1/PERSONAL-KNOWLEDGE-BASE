from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import SecretStr
from functools import lru_cache

class AppConfig(BaseSettings):
    app_name:str
    app_env:str
    database_url:SecretStr
    secret_key:SecretStr
    algorithms:str
    ACCESS_TOKEN_EXPIRE_MINUTE:int
    model_config=SettingsConfigDict(env_file=".env", extra="ignore")

    
@lru_cache
def getAppconfig():
    return AppConfig()
