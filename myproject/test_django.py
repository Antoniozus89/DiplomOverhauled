import os
import time

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
import django
django.setup()

from blog.models import Post

# Функция для создания записей
def create_posts(num_posts):
    start_time = time.time()
    for i in range(num_posts):
        Post.objects.create(title=f'Post {i}', content='This is a test post.')
    end_time = time.time()
    print(f'Создание {num_posts} записей заняло {end_time - start_time:.2f} секунд.')

# Функция для выборки всех записей
def fetch_posts():
    start_time = time.time()
    posts = Post.objects.all()
    end_time = time.time()
    print(f'Выборка всех записей заняла {end_time - start_time:.2f} секунд.')

# Функция для удаления всех записей
def delete_posts():
    start_time = time.time()
    Post.objects.all().delete()
    end_time = time.time()
    print(f'Удаление всех записей заняло {end_time - start_time:.2f} секунд.')

if __name__ == '__main__':
    num_posts = 1000  # Количество создаваемых записей
    create_posts(num_posts)
    fetch_posts()
    delete_posts()