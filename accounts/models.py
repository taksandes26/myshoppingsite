from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    moblile = models.IntegerField()
    address = models.CharField(max_length=50)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    file = models.FileField(upload_to='files')

