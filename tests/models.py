from django.db import models
from courses.models import Lesson
from users.models import User


class Test(models.Model):
    question = models.TextField()  # Вопрос
    question_image = models.ImageField(upload_to='test_images/', null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)  # Связь с моделью "Lesson"

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Тестовый вопрос'
        verbose_name_plural = 'Тестовые вопросы'


class TestChoice(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    choice = models.CharField(max_length=255)
    choice_image = models.ImageField(upload_to='test_choice_images/', null=True, blank=True)
    score = models.PositiveIntegerField(default=0)
    is_correct = models.BooleanField(default=False)


    def __str__(self):
        return self.choice

    class Meta:
        verbose_name = 'Тестовый ответ'
        verbose_name_plural = 'Тестовые ответы'


class TestResult(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(null=True, blank=True)
    attempts = models.PositiveIntegerField(default=0)  # Количество попыток прохождения теста

    def __str__(self):
        return f"Test Result: {self.student.username} - {self.lesson.title}"

    class Meta:
        verbose_name = 'Результат теста'
        verbose_name_plural = 'Результаты тестов'


