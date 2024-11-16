# prediction/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .ml_model import predict_image
import os

def predict_view(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # Ensure the 'temp_images' directory exists
        image_dir = 'temp_images'
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        # Define the image path
        image_file = request.FILES['image']
        image_path = os.path.join(image_dir, image_file.name)

        # Save the uploaded image temporarily
        with open(image_path, 'wb') as f:
            for chunk in image_file.chunks():
                f.write(chunk)

        # Run prediction
        prediction = predict_image(image_path)

        # Delete the temporary image after prediction
        os.remove(image_path)

        return JsonResponse({'prediction': prediction})
    else:
        return render(request, 'weedGuardApp/predict.html')
