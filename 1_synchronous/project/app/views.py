from django.views import View
from django.http import JsonResponse
from .models import Book
import onnxruntime as ort
from PIL import Image
import numpy as np
import base64


class BookView(View):
    def get(self, request):
        books = Book.objects.all().values()
        return JsonResponse(list(books), safe=False)

    def post(self, request):
        pass


class EncodingView(View):
    def get(self, request):
        pass

    def post(self, request):
        image_base64 = request.FILES['image']
        image_width = request.POST['width']
        image_height = request.POST['height']
        # Load the model
        image_bytes_decoded = base64.b64decode(image_base64)
        image = Image.frombytes("RGB", (image_width, image_height), image_bytes_decoded)
        image = image.resize((224, 224))
        image = np.array(image, dtype=np.float32)
        image = image.transpose((2, 0, 1))
        image = np.expand_dims(image, axis=0)

        model = ort.InferenceSession("resnet.onnx")
        output_bytes = model.run(None, {'data': image})[0].tobytes()
        output_base64 = base64.b64encode(output_bytes).decode('utf-8')

        return JsonResponse({'encoded_image': output_base64})
