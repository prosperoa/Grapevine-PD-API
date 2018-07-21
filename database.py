from psycopg2 import pool

class Database:
  _connection_pool = None

  @classmethod
  def init(cls, minconn, maxconn, db_url):
    cls._connection_pool = pool.SimpleConnectionPool(minconn, maxconn, db_url)

  @classmethod
  def get_connection(cls):
    return cls._connection_pool.getconn()

  @classmethod
  def return_connection(cls, connection):
    cls._connection_pool.putconn(connection)

  @classmethod
  def close_all_connections(cls):
    cls._connection_pool.closeall()

class Cursor():
  def __init__(self):
    self.conn = None
    self.cursor = None

  def __enter__(self):
    self.conn = Database.get_connection()
    self.cursor = self.conn.cursor()
    return self.cursor

  def __exit__(self, exc_type, exc_val, exc_tb):
    if exc_val:
      self.conn.rollback()
    else:
      self.cursor.close()
      self.conn.commit()

    Database.return_connection(self.conn)
