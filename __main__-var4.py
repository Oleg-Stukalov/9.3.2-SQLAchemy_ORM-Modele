import asyncio

from sqlalchemy.dialects import postgresql
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.schema import CreateTable
from sqlalchemy import String, BigInteger
from typing import Annotated

tg_id = Annotated[int, mapped_column(BigInteger, primary_key=True)]
required_short_str = Annotated[str, mapped_column(String(10), nullable=False)]
optional_str = Annotated[str | None, mapped_column(String, nullable=True)]

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    # Чисто и аккуратно, а типы можно утащить в другой файл
    # и импортировать в разные модели
    telegram_id: Mapped[tg_id]
    first_name: Mapped[required_short_str]
    last_name: Mapped[optional_str]

async def main():
    engine = create_engine(
        # Строка подключения при использовании Docker-образов из репозитория
        # В противном случае подставьте свои значения
        url="postgresql+psycopg://superuser:superpassword@127.0.0.1/data",
        echo=False
    )

    # Печатает на экран SQL-запрос для создания таблицы в PostgreSQL
    print(CreateTable(User.__table__).compile(dialect=postgresql.dialect()))

    # Удаление предыдущей версии базы
    # и создание таблиц заново
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    asyncio.run(main())