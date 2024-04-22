from django.views import View
from django.http import JsonResponse
from .models import Book
import onnxruntime as ort


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
        image = request.FILES['image']
        # Load the model
        model = ort.InferenceSession('../../../resnet50-v2-7.onnx')
        # Do some processing
        output = model.run(image)
        # Encode the output
        encoded_image = output.encode('base64')
        return JsonResponse({'encoded_image': encoded_image})
        
        


