from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

PG_DSN = 'postgresql+asyncpg://postgres:Qwerty11@127.0.0.1:5432/aiohttp_test'
engine = create_async_engine(PG_DSN)

Base = declarative_base()
Session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class Advertisement(Base):
    __tablename__ = 'advertisement'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    author = Column(Integer, ForeignKey("users.id"), nullable=False)


# Base.metadata.drop_all(bind=engine)  # для очистки таблиц при отладке кода
# Base.metadata.create_all(bind=engine)
