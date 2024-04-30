from locust import FastHttpUser, task


class MyUser(FastHttpUser):
    host = "127.0.0.1:8000"

    @task
    def book(self):
        self.client.get("http://127.0.0.1:8000/books/")
