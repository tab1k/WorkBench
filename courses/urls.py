from django.urls import path, include
from .views import *

app_name = 'courses'

urlpatterns = [
    path('by_type/<int:type_id>/', CoursesByType.as_view(), name='courses_by_type'),
    path('', Courses.as_view(), name='courses'),
    path('detail/<int:course_id>/', CourseDetailView.as_view(), name='detail'),
    path('module<int:pk>/', Modules.as_view(), name='modules'),
    path('module/<int:module_id>/lessons/', LessonsByModule.as_view(), name='lessons_by_module'),
    path('lesson/view/<int:lesson_id>/', LessonView.as_view(), name='lesson_view'),
    path('lesson/answers/', AnswersView.as_view(), name='answers_view'),

    path('students/<int:student_id>/progress/', StudentProgressView.as_view(), name='student_progress'),
    path('passed-students/', PassedStudentsView.as_view(), name='passed_students'),
    path('generate-certificate/<int:student_id>/', CertificateView.as_view(), name='generate_certificate'),

    path('tests', include('tests.urls')),

]

