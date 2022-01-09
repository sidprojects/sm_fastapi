from jose import jwt, JWTError
from datetime import datetime, timedelta
from .config import settings
from sqlalchemy.orm.session import Session
from . import schemas, database, models
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MIN = settings.access_token_expire_min

def create_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MIN)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token:str, credentials_exception):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        
        id:str = payload.get("user_id")
        
        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(id = id)
           
    except JWTError:
        raise credentials_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), 
                     db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, 
                                          detail = f"Could not validate credentials",
                                          headers = {"WWW-Authenticate": "Bearer"})
    
    token_data = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    
    return user