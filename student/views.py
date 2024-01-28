from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView, DetailView, UpdateView, RedirectView
from blog.models import Post
from courses.models import *
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import ListView
from comments.models import Comment
from django.shortcuts import render
from courses.models import Lesson
from student.forms import StudentCustomProfileForm
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from users.models import StudentOrderHistory


class StudentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'student/starter-kit/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.request.user
        context['posts'] = Post.objects.filter().order_by('-date')[:3]
        return context


class StudentProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'student/profile/user_profile.html'
    context_object_name = 'user'
    success_url = reverse_lazy('users:student:dashboard')
    form_class = StudentCustomProfileForm

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        # Сохранение изображения профиля
        if 'image' in form.cleaned_data:
            self.object.image = form.cleaned_data['image']
            self.object.save()
        return response

    def form_invalid(self, form):
        print("Form is invalid!")
        print(form.errors)
        return super().form_invalid(form)


@method_decorator([login_required, never_cache], name='dispatch')
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'student/profile/security.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class StudentOrderHistoryView(LoginRequiredMixin, ListView):
    model = StudentOrderHistory
    template_name = 'student/profile/order-history.html'
    context_object_name = 'orders'

    def get_queryset(self):
        # Возвращаем все объекты StudentOrderHistory, связанные с текущим пользователем
        return StudentOrderHistory.objects.filter(student=self.request.user)


class StudentNotificationListView(ListView):
    model = Notification
    template_name = 'users/student/student_notifications.html'
    context_object_name = 'notifications'
    ordering = ['-timestamp']

    def get_queryset(self):
        student = self.request.user
        return Notification.objects.filter(course__students__in=[student])


class StudentMessagesListView(ListView):
    template_name = 'users/student/student_messages.html'

    def get(self, request):

        student = request.user
        course_type = CourseType.objects.filter(courses__students=student).distinct()
        courses = Course.objects.filter(students=student)


        # Получите сообщения куратора только для текущего студента
        curator_comments = Comment.objects.filter(lesson__module__course__in=courses, is_student_comment=False,
                                                  user=student)

        context = {
            'courses': courses,
            'course_type': course_type,
            'student': student,
            'curator_comments': curator_comments
        }
        return render(request, self.template_name, context=context)


class SendResponseView(View):
    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        student_response = request.POST.get('student_response')
        if student_response:
            comment.student_response = student_response
            comment.save()
        return redirect('users:student:student_messages')  # Перенаправьте, куда вам нужно


class StudentNotificationListView(ListView):

    def get(self, request):
        student = request.user
        course_type = CourseType.objects.filter(courses__students=student).distinct()
        courses = Course.objects.filter(students=student)

        # Получите уведомления, связанные с курсами пользователя
        notifications = Notification.objects.filter(course__in=courses).order_by('-timestamp')

        # Получите сообщения куратора только для текущего студента
        curator_comments = Comment.objects.filter(lesson__module__course__in=courses, is_student_comment=False,
                                                  user=student)
        if request.user.role == 'student':
            return render(request, 'student/starter-kit/student_notifications.html', {
                'courses': courses,
                'course_type': course_type,
                'student': student,
                'notifications': notifications,
                'curator_comments': curator_comments  # Передача сообщений куратора в контекст
            })
        else:
            return redirect('users:login')


class PreviousLessonRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        current_lesson = get_object_or_404(Lesson, pk=self.kwargs['pk'])
        all_lessons = Lesson.objects.filter(module=current_lesson.module).order_by('order')

        current_lesson_index = None
        for index, lesson in enumerate(all_lessons):
            if lesson.id == current_lesson.id:
                current_lesson_index = index
                break

        if current_lesson_index is not None and current_lesson_index > 0:
            previous_lesson = all_lessons[current_lesson_index - 1]
            return previous_lesson.get_absolute_url()  # Замените на ваш метод получения URL урока
        else:
            return current_lesson.get_absolute_url()


class NextLessonRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        current_lesson = get_object_or_404(Lesson, pk=self.kwargs['pk'])
        all_lessons = Lesson.objects.filter(module=current_lesson.module).order_by('order')

        current_lesson_index = None
        for index, lesson in enumerate(all_lessons):
            if lesson.id == current_lesson.id:
                current_lesson_index = index
                break

        if current_lesson_index is not None and current_lesson_index < len(all_lessons) - 1:
            next_lesson = all_lessons[current_lesson_index + 1]
            return next_lesson.get_absolute_url()  # Замените на ваш метод получения URL урока
        else:
            return current_lesson.get_absolute_url()


class LogoutView(View):
    def get(self, request):
        logout(request)
        # Дополнительный код, например, перенаправление на другую страницу
        return redirect('users:login')  # Замените 'home' на имя URL-шаблона для перенаправления на нужную страницу
