from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/users"
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict()) # ** fa l'unpack del dictionary creato dal metodo .dict() e crea una situazione come la riga sopra
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # per recuperare il campo id

    return new_user

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if user == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} doesn't not exist")

    return user