from os import environ

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = "postgresql+asyncpg://admin:admin@postgres"
# DATABASE_URL = "postgresql+asyncpg://admin:admin@localhost"
TEST_DATABASE_URL = "postgresql+asyncpg://test:test@localhost"

testing = environ.get("TESTING")


if testing:
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
else:
    engine = create_async_engine(DATABASE_URL, echo=True)


async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)  # type: ignore

session = async_session()
Base = declarative_base()


fake_db_users = [
    {"name": "Марк Твен", "user_api_key": "test"},
    {"name": "Александр Дюма", "user_api_key": "test1"},
    {"name": "Дмитрий Менделеев", "user_api_key": "test2"},
    {"name": "Иван Тургенев", "user_api_key": "test3"},
    {"name": "Лев Толстой", "user_api_key": "test4"},
    {"name": "Федор Достоевский", "user_api_key": "test5"},
]

fake_db_medias = [
    {"filename": "/app/static/images/user_1_lake.jpeg"},
    {"filename": "/app/static/images/user_3_space.jpg"},
    {"filename": "/app/static/images/user_2_beer.jpg"},
]

fake_db_tweets = [
    {
        "content": "Сегодня открыл для себя множество увлекательных увлечений — от изучения истории"
                   " до создания искусства. Время так ценно, что важно выбирать только лучшие занятия! #Увлечения",
        "attachments": [1],
        "author": 1
    },
    {
        "content": "В этот день встретил море новых впечатлений и знаний. Жизнь — это бесконечное путешествие,"
                   " и каждый день приносит новые страницы в эту книгу. #Путешествия #Знания",
        "attachments": [2],
        "author": 2
    },
    {
        "content": "Сегодняшний день был полон открытий и экспериментов. Мир так разнообразен,"
                   " и я горжусь возможностью вносить свой вклад в его изучение! #Открытия #Эксперименты",
        "attachments": [3],
        "author": 3
    },
    {
        "content": "Продолжаю исследовать мир вокруг себя. Открытия не прекращаются никогда, и я готов к новым"
                   " приключениям! #Исследования #НовыеГоризонты",
        "attachments": [1],
        "author": 1
    },
    {
        "content": "Вечером наслаждаюсь чтением увлекательных книг. В мире слов создается бесконечное количество историй,"
                   " и каждая из них особенна. #Чтение #Книги",
        "attachments": [2],
        "author": 2
    },
    {
        "content": "Сегодня провел несколько интересных экспериментов в химической лаборатории. Химия — это как магия,"
                   " и я горжусь возможностью изучать ее тайны! #Химия #Эксперименты",
        "attachments": [3],
        "author": 3
    }
]

