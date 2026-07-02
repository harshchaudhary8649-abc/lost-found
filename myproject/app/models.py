from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=10)
    location = models.CharField(max_length=150, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True, default='Other')
    contact = models.CharField(max_length=15, blank=True, null=False)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    removed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def is_saved_recently(self):
        if not self.removed_at:
            return True
        return self.removed_at >= timezone.now() - timedelta(days=30)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return self.user.username

