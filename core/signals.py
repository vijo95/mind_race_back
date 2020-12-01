from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from . models import UserProfile, Player

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile.objects.create(user=instance)
        player = Player.objects.create(user_profile=user_profile)
        user = instance
        user.email = ''
        player.username = user.username
        player.save()
        user.save()
