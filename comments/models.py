from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Lesson
from django.utils import timezone


class Comment(models.Model):
    text = models.TextField()  # Текст комментария
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Урок')  # Связь с моделью "Lesson"
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Пользователь')  # Связь с моделью "User"
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)  # Связь с моделью "Lesson"
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # Связь с моделью "User"
    student_response = models.TextField(blank=True, null=True)  # Текст ответа от студента
    curator_response = models.TextField(blank=True, null=True)  # Текст ответа от куратора
    curator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments_curator', blank=True, null=True, verbose_name='Инструктор')  # Связь с моделью "User" для представления куратора
    is_student_comment = models.BooleanField(default=True)
    timestamp = models.DateTimeField(default=timezone.now, verbose_name='Время')



    def __str__(self):
        return f'{self.user} оставил комментарий с текстом - {self.text} под уроком {self.lesson}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
