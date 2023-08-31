from django.db import models
from courses.models import Course


class Schedule(models.Model):

    WEEKDAYS = (
        ('monday', 'Понедельник'),
        ('tuesday', 'Вторник'),
        ('wednesday', 'Среда'),
        ('thursday', 'Четверг'),
        ('friday', 'Пятница'),
        ('saturday', 'Суббота'),
        ('sunday', 'Воскресенье'),
    )

    start_date = models.DateField()  # Дата начала курса
    end_date = models.DateField()  # Дата окончания курса
    weekdays = models.CharField(max_length=15, choices=WEEKDAYS, default='monday')  # Дни недели
    start_time = models.TimeField()  # Время начала занятий
    end_time = models.TimeField()  # Время окончания занятий
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Связь с моделью "Course"

    def __str__(self):
        return f'{self.course} - {self.start_date} to {self.end_date}'

    class Meta:
        verbose_name = 'Расписания'
        verbose_name_plural = 'Расписание'



