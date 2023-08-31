from django.contrib import admin
from courses.models import Course, Module, Lesson, CourseType, Notification


class CourseTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'time')  # Замените 'duration' и 'category' на существующие поля модели CourseType



class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'course_type')
    search_fields = ('title', 'course_type')


class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')


class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'video')
    list_filter = ('module__course',)
    search_fields = ('title', 'module__title', 'module__course__title')


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('course', 'message', 'file', 'timestamp', 'read')
    list_filter = ('course', 'message', 'file', 'timestamp', 'read')
    search_fields = ('course', 'message', 'file', 'timestamp', 'read')



admin.site.register(Notification, NotificationAdmin)
admin.site.register(CourseType, CourseTypeAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Lesson, LessonAdmin)

