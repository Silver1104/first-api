from .. import utils, model, schemas
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import Session, select
from ..database import get_session

routers = APIRouter(prefix="/users", tags=["Users"])

@routers.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_session)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    user_exists = db.exec(select(model.User).filter(model.User.email == user.email)).first()
    if user_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"The user with email {user.email} already exists")
    hashedpassword = utils.Hash.bcrypt(user.password)
    user.password = hashedpassword
    new_user = model.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@routers.get("/{id}", response_model=schemas.UserOut)
async def getOneUser(id: int, response: Response, db: Session = Depends(get_session)):
    statement = select(model.User).filter(model.User.id == id)
    user = db.exec(statement).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The user with id {id} was not found")
    return user