from django.contrib import admin
from django.utils.html import format_html
from .models import Post, Comment, FollowUser, LikePost


class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'preview', 'is_published']

    def preview(self, obj):
        return format_html(f'<img height=50 width=50 src={obj.image.url}>')


class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author']


class LikeAdmin(admin.ModelAdmin):
    list_display = ['post', 'author']


class FollowUserAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(LikePost, LikeAdmin)
admin.site.register(FollowUser, FollowUserAdmin)
