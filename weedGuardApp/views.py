from django.shortcuts import render
import os
import numpy as np
from django.http import JsonResponse
from django.conf import settings
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.preprocessing import image # type: ignore
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# Load the pre-trained model (ensure the path is correct)
model_path = os.path.join(settings.BASE_DIR, 'D:\\Project\\WeedGuard\\my_trained_model.keras')  # Update with the new format
model = load_model(model_path)

# Define image dimensions (must match what you used in training)
IMAGE_SIZE = (150, 150)

@csrf_exempt
def classify_image(request):
    if request.method == 'POST' and 'file' in request.FILES:
        # Save the uploaded file
        uploaded_file = request.FILES['file']
        file_name = default_storage.save(uploaded_file.name, ContentFile(uploaded_file.read()))
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        
        try:
            # Preprocess the image for model input
            img = image.load_img(file_path, target_size=IMAGE_SIZE)
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array /= 255.0  # Normalization (same as in training)

            # Make prediction
            predictions = model.predict(img_array)
            predicted_class = np.argmax(predictions, axis=1)
            confidence = np.max(predictions)  # Get confidence of the prediction

        except Exception as e:
            # Clean up (remove the saved image file after processing)
            os.remove(file_path)
            return JsonResponse({'error': str(e)}, status=500)

        # Clean up (remove the saved image file after processing)
        os.remove(file_path)

        # Return the prediction result as JSON
        return JsonResponse({
            'predicted_class': int(predicted_class[0]),
            'confidence': float(confidence)
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def upload_image(request):
    return render(request, 'weedGuardApp/upload_image.html')
