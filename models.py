"""
создайте алхимичный engine
добавьте declarative base (свяжите с engine)
создайте объект Session
добавьте модели User и Post, объявите поля:
для модели User обязательными являются name, username, email
для модели Post обязательными являются user_id, title, body
создайте связи relationship между моделями: User.posts и Post.user
"""

import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey


PG_CONN_URI = os.environ.get("SQLALCHEMY_PG_CONN_URI") or "postgresql+asyncpg://postgres:password@localhost/postgres"


engine = create_async_engine(PG_CONN_URI, echo=True)


Base = declarative_base()


Session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)

    
    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(name={self.name}, username={self.username}, email={self.email})>"


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)

    
    user = relationship("User", back_populates="posts")

    def __repr__(self):
        return f"<Post(title={self.title}, body={self.body}, user_id={self.user_id})>"

 
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

