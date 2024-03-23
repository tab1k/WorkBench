import shutil

from PyPDF2 import PdfMerger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.timezone import localtime, now
from django.http import JsonResponse, HttpResponseNotFound, FileResponse
from django.views.generic import CreateView, DeleteView
import subprocess  # Для выполнения команд в системной оболочке
from django.core.files.base import ContentFile
from django.shortcuts import redirect, render
from django.views.generic import CreateView
import tempfile
from openai import OpenAI
from reportlab.lib.pagesizes import A4,landscape
from reportlab.pdfgen import canvas
from PIL import Image
from datetime import date
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from comments.forms import CommentForm
from comments.models import Comment
from workbench.settings import OPENAI_API_KEY
from .forms import LessonCreationForm
from .models import Course, Module, CourseType, TemporaryToken
from courses.models import Lesson
from tests.models import TestResult
from django.db.models import Count
from django.http import HttpResponseForbidden
from django.http import HttpResponse
from django.views import View
from django.shortcuts import get_object_or_404
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
from users.models import User


class CoursesByType(LoginRequiredMixin, View):
    login_url = 'users:login'

    def get(self, request, type_id):
        # Получаем тип курса по type_id
        course_type = get_object_or_404(CourseType, id=type_id)

        # Получаем все курсы, относящиеся к данному типу курса
        courses = Course.objects.filter(course_type=course_type)

        # Определение шаблона в зависимости от роли пользователя
        if request.user.groups.filter(name='Студенты').exists():
            template_name = 'users/student/courses_by_type.html'
        elif request.user.groups.filter(name='Кураторы').exists():
            template_name = 'curator/starter-kit/course_type.html'
        elif request.user.groups.filter(name='Администраторы').exists():
            template_name = 'admin/starter-kit/course_type.html'
        else:
            # Если пользователь не принадлежит ни к одной из групп или не аутентифицирован, перенаправляем его на страницу входа
            return redirect('users:login')

        return render(request, template_name, {'course_type': course_type, 'courses': courses})



class Courses(View):

    def get(self, request):
        if request.user.groups.filter(name='Администраторы').exists():
            template_name = 'admin/starter-kit/courses.html'
            courses = Course.objects.all()
        elif request.user.groups.filter(name='Кураторы').exists():
            template_name = 'curator/starter-kit/courses.html'
            courses = Course.objects.all()
        else:
            template_name = 'student/starter-kit/courses.html'
            courses = Course.objects.filter(students=request.user)

        all_comments = Comment.objects.filter(Q(user=request.user) | Q(curator=request.user))

        student_comments = all_comments.filter(is_student_comment=True)
        curator_comments = all_comments.filter(is_student_comment=False)


        current_time = localtime(now())

        return render(request, template_name, {
            'courses': courses,
            'current_time': current_time,
            'student_comments': student_comments,
            'curator_comments': curator_comments
        })


class DeleteCourseView(LoginRequiredMixin,View):
    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        return render(request, 'admin/starter-kit/delete_course_confirm.html', {'course': course})

    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        course.delete()
        return redirect('users:admin:courses:courses')


# Представление для отображения Модулей
class Modules(View):
    template_admin = 'admin/starter-kit/modules.html'
    template_curator = 'curator/starter-kit/modules.html'
    template_student = 'student/starter-kit/modules.html'

    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)

        if request.user.groups.filter(name='Администраторы').exists():
            module = Module.objects.filter(course=course)
            return render(request, self.template_admin, {'modules': module, 'course': course})

        elif request.user.groups.filter(name='Кураторы').exists():
            module = Module.objects.filter(course=course, course__curators=request.user)
            return render(request, self.template_curator, {'modules': module, 'course': course})

        else:
            module = Module.objects.filter(course=course, course__students=request.user)
            return render(request, self.template_student, {'modules': module, 'course': course})


class CourseStudentsView(View):
    template_name = 'admin/starter-kit/course_students.html'

    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        students = course.students.all()

        return render(request, self.template_name, {'course': course, 'students': students})


