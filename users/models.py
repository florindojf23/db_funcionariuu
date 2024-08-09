from django.db import models
from django.contrib.auth.models import User, Group
     
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default_profile_pic.jpg')

    def __str__(self):
        return self.user.username