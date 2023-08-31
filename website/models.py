from django.utils import timezone
from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=155)
    email = models.EmailField()
    phone_number = models.PositiveIntegerField(blank=False, null=True)
    message = models.TextField(max_length=500, blank=True, null=True)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Новая заявка'
        verbose_name_plural = 'Новые заявки'