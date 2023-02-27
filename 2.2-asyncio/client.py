import asyncio
import aiohttp
import requests
from datetime import datetime

from db import Session, People


async def get_names(links, name_inst, session):
    """
    Собирает имена субстанций по их ссылке и наименованию
    """
    coros = []
    for url in links:
        response = get_data(url, session)
        coros.append(response)
    result = await asyncio.gather(*coros)
    results = []
    for item in result:
        results.append(item[name_inst])
    return ', '.join(results)


def get_count():
    """
    Выясняет количество персонажей
    """
    url = "https://swapi.dev/api/people/"
    quantity = requests.get(url).json()['count']
    print(f'Найдено персонажей - {quantity}')
    return quantity


async def get_data(url, session):
    """
    Собирает все данные со страницы
    """
    response = await session.get(url)
    response_json = await response.json()
    return response_json


def bd_update(person):
    """
    Записывает персонажа в БД
    """
    with Session() as session:
        new_person = People(**person)
        session.add(new_person)
        session.commit()


async def main():
    # Собираем количество объектов
    pagination = get_count() // 10 + 1

    session = aiohttp.ClientSession()
    # Собираем корутины для запроса страниц пагинации
    coros_pagi = []
    for i in range(1, pagination + 1):
        url = f"https://swapi.dev/api/people/?page={i}"
        coroutine = get_data(url, session)
        coros_pagi.append(coroutine)
    result_pagi = await asyncio.gather(*coros_pagi)
    print("Собрали данные со страниц пагинации", len(result_pagi))

    # Собираем персонаж
    for page in result_pagi:
        for instance in page['results']:
            person = {
                'id': int(instance['url'][29:-1]),
                'birth_year': instance['birth_year'],
                'eye_color': instance['eye_color'],
                'films': await get_names(instance['films'], 'title', session),
                'gender': instance['gender'],
                'hair_color': instance['hair_color'],
                'height': instance['height'],
                'homeworld': instance['name'],
                'mass': instance['mass'],
                'name': instance['name'],
                'skin_color': instance['skin_color'],
                'species': await get_names(instance['species'], 'name', session),
                'starships': await get_names(instance['starships'], 'name', session),
                'vehicles': await get_names(instance['vehicles'], 'name', session),
            }
            bd_update(person)
            print("Добавлен персонаж")
    await session.close()

if __name__ == '__main__':
    start_time = datetime.now()
    asyncio.run(main())
    print(datetime.now() - start_time)
