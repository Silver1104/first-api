from webbrowser import get
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app import model, schemas, utils, oauth2
from app.database import get_session


routers = APIRouter(tags=["Authentication"])

@routers.post("/login",  response_model=schemas.Token)
async def login(user_creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    statement = select(model.User).filter(model.User.email == user_creds.username)
    user_db = db.exec(statement).first()
    if(not user_db or not utils.Hash.verify(user_db.password, user_creds.password)):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    
    access_token = oauth2.create_access_token(data={"user_id": user_db.id})
    response = {"access_token": access_token, "token_type": "bearer"}

    return response