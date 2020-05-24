import sqlite3


class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_single(self, rownum):
        with self.connection:
            return self.cursor.execute('SELECT * FROM questions WHERE id = ?', (rownum,)).fetchall()[0]

    def count_rows(self):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM questions').fetchall()
            return len(result)

    def close(self):
        self.connection.close()