class LessonsByModule(View):
    template_student = 'student/starter-kit/lessons_list.html'
    template_curator = 'curator/starter-kit/lessons_list.html'
    template_admin = 'admin/starter-kit/lessons_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module, id=module_id)
        lessons = module.lesson_set.all()  # Получаем все уроки модуля
        student = request.user

        context = {'module': module, 'lessons': lessons}

        if student.is_authenticated:
            if student.role == 'student':
                return render(request, self.template_student, context)
            elif student.role == 'curator':
                return render(request, self.template_curator, context)
            elif student.role == 'admin':
                return render(request, self.template_admin, context)

        return render(request, 'users/404.html')


class LessonView(View):
    student_template = 'student/starter-kit/lessons.html'
    curator_template = 'curator/starter-kit/lessons.html'
    admin_template = 'admin/starter-kit/lessons.html'

    def get_next_lesson(self, current_lesson):
        module = current_lesson.module
        next_lesson = Lesson.objects.filter(module=module, id__gt=current_lesson.id).order_by('id').first()
        return next_lesson

    def get_previous_lesson(self, current_lesson):
        module = current_lesson.module
        previous_lesson = Lesson.objects.filter(module=module, id__lt=current_lesson.id).order_by('-id').first()
        return previous_lesson

    def get_comments(self, lesson_id):
        lesson = get_object_or_404(Lesson, id=lesson_id)
        comments = Comment.objects.filter(lesson=lesson)
        comment_list = [{"user": comment.user, "text": comment.text} for comment in comments]
        return JsonResponse({"comments": comment_list})

    def get_chat_response(self, message):
        client = OpenAI(api_key=OPENAI_API_KEY)

        # Создание сессии чата для взаимодействия с моделью
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
                {"role": "user", "content": message}
            ]
        )

        # Возвращаем результат работы модели (текст ответа)
        return completion.choices[0].message.content

    def get(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, id=lesson_id)
        module = lesson.module
        lessons = Lesson.objects.filter(module=module)
        comment_form = CommentForm()
        student_comments = Comment.objects.filter(lesson=lesson, is_student_comment=True)
        student = request.user
        course_type = CourseType.objects.filter(courses__students=student).distinct()
        courses = Course.objects.filter(students=student)




        if request.user.role == 'student':
            next_lesson = self.get_next_lesson(lesson)
            previous_lesson = self.get_previous_lesson(lesson)
            curator_comments = Comment.objects.filter(lesson=lesson, is_student_comment=False, user=student)
            lesson.is_watched = True
            lesson.save()
            return render(request, self.student_template,
                          {'lesson': lesson, 'lessons': lessons, 'comment_form': comment_form,
                           'student_comments': student_comments, 'next_lesson': next_lesson,
                           'previous_lesson': previous_lesson,
                           'courses': courses,
                           'course_type': course_type,
                           'student': student,
                           'curator_comments': curator_comments,
                           'lesson_id': lesson_id,

                           })

        elif request.user.role == 'curator':
            next_lesson = self.get_next_lesson(lesson)
            previous_lesson = self.get_previous_lesson(lesson)
            curator_comments = Comment.objects.filter(lesson=lesson, is_student_comment=False, user=student)
            lesson.is_watched = True
            lesson.save()
            return render(request, self.curator_template,
                          {'lesson': lesson,
                           'lessons': lessons,
                           'next_lesson': next_lesson,
                           'previous_lesson': previous_lesson,
                           'courses': courses,
                           'course_type': course_type,
                           'student': student,
                           'comment_form': comment_form,
                           'curator_comments': curator_comments,
                           'lesson_id': lesson_id,
                           })

        elif request.user.role == 'admin':
            next_lesson = self.get_next_lesson(lesson)
            previous_lesson = self.get_previous_lesson(lesson)
            curator_comments = Comment.objects.filter(lesson=lesson, is_student_comment=False, user=student)
            lesson.is_watched = True
            lesson.save()
            return render(request, self.admin_template,
                          {'lesson': lesson,
                           'lessons': lessons,
                           'next_lesson': next_lesson,
                           'previous_lesson': previous_lesson,
                           'courses': courses,
                           'course_type': course_type,
                           'student': student,
                           'curator_comments': curator_comments,
                           'lesson_id': lesson_id,
                           })
        else:
            return redirect(reverse('users:login'))

    def post(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, id=lesson_id)
        module = lesson.module
        lessons = Lesson.objects.filter(module=module)
        comment_form = CommentForm(request.POST)  # Инициализируем форму данными из POST-запроса

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.lesson = lesson
            comment.is_student_comment = True
            comment.save()

            # Возвращаем обновленный список комментариев в JSON-ответе
            comments = Comment.objects.filter(lesson=lesson, is_student_comment=True)
            comments_data = [{'user': comment.user.username, 'text': comment.text} for comment in comments]
            return JsonResponse({'success': True, 'comments': comments_data})

        elif 'message' in request.POST:
            message = request.POST['message']
            chat_response = self.get_chat_response(message)

            # Возвращаем ответ чата в JSON-ответе
            return JsonResponse({'success': True, 'response': chat_response})

        if request.user.role == 'student':
            return render(request, self.student_template, {'lesson': lesson, 'lessons': lessons, 'comment_form': comment_form})
        elif request.user.role == 'curator':
            return render(request, self.curator_template, {'lesson': lesson, 'lessons': lessons, 'comment_form': comment_form})
        elif request.user.role == 'admin':
            return render(request, self.admin_template, {'lesson': lesson, 'lessons': lessons, 'comment_form': comment_form})
        else:
            # Перенаправление на страницу входа
            return redirect(reverse('users:login'))


