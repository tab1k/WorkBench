from django.db import models


class Post(models.Model):

    HASHTAG = (
        ('startups', 'Стартапы'),
        ('programming', 'Программирование'),
        ('digital', 'Цифровизация'),
        ('strategy', 'IT стратегия'),
        ('physics', 'Физика'),
        ('math', 'Математика'),
        ('business', 'IT Бизнес'),
        ('technology', 'Технологии'),
        ('lifehacks', 'Лайфхаки'),
    )

    title = models.CharField(max_length=255, blank=False)
    author = models.CharField(max_length=255, blank=False)
    author_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='posts/', blank=False)
    video = models.URLField(blank=True, null=True)
    body = models.TextField(blank=False)
    hashtag = models.CharField(max_length=255, choices=HASHTAG, default='programming',blank=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_hashtag_display(self):
        return dict(Post.HASHTAG)[self.hashtag]

    class Meta:
        ordering = ['-date']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'