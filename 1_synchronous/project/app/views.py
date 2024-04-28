from django.views import View
from django.http import JsonResponse
from .models import Book
import onnxruntime as ort
from PIL import Image
import numpy as np
import base64
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import time


@method_decorator(csrf_exempt, name="dispatch")
class BookView(View):
    def get(self, request):
        start = time.time()
        books = Book.objects.all().select_related("user").prefetch_related("contents")
        response = []
        for book in books:
            response.append(
                {
                    "title": book.title,
                    "author": book.user.name,
                    "contents": [content.text for content in book.contents.all()],
                }
            )
        print(f"Time taken: {time.time() - start}")
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class EncodingView(View):
    def post(self, request):
        start = time.time()
        image_width = int(request.POST.get("width", 0))
        image_height = int(request.POST.get("height", 0))
        image = request.FILES.get("image")

        if not image or not image_width or not image_height:
            return JsonResponse({"error": "Invalid input"}, status=400)

        image = Image.open(image)
        image = image.resize((224, 224))
        image = np.array(image, dtype=np.float32)
        image = image.transpose((2, 0, 1))
        image = np.expand_dims(image, axis=0)

        model = ort.InferenceSession("resnet.onnx")
        output_bytes = model.run(None, {"data": image})[0].tobytes()
        output_base64 = base64.b64encode(output_bytes).decode("utf-8")

        print(f"Time taken encode: {time.time() - start}")
        return JsonResponse({"encoded_image": output_base64})
