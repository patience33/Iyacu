from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('upload/', views.upload_video, name='upload_video'),
    path('watch/<int:video_id>/', views.watch_video, name='watch_video'),
    path('request_access/<int:video_id>/', views.request_access, name='request_access'),
    path('download/<int:video_id>/', views.download_video, name='download_video'),

     # Login and Logout URLs
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Registration URL
    path('register/', views.register, name='register'),
]
