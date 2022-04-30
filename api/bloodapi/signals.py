from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .models import Profile

@receiver(post_save, sender=User)
def create_auth_Toen(sender, instance, created, **kwargs):
    if created:
        token = Token.objects.create(user=instance)
        token.save()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        profile.save()

