from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('upload/', upload_video, name='upload_video'),
    path('', home, name='home'),
    path('video/<int:video_id>/', view_video, name='view_video'),
    path('send_gift/<int:gift_id>/', send_gift, name='send_gift'),
    path('send_ar_gift/<int:ar_gift_id>/', send_ar_gift, name='send_ar_gift'),
    path('send_like/', send_like, name='send_like'),
    path('live_stream/', live_stream, name='live_stream'),
    path('post_comment/<int:video_id>/', post_comment, name='post_comment'),
    path('recommended_videos/', recommended_videos, name='recommended_videos'),
    path('follow_user/<str:username>/', follow_user, name='follow_user'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('notifications/', notifications, name='notifications'),
    path('user_settings/', user_settings, name='user_settings'),
]