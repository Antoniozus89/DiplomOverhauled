from tortoise import Tortoise, fields
from tortoise.models import Model

class Post(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=200)
    content = fields.TextField()
    published_date = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "posts"

async def run():
    await Tortoise.init(
        db_url='postgres://postgres:890227@localhost/TortoiseORM',
        modules={'models': ['__main__']}
    )
    await Tortoise.generate_schemas()

    # Добавление записи
    await Post.create(title='My First Post', content='This is the content of my first post.')

    await Tortoise.close_connections()

import asyncio
asyncio.run(run())