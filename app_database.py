import sqlite3
from sqlite3 import Error



class Database:
    def __init__(self,path):
        sql_create_chosenword_table = """CREATE TABLE IF NOT EXISTS chosenword (
                                        id integer PRIMARY KEY,
                                        word text NOT NULL
                                    );"""

        # create a database connection
        self.conn = self.create_connection(path)

        # create tables
        if self.conn is not None:
            # create projects table
            self.create_table(sql_create_chosenword_table)
        else:
            print("Error! cannot create the database connection.")


    def create_connection(self,db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            return self.conn
        except Error as e:
            print(e)

        return self.conn


    def create_table(self, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def add_word(self,word):
        """
        Create a new project into the projects table
        :param item:
        :return: item id
        """
        sql = f''' INSERT INTO chosenword(word)
                VALUES("{word}") '''
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()
        return cur.lastrowid

    def get_word(self,word_id):
      sql = f''' SELECT * FROM chosenword WHERE id={word_id} LIMIT 1'''
      cur = self.conn.cursor()
      cur.execute(sql)
      rows = cur.fetchall()
      word = None
      if len(rows) > 0:
        word = rows[0][1]
      return word