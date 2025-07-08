
from fastapi import FastAPI, Depends
from sqlmodel import Session
from fastapi.middleware.cors import CORSMiddleware
from .routers import user, post, auth, vote
# from .database import get_session
# from typing import Annotated

# SessionDep = Annotated[Session, Depends(get_session)]

# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
    #rating: Optional[int] = None

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     create_db_and_tables()  # This will run at startup
#     yield

# app = FastAPI(lifespan=lifespan)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_credentials= True,
    allow_methods= ["*"],
    allow_headers= ["*"],
)

# my_posts = [{'title':'this is an f1 app', 'content':'f1 cars go brrr', 'id':1}, {'title':'this is a food app', 'content':'food is yummy', 'id':2}]

# while True:
#     try:
#         conn = psycopg.connect(host='localhost', dbname='fastapi', user='postgres', password='Only1life')
#         cursor = conn.cursor(row_factory=dict_row)
#         print("Database connected successfully")
#         break
#     except Exception as error:
#         print("Database connection failed")
#         print("Error: ", error)
#         time.sleep(5)

# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p

# def find_post_index(id):
#     for i,p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

@app.get("/")
async def root():
    return {"message": "Helloworld!!!!! THIS WORKKKSSS in ubuntuuu"}

print("🔥 This line should show if reload works.")

app.include_router(
    user.routers)
app.include_router(
    post.routers)
app.include_router(
    auth.routers)
app.include_router(
    vote.routers)
# @app.get("/posts", response_model=List[schemas.PostOut])
# async def get_posts(db: Session = Depends(get_session)):
#     # cursor.execute("""SELECT * FROM posts ORDER BY id""")
#     # posts = cursor.fetchall()
#     # posts = db.query(model.Post).all()  -- depreciated
#     statement = select(model.Post)
#     posts = db.exec(statement).all()
#     return posts

# @app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
# async def create_post(post: schemas.PostCreate, db: Session = Depends(get_session)):
#     # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
#     # new_post = cursor.fetchone()
#     # conn.commit()

#     new_post = model.Post(**post.model_dump())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return new_post

# @app.get("/posts/{id}", response_model=schemas.PostOut)
# async def getOnePost(id: int, response: Response, db: Session = Depends(get_session)):
#     # cursor.execute("""SELECT * FROM posts WHERE id= %s """, (str(id),))
#     # post = cursor.fetchone()

#     statement = select(model.Post).filter(model.Post.id == id)
#     post = db.exec(statement).first()

#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} was not found")
#         # response.status_code = status.HTTP_404_NOT_FOUND
#     return post

# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# async def deletePost(id: int, db: Session = Depends(get_session)):
#     # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
#     # deleted_post = cursor.fetchone()
#     # conn.commit()

#     post = select(model.Post).filter(model.Post.id == id)
#     deleted_post = db.exec(post).first()

#     if not deleted_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} does not exist")

#     db.delete(deleted_post)
#     db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# @app.put("/posts/{id}", response_model=schemas.PostOut)
# async def updatePost(id: int, post: schemas.PostCreate, db: Session = Depends(get_session)):
#     # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id),))
#     # updated_post = cursor.fetchone()
#     # conn.commit()

#     stmt = (
#         update(model.Post)
#         .where(model.Post.id == id)
#         .values(post.model_dump(exclude_unset=True, exclude={"id"}))
#     )

#     result = db.exec(stmt)
#     db.commit()

#     # Step 2: Check if any row was updated
#     if result.rowcount == 0:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"The post with id {id} does not exist"
#         )

#     # Step 3: Fetch and return updated post
#     fetch_stmt = select(model.Post).where(model.Post.id == id)
#     updated_post = db.exec(fetch_stmt).first()

#     return updated_post

# import psycopg
# print(psycopg.__version__)

# @app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
# async def create_post(user: schemas.UserCreate, db: Session = Depends(get_session)):
#     # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
#     # new_post = cursor.fetchone()
#     # conn.commit()
#     hashedpassword = utils.Hash.bcrypt(user.password)
#     user.password = hashedpassword
#     new_user = model.User(**user.model_dump())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

# @app.get("/users/{id}", response_model=schemas.UserOut)
# async def getOneUser(id: int, response: Response, db: Session = Depends(get_session)):
#     statement = select(model.User).filter(model.User.id == id)
#     user = db.exec(statement).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The user with id {id} was not found")
#     return user