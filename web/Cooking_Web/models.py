from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Category(models.Model):
    title = models.CharField(
        max_length=160, 
        unique=True,
        verbose_name='Название'
    )

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse(
            'category_list',
            kwargs={'pk': self.pk}
        )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Post(models.Model):
    title = models.CharField(
        max_length=250, 
        verbose_name='Название поста'
    )  
    content = models.TextField(
        default='Скоро здесь будет статья..', 
        verbose_name='Текст поста'
    )
    created_post = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Дата создания поста'
    )
    updated_post = models.DateTimeField(
        auto_now=True, 
        verbose_name='Дата изменения поста'
    )
    photo = models.ImageField(
        upload_to='photo/',
        blank=True, 
        null=True, 
        verbose_name='Фото-карточка'
    )
    watched = models.IntegerField(
        default=0, 
        verbose_name='Просмотры'
    )
    published = models.BooleanField(
        default=True, 
        verbose_name='Публикация'
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        verbose_name='Категория', 
        related_name='posts'
    )    
    author = models.ForeignKey(
        User, 
        default=None, 
        null=True,
        blank=True, 
        on_delete=models.CASCADE, 
        verbose_name='Пользователь'
    )
    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'pk': self.pk})
    
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

class Comment(models.Model):
    """Коментарии статей"""
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE,
        verbose_name='Пост'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    text = models.TextField(
        verbose_name='Коментарий'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии '