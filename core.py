import json
import os
import smtplib
import email


def save_json_to_file(location, filename, data):
    if not os.path.exists(location):
        os.makedirs(location)

    with open(location + filename, 'w') as outfile:
        json.dump(data, outfile)


def notify(content):
    # creating the email
    msg = email.message.EmailMessage()
    msg['From'] = os.environ['SENDER']
    msg['To'] = os.environ['RECIPIENTS']
    msg['Subject'] = 'AWS Notification'
    msg.set_content(content)

    # sending the email
    with smtplib.SMTP('localhost') as smtp:
        smtp.send_message(msg)
