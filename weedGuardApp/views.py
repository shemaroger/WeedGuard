from django.shortcuts import render
from django.http import JsonResponse
from .ml_model import predict_image
from .models import Prediction
import os

def predict_view(request):
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            # Ensure the temporary images directory exists
            image_dir = 'temp_images'
            os.makedirs(image_dir, exist_ok=True)

            # Save the uploaded image temporarily
            image_file = request.FILES['image']
            image_path = os.path.join(image_dir, image_file.name)
            with open(image_path, 'wb') as f:
                for chunk in image_file.chunks():
                    f.write(chunk)

            # Get additional data from the POST request
            location = request.POST.get('location', '')
            site_name = request.POST.get('site_name', '')
            farmer = request.POST.get('farmer', '')

            # Perform prediction
            prediction_result = predict_image(image_path)

            # Save the result to the database
            prediction_entry = Prediction.objects.create(
                image=image_file,
                result=prediction_result,
                location=location,
                site_name=site_name,
                farmer=farmer,
            )

            # Clean up the temporary image
            os.remove(image_path)

            return JsonResponse({'prediction': prediction_result, 'id': prediction_entry.id})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return render(request, 'weedGuardApp/predict.html')
