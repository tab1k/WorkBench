from django.shortcuts import render
from django.views import View


class WebSiteView(View):
    template_name = 'website/index.html'

    def get(self, request):
        return render(request, self.template_name)


class AboutView(View):
    template_name = 'website/about.html'

    def get(self, request):
        return render(request, self.template_name)
