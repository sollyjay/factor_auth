from django.db.models.signals import post_save
from FactorApp.models import User, Follow, Following
from django.dispatch import receiver
 
 
@receiver(post_save, sender=User)
def create_user_follow(sender, instance, created, **kwargs):
    if created:
        Follow.objects.create(user=instance)
  
@receiver(post_save, sender=User)
def save_user_follow(sender, instance, **kwargs):
        instance.user_follower.save()

@receiver(post_save, sender=User)
def create_user_following(sender, instance, created, **kwargs):
    if created:
        Following.objects.create(user=instance)
  
@receiver(post_save, sender=User)
def save_user_following(sender, instance, **kwargs):
    instance.user_following.save()