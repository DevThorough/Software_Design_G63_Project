from . import db
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey

##from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import Optional

# declarative base class
class Base(DeclarativeBase):
    pass

"""
# an example mapping using the base
class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    fullname: Mapped[str] = mapped_column(String(30))
    nickname: Mapped[Optional[str]]

class Parent(Base):
    __tablename__ = "parent_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    child: Mapped["Child"] = relationship(back_populates="parent")


class Child(Base):
    __tablename__ = "child_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parent_table.id"))
    parent: Mapped["Parent"] = relationship(back_populates="child")
"""


class Profile(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    fullName: Mapped[str] = mapped_column(String(50))
    address1: Mapped[str] = mapped_column(String(100))
    address2: Mapped[Optional[str]] = mapped_column(String(100))
    city: Mapped[str] = mapped_column(String(100))
    state: Mapped[str] = mapped_column(String(2))
    zipcode: Mapped[str] = mapped_column(String(9))
    user_id = Column(Integer, ForeignKey('user.id'))
    user: Mapped["User"] = relationship(back_populates="profile")


class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32), unique=True)
    password: Mapped[str] = mapped_column(String(64))
    profile: Mapped["Profile"] = relationship(back_populates="user")