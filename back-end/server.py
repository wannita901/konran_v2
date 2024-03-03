from flask import Flask, request
from database import *
from datetime import datetime, timedelta
import base64
import numpy as np
import cv2
from apscheduler.schedulers.background import BackgroundScheduler
from send_email import send_email
import cv_function

date_list = [datetime(2024, 3, 2), datetime(2024, 3, 1), datetime(2024, 3, 3)]
name_list = ["apple", "banana"]

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

def detect_objects(image):

    # Pass image to model, get the output as a list of items.
    output = cv_function.wimp_it(image)

    return output
def process_found_items(found_items):
    '''
    Input: found_items in the format ["item1_name", "item2_name",...]
    Output: None

    This function will looks at the found items and compare it against what's in the database.
    It will then remove items in the database that aren't detected and add new items.
    '''
    existing_items = Item.query.all()
    existing_items = [item.name for item in existing_items]

    itemnames_to_delete = []
    itemnames_to_add = []
    expiry_dates_dct = {}

    # For each existing item, we delete items that aren't found this time.
    # Bad time complexity, but it's a hackathon. :)
    for item_name in existing_items:
        if item_name not in found_items:
            itemnames_to_delete.append(item_name)
    
    # For each item found, we add the items that weren't previously in the database INTO the database.
    for item_name in found_items:
        if item_name not in existing_items:
            itemnames_to_add.append(item_name)


    ## DEBUG####################
    print("DEBUG!!! ITEMS TO ADD: ")
    for item in itemnames_to_add:
        print(item)

    print("DEBUG!!! ITEMS TO REMOVE: ")
    for item in itemnames_to_delete:
        print(item)
    #################################

    ## We need to determine the expiry dates for each of them.
    expiry_dates = ExpiryDate.query.filter(ExpiryDate.name.in_(itemnames_to_add)).all()
    for row in expiry_dates:
        expiry_dates_dct[row.name] = row.days_til_expiry

    #### REMOVE ITEMS FROM DATABASE
    # Now, we have a list of item objects we want to remove from the database.
    items_to_delete = Item.query.filter(Item.name.in_(itemnames_to_delete)).all()

    for item in items_to_delete:
        db.session.delete(item)

    #### ADD ITEMS INTO THE DATABASE
    # After this, we'll have a list of item objects we want to add into the database.
    items_to_add = []
    for item_name in itemnames_to_add:
        current_date = datetime.now()

        name = item_name

        # Calculate the expiry date by adding the shelf life to current date.

        if name in expiry_dates_dct:
            expiry_date = current_date + timedelta(days=expiry_dates_dct[name])
        else:
            expiry_date = current_date + timedelta(days=7)

        items_to_add.append(Item(name=name, expiry_date=expiry_date))

    for item in items_to_add:
        db.session.add(item)

    db.session.commit()
    #########################

def alert_user():
    with app.app_context():
        items = db.session.execute(db.select(Item)).scalars()

        items_to_alert = []
        for item in items:
            difference = item.expiry_date.date() - datetime.now().date()
            if difference.days <= 3:
                items_to_alert.append([item, difference.days])

        items_to_alert.sort(key=lambda item:item[1])

        subject = "W.I.M.P Alert: Your groceries are about to expire!"
        message = "The following groceries in your pantry are about to expire.\n\n"
        item_count = 1
        if len(items_to_alert) > 0:
            for item, days_til_expiry in items_to_alert:
                expiry_date = item.expiry_date.strftime("%d/%m/%y")
                message += f"{item_count}. {item.name}: expires {expiry_date} [{days_til_expiry} day(s)]\n"
                item_count += 1
            
            message += "\n Make sure you use them before they go to waste!\n"
            message += "\n - Konran W.I.M.P Team"
            send_email(subject=subject, message=message)
            print("Sent email!")


### ROUTES ###
@app.route('/get_user_items')
def get_user_items():
    '''
    Returns a list of objects, where each object has keys "name" and "expiry_date".
        name: str
        expiry_date: str ("dd/mm/yyyy")
    '''
    items = db.session.execute(db.select(Item)).scalars()
    
    items_list = []

    for item in items:
        items_list.append({"id": item.id, "name": item.name, "expiry_date": item.expiry_date.strftime("%d/%m/%Y")})

    return items_list

@app.route("/detect_image", methods=["POST"])
def detect_image():
    response = request.json

    image = decode_image(response['image'])

    found_items = detect_objects(image)

    process_found_items(found_items)
    return ""


@app.route("/test")
def test():
    found_items = ["cake", "apple", "banana"]
    process_found_items(found_items)
    return ""

### SCHEDULER ###
scheduler = BackgroundScheduler()
scheduler.add_job(alert_user, 'cron', hour=0)
scheduler.start()




######################
@app.route('/check')
def check_all():
    items = db.session.execute(db.select(Item)).scalars()
    string = ""
    for item in items:
        string += item.name + item.expiry_date.strftime("%d/%m/%y") + "\n"
    return string

@app.route("/date")
def dates():
    eds = db.session.execute(db.select(ExpiryDate)).scalars()
    string = ""
    for ed in eds:
        string += f"{ed.name} : {ed.days_til_expiry}"
    return string


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
