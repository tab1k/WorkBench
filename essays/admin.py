from django.contrib import admin
from essays.models import Essay, EssaySubmission


class EssayAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'text')
    list_filter = ('lesson',)
    search_fields = ('text', 'lesson__title')


class EssaySubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'essay_text', 'files', 'is_passed')
    list_filter = ('student','lesson', 'is_passed')
    search_fields = ('student','lesson', 'is_passed')


admin.site.register(Essay, EssayAdmin)
admin.site.register(EssaySubmission, EssaySubmissionAdmin)
