from django.contrib.auth.models import User
from django.db import models


# Модель поста
class Post(models.Model):
    title = models.CharField(max_length=200)  # Заголовок поста (строка до 200 символов)
    content = models.TextField()  # Содержимое поста
    published_date = models.DateTimeField(
        auto_now_add=True)  # Дата публикации (автоматически устанавливается при создании)

    def __str__(self):  # Этот метод переопределяет стандартное строковое представление объекта. Когда вы
        # вызываете str() на объекте или когда Django пытается отобразить объект (например, в админке),
        # будет вызван этот метод.
        return self.title  # Метод возвращает значение self.title, что означает,
        # что строковое представление объекта будет равно значению поля title этого объекта.


class Comment(models.Model):  # Класс Comment наследуется от models.Model, что делает его моделью Django.
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)  # Это поле устанавливает связь с
    # моделью Post. Оно является внешним ключом (ForeignKey),
    # что означает, что каждый комментарий связан с конкретным постом.
    # related_name='comments' позволяет вам обращаться к комментариям поста через атрибут comments. Например,
    # вы можете получить все комментарии к посту с помощью post.comments.all().on_delete=models.CASCADE указывает,
    # что если пост будет удален, все связанные с ним комментарии также будут удалены.
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Это поле устанавливает связь с моделью User,
    # представляющей автора комментария.
    # При удалении пользователя все его комментарии также будут удалены.
    content = models.TextField()  # Это текстовое поле для хранения содержимого комментария. Оно может содержать длинные тексты.
    created_at = models.DateTimeField(auto_now_add=True)  # Это поле автоматически заполняется текущей датой

    # и временем при создании нового комментария. Параметр auto_now_add=True означает,
    # что значение устанавливается только один раз — при создании объекта.

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'  # Этот метод возвращает строковое представление
    # объекта комментария. Он будет использоваться, например, в админке Django для отображения комментариев.
    # В данном случае возвращается строка вида "Comment by username on post_title", что делает вывод более
    # информативным.
