from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse
from django.urls import reverse_lazy


class UserLoginView(LoginView):
    template_name = 'signin.html'
    success_url = reverse_lazy('users:student:dashboard')

    def form_valid(self, form):
        super().form_valid(form)
        user = self.request.user
        if user.is_staff:
            if user.role == 'curator':
                return redirect('users:curator:dashboard')
            elif user.role == 'admin':
                return redirect('users:admin:administrator')
        else:
            return redirect(self.success_url)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form, 'error': 'Не правильные данные!'})




# BACK_TO_HOME

def back_to_home(request):
    if request.user.is_authenticated:
        if request.user.role == 'admin':
            return redirect('users:admin:admin')  # Замените 'admin_home' на имя URL-шаблона главной страницы администратора
        elif request.user.role == 'curator':
            return redirect('users:curator:curator')  # Замените 'curator_home' на имя URL-шаблона главной страницы куратора
        else:
            return redirect('users:student:student')  # Замените 'student_home' на имя URL-шаблона главной страницы студента
    else:
        return redirect('login')  # Замените 'login' на имя URL-шаблона страницы входа


# ERROR - 404

def error_404_view(request, exception):
    return render(request, 'website/404.html', status=404)


def open_website(request):
    # Здесь вы можете указать URL вашего сайта
    website_url = "http://127.0.0.1:8000"  # Замените на ваш URL
    return redirect(website_url)


