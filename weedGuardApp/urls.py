from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('predict/', predict_view, name='predict'),  # Create
    path('predictions/', list_predictions, name='list_predictions'),  # Read list
    path('predictions/<int:prediction_id>/', get_prediction, name='get_prediction'),  # Read single
    path('predictions/<int:prediction_id>/update/', update_prediction, name='update_prediction'),  # Update
    path('predictions/<int:prediction_id>/delete/', delete_prediction, name='delete_prediction'),  # Delete
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