class LessonCreateView(LoginRequiredMixin, CreateView):
    template_name = 'admin/starter-kit/create_lesson.html'
    form_class = LessonCreationForm
    model = Lesson

    def get_initial(self):
        initial = super().get_initial()
        module_id = self.kwargs.get('module_id')  # Получаем идентификатор модуля из URL
        if module_id:
            module = get_object_or_404(Module, pk=module_id)
            initial['module'] = module
        return initial

    def form_valid(self, form):
        lesson = form.save(commit=False)
        lesson.module = self.get_initial()['module']  # Устанавливаем модуль урока

        # Обработка загруженного видео и создание потокового URL
        video_file = form.cleaned_data['video']  # Получаем загруженный видеофайл из формы
        if video_file:
            # Сохраняем файл в медиа
            lesson.video = video_file
            lesson.save()  # Сохраняем урок для получения id

            # Создаем потоковый URL для видео
            lesson.stream_url = lesson.video.url

        lesson.save()
        return redirect('users:student:courses:lesson_view', lesson_id=lesson.id)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})







class LessonDeleteView(DeleteView):
    model = Lesson
    template_name = 'admin/starter-kit/lesson_confirm_delete.html'  # шаблон для подтверждения удаления
    success_url = reverse_lazy('users:admin:courses:courses')


