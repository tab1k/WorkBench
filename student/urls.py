from django.urls import path, include
from student.views import *

app_name = 'student'

urlpatterns = [
    path('', dashboard_view, name='student'),
    path('previous/<int:lesson_id>/', show_previous_lesson, name='previous_lesson'),
    path('next/<int:lesson_id>/', show_next_lesson, name='next_lesson'),
    path('courses/', include('courses.urls')),
    path('profile/', include('profiles.urls', namespace='profile')),
    path('schedule/', include('schedule.urls')),
    path('notifications/', StudentNotificationListView.as_view(), name='student_notifications'),
    path('messages/', StudentMessagesListView.as_view(), name='student_messages'),
    path('send_response/<int:comment_id>/', SendResponseView.as_view(), name='send_response'),
    path('student_notifications', StudentNotificationListView.as_view(), name='student_notifications'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Другие пути для пользователей...
]


