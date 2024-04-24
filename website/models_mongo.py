from flask import Flask, jsonify
from flask_login import UserMixin
from pymongo import MongoClient
from typing import Optional, List
import datetime


class Profile:
    def __init__(self, fullName: str, address1: str, address2: Optional[str], city: str, state: str, zipCode: str, user_id: int):
        self.fullName = fullName
        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.state = state
        self.zipCode = zipCode
        self.user_id = user_id

class User(UserMixin):
    def __init__(self, username: str, password: str, profile: Profile, quotes: List["FuelQuote"]):
        self.username = username
        self.password = password
        self.profile = profile
        self.quotes = quotes

class FuelQuote:
    def __init__(self, delivery_address: str, delivery_date: str, gallons: float, price: float, total_amount_due: float, created_date: datetime.datetime, user_id: int):
        self.delivery_address = delivery_address
        self.delivery_date = delivery_date
        self.gallons = gallons
        self.price = price
        self.total_amount_due = total_amount_due
        self.created_date = created_date
        self.user_id = user_id
