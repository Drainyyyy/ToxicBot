
from utils.db import db

blacklisted = []


class Blacklist:
    def __init__(self, bot):
        self.bot = bot

    async def insert(self, uid: int, reason, executor_id: int):
            await db.Database.insert(db.Database(self.bot), table="blacklist", rows=["uid", "reason", "executor_id"], values=[uid, reason, executor_id])
            blacklisted.append(uid)
            print(f"[BLACKLIST] Blacklisted {self.bot.get_user(uid)} (ID: {uid})")

    async def remove(self, uid: int):
        blacklisted.remove(uid)
        await db.Database.remove(db.Database(self.bot), "blacklist", "uid", uid)

    async def load_blacklist(self):
        blacklists = await db.Database.get_list(db.Database(self.bot), "uid", "blacklist")
        for blacklist in blacklists:
            blacklisted.append(blacklist)
        print(f"[BLACKLIST] {blacklisted}")

    async def get(self, uid: int, row):
        return await db.Database.get_single(db.Database(self.bot), row, "blacklist", "uid", uid)

    async def get_all(self, uid: int):
        record = await db.Database.get_all(db.Database(self.bot), "blacklist", "uid", uid)
        return record[0]

    @staticmethod
    def unload_blacklist():
        blacklisted.clear()
