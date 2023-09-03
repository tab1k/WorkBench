from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views import View
from courses.models import Course
from users.models import User
from django.views.generic import DetailView
from django.utils.timezone import localtime
from django.shortcuts import get_object_or_404


class Profile(View):
    def get(self, request):
        # Получите аутентифицированного пользователя
        authenticated_user = request.user

        courses = Course.objects.all()

        context = {
            'authenticated_user': authenticated_user,
            'courses': courses
        }

        if authenticated_user.role == 'student':
            courses = Course.objects.filter(students=authenticated_user)
            return render(request, 'student/starter-kit/user_profile.html', {'context': context, 'courses': courses})
        elif authenticated_user.role == 'curator':
            courses = Course.objects.filter(curators=authenticated_user)
            return render(request, 'curator/starter-kit/profile.html', {'context': context, 'courses': courses})
        elif authenticated_user.role == 'admin':
            courses = Course.objects.all()
            return render(request, 'admin/starter-kit/profile.html', {'context': context, 'courses': courses})
        else:
            return render(request, 'users/404.html')





class ProfileView(View):
    template_name_curator = 'users/curator/profileSettingsAdmin.html'
    template_name_admin = 'admin/starter-kit/user_profile.html'

    def get(self, request, pk):
        # Check if the user is allowed to access this view based on their role
        if request.user.role not in ['curator', 'admin']:
            return HttpResponseForbidden("У вас нет доступа к этой странице.")

        # Fetch the specific student object based on the provided 'pk' parameter
        student = get_object_or_404(User, pk=pk, role='student')
        courses = student.courses.all()
        email = student.email

        context = {
            'student': student,
            'courses': courses,
            'email': email,
        }

        # Render the appropriate template based on the user's role
        if request.user.role == 'curator':
            return render(request, self.template_name_curator, context)
        elif request.user.role == 'admin':
            return render(request, self.template_name_admin, context)












