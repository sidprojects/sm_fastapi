from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(raw_passwd, hashed_passwd):
    return pwd_context.verify(raw_passwd, hashed_passwd)