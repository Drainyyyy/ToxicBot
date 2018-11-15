import psycopg2

from util import important


class Database:
    def __init__(self, bot):
        self.bot = bot
        try:
            self.connection = psycopg2.connect("dbname={} user={} host={} password={}"
                                               .format(important.db_name, important.db_user, important.db_host, important.db_pw))
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            print("[DB] Connected.")
        except Exception as error:
            print("[DB] Connection failed.\nError: \n[{}]".format(error))

    def get_list(self, table, row):
        self.cursor.execute("FROM {} SELECT {}".format(table, row))

    def get_content(self, row1, table, row2, row2content):
        self.cursor.execute("SELECT {} FROM {} WHERE {} = {}".format(row1, table, row2, row2content))
        out = self.cursor.fetchall()
        return out

    def insert(self, table, rows, content):
        self.cursor.execute("INSERT INTO {} ({}) VALUES ({})".format(table, rows, content))

    def remove(self, table, row, content):
        self.cursor.execute("DELETE FROM {} WHERE {} = {}".format(table, row, content))


def setup(bot):
    bot.add_cog(Database(bot))
