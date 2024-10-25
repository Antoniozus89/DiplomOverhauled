import time
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Создание подключения к базе данных
engine = create_engine('postgresql://postgres:890227@localhost/SqlAlchemy')
# Определение базового класса
Base = declarative_base()
# Создание сессии
Session = sessionmaker(bind=engine)


# Определение модели Post
class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    published_date = Column(DateTime, default=datetime.now)


# Создание таблиц в базе данных
Base.metadata.create_all(engine)


# Добавление новой записи
def create_posts(num_posts):
    session = Session()  # Создание новой сессии
    start_time = time.time()  # Запись времени начала операции
    for i in range(num_posts):  # Цикл для создания записей
        post = Post(title=f'Post {i}', content='This is a test post.')  # Создание нового поста
        session.add(post)  # Добавление поста в сессию
    session.commit()  # Сохранение всех изменений в базе данных
    end_time = time.time()  # Запись времени окончания операции
    print(f'Создание {num_posts} записей заняло {end_time - start_time:.2f} секунд.')  # Вывод времени выполнения


# Выборкf всех записей из таблицы
def fetch_posts():
    session = Session()  # Создание новой сессии
    start_time = time.time()  # Запись времени начала операции
    posts = session.query(Post).all()  # Выполнение запроса для получения всех записей
    end_time = time.time()  # Запись времени окончания операции
    print(f'Выборка всех записей заняла {end_time - start_time:.2f} секунд.')  # Вывод времени выполнения


# Удаление записей
def delete_posts():
    session = Session()
    start_time = time.time()
    session.query(Post).delete()
    session.commit()
    end_time = time.time()
    print(f'Удаление всех записей заняло {end_time - start_time:.2f} секунд.')


if __name__ == '__main__':
    num_posts = 1000  # Количество создаваемых записей
    create_posts(num_posts)
    fetch_posts()
    delete_posts()
