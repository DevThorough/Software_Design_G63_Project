from website.__init__ import db
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, create_engine, Text

##from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import DeclarativeBase, declarative_base, relationship, sessionmaker
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from typing import Optional
from typing import List
import datetime
from sqlalchemy.engine import URL
##import pytest

# declarative base class
class Base(DeclarativeBase):
    pass


class Profile(db.Model):
    __tablename__ = "profile_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    fullName: Mapped[str] = mapped_column(String(50))
    address1: Mapped[str] = mapped_column(String(100))
    address2: Mapped[Optional[str]] = mapped_column(String(100))
    city: Mapped[str] = mapped_column(String(100))
    state: Mapped[str] = mapped_column(String(2))
    zipCode: Mapped[str] = mapped_column(String(9))
    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    user: Mapped["User"] = relationship(back_populates="profile")


class User(db.Model, UserMixin):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32), unique=True)
    password: Mapped[str] = mapped_column(String(64))
    profile: Mapped["Profile"] = relationship(back_populates="user")
    quotes: Mapped[List["FuelQuote"]] = relationship()

""" // Example of one to many sqlalchemy relationship
class Parent(Base):
    __tablename__ = "parent_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[List["Child"]] = relationship()


class Child(Base):
    __tablename__ = "child_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parent_table.id"))

"""

class FuelQuote(db.Model):
    __tablename__ = "quote_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    delivery_address: Mapped[str] = mapped_column(String(200))
    delivery_date: Mapped[str] = mapped_column(String(100))
    gallons: Mapped[float] = mapped_column(Float(2))
    price: Mapped[float] = mapped_column(Float(2))
    total_amount_due: Mapped[float] = mapped_column(Float(2))
    created_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))

class State_Price(db.Model):
    state: Mapped[str] = mapped_column(primary_key=True)
    price: Mapped[float] = mapped_column(Float(2))

##Example
# url = URL.create(
#     drivername="postgresql",
#     username="coderpad",
#     host="/tmp/postgresql/socket",
#     database="coderpad"
#     )

# engine = create_engine(url)
# Session = sessionmaker(bind=engine)