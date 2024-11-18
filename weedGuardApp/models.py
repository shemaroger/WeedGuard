from django.db import models

class User(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('farmer', 'Farmer'),
    )
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.fullname} ({self.role})"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Prediction(models.Model):
    image = models.ImageField(upload_to='predictions/')
    result = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255, null=True, blank=True)  # GPS coordinates
    site_name = models.CharField(max_length=100, null=True, blank=True)  # Site name
    farmer = models.CharField(max_length=100, null=True, blank=True)  # Farmer's name or ID

    def __str__(self):
        return f"{self.result} - {self.timestamp} - {self.site_name or 'Unknown Site'}"

    class Meta:
        verbose_name = "Prediction"
        verbose_name_plural = "Predictions"
