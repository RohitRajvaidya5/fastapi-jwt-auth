import requests
from faker import Faker

url = "http://127.0.0.1:8000/posts/"

fake = Faker()

# Paste your JWT token here
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJoaW5hdGFfc2hveW9AZW1haWwuY29tIiwiZXhwIjoxNzg4MzY4NzMxfQ.RxXXFHydYCcPwgXd6PDxCACZDxorNvCaRYuEWQtJH34"

headers = {
    "Authorization": f"Bearer {token}"
}

for i in range(30):
    response = requests.post(
        url,
        headers=headers,
        json={
            "title": fake.sentence(nb_words=6),
            "content": fake.paragraph(nb_sentences=5)
        }
    )

    if response.status_code == 200:
        print(f"Post {i + 1} created successfully")

    else:
        print(f"Failed to create post {i + 1}: {response.status_code} - {response.text}")

print("Script Ended")
