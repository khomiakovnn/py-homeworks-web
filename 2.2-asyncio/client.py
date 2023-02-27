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


def bd_update(persons):
    """
    Записывает персонажа в БД
    """
    with Session() as session:
        for i in range(0, len(persons)):
            new_person = People(**persons[i])
            session.add(new_person)
        session.commit()


async def main():
    # Собираем количество объектов
    count_person = get_count()
    pagination = count_person // 10 + 1

    session = aiohttp.ClientSession()
    # Собираем корутины для запроса страниц пагинации
    coros_pagi = []
    for i in range(1, pagination + 1):
        url = f"https://swapi.dev/api/people/?page={i}"
        coroutine = get_data(url, session)
        coros_pagi.append(coroutine)
    result_pagi = await asyncio.gather(*coros_pagi)
    print("Собрали данные со страниц пагинации", len(result_pagi))

    # Собираем заготовку персонажа
    person_tasks = []
    persons = []
    for page in result_pagi:
        for instance in page['results']:
            person = {
                'id': int(instance['url'][29:-1]),
                'birth_year': instance['birth_year'],
                'eye_color': instance['eye_color'],
                'films': asyncio.create_task(get_names(instance['films'], 'title', session)),
                'gender': instance['gender'],
                'hair_color': instance['hair_color'],
                'height': instance['height'],
                'homeworld': instance['name'],
                'mass': instance['mass'],
                'name': instance['name'],
                'skin_color': instance['skin_color'],
                'species': asyncio.create_task(get_names(instance['species'], 'name', session)),
                'starships': asyncio.create_task(get_names(instance['starships'], 'name', session)),
                'vehicles': asyncio.create_task(get_names(instance['vehicles'], 'name', session)),
            }
            person_tasks.append(person['films'])
            person_tasks.append(person['species'])
            person_tasks.append(person['starships'])
            person_tasks.append(person['vehicles'])
            persons.append(person)
    await asyncio.gather(*person_tasks)
    await session.close()
    for i in range(0, count_person):
        persons[i]['films'] = persons[i]['films'].result()
        persons[i]['species'] = persons[i]['species'].result()
        persons[i]['starships'] = persons[i]['starships'].result()
        persons[i]['vehicles'] = persons[i]['vehicles'].result()
    bd_update(persons)


if __name__ == '__main__':
    start_time = datetime.now()
    asyncio.run(main())
    print(datetime.now() - start_time)