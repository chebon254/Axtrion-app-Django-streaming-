from django.contrib import admin
from .models import UserProfile, UserFollowing, Video,Comment, UserHistory, Notification

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'bio')
    search_fields = ('user__username', 'full_name', 'bio')

admin.site.register(UserProfile, UserProfileAdmin)

class UserFollowingAdmin(admin.ModelAdmin):
    list_display = ('user', 'followed_user')
    search_fields = ('user__username', 'followed_user__username')

admin.site.register(UserFollowing, UserFollowingAdmin)

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'upload_date', 'user')
    search_fields = ('title', 'description', 'user__username')
    list_filter = ('upload_date',)

admin.site.register(Video, VideoAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'text', 'created_at')
    search_fields = ('user__username', 'video__title', 'text')
    list_filter = ('created_at',)

admin.site.register(Comment, CommentAdmin)

class UserHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'timestamp')
    search_fields = ('user__username', 'video__title')
    list_filter = ('timestamp',)

admin.site.register(UserHistory, UserHistoryAdmin)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'is_read')
    search_fields = ('user__username', 'message')
    list_filter = ('created_at', 'is_read')

admin.site.register(Notification, NotificationAdmin)
