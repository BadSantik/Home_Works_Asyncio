import asyncio
import aiohttp
import asyncpg
import os
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


async def create_pool():
    return await asyncpg.create_pool(DATABASE_URL)


async def create_table(pool):
    async with pool.acquire() as connection:
        await connection.execute('''
            CREATE TABLE IF NOT EXISTS characters (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                birth_year VARCHAR(50),
                eye_color VARCHAR(50),
                gender VARCHAR(20),
                hair_color VARCHAR(50),
                height VARCHAR(50),
                mass VARCHAR(50),
                homeworld VARCHAR(100),
                films TEXT[],
                species TEXT[],
                starships TEXT[],
                vehicles TEXT[]
            );
        ''')


async def load_data(pool, characters):
    async with pool.acquire() as connection:
        for character in characters:
            await connection.execute('''
                INSERT INTO characters (name, birth_year, eye_color, gender, hair_color, height,
                mass, homeworld, films, species, starships, vehicles)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
            ''', character['name'], character['birth_year'], character['eye_color'],
                                     character['gender'], character['hair_color'], character['height'],
                                     character['mass'], character['homeworld'], character.get('films', []),
                                     character.get('species', []), character.get('starships', []),
                                     character.get('vehicles', []))


async def fetch_person(session, url):
    async with session.get(url) as response:
        return await response.json()


async def fetch_all_people(session, base_url):
    url = f"{base_url}/people/"
    results = []

    while url:
        response = await fetch_person(session, url)
        results.extend(response['results'])
        url = response['next']

    return results


async def main():
    base_url = "https://swapi.dev/api"
    async with aiohttp.ClientSession() as session:
        people_data = await fetch_all_people(session, base_url)
        pool = await create_pool()
        await load_data(pool, people_data)
        await pool.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    pool = loop.run_until_complete(create_pool())
    loop.run_until_complete(create_table(pool))
    loop.run_until_complete(main())
