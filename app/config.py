from pydantic import BaseSettings

class Settings(BaseSettings):
    db_name: str
    db_username: str
    db_passwd: str
    db_port: str
    db_hostname: str
    
    secret_key: str
    algorithm: str
    access_token_expire_min: int
    
    class Config:
        env_file = ".env"
        
settings = Settings()