class AnswersView(View):
    template_curator = 'curator/starter-kit/answers.html'
    template_admin = 'admin/starter-kit/answers.html'
    template_error = 'users/404.html'

    def get(self, request):
        student_comments = Comment.objects.filter(is_student_comment=True)

        # Получаем список всех курсов
        all_courses = Course.objects.all()

        # Получаем выбранный курс из параметра запроса
        course_filter = request.GET.get('course_filter')
        module_filter = request.GET.get('module_filter')
        lesson_filter = request.GET.get('lesson_filter')
        student_filter = request.GET.get('student_filter')

        selected_course = None
        selected_module = None
        selected_lesson = None
        selected_student = None  # Добавляем переменную для выбранного студента

        # Фильтруем комментарии по выбранным параметрам
        if course_filter:
            selected_course = Course.objects.filter(id=course_filter).first()
            student_comments = student_comments.filter(lesson__module__course=selected_course)

            if module_filter:
                selected_module = Module.objects.filter(id=module_filter).first()
                student_comments = student_comments.filter(lesson__module=selected_module)

                if lesson_filter:
                    selected_lesson = Lesson.objects.filter(id=lesson_filter).first()
                    student_comments = student_comments.filter(lesson_id=lesson_filter)

            if student_filter:  # Фильтр по студенту
                selected_student = User.objects.filter(id=student_filter).first()
                student_comments = student_comments.filter(user=selected_student)


        if request.user.role == 'curator':
            template_name = self.template_curator
        elif request.user.role == 'admin':
            template_name = self.template_admin
        else:
            template_name = self.template_error

        return render(request, template_name, {
            'comments': student_comments,
            'all_courses': all_courses,
            'selected_course': selected_course,
            'selected_module': selected_module,
            'selected_student': selected_student,
            'is_student_comment': True
        })

    def post(self, request):
        if 'delete_comment' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = Comment.objects.filter(id=comment_id).first()
            if comment and comment.is_student_comment:
                comment.delete()
        elif 'curator_response' in request.POST:
            comment_id = request.POST.get('comment_id')
            curator_response = request.POST.get('curator_response')
            comment = Comment.objects.filter(id=comment_id, is_student_comment=True).first()
            if comment:
                comment.curator_response = curator_response
                comment.curator = request.user
                comment.is_student_comment = False
                comment.save()

        # Перенаправление в зависимости от роли пользователя
        if request.user.role == 'curator':
            return redirect('users:curator:courses:answers_view')
        elif request.user.role == 'admin':
            return redirect('users:admin:courses:answers_view')
        else:
            # Пользователь не имеет определенной роли, обработайте этот случай по своему усмотрению
            return render(request, 'users/404.html')



class StudentProgressView(View):
    template_name_curator = 'curator/starter-kit/student_progress.html'
    template_name_admin = 'admin/starter-kit/student_progress.html'

    def get(self, request, student_id):
        if request.user.role not in ['curator', 'admin']:
            return HttpResponseForbidden("У вас нет доступа к этой странице.")



        student = User.objects.get(pk=student_id)
        courses = student.courses.all()

        progress = []
        total_test_scores = 0
        lessons_titles = []
        test_scores = []
        total_test_lessons = 0
        total_lessons = 0


        for course in courses:
            modules = course.modules.all()
            for module in modules:
                lessons = module.lesson_set.all()
                for lesson in lessons:
                    test_result = TestResult.objects.filter(student=student, lesson=lesson).first()

                    if test_result:
                        total_test_scores += test_result.score
                        test_scores.append(test_result.score)
                        total_test_lessons += 1

                    progress.append({
                        'course': course,
                        'module': module,
                        'lesson': lesson,
                        'test_result': test_result,
                    })

                    lessons_titles.append(lesson.title)
                    total_lessons += 1

        lesson_count_with_tests = total_test_lessons
        average_test_score = total_test_scores / lesson_count_with_tests if lesson_count_with_tests > 0 else 0

        print("lessons_titles:", lessons_titles)
        print("test_scores:", test_scores)

        context = {
            'student': student,
            'progress': progress,
            'average_test_score': average_test_score,
            'lessons_titles': lessons_titles,
            'test_scores': test_scores,
        }

        if request.user.role == 'curator':
            return render(request, self.template_name_curator, context)
        elif request.user.role == 'admin':
            return render(request, self.template_name_admin, context)


# Ваш файл views.py



