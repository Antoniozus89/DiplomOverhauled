
import asyncio
from tortoise import Tortoise, fields
from tortoise.models import Model
import time


class Post(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=200)
    content = fields.TextField()


async def init():
    await Tortoise.init(
        db_url='postgres://postgres:890227@localhost:5432/TortoiseORM',
        modules={'models': ['__main__']}
    )
    await Tortoise.generate_schemas()


async def create_posts(num_posts):
    start_time = time.time()

    post_list = [Post(title=f'Post {i}', content='This is a test post.') for i in range(num_posts)]
    await Post.bulk_create(post_list)

    end_time = time.time()
    print(f'Создание {num_posts} записей заняло {end_time - start_time:.2f} секунд.')


async def fetch_posts():
    start_time = time.time()

    posts = await Post.all()

    end_time = time.time()
    print(f'Выборка всех записей заняла {end_time - start_time:.2f} секунд. Всего записей: {len(posts)}')


async def delete_posts():
    start_time = time.time()

    await Post.all().delete()

    end_time = time.time()
    print(f'Удаление всех записей заняло {end_time - start_time:.2f} секунд.')


async def main(num_posts):
    await init()
    await create_posts(num_posts)
    await fetch_posts()
    await delete_posts()
    await Tortoise.close_connections()


if __name__ == '__main__':
    num_posts = 1000
    asyncio.run(main(num_posts))
