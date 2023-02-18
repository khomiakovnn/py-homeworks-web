import requests

href = "http://127.0.0.1:5000"

response = requests.get(url=href+'/test_page/')
print(response.status_code)
print(response.json())