class PassedStudentsView(View):
    template_name = 'admin/starter-kit/passed_students.html'
    template_name_curator = 'curator/starter-kit/passed_students.html'

    def get(self, request):
        if request.user.role not in ['curator', 'admin']:
            return HttpResponseForbidden("У вас нет доступа к этой странице.")

        search_query = request.GET.get('q', '')

        passed_students = []
        students = User.objects.filter(role='student')

        for student in students:
            courses = Course.objects.filter(students=student)

            # Check if the student passed all lessons with tests in each course
            for course in courses:
                modules = course.modules.all()
                lessons_passed = 0

                # Check if the student passed all lessons with tests in each module
                for module in modules:
                    lessons_with_tests = Lesson.objects.filter(module=module)

                    total_lessons_in_module = lessons_with_tests.count()

                    # Check if the student passed all lessons in the module
                    passed_all_lessons_in_module = (
                        lessons_with_tests
                        .annotate(test_passed=Count('testresult', filter=Q(testresult__student=student, testresult__score__gte=50)))
                        .filter(test_passed__gte=1)
                        .count() == total_lessons_in_module
                    )

                    if passed_all_lessons_in_module:
                        lessons_passed += total_lessons_in_module
                    else:
                        break

                # Check if the student passed all lessons in all modules of the course
                if lessons_passed == Course.objects.get(pk=course.pk).modules.count():
                    passed_students.append(student)
                    break

        # Apply search query if provided
        search_query = request.GET.get('q', None)

        if search_query:
            filtered_students = User.objects.filter(
                Q(role='student'),
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query)
            )

            passed_students = [student for student in filtered_students if student in passed_students]
        else:
            passed_students = User.objects.filter(id__in=[student.id for student in passed_students])

        selected_course_id = request.GET.get('course_filter')

        if selected_course_id:
            selected_course = Course.objects.get(pk=selected_course_id)
            passed_students = [student for student in passed_students if selected_course in student.courses.all()]

        all_courses = Course.objects.all()

        context = {
            'passed_students': passed_students,
            'search_query': search_query,
            'all_courses': all_courses,
            'selected_course_id': selected_course_id,
        }

        if request.user.role == 'curator':
            return render(request, self.template_name_curator, context)
        elif request.user.role == 'admin':
            return render(request, self.template_name, context)



class CertificateView(View):
    def get(self, request, student_id):
        try:
            student = get_object_or_404(User, pk=student_id)
        except User.DoesNotExist:
            return HttpResponse("Студент с указанным ID не найден.", status=404)

        # Создаем сертификаты для каждого курса студента
        certificates = []
        for index, course in enumerate(student.courses.all(), start=1):
            today = date.today()
            month_name = today.strftime("%B")
            today_str = f"{today.day} {month_name.capitalize()} {today.year} года"

            certificate_path = 'static/student/certificate/cert.png'  # Обновите путь к вашему сертификату
            certificate_image = Image.open(certificate_path)

            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_filepath = temp_file.name
                certificate_image.save(temp_filepath, format='PNG')

            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=landscape(A4))

            p.drawImage(temp_filepath, 0, 0, width=850, height=600)

            font_path = 'static/student/certificate/fonts/Tinos-Italic.ttf'
            pdfmetrics.registerFont(TTFont('Tinos', font_path))

            p.setFillColor('white')

            text_x = 200
            text_y = 300
            line_height = 20

            full_name = f"{student.first_name} {student.last_name}"
            text_width = p.stringWidth(full_name, "Tinos", 60)

            # Вычисляем горизонтальную позицию для центрирования текста имени студента
            text_x = (850 - text_width) / 2

            p.setFont("Tinos", 60)
            p.drawString(text_x, text_y, student.first_name)
            p.drawString(text_x + p.stringWidth(student.first_name) + 10, text_y, student.last_name)

            text_y -= line_height * 1

            date_text_x = 30
            date_text_y = 565
            p.setFont("Tinos", 15)
            p.drawString(date_text_x, date_text_y, today_str)

            text_y -= line_height * 2

            text_course_x = 512
            text_course_y = 205
            course_text = course.title
            p.setFont("Tinos", 17)
            p.drawString(text_course_x, text_course_y, course_text)

            p.save()

            buffer.seek(0)
            certificates.append(buffer)

        # Объединяем все сертификаты в один PDF-файл
        merged_buffer = BytesIO()
        merger = PdfMerger()

        for certificate_buffer in certificates:
            merger.append(BytesIO(certificate_buffer.read()))

        merger.write(merged_buffer)
        merger.close()

        merged_buffer.seek(0)

        return HttpResponse(merged_buffer, content_type='application/pdf')



