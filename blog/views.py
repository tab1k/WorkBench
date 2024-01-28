from django.contrib.postgres.search import SearchVector, SearchQuery
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from blog.models import Post


class BlogListView(ListView):
    model = Post
    template_name = 'student/blog/blog.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.all().order_by('-date')

        # Filter by hashtag
        hashtag_filter = self.request.GET.get('hashtag', '')
        if hashtag_filter:
            queryset = queryset.filter(hashtag=hashtag_filter)

        # Search
        search_query = self.request.GET.get('search', '')
        if search_query:
            search_condition = Q()
            for field in ['title', 'author', 'body', 'hashtag']:
                search_condition |= Q(**{f'{field}__icontains': search_query})

            queryset = queryset.filter(search_condition)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pagination
        paginator = Paginator(context['posts'], self.paginate_by)
        page = self.request.GET.get('page')

        try:
            context['posts'] = paginator.page(page)
        except PageNotAnInteger:
            context['posts'] = paginator.page(1)
        except EmptyPage:
            context['posts'] = paginator.page(paginator.num_pages)

        return context


class BlogDetailView(DetailView):
    model = Post
    template_name = 'student/blog/blog_detail.html'
    context_object_name = 'detail'

