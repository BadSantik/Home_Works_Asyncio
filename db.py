import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

pool = None


async def create_pool():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)


async def close_pool():
    await pool.close()


async def insert_person(person):
    async with pool.acquire() as connection:
        await connection.execute("""
            INSERT INTO characters (id, name, birth_year, eye_color, gender, hair_color,
                                    height, mass, homeworld, films, species, starships, vehicles)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
        """, person['id'], person['name'], person['birth_year'], person['eye_color'],
                                 person['gender'], person['hair_color'], person['height'], person['mass'],
                                 person['homeworld'], person['films'], person['species'], person['starships'],
                                 person['vehicles'])


async def load_data(people_data):
    for index, person in enumerate(people_data, start=1):
        person['id'] = index  # Присвоение ID
        person['films'] = ', '.join(person.get('films', []))
        person['species'] = ', '.join(person.get('species', []))
        person['starships'] = ', '.join(person.get('starships', []))
        person['vehicles'] = ', '.join(person.get('vehicles', []))

        await insert_person(person)
