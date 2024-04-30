from locust import FastHttpUser, task
from PIL import Image


class MyUser(FastHttpUser):
    host = "127.0.0.1:8000"

    @task
    def encode(self):
        self.client.post(
            "http://127.0.0.1:8000/encodes/",
            data={
                "width": self.image_height,
                "height": self.image_height,
            },
            files={"image": ("image.jpg", self.image)},
        )

    def on_start(self) -> None:
        super().on_start()
        image = Image.open("image.jpg")
        self.image_width, self.image_height = image.size
        with open("image.jpg", "rb") as image_file:
            self.image = image_file.read()
