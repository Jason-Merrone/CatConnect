from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):  
    user = models.OneToOneField(User,on_delete=models.CASCADE)  
    cat_breed = models.TextField(default="None")
    link_to_pfp = models.TextField(default="https://i.imgur.com/Fq5xOFO.png")
    bio = models.TextField(default="None")

    def __str__(self):  
          return "%s's profile" % self.user  

def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
       profile, created = UserProfile.objects.get_or_create(user=instance)  

post_save.connect(create_user_profile, sender=User)
