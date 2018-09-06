import os
import server
import smtplib

from utils import read_template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = os.environ.get('SMTP_PORT')
SMTP_EMAIL = os.environ.get('SMTP_EMAIL')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')

def new_user(email, password):
  message = MIMEMultipart()
  message['From'] = 'noreply@grapevinepd.com'
  message['To'] = email
  message['Subject'] = 'Welcome to GrapevinePD'

  new_user_template = read_template('email_templates/new_user.html')
  message_body = new_user_template.substitute(EMAIL=email, PASSWORD=password)
  message.attach(MIMEText(message_body, 'html'))

  smtp = smtplib.SMTP(host=SMTP_HOST, port=SMTP_PORT)
  smtp.starttls()
  smtp.login(SMTP_EMAIL, SMTP_PASSWORD)
  smtp.send_message(message)