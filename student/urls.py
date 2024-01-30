from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import path, include
from student.views import *

app_name = 'student'

urlpatterns = [
    path('courses/', include('courses.urls')),
    path('schedule/', include('schedule.urls')),
    path('dashboard/', StudentDashboardView.as_view(), name='dashboard'),
    path('profile/', StudentProfileView.as_view(), name='profile'),
    path('security/', CustomPasswordChangeView.as_view(), name='security'),
    path('order-history/', StudentOrderHistoryView.as_view(), name='order-history'),
    path('send_response/<int:comment_id>/', SendResponseView.as_view(), name='send_response'),
    path('student_notifications', StudentNotificationListView.as_view(), name='student_notifications'),
    path('lesson/<int:pk>/previous/', PreviousLessonRedirectView.as_view(), name='previous_lesson_redirect'),
    path('lesson/<int:pk>/next/', NextLessonRedirectView.as_view(), name='next_lesson_redirect'),
    path('logout/', LogoutView.as_view(), name='logout'),

]


