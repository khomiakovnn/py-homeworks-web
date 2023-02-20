import atexit
from sqlalchemy import Column, String, Integer, DateTime, create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

PG_DSN = 'postgresql://postgres:Qwerty11@127.0.0.1:5432/flask_test'
engine = create_engine(PG_DSN)

Base = declarative_base()
Session = sessionmaker(bind=engine)

atexit.register(engine.dispose)

# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     username = Column(String, nullable=False, unique=True, index=True)
#     password = Column(String, nullable=False)
#     email = Column(String, nullable=False)


class Advertisement(Base):
    __tablename__ = 'advertisement'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    author = Column(String, nullable=False)


Base.metadata.create_all(bind=engine)
