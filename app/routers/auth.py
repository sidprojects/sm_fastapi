from os import access
from fastapi import APIRouter, HTTPException, Depends, status, Response
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oath2
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags = ['Authentication']
)

@router.post("/login", response_model=schemas.Token)
def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_cred.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid User Credentials")
    
    if not utils.verify(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid User Credentials")
    
    access_token = oath2.create_token(data = {"user_id" : user.id})
    
    return({"access_token" : access_token, "token_type": "bearer"})
    
