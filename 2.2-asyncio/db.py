import atexit
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

PG_DSN = 'postgresql://postgres:Qwerty11@127.0.0.1:5432/asyncio_db'
engine = create_engine(PG_DSN)

Base = declarative_base()
Session = sessionmaker(bind=engine)

atexit.register(engine.dispose)  # Закрываем подключение при выходе


class People(Base):
    __tablename__ = 'people'
    pass


# Base.metadata.drop_all(bind=engine)  # для очистки таблиц при отладке кода
Base.metadata.create_all(bind=engine)
