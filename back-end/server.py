from flask import Flask, request
from database import *
from datetime import datetime
import random
import base64
import numpy as np
import cv2

date_list = [datetime(2024, 3, 2), datetime(2024, 3, 1), datetime(2024, 3, 3)]
name_list = ["apple", "banana", "potato", "water"]

### FUNCTIONS REQUIRED ###
def decode_image(encoding):
    '''
    Input: An image encoded as Base64 String.
    Output: An OpenCV Image object.
    '''
    image = base64.b64decode(encoding)

    image_np = np.frombuffer(image, dtype=np.uint8)

    image_cv2 = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    return image_cv2



##########################



@app.route('/get_user_items')
def get_user_items():
    items = db.session.execute(db.select(Item)).scalars()
    
    items_list = []

    for item in items:
        items_list.append({"name": item.name, "expiry_date": item.expiry_date.strftime("%d/%m/%Y")})

    return items_list

@app.route("/detect_image")
def detect_image():
    response = request.json()

    image = decode_image(response['image'])










######################
@app.route('/')
def hello_world():
    item = Item(
        name=random.choice(name_list),
        expiry_date = random.choice(date_list)
    )
    db.session.add(item)
    db.session.commit()
    return item.name + " added!"

@app.route('/check')
def check_all():
    items = db.session.execute(db.select(Item)).scalars()
    string = ""
    for item in items:
        string += item.name
    return string

@app.route("/date")
def dates():
    eds = db.session.execute(db.select(ExpiryDate)).scalars()
    string = ""
    for ed in eds:
        string += f"{ed.name} : {ed.days_til_expiry}"
    return string


if __name__ == '__main__':
    app.run(debug=True)
