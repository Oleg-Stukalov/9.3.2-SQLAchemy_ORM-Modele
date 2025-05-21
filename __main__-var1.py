import asyncio

from sqlalchemy.dialects import postgresql
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.schema import CreateTable
from sqlalchemy import String, BigInteger
from sqlalchemy.dialects.postgresql import BIGINT
# Вместо BigInteger можно указать явно тип в PostgreSQL,
# если не планируете менять базу данных в будущем для проекта.
# from sqlalchemy.dialects.postgresql import BIGINT

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    #                                   или (BigInteger, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str | None] = mapped_column(String)

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