import bcrypt
import jwt
import os
import server
from database import Cursor, Database as db

def login(email, password):
  try:
    with Cursor() as cur:
      cur.execute('SELECT first_name, last_name, email, password FROM admins WHERE '
        'email = %s', (email,))

      if cur.rowcount:
        user = cur.fetchone()
        data = {}
        data['user'] = user

        if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
          data['auth_token'] = jwt.encode({}, os.environ.get('JWT_SIGNING_KEY'),
            algorithm='HS256').decode('utf-8')
          return server.ok(data=data)
        else:
          return server.bad_req('incorrect password')
      else:
        return server.bad_req("account doesn't exist")
  except:
    return server.error('unable to login')
