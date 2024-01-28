from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.views.generic import ListView, TemplateView, DetailView, RedirectView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from blog.models import Post
from .forms import NotificationForm, AdminCustomProfileForm, StudentCustomProfileForm
from website.models import Contact
from users.models import User, Stream
from django.contrib.auth.models import Group
from django.views import View
from courses.models import Notification
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.views import View
from courses.models import *
from .forms import *
from datetime import datetime, timedelta
from django.utils import timezone


class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'admin/starter-kit/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter().order_by('-date')[:3]
        context['notifications'] = Notification.objects.all().order_by('-timestamp')
        context['contacts'] = Contact.objects.all().order_by('-timestamp')
        return context


class StudentProfileDetailView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'admin/starter-kit/student_profile.html'
    context_object_name = 'student'
    success_url = reverse_lazy('users:admin:dashboard')
    form_class = StudentCustomProfileForm

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


class StudentProfileDeleteView(UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'admin/starter-kit/student_confirm_delete.html'

    def test_func(self):
        return self.request.user.role == 'admin'

    def get_success_url(self):
        return reverse_lazy('users:admin:dashboard')

    def delete(self, request, *args, **kwargs):
        student = get_object_or_404(User, id=self.kwargs['pk'], role='student')

        if self.request.user.role == 'admin':
            student.delete()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseForbidden("У вас нет разрешения на удаление студента.")


class AdminProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'admin/starter-kit/user_profile.html'
    context_object_name = 'user'
    success_url = reverse_lazy('users:admin:dashboard')
    form_class = AdminCustomProfileForm

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


class StudentsCheckAdmin(View):
    template_name = 'admin/starter-kit/students.html'
    items_per_page = 10  # Количество студентов на странице

    def get(self, request):
        stream_id = request.GET.get('stream')
        streams = Stream.objects.all()
        selected_stream = None
        students = User.objects.filter(role='student')

        if stream_id:
            selected_stream = get_object_or_404(Stream, id=stream_id)
            students = students.filter(stream=selected_stream)

        # Создаем объект пагинатора и получаем текущую страницу из параметра запроса
        paginator = Paginator(students, self.items_per_page)
        page_number = request.GET.get('page')

        # Получаем студентов для текущей страницы
        students_page = paginator.get_page(page_number)

        return render(request, self.template_name, {
            'students': students_page,
            'streams': streams,
            'selected_stream': selected_stream
        })


class CuratorCheckAdmin(View):
    template_name = 'admin/starter-kit/curators.html'

    def get(self, request):
        curators = User.objects.filter(role='curator')

        # Применяем пагинацию
        page = request.GET.get('page', 1)
        paginator = Paginator(curators, 10)  # Разбиваем на страницы по 10 элементов
        try:
            curators = paginator.page(page)
        except PageNotAnInteger:
            curators = paginator.page(1)
        except EmptyPage:
            curators = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'curators': curators})


class AddStudent(View):
    template_name = 'admin/starter-kit/addstudent.html'

    def get(self, request):
        form = StudentForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = StudentForm(request.POST)
        if form.is_valid():
            User = get_user_model()
            student = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                role='student'
            )
            courses = form.cleaned_data['courses']
            student.courses.set(courses)

            # Добавляем студента в группу 'Студенты'
            student_group = Group.objects.get(name='Студенты')
            student.groups.add(student_group)

            return render(request, 'admin/starter-kit/students.html', {'student': student})
        return render(request, self.template_name, {'form': form})


class AddCurator(View):
    template_name = 'admin/starter-kit/addcoach.html'

    def get(self, request):
        form = CuratorForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CuratorForm(request.POST)
        if form.is_valid():
            User = get_user_model()
            curator = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                role='curator'
            )
            courses = form.cleaned_data['courses']
            curator.courses.set(courses)

            # Добавляем куратора в группу 'Кураторы'
            curator_group = Group.objects.get(name='Кураторы')
            curator.groups.add(curator_group)

            return render(request, 'admin/starter-kit/curators.html', {'curator': curator})
        return render(request, self.template_name, {'form': form})


