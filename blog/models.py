from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255, blank=False)
    author = models.CharField(max_length=255, blank=False)
    image = models.ImageField(upload_to='posts/', blank=False)
    body = models.TextField(blank=False)
    hashtag = models.CharField(max_length=255, blank=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'