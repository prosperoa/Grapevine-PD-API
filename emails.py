import os
import server
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import open
from string import Template

SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = os.environ.get('SMTP_PORT')
SMTP_EMAIL = os.environ.get('SMTP_EMAIL')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
print(SMTP_HOST, SMTP_PORT, SMTP_EMAIL, SMTP_PASSWORD)

def new_user(email, password):
  message = MIMEMultipart()
  message['From'] = 'noreply@grapevinepd.com'
  message['To'] = email
  message['Subject'] = 'Welcome to GrapevinePD'

  f = open('email_templates/new_user.html', encoding='utf-8')
  new_user_template = Template(f.read())

  values = {
    'EMAIL': email,
    'PASSWORD': password
  }
  message_body = new_user_template.substitute(values)
  message.attach(MIMEText(message_body, 'html'))

  smtp = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
  smtp.ehlo()
  smtp.starttls()
  smtp.ehlo()
  smtp.login(SMTP_EMAIL, SMTP_PASSWORD)

  smtp.sendmail('noreplay@grapevinepd.csub@gmail.com', email, message.as_string())
  smtp.quit()
