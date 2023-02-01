import requests


def create_prod(title, description):
    href = 'http://localhost:8000/api/v1/products/'
    param = {
        "title": title,
        "description": description
    }
    response = requests.post(href, param)

    print(response.text)
    print(response.status_code)


def upd_prod(pk, title, description):
    href = 'http://localhost:8000/api/v1/products/' + str(pk) + '/'
    param = {}
    if title is not None:
        param['title'] = title
    if description is not None:
        param['description'] = description
    response = requests.patch(href, param)

    print(response.text)
    print(response.status_code)


def create_stock():
    href = 'http://localhost:8000/api/v1/stocks/'
    param = {
        "address": "Товарная ул., 23",
        "positions": [
            {
                "product": 1,
                "quantity": 250,
                "price": 120.50
            },
            {
                "product": 2,
                "quantity": 100,
                "price": 80
            }
        ]
    }
    response = requests.post(href, data=param)

    print(response.text)
    print(response.status_code)


if __name__ == '__main__':
    pass
    # create_prod(title="Помидор", description="Московский") # Тест POST продукта (CREATE)
    # upd_prod(pk=3, title="Перец чили", description="Острый перец") # Тест PATCH продукта (UPDATE)
    # create_stock()  # Тест POST склада (CREATE)
