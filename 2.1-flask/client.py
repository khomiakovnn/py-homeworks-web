import requests

# Prepare block
base_url = "http://127.0.0.1:5000/api/adverts/"
adv_id = 1
token = 'my_token'
adv_data = {
    'title': 'Первое объявление',
    'description': 'Текст объявления',
    'author': 'Иванов Иван',
}

headers = {
    'token': token
}

# # GET method test
# url = base_url + str(adv_id) + '/'
# response = requests.get(url)
# print(response.status_code)
# print(response.json())

# POST method test
url = base_url
response = requests.post(url, json=adv_data)
print(response.status_code)
print(response.json())

# # PATCH method test
# url = base_url + str(adv_id) + '/'
# response = requests.patch(url, headers=headers, json=adv_data)
# print(response.status_code)
# print(response.json())

# # DELETE method test
# url = base_url + str(adv_id) + '/'
# response = requests.delete(url, headers=headers)
# print(response.status_code)
# print(response.json())

# # QueryString test
# url = base_url + '?param_1=value_1&param_2=value_2'
# response = requests.post(url, headers=headers, json=adv_data)
# print(response.status_code)
# print(response.json())
