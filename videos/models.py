from django.contrib.auth.models import User
from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/file')
    video_banner = models.ImageField(upload_to='videos/banner')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
     return self.title

class UserVideoAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    access_start = models.DateTimeField()
    access_end = models.DateTimeField()

    
