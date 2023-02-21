import requests

# Prepare block
adv_url = "http://127.0.0.1:5000/api/adverts/"
user_url = "http://127.0.0.1:5000/api/users/"
adv_id = 1
user_id = 2
token = 'my_token'
adv_data = {
    'title': 'Первое исправленное объявление',
    'description': 'Текст нового объявления',
    'author': 'Иванов Иван',
}
user_data = {
    'username': 'Петров Петр',
    'password': 'Qwerty33',
    'email': 'petrov@petr.com',
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
# url = base_url
# response = requests.post(url, json=adv_data)
# print(response.status_code)
# print(response.json())

# # PATCH method test
# url = base_url + str(adv_id) + '/'
# response = requests.patch(url, json=adv_data)
# print(response.status_code)
# print(response.json())

# # DELETE method test
# url = base_url + str(adv_id) + '/'
# response = requests.delete(url)
# print(response.status_code)
# print(response.json())

# # QueryString test
# url = base_url + '?param_1=value_1&param_2=value_2'
# response = requests.post(url, headers=headers, json=adv_data)
# print(response.status_code)
# print(response.json())

# GET USER method test
# url = user_url + str(user_id) + '/'
# response = requests.get(url)
# print(response.status_code)
# print(response.json())

# POST USER method test
# url = user_url
# response = requests.post(url, json=user_data)
# print(response.status_code)
# print(response.json())

# PATCH method test
# url = user_url + str(user_id) + '/'
# response = requests.patch(url, json=user_data)
# print(response.status_code)
# print(response.json())

# DELETE USER method test
# url = user_url + str(user_id) + '/'
# response = requests.delete(url)
# print(response.status_code)
# print(response.json())
