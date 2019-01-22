from utils.db import db

profiles = []


class Profile:
    def __init__(self, bot):
        self.bot = bot

    async def insert(self, uid: int, description):
        await db.Database.insert(db.Database(self.bot), "profile", ["uid", "description"], [uid, description])

    async def get(self, uid: int):
        return await db.Database.get_single(db.Database(self.bot), "description", "profile", "uid", uid)

    async def delete(self, uid: int):
        await db.Database.remove(db.Database(self.bot), "profile", "uid", uid)

    async def load_profiles(self):
        profile_list = await db.Database.get_list(db.Database(self.bot), "uid", "profile")
        for profile_id in profile_list:
            profiles.append(profile_id)

    @staticmethod
    def unload_profile():
        profiles.clear()
