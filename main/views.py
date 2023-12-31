from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .forms import *
from .utils import generate_thumbnail
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import *
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.db import IntegrityError
from django.db import transaction

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

def recommended_videos(request):
    user = request.user

    # Get the user's viewing history
    user_history = UserHistory.objects.filter(user=user)

    # Extract video IDs from the user's viewing history
    video_ids = [history.video.id for history in user_history]

    # Get videos watched by the user and exclude them from recommendations
    watched_videos = Video.objects.filter(id__in=video_ids)
    
    # Get recommended videos (exclude watched videos)
    recommended_videos = Video.objects.exclude(id__in=video_ids)

    return render(request, 'registration/recommended_videos.html', {'watched_videos': watched_videos, 'recommended_videos': recommended_videos})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')

    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            
            try:
                with transaction.atomic():
                    # Try to get the existing profile or create a new one
                    profile, created = UserProfile.objects.get_or_create(user=user)
                    if not created:
                        # Update the existing profile
                        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
                        profile_form.save()

                    # Save the profile (either new or updated)
                    profile = profile_form.save(commit=False)
                    profile.user = user
                    profile.save()

                    login(request, user)
                    messages.success(request, 'Account created successfully!')
                    return redirect('home')

            except IntegrityError:
                # Handle the case where a profile was created concurrently by another request
                messages.error(request, 'There was an issue creating your account. Please try again.')

        else:
            messages.error(request, 'Username is taken')

    else:
        form = SignUpForm()
        profile_form = UserProfileForm()

    return render(request, 'registration/signup.html', {'form': form, 'profile_form': profile_form})

@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.save()

            # If a custom thumbnail is provided, use it; otherwise, generate a thumbnail from the video
            if video.custom_thumbnail:
                video.thumbnail = video.custom_thumbnail
            else:
                # Generate and save thumbnail
                thumbnail_path = f'media/thumbnails/{video.id}.jpg'
                generate_thumbnail(video.file.path, thumbnail_path)
                video.thumbnail = thumbnail_path

            video.save()

            return redirect('home')  # Update with your home view name
    else:
        form = VideoForm()
    return render(request, 'registration/upload_video.html', {'form': form})

def home(request):
    user = request.user

    # Get the list of users the logged-in user is following
    following_users = []
    if user.is_authenticated:
        following_users = UserFollowing.objects.filter(user=user).values_list('followed_user__username', flat=True)

    short_videos = Video.objects.filter(category='short')
    long_videos = Video.objects.filter(category='long')
    return render(request, 'registration/home.html', {'short_videos': short_videos, 'long_videos': long_videos, 'following_users': following_users})

def account_page(request, username):
    user = get_object_or_404(User, username=username)

    uploaded_videos = Video.objects.filter(user=user)
    short_videos = Video.objects.filter(user=user, category='short')
    # liked_videos = user.userprofile.liked_videos.all()

    return render(request, 'registration/account.html', {'user': user, 'uploaded_videos': uploaded_videos, 'short_videos': short_videos }) #'liked_videos': liked_videos

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    user = request.user

    # Check if the user is not trying to follow themselves
    if user != user_to_follow:
        # Check if the user is not already following the target user
        if not UserFollowing.objects.filter(user=user, followed_user=user_to_follow).exists():
            # Create a new UserFollowing entry
            UserFollowing.objects.create(user=user, followed_user=user_to_follow)

            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'already_following'})
    else:
        return JsonResponse({'status': 'cannot_follow_yourself'})

def view_video(request, video_id):
    videos = get_object_or_404(Video, id=video_id)
    context = {'video': videos}
    return render(request, 'registration/view_video.html', context)

@login_required
def notifications(request):
    user = request.user

    # Get unread notifications for the user
    unread_notifications = Notification.objects.filter(user=user, is_read=False)

    # Mark unread notifications as read
    unread_notifications.update(is_read=True)

    return render(request, 'registration/notifications.html', {'notifications': unread_notifications})

@login_required
def user_settings(request):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid():
            user_form.save()

            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('user_settings')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserProfileForm(instance=user_profile)

    return render(request, 'registration/user_settings.html', {'user_form': user_form})

def short_video_scroll_page(request, video_id=None):
    short_videos = Video.objects.filter(category='short')

    if video_id:
        clicked_video = get_object_or_404(Video, id=video_id, category='short')
    else:
        clicked_video = short_videos.first()

    return render(request, 'registration/shorts.html', {'short_videos': short_videos, 'clicked_video': clicked_video})