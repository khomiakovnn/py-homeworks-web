import asyncio
import random
from aiohttp import ClientSession

api_url_ad = 'http://127.0.0.1:8080/api/ads/'
api_url_user = 'http://127.0.0.1:8080/api/users/'
ad_num = random.randrange(10000, 99999, 1)
user_num = random.choice([2, 3, 5, 6, 7])
create_ad_json = {
    'title': f'Объявление № {ad_num}',
    'description': f'Текст объявления № {ad_num}',
    'author': user_num,
}
patch_ad_json = {
    'title': f'Объявление № {ad_num}',
    'description': f'Текст объявления № {ad_num}',
}
create_user_json = {
    'username': 'Fedia2',
    'password': '12224578',
    'email': 'fedia2@ivanov',
}


async def post_ad():
    async with ClientSession() as session:
        response = await session.post(api_url_ad, json=create_ad_json)
        print(response.status)
        print(await response.json())


async def get_ad(ad_id):
    async with ClientSession() as session:
        response = await session.get(api_url_ad+ str(ad_id) + '/')
        print(response.status)
        print(await response.json())


async def patch_ad(ad_id, user_id):
    patch_ad_json.update({'user_id': user_id})
    async with ClientSession() as session:
        response = await session.patch(api_url_ad+ str(ad_id) + '/',
                                       json=patch_ad_json)
        print(response.status)
        print(await response.json())


async def delete_ad(ad_id, user_id):
    async with ClientSession() as session:
        response = await session.delete(api_url_ad+ str(ad_id) + '/', json={'user_id': user_id})
        print(response.status)
        print(await response.json())


async def post_user():
    async with ClientSession() as session:
        response = await session.post(api_url_user, json=create_user_json)
        print(response.status)
        print(await response.json())


async def get_user(user_id):
    async with ClientSession() as session:
        response = await session.get(api_url_user + str(user_id) + '/')
        print(response.status)
        print(await response.json())


async def patch_user(user_id):
    async with ClientSession() as session:
        response = await session.patch(api_url_user + str(user_id) + '/', json=create_user_json)
        print(response.status)
        print(await response.json())


async def delete_user(user_id):
    async with ClientSession() as session:
        response = await session.delete(api_url_user + str(user_id) + '/')
        print(response.status)
        print(await response.json())


asyncio.run(delete_ad(2, 6))
