from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, User)
def profile_create_receiver(sender, instance, created, **kwargs):
    if created:
        new_user = instance
        profile = Profile(user=new_user)
        profile.save()
        print("profile created")
