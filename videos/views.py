from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse
from .models import Video, UserVideoAccess
from .forms import VideoForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login,logout

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Log the user in after registration
            return redirect('index')  # Replace 'home' with your desired URL after registration
    else:
        form = UserCreationForm()
    return render(request, 'user/register.html', {'form': form})

# Display the list of all videos
@login_required
def index(request):
    videos = Video.objects.all()
    return render(request, 'videos/index.html', {'videos': videos})


# Upload a new video (only accessible to logged-in users)
@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = VideoForm()
    return render(request, 'videos/upload_video.html', {'form': form})

# Watch a video (only accessible to logged-in users with valid access)
@login_required
def watch_video(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    access = UserVideoAccess.objects.filter(user=request.user, video=video).first()
    if access and access.access_start <= timezone.now() <= access.access_end:
        return render(request, 'videos/watch_video.html', {'video': video})
    else:
        return redirect('request_access', video_id=video.id)

# Request access to a video (only accessible to logged-in users)
@login_required
def request_access(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    if request.method == 'POST':
        # Handle access request
        access_end = timezone.now() + timezone.timedelta(days=30)
        UserVideoAccess.objects.create(user=request.user, video=video, access_start=timezone.now(), access_end=access_end)
        return redirect('watch_video', video_id=video.id)
    return render(request, 'videos/request_access.html', {'video': video})

# Download a video (only accessible to logged-in users with a valid password)
@login_required
def download_video(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    if request.method == 'POST':
        password = request.POST.get('download_password')
        if password == 'admin_given_password':  # Replace with the actual logic
            response = HttpResponse(video.video_file, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{video.video_file.name}"'
            return response
    return render(request, 'videos/download_video.html', {'video': video})


def logout_view(request):
    logout(request)
    return redirect('login')