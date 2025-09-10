from asyncmy.pool import Pool

from core.settings import settings

import asyncmy

async def ensure_database_exists():
    """
    Ensure the target database exists.
    Connect to MySQL without specifying db, create the DB if missing.
    """
    conn = await asyncmy.connect(
        host=settings.db.ip,
        port=3306,
        user=settings.db.user,
        password=settings.db.password,
        autocommit=True,
    )
    async with conn.cursor() as cur:
        await cur.execute(f"CREATE DATABASE IF NOT EXISTS `{settings.db.db}`")
    conn.close()

async def create_mysql_pool() -> Pool:
    """
    Create a connection pool to the MySQL database.
    """
    await ensure_database_exists()
    
    return await asyncmy.create_pool(
        host=settings.db.ip,
        port=3306,
        user=settings.db.user,
        password=settings.db.password,
        db=settings.db.db,
        autocommit=True
    )

async def db_setup(pool: Pool):
    
    users_table = (
        'CREATE TABLE IF NOT EXISTS Users ('
        ' user_id BIGINT(16) NOT NULL PRIMARY KEY,'
        ' full_name VARCHAR(128) NOT NULL,'
        ' username VARCHAR(32) DEFAULT NULL'
        ');'
    )

    tasks = [
        users_table,
    ]
    
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            for ex in tasks:
                await cur.execute(ex)
