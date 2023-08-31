from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from courses.models import Lesson
from .models import EssaySubmission, Essay
from django.contrib import messages


class EssaySubmissionView(View):
    template_name_student = 'users/student/essay.html'
    template_name_curator = 'users/curator/essay_curator.html'
    template_name_admin = 'users/admin/essay_admin.html'

    def get(self, request, lesson_id):
        lesson = Lesson.objects.get(pk=lesson_id)
        essay = Essay.objects.get(lesson_id=lesson_id)
        context = {
            'lesson': lesson,
            'essay' : essay,
        }

        # Фильтрация шаблонов на основе роли пользователя
        if request.user.role == 'student':
            return render(request, self.template_name_student, context)
        elif request.user.role == 'curator':
            return render(request, self.template_name_curator, context)
        elif request.user.role == 'admin':
            return render(request, self.template_name_admin, context)
        else:
            # Если пользователь не имеет определенной роли, обработайте этот случай по своему усмотрению
            # Здесь можно использовать шаблон по умолчанию или вернуть ошибку доступа
            # return render(request, 'default_template.html', context)
            messages.error(request, "У вас нет доступа для сдачи эссе.")
            return redirect('users:student:courses:tests:take_test', lesson_id=lesson_id)

    def post(self, request, lesson_id):
        student = request.user

        # Проверка, является ли пользователь студентом
        if student.role != 'student':
            # Если пользователь не студент, выдаем сообщение об ошибке
            messages.error(request, "У вас нет прав для сдачи эссе.")
            return redirect('users:student:courses:tests:take_test', lesson_id=lesson_id)

        lesson = get_object_or_404(Lesson, pk=lesson_id)
        # Получаем текст эссе от студента
        essay_text = request.POST.get('essay_text', '')

        # Получаем загруженный файл эссе
        essay_file = request.FILES.get('essay_file')

        # Создаем объект EssaySubmission и сохраняем его
        essay_submission = EssaySubmission.objects.create(student=student, lesson=lesson, essay_text=essay_text, files=essay_file)

        # Перенаправляем пользователя на страницу урока после отправки эссе
        return redirect('users:student:courses:lesson_view', lesson_id=lesson_id)


class CheckEssayView(View):
    template_name_curator = 'users/curator/check_essay.html'
    template_name_admin = 'users/admin/check_essay.html'
    template_name_student = 'check_essay.html'

    def get(self, request, essay_submission_id):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("У вас нет доступа к этой странице.")

        essay_submission = get_object_or_404(EssaySubmission, id=essay_submission_id)
        if request.user.role in ['curator']:
            template_name = self.template_name_curator
        elif request.user.role in ['admin']:
            template_name = self.template_name_admin
        else:
            template_name = self.template_name_student

        context = {
            'essay_submission': essay_submission,
        }
        return render(request, template_name, context)

    def post(self, request, essay_submission_id):
        if request.user.role != 'curator':
            return HttpResponseForbidden("У вас нет доступа к этой странице.")

        essay_submission = get_object_or_404(EssaySubmission, id=essay_submission_id)
        essay_submission.is_passed = True  # Помечаем эссе как проверенное и прошедшее
        essay_submission.save()

        return redirect('check_essay_success')





