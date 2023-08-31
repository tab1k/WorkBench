from django.contrib import admin
from comments.models import Comment
from courses.models import Notification


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'curator_response','curator', 'lesson', 'user', 'timestamp')
    list_filter = ('lesson', 'user', 'curator' ,'timestamp')
    search_fields = ('text', 'lesson__title', 'user__username', 'curator', 'timestamp')

admin.site.register(Comment, CommentAdmin)
