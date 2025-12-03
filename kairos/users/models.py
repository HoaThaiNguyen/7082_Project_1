from django.db import models
from django.contrib.auth.models import User

def user_profile_pic_path(instance, filename):
    # store in: media/username/profile/profile_picture/<filename>
    return f'{instance.user.username}/profile/profile_picture/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    nickname = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to=user_profile_pic_path, blank=True, null=True)
    bio = models.TextField(max_length=50, blank=True)
    is_calendar_public = models.BooleanField(default=True)

    def __str__(self):
        return self.nickname or self.user.username
