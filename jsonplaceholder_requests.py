import aiohttp
import asyncio

USERS_DATA_URL = "https://jsonplaceholder.typicode.com/users"
POSTS_DATA_URL = "https://jsonplaceholder.typicode.com/posts"

async def fetch_json(session, url):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()
    except aiohttp.ClientError as e:
        print(f"Ошибка: {e}")
        return None

async def fetch_users_data():
    async with aiohttp.ClientSession() as session:
        return await fetch_json(session, USERS_DATA_URL)

async def fetch_posts_data():
    async with aiohttp.ClientSession() as session:
        return await fetch_json(session, POSTS_DATA_URL)

