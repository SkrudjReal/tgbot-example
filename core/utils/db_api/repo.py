from dataclasses import dataclass
from asyncmy.cursors import DictCursor


@dataclass
class RequestsRepo:
    cur: DictCursor
    
    ### SQL Simple Queries ###
    
    async def select_all(self, sql: str, params: tuple = None, use_index_zero: bool = True):
        await self.cur.execute(sql, params)
        result = await self.cur.fetchall()
        if result:
            return result[0] if use_index_zero else result
        else:
            return None
    
    async def select_one(self, sql: str, params: tuple = None):
        await self.cur.execute(sql, params)
        result = await self.cur.fetchone()
        return next(iter(result.values())) if result else None
    
    ### Main Elements ###
    
    async def get_user(self, link: int | str):
        return await self.select_all(
            'SELECT * FROM Users WHERE user_id=%s OR username=%s;', 
            (link, link)
        )
    
    ### Add main elements ###
    
    async def add_data_user(self, user_id: int, full_name: str, username: str = None):
        query = 'UPDATE Users SET username=NULL WHERE user_id!=%s AND username=%s;'
        query1 = (
            'INSERT INTO Users (user_id, full_name, username) VALUES (%s, %s, %s) '
            'ON DUPLICATE KEY UPDATE'
            ' full_name=%s,'
            ' username=%s;'
        )
        await self.cur.execute(query, (user_id, username))
        params = (user_id, full_name, username, full_name, username)
        await self.cur.execute(query1, params)

