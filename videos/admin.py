from django.contrib import admin
from .models import Video, UserVideoAccess

admin.site.register(Video)
admin.site.register(UserVideoAccess)
