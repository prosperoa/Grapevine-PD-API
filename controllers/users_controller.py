import server
from database import Cursor, Database as db

def get_users(page_size, page_index):
  try:
    with Cursor() as cur:
      cur.execute("SELECT * FROM users WHERE type = 'regular' LIMIT %s OFFSET %s",
        (page_size, page_size * page_index))

      if cur.rowcount:
        return server.ok(data=cur.fetchall())
      else:
        return server.not_found('no users found')
  except:
    return server.error('unable to get users')