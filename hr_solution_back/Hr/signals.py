from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group

from rest_framework.authtoken.models import Token

from .models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def set_user_group(sender, instance=None, created=False, **kwargs):
    if created:
        my_group = Group.objects.get(name='Regular employee')
        my_group.user_set.add(instance)
