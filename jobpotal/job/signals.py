from django.db.models.signals import post_save
from .models import User, Profile
from PIL import Image
import os
# from django.contrib.auth.models import User
from django.dispatch import receiver

# def save_post(sender, instance, **kwargs):
#     print("post save working")

# def save_pre(sender, instance, **kwargs):
#     print("pre save working")

# def delete_pre(sender,instance,**kwargs):
#     print("deleted")


# pre_save.connect(save_pre, sender=User)
# pre_delete.connect(delete_pre, sender=User)

@receiver(post_save, sender=User)
def prof(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(prof, sender=User)