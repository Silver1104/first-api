from hmac import new
from typing import List, Optional
from fastapi import APIRouter, FastAPI, Depends, HTTPException, status, Response
from sqlmodel import Session, select, update, func

from app import oauth2
from ..database import get_session
from .. import schemas, model
routers = APIRouter(prefix="/posts", tags=["Posts"])

@routers.get("/", response_model=List[schemas.PostVoteOut])
async def get_posts(db: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts ORDER BY id""")
    # posts = cursor.fetchall()
    # posts = db.query(model.Post).all()  -- depreciated
    # statement = select(model.Post).filter(model.Post.title.contains(search)).limit(limit).offset(skip)

    # posts = db.exec(statement).all()
    post_vote_join = (
        select(model.Post, func.count(model.Vote.post_id).label("votes"))
        .outerjoin(model.Vote, model.Vote.post_id == model.Post.id)
        .filter(model.Post.title.contains(search))
        .group_by(model.Post.id)
        .limit(limit)
        .offset(skip)
    )
    results = db.exec(post_vote_join).all()

    return [{"Post": post, "votes": votes} for post, votes in results]
    # return posts

@routers.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = model.Post(owner_id=current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@routers.get("/{id}", response_model=schemas.PostVoteOut)
async def getOnePost(id: int, response: Response, db: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id= %s """, (str(id),))
    # post = cursor.fetchone()

    post_vote_join = (
        select(model.Post, func.count(model.Vote.post_id).label("votes"))
        .outerjoin(model.Vote, model.Vote.post_id == model.Post.id)
        .filter(model.Post.id == id)
        .group_by(model.Post.id)
    )

    #statement = select(model.Post).filter(model.Post.id == id)
    post = db.exec(post_vote_join).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND

    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    return post

@routers.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletePost(id: int, db: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = select(model.Post).filter(model.Post.id == id)
    post_to_delete = db.exec(post).first()

    if not post_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} does not exist")
    
    if post_to_delete.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    db.delete(post_to_delete)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@routers.put("/{id}", response_model=schemas.PostOut)
async def updatePost(id: int, post: schemas.PostCreate, db: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()
    fetch_stmt = select(model.Post).where(model.Post.id == id)
    existing_post = db.exec(fetch_stmt).first()

    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} does not exist")
    
    if existing_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")


    stmt = (
        update(model.Post)
        .where(model.Post.id == id)
        .values(post.model_dump(exclude_unset=True, exclude={"id"}))
    )

    db.exec(stmt)
    db.commit()
    db.refresh(existing_post)
    # # Step 3: Fetch and return updated post
    # fetch_stmt = select(model.Post).where(model.Post.id == id)
    # updated_post = db.exec(fetch_stmt).first()

    return existing_post