# import post_save
from allauth.socialaccount.models import SocialAccount
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=SocialAccount)
def social_account_post_save(sender, instance, created, **kwargs):
    if created:
        print("New social account created")
        data = instance.extra_data
        print(data)
