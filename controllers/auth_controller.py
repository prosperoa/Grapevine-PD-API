import bcrypt
import server
from database import Cursor, Database as db

def login(email, password):
  try:
    with Cursor() as cur:
      cur.execute('SELECT first_name, last_name, email, password FROM admins WHERE '
        'email = %s', (email,))

      if cur.rowcount:
        user = cur.fetchone()

        if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
          return server.ok(data=user)
        else:
          return server.bad_req('incorrect password')
      else:
        return server.bad_req("account doesn't exist")
  except:
    return server.error('unable to login')
