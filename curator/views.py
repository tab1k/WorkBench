from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView
from administrator.forms import NotificationForm
from courses.models import Course, CourseType, Notification
from website.models import Contact
from users.models import User, Stream
from django.contrib import messages


@login_required(login_url='users:login')
def curator_view(request):
    curator = request.user
    if request.user.role == 'curator':

        # Получите список курсов, связанных с текущим куратором
        courses = Course.objects.filter(curators=curator)
        courses_type = CourseType.objects.all()

        # Получите список заявок
        contacts = Contact.objects.all().order_by('-timestamp')  # Замените на необходимый способ получения заявок

        # Отметьте все заявки как прочитанные
        Contact.objects.all().update(read=True)

        # Получите количество заявок
        contact_count = Contact.objects.count()

        # Получите список уведомлений
        notifications = Notification.objects.all().order_by('-timestamp')  # Замените на необходимый способ получения уведомлений

        return render(request, 'users/curator/mainAfterSignUpСurator.html',
                      {'courses': courses, 'courses_type': courses_type, 'curator': curator, 'contacts': contacts,
                       'contact_count': contact_count, 'notifications': notifications})
    else:
        return redirect('users:login')


class StudentsCheckAdmin(View):
    template_name = 'users/curator/student.html'

    def get(self, request):
        stream_id = request.GET.get('stream')
        streams = Stream.objects.all()
        selected_stream = None
        students = User.objects.filter(role='student')

        if stream_id:
            selected_stream = get_object_or_404(Stream, id=stream_id)
            students = students.filter(stream=selected_stream)

        return render(request, self.template_name, {
            'students': students,
            'streams': streams,
            'selected_stream': selected_stream
        })

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
        return redirect('users:curator:previous_lesson', lesson_id=previous_lesson.id)
    else:
        return redirect('users:curator:courses:lesson_view', lesson_id=current_lesson.id)


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
        return redirect('users:curator:next_lesson', lesson_id=next_lesson.id)
    else:
        return redirect('users:curator:courses:lesson_view', lesson_id=current_lesson.id)

class StreamListView(ListView):
    model = Stream
    template_name = 'users/curator/streams.html'
    context_object_name = 'streams'


class ContactListView(ListView):
    model = Contact
    template_name = 'users/curator/applications.html'
    context_object_name = 'contacts'
    paginate_by = 10

    def get_queryset(self):
        contacts = Contact.objects.all().order_by('-timestamp')

        # Отметьте заявки как прочитанные
        for contact in contacts:
            if not contact.read:
                contact.read = True
                contact.save()

        return contacts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_count'] = Contact.objects.count()
        return context


from datetime import datetime, timedelta
from django.utils import timezone

class NotificationListView(ListView):
    model = Notification
    template_name = 'users/curator/view_notifications.html'
    context_object_name = 'notifications'
    ordering = ['-timestamp']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()  # Замените на ваш запрос для получения списка курсов
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        course_id = self.request.GET.get('course_id')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if course_id:
            queryset = queryset.filter(course_id=course_id)

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
            queryset = queryset.filter(timestamp__gte=start_date)

        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').replace(tzinfo=timezone.utc) + timedelta(days=1)
            queryset = queryset.filter(timestamp__lt=end_date)

        return queryset


from django.db.models import Q

class SearchView(View):
    template_name = 'users/curator/search_results.html'

    def get(self, request):
        query = request.GET.get('q')
        courses = Course.objects.filter(title__icontains=query) if query else []
        students = User.objects.filter(Q(role='student'),
                                       Q(username__icontains=query) | Q(first_name__icontains=query) | Q(
                                           last_name__icontains=query)) if query else []
        notifications = Notification.objects.filter(message__icontains=query) if query else []

        return render(request, self.template_name,
                      {'courses': courses, 'students': students, 'notifications': notifications})


class NotificationCreateView(CreateView):
    model = Notification
    form_class = NotificationForm
    template_name = 'users/curator/create_notification.html'
    success_url = reverse_lazy('users:admin:create_notification')  # Используем 'admin:create_notification' из app_name

    def form_valid(self, form):
        messages.success(self.request, 'Уведомление успешно создано.')
        return super().form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        # Дополнительный код, например, перенаправление на другую страницу
        return redirect('users:login')  # Замените 'home' на имя URL-шаблона для перенаправления на нужную страницу



