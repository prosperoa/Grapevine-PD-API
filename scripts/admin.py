import bcrypt
import os
import psycopg2
import re
import sys

RED = '\033[91m'
GREEN = '\033[92m'
BOLD = '\033[1m'
ENDC = '\033[0m'
EMAIL_REGEX = re.compile(r'[^@]+@[^@]+\.[^@]+')

CREATE_ADMIN_DISCLAIMER = (
  'An admin has the ability to, but not limited to:\n'
  '  - create user accounts\n'
  '  - view user account information\n'
  '  - delete user accounts\n'
  '  - update user accounts\n\n'
)

def create():
  print(CREATE_ADMIN_DISCLAIMER)

  first_name = input('First Name (max 20 characters): ').replace(' ', '')
  last_name = input('Last Name: (max 20 characters) ').replace(' ', '')
  email = input('Email Address: ').replace(' ', '')
  password = input('Password (6-50 characters): ').replace(' ', '')

  if not first_name or not last_name or not email or not password:
    error('missing values')

  if len(first_name) > 20 or len(last_name) > 20:
    error('invalid first or last name length')

  if not EMAIL_REGEX.match(email):
    error('invalid email address')

  if len(password) < 6 or len(password) > 50:
    error('invalid password length')

  print('\nConfirm Credentials')
  print('=====================')
  print(
    'First Name: {style}{}{endc}\n'
    'Last Name: {style}{}{endc}\n'
    'Email Address: {style}{}{endc}\n'
    'Password: {style}{}{endc}\n'
    .format(first_name, last_name, email, password, style=GREEN + BOLD, endc=ENDC)
  )

  while True:
    answer = input('(yes/no) ').lower()

    if answer == 'yes' : break
    elif answer == 'no': create()
    else               : continue

  conn = None
  try:
    conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
  except:
    error('unable to connect to database', True)

  cur = conn.cursor()
  cur.execute('SELECT id FROM admins WHERE email = %s', (email,))

  if cur.rowcount:
    error('admin account already exists')

  password_hash = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()).decode('utf8')
  try:
    print('\ncreating account...')
    cur.execute('INSERT INTO admins (first_name, last_name, email, password) values'
      '(%s, %s, %s, %s)', (first_name, last_name, email, password_hash))

    conn.commit()
    cur.close()
    conn.close()
    print('Admin account successfully created.\n')
  except:
    error('unable to create admin account', True)

def error(message, quit=False):
  output = '{}{}{}\n'.format(RED, message, ENDC)

  if quit:
    sys.exit(output)
  else:
    print(output)
    create()
