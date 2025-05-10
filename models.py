import asyncpg
import os

DATABASE_URL = os.getenv("DATABASE_URL")

async def create_table():
    async with asyncpg.create_pool(DATABASE_URL) as pool:
        async with pool.acquire() as connection:
            await connection.execute("""
            CREATE TABLE IF NOT EXISTS characters (
                id SERIAL PRIMARY KEY,
                name VARCHAR,
                birth_year VARCHAR,
                eye_color VARCHAR,
                gender VARCHAR,
                hair_color VARCHAR,
                height VARCHAR,
                mass VARCHAR,
                homeworld VARCHAR,
                films TEXT[],
                species TEXT[],
                starships TEXT[],
                vehicles TEXT[]
            )
            """)