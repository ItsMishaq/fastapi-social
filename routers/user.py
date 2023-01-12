from fastapi import FastAPI, Response, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, utils



router = APIRouter(
    tags=['Users']
)



#FOR CREATING NEW USERS
@router.post("/create", status_code=201, response_model=schemas.UserOut)
def create_users(user: schemas.UserCreate, db: Session= Depends(get_db)): #schemas is used to ensure that users does provide both of those
     
     hashed_password= utils.hash(user.password)
     user.password=hashed_password

     new_user = models.User(**user.dict())
     db.add(new_user)
     db.commit()
     db.refresh(new_user)

     return new_user

#FOR GETTING USER DEtails.

@router.get("/user/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session= Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")
    
    return user

