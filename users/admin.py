from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from users.models import *


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'stream', 'username', 'email', 'first_name', 'last_name', 'role', 'display_image')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'image')}),
        ('Разрешения', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Последний вход', {'fields': ('last_login', 'date_joined')}),
        ('Роль', {'fields': ('role', 'stream',)}),
    )
    readonly_fields = ('display_image',)

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return None

    display_image.short_description = 'Profile Image'


class StreamAdmin(admin.ModelAdmin):
    list_display = ('id', 'number')



admin.site.register(Stream, StreamAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(StudentOrderHistory)




