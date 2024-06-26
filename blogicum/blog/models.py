from core.models import PublishedModel
from django.contrib.auth import get_user_model
from django.db import models


from blog.constant import HEADER_MODEL_LEN

User = get_user_model()


class Location(PublishedModel, models.Model):
    name = models.CharField(
        'Название места',
        max_length=256)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:HEADER_MODEL_LEN]


class Category(PublishedModel, models.Model):
    title = models.CharField(
        'Заголовок',
        max_length=256)
    description = models.TextField(
        'Описание')
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text=('Идентификатор страницы для URL; разрешены'
                   ' символы латиницы, цифры, дефис и подчёркивание.'))

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:HEADER_MODEL_LEN]


class Post(PublishedModel, models.Model):
    title = models.CharField(
        'Заголовок',
        max_length=256)
    text = models.TextField(
        'Текст',)
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text=('Если установить дату и время в будущем'
                   ' — можно делать отложенные публикации.'))
    author = models.ForeignKey(
        User,
        verbose_name='Автор публикации',
        on_delete=models.CASCADE)
    location = models.ForeignKey(
        Location,
        verbose_name='Местоположение',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True)
    image = models.ImageField(
        verbose_name='Фото',
        upload_to='post_images',
        blank=True)

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        default_related_name = '%(model_name)s'
        default_related_name = 'posts'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title[:HEADER_MODEL_LEN]


class Comment(PublishedModel, models.Model):
    text = models.TextField('Текс коментария')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Заголовок публикации',)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор публикации')

    def __str__(self):
        return f'Комментарий от {self.author} к публикации "{self.post.title}"'

    class Meta:
        verbose_name = 'коментарий'
        verbose_name_plural = 'Коментарии'
        default_related_name = 'comments'
        ordering = ['created_at']
