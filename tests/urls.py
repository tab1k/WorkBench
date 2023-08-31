from django.urls import path
from .views import *

app_name = 'tests'

urlpatterns = [
    path('take-test/<int:lesson_id>/', TakeTestView.as_view(), name='take_test'),
    path('test_result/<int:lesson_id>/', TestResultView.as_view(), name='test_result'),
]