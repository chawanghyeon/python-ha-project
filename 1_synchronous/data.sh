#!/bin/bash

source .env/bin/activate

python manage.py shell <<EOF
from project.app.models import User, Book, Content

user = User.objects.create(name="Test User", email="test@test.com", password="test")

for i in range(100):
    book = Book.objects.create(title=f"Test Book{i}", user=user)
    for j in range(500):
        Content.objects.create(book=book, text=f"Test Content{j}")
EOF
