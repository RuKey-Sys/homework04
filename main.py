"""
Домашнее задание №4
Асинхронная работа с сетью и бд

доработайте функцию main, по вызову которой будет выполняться полный цикл программы
(добавьте туда выполнение асинхронной функции async_main):
- создание таблиц (инициализация)
- загрузка пользователей и постов
    - загрузка пользователей и постов должна выполняться конкурентно (параллельно)
      при помощи asyncio.gather (https://docs.python.org/3/library/asyncio-task.html#running-tasks-concurrently)
- добавление пользователей и постов в базу данных
  (используйте полученные из запроса данные, передайте их в функцию для добавления в БД)
- закрытие соединения с БД
"""
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Post
from jsonplaceholder_requests import fetch_users_data, fetch_posts_data
from typing import List

PG_CONN_URI = "postgresql+asyncpg://postgres:password@localhost/postgres"

engine = create_async_engine(PG_CONN_URI, echo=True)
async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def init_db():
    async with engine.begin() as conn:
        print("Инициализация базы данных...")
        await conn.run_sync(Base.metadata.create_all)


async def add_users_and_posts_to_db(users_data: List[dict], posts_data: List[dict]):
    async with async_session() as session:
        async with session.begin():  # транзакция
            print("Добавление пользователей в базу данных...")
            for user in users_data:
                new_user = User(
                    id=user["id"],
                    name=user["name"],
                    username=user["username"],
                    email=user["email"],
                )
                session.add(new_user)

            print("Добавление постов в базу данных...")
            for post in posts_data:
                new_post = Post(
                    id=post["id"],
                    user_id=post["userId"],
                    title=post["title"],
                    body=post["body"],
                )
                session.add(new_post)

        print("Запись пользователей и постов завершена.")


async def async_main():
    await init_db()
    print("Загрузка данных...")
    users_data, posts_data = await asyncio.gather(
        fetch_users_data(), fetch_posts_data()
    )
    await add_users_and_posts_to_db(users_data, posts_data)
    await engine.dispose()
    print("Программа завершена.")


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
