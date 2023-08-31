from django.urls import path
from .views import *

app_name = 'essays'

urlpatterns = [
    path('essay-submission/<int:lesson_id>/', EssaySubmissionView.as_view(), name='essay_submission'),
    path('check_essay/<int:essay_submission_id>/', CheckEssayView.as_view(), name='check_essay'),
]