class SearchStudentsView(View):
    def get_template_names(self):
        # Получаем текущего пользователя
        user = self.request.user

        # Если поле role у пользователя равно "admin", используем шаблон для администратора
        if user.role == 'admin':
            return ['admin/starter-kit/students.html']
        # Иначе используем шаблон для куратора
        else:
            return ['curator/starter-kit/students.html']

    def get(self, request):
        query = request.GET.get('q')
        stream = request.GET.get('stream')

        students = User.objects.filter(
            role='student',
            first_name__icontains=query,
        )

        if stream:
            students = students.filter(stream__number=int(stream))

        context = {'students': students}
        return render(request, self.get_template_names(), context)


class SearchCuratorsView(View):
    template_name = 'admin/starter-kit/curators.html'

    def get(self, request):
        query = request.GET.get('q')
        stream = request.GET.get('stream')

        curators = User.objects.filter(role='curator')

        if query:
            curators = curators.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )

        if stream:
            try:
                stream_number = int(stream)
                curators = curators.filter(stream__number=stream_number)
            except ValueError:
                return HttpResponseBadRequest("Неверный формат значения 'поток'.")

        context = {'results': curators}
        return render(request, self.template_name, context)


class ContactListView(ListView):
    model = Contact
    template_name = 'admin/starter-kit/applications.html'
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


class NotificationListView(ListView):
    model = Notification
    template_name = 'admin/starter-kit/notifications.html'
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






class NotificationCreateView(CreateView):
    model = Notification
    form_class = NotificationForm
    template_name = 'admin/starter-kit/create_notification.html'
    success_url = reverse_lazy('users:admin:create_notification')  # Используем 'admin:create_notification' из app_name

    def form_valid(self, form):
        messages.success(self.request, 'Уведомление успешно создано.')
        return super().form_valid(form)






class StreamListView(ListView):
    model = Stream
    template_name = 'users/admin/streams.html'
    context_object_name = 'streams'





from django.db.models import Q

class SearchView(View):
    template_name = 'users/admin/search_results.html'

    def get(self, request):
        query = request.GET.get('q')
        courses = Course.objects.filter(title__icontains=query) if query else []
        students = User.objects.filter(Q(role='student'),
                                       Q(username__icontains=query) | Q(first_name__icontains=query) | Q(
                                           last_name__icontains=query)) if query else []
        notifications = Notification.objects.filter(message__icontains=query) if query else []

        return render(request, self.template_name,
                      {'courses': courses, 'students': students, 'notifications': notifications})


class AddCourseView(View):
    def get(self, request):
        # Retrieve all available course types
        course_types = CourseType.objects.all()

        # Create an empty form instance
        form = CourseForm()

        return render(request, 'admin/starter-kit/add_course.html', {'course_types': course_types, 'form': form})

    def post(self, request):
        # Create a form instance with POST data
        form = CourseForm(request.POST, request.FILES)

        if form.is_valid():
            # Save the course object to the database
            course = form.save()

            # Redirect to the course detail page or any other desired URL
            return render(request, 'admin/starter-kit/index.html', {'form': form, 'success_message': 'Course added successfully'})

        # If the form is not valid, re-render the form with errors
        return render(request, 'admin/starter-kit/add_course.html', {'form': form})


class AddModuleView(View):
    def get(self, request):
        # Retrieve all available course types
        course_types = CourseType.objects.all()

        # Create an empty form instance
        form = ModuleForm()

        return render(request, 'admin/starter-kit/add_module.html', {'course_types': course_types, 'form': form})

    def post(self, request):
        # Create a form instance with POST data
        form = ModuleForm(request.POST)

        if form.is_valid():
            # Save the module object to the database
            module = form.save()

            # Redirect to a success page or any other desired URL
            return render(request, 'admin/starter-kit/add_module.html', {'form': form, 'success_message': 'Модуль был успешно добавлен!'})

        # If the form is not valid, re-render the form with errors
        return render(request, 'admin/starter-kit/add_module.html', {'form': form})






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
        return redirect('website:home')  # Замените 'home' на имя URL-шаблона для перенаправления на нужную страницу
