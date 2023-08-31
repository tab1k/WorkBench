from django.urls import path
from website.views import *

app_name = 'website'

urlpatterns = [
    path('', WebSiteView.as_view(), name='home'),
    path('about', AboutView.as_view(), name='about'),
    path('courses', CoursesView.as_view(), name='courses'),
    path('contacts', ContactsView.as_view(), name='contacts'),
    path('collaboration', Collaboration.as_view(), name='collaboration'),

]