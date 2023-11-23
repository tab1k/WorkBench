from django.urls import path
from website.views import *

app_name = 'website'

urlpatterns = [
    path('', WebSiteView.as_view(), name='home'),
    path('about', AboutView.as_view(), name='about'),
    path('courses', CoursesView.as_view(), name='courses'),
    path('contacts', ContactsView.as_view(), name='contacts'),
    path('collaboration', Collaboration.as_view(), name='collaboration'),
    path('full-stack', FullStackView.as_view(), name='full-stack'),
    path('html-css', HtmlCssView.as_view(), name='html-css'),
    path('python-django', PythonDjangoView.as_view(), name='python-django'),
    path('computer-literacy', ComputerLiteracyView.as_view(), name='computer-literacy'),
    path('terms', TermsView.as_view(), name='terms'),
    path('privacy', PrivacyView.as_view(), name='privacy'),
]