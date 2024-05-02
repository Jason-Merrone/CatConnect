from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):  
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    cat_breed = models.TextField(default="Not Specified")
    link_to_pfp = models.TextField(default="https://i.imgur.com/Fq5xOFO.png")
    bio = models.TextField(default="Not Specified")

    def __str__(self):  
          return "%s's profile" % self.user 

def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
       profile, created = UserProfile.objects.get_or_create(user=instance)
       
class Post(models.Model):
    profile = models.ForeignKey(UserProfile, related_name='posts', on_delete=models.CASCADE)
    caption = models.TextField(default="")
    link_to_image = models.TextField(default="")
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    liked_by = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    @property
    def likes(self):
        return self.liked_by.count()

    def __str__(self):
        return f"Post by {self.profile.user.username} on {self.created_at}"
    
post_save.connect(create_user_profile, sender=User)