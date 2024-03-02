import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import json

with open("email-authentication.json", 'r') as file:
    data = json.load(file)

# Access email and password from auth file.
sender_email = data.get('email')
sender_password = data.get('password')


def send_email(recipient_email="bteo0002@student.monash.edu", subject= "Test Subject", message="This is an automated message.\nSent from Python."):
    smtpserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtpserver.ehlo()
    smtpserver.login(sender_email, sender_password)

    sent_from = sender_email
    sent_to = recipient_email

    message = "Subject: " + subject + "\n" + message

    smtpserver.sendmail(sent_from, sent_to, message)
    # Close the connection
    smtpserver.close()

send_email(recipient_email="taylorramnarong@gmail.com")