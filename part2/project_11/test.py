import requests


# check add contact

data = requests.post(f'http://127.0.0.1:8000/api/add_contact?first_name=Qwerty&last_name=Doe&email=johndoe@example.com&phone_number=123456789&birthday=2024-04-05').json()
print(data)

# check show all contacts

data = requests.get('http://127.0.0.1:8000/api/show_contacts').json()
print(data)

# check delete contact
data = requests.delete('http://127.0.0.1:8000/api/delete_contact?contact_id=1').json()
print(data)

# check update contact

url = "http://127.0.0.1:8000/api/update_contact?contact_id=2"  # Замените на правильный URL для вашего сервера
data = {
    "first_name": "Новое имя",
    "last_name": "Новая фамилия",
    "email": "новый@example.com",
    "phone_number": "новый номер",
    "birthday": "новая дата",
    "additional_info": "новая дополнительная информация"
}

response = requests.put(url, json=data)
print(response)

# get contact with name, lastname or email

req = requests.get("http://127.0.0.1:8000/api/contact_card?query=John").json()
print(req)