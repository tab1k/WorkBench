from django.contrib import admin
from tests.models import Test, TestChoice, TestResult


class TestAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'question')
    list_filter = ('lesson',)
    search_fields = ('question', 'lesson__title')


class TestChoiceAdmin(admin.ModelAdmin):
    list_display = ('test', 'choice', 'is_correct')
    list_filter = ('test__lesson',)
    search_fields = ('choice', 'test__question', 'test__lesson__title')


class TestResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'score', 'attempts')
    list_filter = ('student','lesson')
    search_fields = ('student', 'lesson', 'score', 'attempts')


admin.site.register(Test, TestAdmin)
admin.site.register(TestChoice, TestChoiceAdmin)
admin.site.register(TestResult,TestResultAdmin)
