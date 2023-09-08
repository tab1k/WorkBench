from courses.models import Course
from django.shortcuts import render, redirect
from django.views import View
from .models import Schedule
from .forms import ScheduleForm



class StudentScheduleView(View):
    template_name_student = 'student/starter-kit/schedule.html'
    template_name_curator = 'curator/starter-kit/schedule.html'
    template_name_admin = 'admin/starter-kit/schedule.html'

    def get(self, request):
        # Получить текущего пользователя
        current_user = request.user

        # Определить тип пользователя
        user_role = current_user.role

        # Определим дни недели
        weekdays = [
            ('Пн', 'Понедельник'),
            ('Вт', 'Вторник'),
            ('Ср', 'Среда'),
            ('Чт', 'Четверг'),
            ('Пт', 'Пятница'),
            ('Сб', 'Суббота'),
        ]

        # В зависимости от типа пользователя, выберем соответствующий шаблон
        if user_role == 'student':
            template_name = self.template_name_student
            # Получить расписание для курсов, на которых состоит текущий студент
            schedules = Schedule.objects.filter(course__students=current_user)
        elif user_role == 'curator':
            template_name = self.template_name_curator
            # TODO: Implement curator's schedules filtering if needed
            # Get the courses where the current_user is the curator
            courses_as_curator = Course.objects.filter(curators=current_user)

            # Get schedules for the courses where the current_user is the curator
            schedules = Schedule.objects.filter(course__in=courses_as_curator)
        else:
            template_name = self.template_name_admin
            # For admin, display all schedules regardless of the assigned students
            schedules = Schedule.objects.all()

        # Группируем расписание по курсам
        schedules_by_course = {}
        for schedule in schedules:
            if schedule.course not in schedules_by_course:
                schedules_by_course[schedule.course] = []
            schedules_by_course[schedule.course].append(schedule)

        # Преобразуем группированный словарь в список для порядкового вывода
        grouped_schedules = []
        for course, course_schedules in schedules_by_course.items():
            grouped_schedules.append({
                'course': course,
                'schedules': course_schedules
            })

        context = {
            'grouped_schedules': grouped_schedules,
            'weekdays': weekdays,
            'user_role': user_role,
        }
        return render(request, template_name, context)



from django.views import View
from django.shortcuts import render, redirect
from .models import Schedule
from .forms import ScheduleForm
from courses.models import Course  # Здесь нужно импортировать модель Course

class AddScheduleView(View):
    template_name = 'admin/starter-kit/add_schedule.html'

    def get(self, request):
        form = ScheduleForm()
        courses = Course.objects.all()  # Получаем список всех курсов
        return render(request, self.template_name, {'form': form, 'courses': courses})

    def post(self, request):
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)  # Создаем объект расписания без сохранения в базу данных
            schedule.course = form.cleaned_data['course']  # Устанавливаем курс из формы
            schedule.save()  # Теперь сохраняем объект расписания

            # Дополнительная обработка, если нужно

            return render(request, self.template_name, {'form': form, 'course_added': True})
        else:
            courses = Course.objects.all()
            return render(request, self.template_name, {'form': form, 'courses': courses})





