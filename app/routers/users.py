
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils

router = APIRouter(
    prefix = "/users",
    tags = ['Users']
)

'''
Managing user accounts code starts here
'''

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.UserOutput)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    
    email = user.email
    exists = db.query(models.User).filter(models.User.email ==  email).first()
    
    if exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail=f'email address {email} is taken, try a different one')    
    
    # Hashing the password - user.password
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get("/{id}", response_model=schemas.UserOutput)
def get_one_user(id: int, response:Response, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"requested user with id {id} was not found")
    
    return user