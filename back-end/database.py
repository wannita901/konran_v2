from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime
import csv
from datetime import datetime, timedelta
import random

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

db.init_app(app)

class Item(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    expiry_date: Mapped[DateTime] = mapped_column(DateTime)
    
class ExpiryDate(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    days_til_expiry: Mapped[int] = mapped_column(Integer)

def add_items_from_expiry(filepath="expiry.csv"):
    with open(filepath, 'r', encoding='utf-8-sig') as file:
        csv_reader = csv.reader(file)

        for row in csv_reader:
            name, days_til_expiry = row
            expiry_date = ExpiryDate(name=name, days_til_expiry=days_til_expiry)
            db.session.add(expiry_date)
        
    db.session.commit()

def add_fake_database():
    name_list = ['apple', 'banana', 'orange']
    date_list = [datetime.now(), datetime.now() + timedelta(days=2), datetime.now() + timedelta(days=5)]

    for i in range(len(name_list)):

        item = Item(
            name=name_list[i],
            expiry_date = date_list[i]
        )
        db.session.add(item)
    db.session.commit()




with app.app_context():
    db.create_all()

    if not ExpiryDate.query.first():
        add_items_from_expiry()
        add_fake_database()


