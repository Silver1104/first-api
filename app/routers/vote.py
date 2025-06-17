from webbrowser import get
from fastapi import APIRouter, FastAPI, Depends, HTTPException, status, Response
from sqlmodel import Session, select
from .. import schemas, model, oauth2
from ..database import get_session

routers = APIRouter(prefix="/vote", tags=["Votes"])

@routers.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(vote: schemas.VoteCreate, db: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user)):
    post = select(model.Post).filter(model.Post.id == vote.post_id)
    post_to_delete = db.exec(post).first()
    if not post_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {vote.post_id} does not exist")
    vote_query = select(model.Vote).filter(
            model.Vote.post_id == vote.post_id,
            model.Vote.user_id == current_user.id
        )
    found_vote = db.exec(vote_query).first()
    if vote.vote_dir == 1:
        # vote_query = select(model.Vote).filter(
        #     model.Vote.post_id == vote.post_id,
        #     model.Vote.user_id == current_user.id
        # )
        # found_vote = db.exec(vote_query).first()
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User has already voted on this post")
        new_vote = model.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added successfully"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        db.delete(found_vote)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
