from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('upload/', upload_video, name='upload_video'),
    path('', home, name='home'),
    path('video/<int:video_id>/', view_video, name='view_video'),
    path('recommended_videos/', recommended_videos, name='recommended_videos'),
    path('follow_user/<str:username>/', follow_user, name='follow_user'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('notifications/', notifications, name='notifications'),
    path('user_settings/', user_settings, name='user_settings'),
    path('account/<str:username>/', account_page, name='account_page'),
     path('shorts/', short_video_scroll_page, name='short_video_scroll_page'),
    path('shorts/<int:video_id>/', short_video_scroll_page, name='short_video_scroll_page_with_id'),
]