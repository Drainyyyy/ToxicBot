from cogs import db


class Trust:
    def __init__(self, bot):
        self.bot = bot
        self.db = db.Database(bot)
        self.trusted = [].append(self.db.get_list("trust", "uid"))

    def remove(self, uid):
        self.db.remove("trust", "uid", uid)

    def insert(self, uid):
        self.db.insert("trust", "uid", "{}".format(uid))

    def list(self):
        self.db.get_list("trust", "uid")
