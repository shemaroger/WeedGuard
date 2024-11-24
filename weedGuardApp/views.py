from django.http import JsonResponse
from rest_framework import generics,status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
import os
from .models import *
from .serializers import *
from .ml_model import predict_image  # Assuming this is your prediction logic
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def create_user(request):
    data = request.data
    if 'name' not in data or 'email' not in data or 'password' not in data:
        return Response({"detail": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Assuming user creation logic here
    return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving, updating, and deleting a user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated] 
class LoginView(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this view

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            # Get the validated data
            email = serializer.validated_data["email"]
            user = User.objects.get(email=email)
            
            # Generate JWT token for the user
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            # Send the token in response
            return Response({
                "access_token": str(access_token),
                "refresh_token": str(refresh)
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Create a new prediction
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Ensure only authenticated users can access this
def predict_view(request):
    """
    Handles custom prediction requests and directly returns the prediction result.
    This view will save the prediction details and return them at the same time.
    """
    if 'image' in request.FILES:
        try:
            # Retrieve the uploaded image file
            image_file = request.FILES['image']
            
            # Save image temporarily
            temp_image_path = os.path.join('temp_images', image_file.name)
            os.makedirs('temp_images', exist_ok=True)

            # Save image to the temp directory
            with open(temp_image_path, 'wb') as f:
                for chunk in image_file.chunks():
                    f.write(chunk)

            # Perform the prediction using the image
            prediction_result = predict_image(temp_image_path)

            # Get additional metadata from the request
            location = request.POST.get('location', '')
            site_name = request.POST.get('site_name', '')

            # Save the prediction to the database
            prediction = Prediction.objects.create(
                image=image_file,
                result=prediction_result,
                location=location,
                site_name=site_name,
                user=request.user  # Associated with the currently authenticated user
            )

            # Clean up the temporary image file after processing
            os.remove(temp_image_path)

            # Serialize the prediction details and return the response
            prediction_data = {
                'id': prediction.id,
                'result': prediction_result,
                'location': prediction.location,
                'site_name': prediction.site_name,
                'timestamp': prediction.timestamp,
            }
            return JsonResponse(prediction_data, status=201)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'No image file provided'}, status=400)

# Read a list of predictions
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_predictions(request):
    """
    Retrieve a list of all predictions made by the authenticated user.
    """
    predictions = Prediction.objects.filter(user=request.user)  # Filter by the authenticated user
    predictions_data = [
        {
            'id': prediction.id,
            'result': prediction.result,
            'location': prediction.location,
            'site_name': prediction.site_name,
            'timestamp': prediction.timestamp,
        } for prediction in predictions
    ]
    return JsonResponse({'predictions': predictions_data}, safe=False)

# Read a specific prediction by ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_prediction(request, prediction_id):
    """
    Retrieve a specific prediction by ID.
    """
    prediction = get_object_or_404(Prediction, id=prediction_id, user=request.user)  # Ensure it belongs to the user
    prediction_data = {
        'id': prediction.id,
        'result': prediction.result,
        'location': prediction.location,
        'site_name': prediction.site_name,
        'timestamp': prediction.timestamp,
    }
    return JsonResponse(prediction_data)

# Update a prediction
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_prediction(request, prediction_id):
    """
    Update the result or metadata of a specific prediction.
    """
    prediction = get_object_or_404(Prediction, id=prediction_id, user=request.user)

    # Update fields from request data
    result = request.data.get('result', prediction.result)
    location = request.data.get('location', prediction.location)
    site_name = request.data.get('site_name', prediction.site_name)

    # Save the updated prediction
    prediction.result = result
    prediction.location = location
    prediction.site_name = site_name
    prediction.save()

    updated_prediction_data = {
        'id': prediction.id,
        'result': prediction.result,
        'location': prediction.location,
        'site_name': prediction.site_name,
        'timestamp': prediction.timestamp,
    }
    return JsonResponse(updated_prediction_data)

# Delete a prediction
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_prediction(request, prediction_id):
    """
    Delete a specific prediction.
    """
    prediction = get_object_or_404(Prediction, id=prediction_id, user=request.user)

    # Delete the prediction record
    prediction.delete()
    return JsonResponse({'message': 'Prediction deleted successfully'}, status=204)
