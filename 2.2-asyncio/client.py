import requests
from datetime import datetime

from db import Session, People


def get_names(links, name_inst):
    result = []
    for link in links:
        response = requests.get(link).json()[name_inst]
        result.append(response)
    return ', '.join(result)


def main():
    start_time = datetime.now()

    url = "https://swapi.dev/api/people/"
    quantity = requests.get(url).json()['count']
    print(f'Найдено персонажей - {quantity}')

    with Session() as session:
        finded = 0
        person_id = 1
        while finded < quantity:
            url = f'https://swapi.dev/api/people/{person_id}/'
            querry_time = datetime.now()
            response = requests.get(url)
            if response.status_code == 200:
                finded += 1
                person = {
                    'id': person_id,
                    'birth_year': response.json()['birth_year'],
                    'eye_color': response.json()['eye_color'],
                    'films': get_names(response.json()['films'], 'title'),
                    'gender': response.json()['gender'],
                    'hair_color': response.json()['hair_color'],
                    'height': response.json()['height'],
                    'homeworld': requests.get(response.json()['homeworld']).json()['name'],
                    'mass': response.json()['mass'],
                    'name': response.json()['name'],
                    'skin_color': response.json()['skin_color'],
                    'species': get_names(response.json()['species'], 'name'),
                    'starships': get_names(response.json()['starships'], 'name'),
                    'vehicles': get_names(response.json()['vehicles'], 'name'),
                }
                new_person = People(**person)
                session.add(new_person)
                session.commit()
                print(f'Обработано {finded} из {quantity}. Время запроса: {datetime.now() - querry_time}')
            person_id += 1


    print(datetime.now() - start_time)


if __name__ == '__main__':
    main()
