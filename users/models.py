from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (
        ('student', 'Студент'),
        ('curator', 'Куратор'),
        ('admin', 'Администратор'),
    )

    COUNTRY_CHOICES = (
        ('kz', 'Казахстан'),
        ('ru', 'Россия'),
        ('ukr', 'Украина'),
        ('kg', 'Кыргызстан'),
        ('uz', 'Узбекистан'),
    )

    CITY_CHOICES = (
        ('tse', 'Астана'),
        ('ala', 'Алматы'),
        ('msq', 'Москва'),
        ('kiev', 'Киев'),
        ('bishkek', 'Бишкек'),
        ('tashkent', 'Ташкент'),
    )

    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=25, blank=True)
    bio = models.TextField(blank=True, null=True, default='Всем привет! Я ученик компании WorkBench!')
    country = models.CharField(choices=COUNTRY_CHOICES, max_length=15, default='kz')
    city = models.CharField(choices=CITY_CHOICES, max_length=20, default='tse')
    address = models.CharField(blank=True, null=True, default='', max_length=255)
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


class StudentOrderHistory(models.Model):

    CASH_METHOD_CHOICES = (
        ('nal', 'Наличными'),
        ('send', 'Перевод на карту'),
        ('payment', 'Оплата по реквизитам'),
    )

    BANK = (
        ('kaspi_bank', 'Kaspi Банк'),
        ('halyk_bank', 'Halyk банк'),
        ('forte_bank', 'Forte Банк'),
        ('freedom', 'Freedom Finance'),
        ('simply', 'Simply'),
        ('bereke_bank', 'Береке Банк'),
        ('jusan_bank', 'Jusan Bank')
    )

    cash_method = models.CharField(max_length=30, choices=CASH_METHOD_CHOICES, default='payment', verbose_name='cash_method')
    cash_count = models.PositiveBigIntegerField(blank=True, null=True, verbose_name='cash_count')
    bank = models.CharField(max_length=255, choices=BANK, verbose_name='bank')
    created_date = models.DateField(default=datetime.now, verbose_name='date')
    student = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.student.first_name} | {self.bank} | {self.cash_count}'

    def get_bank_name(self):
        bank_choices = dict(self.BANK)
        return bank_choices.get(self.bank, 'Неизвестный банк')

    def get_cash_method_name(self):
        cash_method_choices = dict(self.CASH_METHOD_CHOICES)
        return cash_method_choices.get(self.cash_method, 'Неизвестный метод')

    class Meta:
        verbose_name = 'История покупок студентов'
        verbose_name_plural = 'Истории покупок студентов'