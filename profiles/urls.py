from django.urls import path
from profiles.views import Profile, ProfileView

app_name = 'profiles'

urlpatterns = [
    path('', Profile.as_view(), name='profile'),
    path('<int:pk>/', ProfileView.as_view(), name='profile_view'),
    # Другие URL-шаблоны вашего приложения с курсами...
]
