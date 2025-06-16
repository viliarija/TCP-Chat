from email.message import EmailMessage
from random import random
import smtplib
import ssl


def send_code(email_receiver):
    email_sender = "EMAIL-HERE"
    email_password = "PASSWORD-HERE"

    subject = "Discuss Thing verification code"
    body = str(random())[2:8]

    message = EmailMessage()
    message['From'] = email_sender
    message['To'] = email_receiver
    message['Subject'] = subject
    message.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as client:
        client.login(email_sender, email_password)
        client.sendmail(email_sender, email_receiver, message.as_string())

    return body
