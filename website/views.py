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


class ContactsView(View):
    template_name = 'website/contacts.html'

    def get(self, request):
        return render(request, self.template_name)


class Collaboration(View):
    template_name = 'website/collaboration.html'

    def get(self, request):
        return render(request, self.template_name)


class CoursesView(View):
    template_name = 'website/courses.html'

    def get(self, request):
        return render(request, self.template_name)


class SignInView(View):
    template_name = 'signin.html'

    def get(self, request):
        return render(request, self.template_name)
