from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from django.core.mail import send_mail
from users.forms import LoginForm
from users.models import User


def login_view(request):
    error = None

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:
                    if user.role == 'curator':
                        return redirect('users:curator:curator')
                    elif user.role == 'admin':
                        return redirect('users:admin:administrator')
                else:
                    return redirect('users:student:student')
            else:
                error = 'Не правильные данные!'
    else:
        form = LoginForm()

    return render(request, 'signin.html', {'form': form, 'error': error})


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


