

# from typing import Optional
# from fastapi import Depends, FastAPI, HTTPException, Query
# from sqlalchemy import TIMESTAMP, null
# from sqlmodel import Field, Session, SQLModel, create_engine, select
# from sqlalchemy.sql.expression import text
# from sqlalchemy.sql.sqltypes import TIMESTAMP

# class posts(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     title: str = Field(index=True, nullable=False)
#     content: str = Field(default=None, index=True, nullable=False)
#     published: Optional[bool] = Field(default=True, nullable=False)
#     created_at: Optional[TIMESTAMP(timezone=True)] = Field(nullable=False, default=text("now()"))

import datetime
from typing import Optional
# from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import EmailStr
from sqlalchemy import TIMESTAMP, Column, text
from sqlmodel import Field, Relationship, SQLModel

class Post(SQLModel, table=True):
    __tablename__ = 'posts'
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, nullable=False)
    content: str = Field(index=True, nullable=False)
    published: Optional[bool] = Field(default=True, nullable=False)
    created_at: Optional[datetime.datetime] = Field(
        sa_column=Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    )
    owner_id: Optional[int] = Field(
        default=None, foreign_key = "users.id", nullable=False, index=True, ondelete="CASCADE"
    )
    owner: Optional["User"] = Relationship(back_populates="posts")

class User(SQLModel, table=True):
    __tablename__ = 'users'
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    email: EmailStr = Field(index=True, nullable=False)
    password: str = Field(index=True, nullable=False)
    created_at: Optional[datetime.datetime] = Field(
        sa_column=Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    )
    posts: list["Post"] = Relationship(back_populates="owner")

class Vote(SQLModel, table=True):
    __tablename__ = "votes"
    post_id: Optional[int] = Field(
        default=None, foreign_key="posts.id", primary_key=True, nullable=False, index=True, ondelete="CASCADE"
    )
    user_id: Optional[int] = Field(
        default=None, foreign_key="users.id", primary_key=True, nullable=False, index=True, ondelete="CASCADE"
    )