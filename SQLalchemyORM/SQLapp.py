from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Создание подключения к базе данных
engine = create_engine('postgresql://your_username:your_password@localhost/your_database_name')
# Определение базового класса
Base = declarative_base()


# Определение модели Post
class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    published_date = Column(DateTime, ddefault=datetime.now)

# Создание таблиц в базе данных
Base.metadata.create_all(engine)

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

# Добавление новой записи
new_post = Post(title='My First Post', content='This is the content of my first post.')
session.add(new_post)

# Сохранение изменений в базе данных
session.commit()

print("New post added successfully!")