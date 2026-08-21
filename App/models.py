from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Photo(models.Model):
    # Core Metadata
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    title = models.CharField(max_length=150, default="Untitled Shot")
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='images/')
    
    # EXIF & Technical Details
    camera_model = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. Sony A7IV")
    aperture = models.CharField(max_length=20, blank=True, null=True, help_text="e.g. f/2.8")
    shutter_speed = models.CharField(max_length=20, blank=True, null=True, help_text="e.g. 1/1000s")
    iso = models.IntegerField(blank=True, null=True, help_text="e.g. 100")
    focal_length = models.CharField(max_length=20, blank=True, null=True, help_text="e.g. 50mm")
    
    # Location & Context
    location = models.CharField(max_length=150, blank=True, null=True, help_text="e.g. Pokhara, Nepal")
    
    # Metrics & Engagement
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='liked_photos', blank=True)
    is_featured = models.BooleanField(default=False)
    
    # Timestamps
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.user.username}"