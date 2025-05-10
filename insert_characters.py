import asyncio
import asyncpg
import os
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

async def create_pool():
    return await asyncpg.create_pool(DATABASE_URL)

async def load_data(pool, characters):
    async with pool.acquire() as connection:
        for character in characters:
            await connection.execute('''
                INSERT INTO characters (name, birth_year, eye_color, gender, hair_color, height,
                mass, homeworld, films, species, starships, vehicles)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
            ''', character['name'], character['birth_year'], character['eye_color'],
               character['gender'], character['hair_color'], character['height'],
               character['mass'], character['homeworld'],
               character.get('films', []), character.get('species', []),
               character.get('starships', []), character.get('vehicles', []))

async def main():
    characters_data = [
        {
            "birth_year": "19 BBY",
            "eye_color": "Blue",
            "films": ["https://swapi.dev/api/films/1/"],
            "gender": "Male",
            "hair_color": "Blond",
            "height": "172",
            "mass": "77",
            "name": "Luke Skywalker",
            "homeworld": "https://swapi.dev/api/planets/1/",
            "species": ["https://swapi.dev/api/species/1/"],
            "starships": ["https://swapi.dev/api/starships/12/"],
            "vehicles": ["https://swapi.dev/api/vehicles/14/"]
        },
        {
            "birth_year": "19 BBY",
            "eye_color": "Brown",
            "films": ["https://swapi.dev/api/films/1/"],
            "gender": "Male",
            "hair_color": "Brown",
            "height": "180",
            "mass": "80",
            "name": "Han Solo",
            "homeworld": "https://swapi.dev/api/planets/1/",
            "species": ["https://swapi.dev/api/species/1/"],
            "starships": ["https://swapi.dev/api/starships/10/"],
            "vehicles": ["https://swapi.dev/api/vehicles/11/"]
        },
        {
            "birth_year": "19 BBY",
            "eye_color": "Hazel",
            "films": ["https://swapi.dev/api/films/1/"],
            "gender": "Female",
            "hair_color": "Brown",
            "height": "165",
            "mass": "55",
            "name": "Leia Organa",
            "homeworld": "https://swapi.dev/api/planets/2/",
            "species": ["https://swapi.dev/api/species/1/"],
            "starships": ["https://swapi.dev/api/starships/11/"],
            "vehicles": ["https://swapi.dev/api/vehicles/14/"]
        },
        {
            "birth_year": "32 BBY",
            "eye_color": "Green",
            "films": ["https://swapi.dev/api/films/5/"],
            "gender": "Male",
            "hair_color": "Brown",
            "height": "188",
            "mass": "84",
            "name": "Qui-Gon Jinn",
            "homeworld": "https://swapi.dev/api/planets/2/",
            "species": ["https://swapi.dev/api/species/1/"],
            "starships": ["https://swapi.dev/api/starships/14/"],
            "vehicles": ["https://swapi.dev/api/vehicles/16/"]
        },
        {
            "birth_year": "41.9 BBY",
            "eye_color": "Blue",
            "films": ["https://swapi.dev/api/films/2/"],
            "gender": "Male",
            "hair_color": "Brown",
            "height": "175",
            "mass": "74",
            "name": "Obi-Wan Kenobi",
            "homeworld": "https://swapi.dev/api/planets/20/",
            "species": ["https://swapi.dev/api/species/1/"],
            "starships": ["https://swapi.dev/api/starships/13/"],
            "vehicles": []
        },
        {
            "birth_year": "41 BBY",
            "eye_color": "Brown",
            "films": ["https://swapi.dev/api/films/3/"],
            "gender": "Female",
            "hair_color": "Red",
            "height": "160",
            "mass": "50",
            "name": "Padmé Amidala",
            "homeworld": "https://swapi.dev/api/planets/8/",
            "species": ["https://swapi.dev/api/species/1/"],
            "starships": [],
            "vehicles": []
        },
        {
            "birth_year": "41.9 BBY",
            "eye_color": "Green",
            "films": ["https://swapi.dev/api/films/1/"],
            "gender": "Female",
            "hair_color": "Black",
            "height": "170",
            "mass": "60",
            "name": "Ahsoka Tano",
            "homeworld": "https://swapi.dev/api/planets/8/",
            "species": ["https://swapi.dev/api/species/3/"],
            "starships": [],
            "vehicles": []
        },
        {
            "birth_year": "41.9 BBY",
            "eye_color": "Red",
            "films": ["https://swapi.dev/api/films/4/"],
            "gender": "Male",
            "hair_color": "Gray",
            "height": "190",
            "mass": "90",
            "name": "Mace Windu",
            "homeworld": "https://swapi.dev/api/planets/1/",
            "species": ["https://swapi.dev/api/species/1/"],
            "starships": [],
            "vehicles": []
        },
        {
            "birth_year": "19 BBY",
            "eye_color": "Black",
            "films": ["https://swapi.dev/api/films/1/"],
            "gender": "Male",
            "hair_color": "Black",
            "height": "177",
            "mass": "75",
            "name": "Finn",
            "homeworld": "https://swapi.dev/api/planets/1/",
            "species": ["https://swapi.dev/api/species/1/"],
            "starships": [],
            "vehicles": []
        },
        {
            "birth_year": "19 BBY",
            "eye_color": "Brown",
            "films": ["https://swapi.dev/api/films/2/"],
            "gender": "Female",
            "hair_color": "Brown",
            "height": "160",
            "mass": "65",
            "name": "Rey",
            "homeworld": "https://swapi.dev/api/planets/1/",
            "species": ["https://swapi.dev/api/species/1/"],
            "starships": [],
            "vehicles": []
        }
    ]

    pool = await create_pool()
    await load_data(pool, characters_data)
    await pool.close()

if __name__ == "__main__":
    asyncio.run(main())