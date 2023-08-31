from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (
        ('student', 'Студент'),
        ('curator', 'Куратор'),
        ('admin', 'Администратор'),
    )
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    stream = models.ForeignKey('Stream', on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return self.username


class Stream(models.Model):
    number = models.PositiveIntegerField()

    def __str__(self):
        return str(self.number)

    class Meta:
        verbose_name = 'Поток'
        verbose_name_plural = 'Потоки'