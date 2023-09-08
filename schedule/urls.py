from django.urls import path, include
from schedule.views import *

app_name = 'schedule'

urlpatterns = [
    path('student-schedule/', StudentScheduleView.as_view(), name='student_schedule'),
    path('add_schedule/', AddScheduleView.as_view(), name='add_schedule'),
]
