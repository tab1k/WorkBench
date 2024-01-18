from django.shortcuts import render
from django.views.generic import ListView, DetailView

from blog.models import Post


class BlogListView(ListView):
    model = Post
    template_name = 'student/blog/blog.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter().order_by('-date')


class BlogDetailView(DetailView):
    model = Post
    template_name = 'student/blog/blog_detail.html'
    context_object_name = ''

