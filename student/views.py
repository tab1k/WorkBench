from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import ListView
from comments.models import Comment
from courses.models import *

@login_required(login_url='users:login')
def dashboard_view(request):
    student = request.user
    course_type = CourseType.objects.filter(courses__students=student).distinct()
    courses = Course.objects.filter(students=student)

    # Получите уведомления, связанные с курсами пользователя
    notifications = Notification.objects.filter(course__in=courses).order_by('-timestamp')

    # Получите сообщения куратора только для текущего студента
    curator_comments = Comment.objects.filter(lesson__module__course__in=courses, is_student_comment=False,
                                              user=student)
    if request.user.role == 'student':
        return render(request, 'users/student/mainAfterSignupStudent.html', {
            'courses': courses,
            'course_type': course_type,
            'student': student,
            'notifications': notifications,
            'curator_comments': curator_comments  # Передача сообщений куратора в контекст
        })
    else:
        return redirect('users:login')





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



from django.shortcuts import render, get_object_or_404, redirect
from courses.models import Lesson

def show_previous_lesson(request, lesson_id):
    current_lesson = get_object_or_404(Lesson, pk=lesson_id)
    all_lessons = Lesson.objects.filter(module=current_lesson.module).order_by('id')

    current_lesson_index = None
    for index, lesson in enumerate(all_lessons):
        if lesson.id == current_lesson.id:
            current_lesson_index = index
            break

    if current_lesson_index is not None and current_lesson_index > 0:
        previous_lesson = all_lessons[current_lesson_index - 1]
        return redirect('users:student:previous_lesson', lesson_id=previous_lesson.id)
    else:
        return redirect('users:student:courses:lesson_view', lesson_id=current_lesson.id)


def show_next_lesson(request, lesson_id):
    current_lesson = get_object_or_404(Lesson, pk=lesson_id)
    all_lessons = Lesson.objects.filter(module=current_lesson.module).order_by('id')

    current_lesson_index = None
    for index, lesson in enumerate(all_lessons):
        if lesson.id == current_lesson.id:
            current_lesson_index = index
            break

    if current_lesson_index is not None and current_lesson_index < len(all_lessons) - 1:
        next_lesson = all_lessons[current_lesson_index + 1]
        return redirect('users:student:next_lesson', lesson_id=next_lesson.id)
    else:
        return redirect('users:student:courses:lesson_view', lesson_id=current_lesson.id)


class StudentNotificationListView(ListView):
    model = Notification
    template_name = 'users/student/student_notifications.html'
    context_object_name = 'notifications'
    ordering = ['-timestamp']

    def get_queryset(self):
        student = self.request.user
        return Notification.objects.filter(course__students__in=[student])




from django.views.generic import ListView
from comments.models import Comment

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


from django.shortcuts import redirect, get_object_or_404
from django.views import View

class SendResponseView(View):
    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        student_response = request.POST.get('student_response')
        if student_response:
            comment.student_response = student_response
            comment.save()
        return redirect('users:student:student_messages')  # Перенаправьте, куда вам нужно




class LogoutView(View):
    def get(self, request):
        logout(request)
        # Дополнительный код, например, перенаправление на другую страницу
        return redirect('users:login')  # Замените 'home' на имя URL-шаблона для перенаправления на нужную страницу
