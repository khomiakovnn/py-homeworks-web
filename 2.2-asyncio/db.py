import atexit
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base

PG_DSN = 'postgresql://postgres:Qwerty11@127.0.0.1:5432/asyncio_db'
engine = create_engine(PG_DSN)

Base = declarative_base()
Session = sessionmaker(bind=engine)

atexit.register(engine.dispose)  # Закрываем подключение при выходе


class People(Base):
    __tablename__ = 'people'
    pk = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id = Column(Integer)
    birth_year = Column(String)
    eye_color = Column(String)
    films = Column(String)
    gender = Column(String)
    hair_color = Column(String)
    height = Column(String)
    homeworld = Column(String)
    mass = Column(String)
    name = Column(String)
    skin_color = Column(String)
    species = Column(String)
    starships = Column(String)
    vehicles = Column(String)


# Base.metadata.drop_all(bind=engine)  # для очистки таблиц при отладке кода
Base.metadata.create_all(bind=engine)
