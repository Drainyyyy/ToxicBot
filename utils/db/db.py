import asyncpg
from discord.ext import commands
from utils.db import trust, blacklist, profile


class Database:
    def __init__(self, bot):
        self.bot = bot
        self.conn = self.bot.db

    async def insert(self, table, rows: list, values: list):
        try:
            prepared_value = []
            for value in values:
                if type(value) is str:
                    prepared_value.append(f"'{value}'")
                elif type(value) is int:
                    prepared_value.append(str(value))
                else:
                    prepared_value.append(value)
            query = f"INSERT INTO {table} ({', '.join(str(row) for row in rows)}) VALUES ({', '.join(prepared_value)})"
            await self.conn.execute(query)
        except asyncpg.PostgresError as error:
            raise commands.CommandInvokeError(error)

    async def remove(self, table, row, compare):
        query = f"DELETE FROM {table} WHERE {row} = {str(compare)}"
        await self.conn.execute(query)

    async def get_single(self, row, table, attribute, compare):
        try:
            query = f"SELECT {row} FROM {table} WHERE {attribute} = {compare}"
            out = await self.conn.fetchrow(query)
            return dict(out)[row]
        except AttributeError:
            raise commands.UserInputError(f"No results found for {row} in {table}")

    async def get_dict(self, table):
        query = f"SELECT * from {table}"
        out = await self.conn.fetch(query)
        return dict(out)

    async def get_list(self, row, table):
        query = f"SELECT {row} FROM {table}"
        out = await self.conn.fetch(query)
        return [out[row] for out in out]

    async def get_all(self, table, attribute, compare):
        query = f"SELECT * FROM {table} WHERE {attribute} = {compare}"
        out = await self.conn.fetch(query)
        return out

    async def updatedb(self):
        try:
            trust.Trust.unload_trusts()
            await trust.Trust.load_trusts(trust.Trust(self.bot))
            blacklist.Blacklist.unload_blacklist()
            await blacklist.Blacklist.load_blacklist(blacklist.Blacklist(self.bot))
            profile.Profile.unload_profile()
            await profile.Profile.load_profiles(profile.Profile(self.bot))
        except Exception as error:
            print(f"[DB] An error occurred while updating the database.\n[{error}]")
