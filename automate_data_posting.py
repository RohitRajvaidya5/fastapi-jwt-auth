import requests
from faker import Faker

url = "http://127.0.0.1:8000/users"

fake = Faker()

for i in range(1, 21):
    requests.post(
        url,
        json={
            "username": fake.user_name(),
            "email": fake.email(),
            "password": fake.password()
        }
    )

print("Done")
