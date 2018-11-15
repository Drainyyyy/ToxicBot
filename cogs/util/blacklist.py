from cogs import db

blacklisted = []


class Blacklist:
    def __init__(self, bot):
        self.bot = bot

        self.db = db.Database(bot)

    def remove(self, uid):
        self.db.remove("blacklist", "uid", uid)
        blacklisted.remove(uid)

    def insert(self, uid, reason):
        self.db.insert("blacklist", "uid, reason", "{}, '{}'".format(uid, reason))
        blacklisted.append(uid)

    def reason(self, uid):
        reason = self.db.get_content("reason", "blacklist", "uid", uid)
        return reason
