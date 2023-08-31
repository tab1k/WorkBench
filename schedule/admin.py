from django.contrib import admin
from schedule.models import Schedule


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('course', 'start_date', 'end_date', 'weekdays', 'start_time', 'end_time')
    list_filter = ('course', 'weekdays')
    search_fields = ('course__title', 'weekdays')


admin.site.register(Schedule, ScheduleAdmin)
