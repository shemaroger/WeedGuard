from django.db import models

class Prediction(models.Model):
    image = models.ImageField(upload_to='predictions/')
    result = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255, null=True, blank=True)  # GPS coordinates
    site_name = models.CharField(max_length=100, null=True, blank=True)  # Site name
    farmer = models.CharField(max_length=100, null=True, blank=True)  # Farmer's name or ID

    def __str__(self):
        return f"{self.result} - {self.timestamp} - {self.site_name or 'Unknown Site'}"
