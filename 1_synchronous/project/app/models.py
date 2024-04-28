from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Book(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Content(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="contents")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# from project.app.models import User, Book, Content
# user = User.objects.create(name="Test User", email="test@test.com", password="test")

# for i in range(10):
#     book = Book.objects.create(title=f"Test Book{i}", user=user)
#     for j in range(100):
#         Content.objects.create(book=book, text=f"Test Content{j}")
