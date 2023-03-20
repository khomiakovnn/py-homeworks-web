import asyncio
from aiohttp import ClientSession


async def main():
    async with ClientSession() as session:
        response = await session.get('http://127.0.0.1:8080/')
        print(response.status)
        print(await response.text())


asyncio.run(main())
