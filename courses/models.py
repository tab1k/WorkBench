from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from users.models import User
from embed_video.fields import EmbedVideoField


class CourseType(models.Model):
    title = models.CharField(max_length=155, null=True, blank=True)
    description = models.CharField(max_length=155, null=True, blank=True)
    time = models.PositiveIntegerField(default=90, null=True, blank=True)
    photo = models.ImageField(upload_to='course_type_images', null=True, blank=True)

    def __str__(self):
        return self.title

    def has_courses_with_curators(self, user):
        return self.courses.filter(curators=user).exists()

    class Meta:
        verbose_name = 'Тип курса'
        verbose_name_plural = 'Типы курсов'


class Course(models.Model):
    title = models.CharField(max_length=255)  # Название курса
    description = models.TextField()  # Описание курса
    duration = models.PositiveIntegerField()  # Продолжительность курса
    image = models.ImageField(upload_to='course_images', null=True, blank=True)
    start_date = models.DateField(blank=True, null=True, auto_created=True)
    course_type = models.ForeignKey(CourseType, on_delete=models.CASCADE, related_name='courses') # Связь с моделью "Course Type"
    curators = models.ManyToManyField(get_user_model())   # Связь с моделью "Curator"
    students = models.ManyToManyField(User, related_name='courses', blank=True)

    def create_notification(self, message):
        notification = Notification(course=self, message=message)
        notification.save()
        notification.students.set(self.students.all())

    def get_unread_notifications(self):
        return Notification.objects.filter(course=self, read=False)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Module(models.Model):
    title = models.CharField(max_length=255)  # Название модуля
    description = models.TextField()  # Описание модуля
    order = models.PositiveIntegerField()  # Порядковый номер модуля
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')  # Связь с моделью "Course"

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'


class Lesson(models.Model):
    title = models.CharField(max_length=255)  # Название урока
    description = models.TextField()  # Описание урока
    zoom_link = models.URLField(blank=True, null=True)
    start_datetime = models.DateTimeField(blank=True, null=True)
    video = EmbedVideoField(blank=True, null=True) # Видео
    learn_documentation = models.FileField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('users:student:courses:lesson_view', args=[str(self.id)])

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'



class Notification(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    students = models.ManyToManyField(get_user_model(), blank=True, related_name='notifications')
    file = models.FileField(upload_to='notifications/', blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.message


    class Meta:
        verbose_name = 'Объявление курсу'
        verbose_name_plural = 'Объявление курсам'



