from utils.db import db

'''The permission level function is not used yet.'''

trusted = {}


class Trust:
    def __init__(self, bot):
        self.bot = bot

    async def load_trusts(self):
        try:
            trusts = await db.Database.get_dict(db.Database(self.bot), "trust")
            for user in trusts:
                if trusts[user] > 5:
                    trusts[user] = 5
                trusted[user] = trusts[user]
            print(f"[TRUST] {trusted}")
        except Exception as error:
            print(error)

    async def trust(self, uid: int, perm_level: int = 1):
        if perm_level > 5:
            perm_level = 5
        trusted[uid] = perm_level
        await db.Database.insert(db.Database(self.bot), "trust", ["uid", "perm_level"], [uid, perm_level])

    async def untrust(self, uid: int):
        trusted.pop(uid)
        await db.Database.remove(db.Database(self.bot), "trust", "uid", uid)

    @staticmethod
    def unload_trusts():
        trusted.clear()

