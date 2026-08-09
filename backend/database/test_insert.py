from db import db

users = db["users"]

user = {
    "name": "Shashi",
    "email": "shashi@gmail.com",
    "skills": [
        "Python",
        "Flask",
        "MongoDB"
    ]
}

result = users.insert_one(user)

print("Inserted ID:", result.inserted_id)