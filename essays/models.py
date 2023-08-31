from django.db import models
from courses.models import Lesson
from users.models import User


class Essay(models.Model):
    text = models.CharField(max_length=255)  # Тема эссе
    description = models.TextField(null=True, default=None)  # Описание темы эссе with a default value
    photo = models.ImageField(upload_to='essay_photos/', null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    def __str__(self):
        return self.text  # Change from self.topic to self.text

    class Meta:
        verbose_name = 'Тема эссе'
        verbose_name_plural = 'Темы эссе'


class EssaySubmission(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    essay_text = models.TextField()
    files = models.FileField(upload_to='essay_submissions/', blank=True, null=True)
    is_passed = models.BooleanField(default=False)

    def __str__(self):
        return f"Essay Submission: {self.student.username} - {self.lesson.title}"

    class Meta:
        verbose_name = 'Сдача эссе'
        verbose_name_plural = 'Сдачи эссе'
