from django.contrib import admin
from django.utils.html import format_html
from .models import MyUser


class MyUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'image']

    def username(self, obj):
        return obj.user.username

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    def email(self, obj):
        return obj.user.email

    def image(self, obj):
        if obj.profile_picture:
            return format_html(f'<img height=50 width=50 src={obj.profile_picture.url}>')


admin.site.register(MyUser, MyUserAdmin)
