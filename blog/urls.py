from django.urls import path
from blog.views import *

app_name = 'blog'

urlpatterns = [
    path('', BlogListView.as_view(), name='blog'),
    path('create_post/', CreatePostView.as_view(), name='create_post'),
    path('detail/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
]


