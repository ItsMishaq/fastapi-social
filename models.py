import builtins
from datetime import timezone
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.functions import now
from sqlalchemy.sql.schema import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.sql.sqltypes import TIMESTAMP, Boolean, Integer, String
# from app.database import Base
from database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable= False)
    content = Column(String, nullable= False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    published = Column(Boolean, default= True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable= False, unique=True)
    password = Column(String, nullable= False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts].id", ondelete="CASCADE"), primary_key=True)

