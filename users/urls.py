from django.conf.urls.static import static
from django.urls import path, include
from users.views import *
from django.conf import settings

app_name = 'users'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('administrator/', include('administrator.urls', namespace='administrator')),
    path('student/', include('student.urls', namespace='student')),
    path('curator/', include('curator.urls', namespace='curator')),
    path('back-to-home/', back_to_home, name='back_to_home'),
    path('open-website/', open_website, name='open_website'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


