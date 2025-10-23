from sqlalchemy import  BigInteger, String, Integer, Boolean, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from datetime import datetime
from typing import Optional
from sqlalchemy import Identity

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3',
                             echo = True)

async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)  # Автоинкремент
    tg_id = mapped_column(BigInteger, unique=True) # id в TG
    link_code: Mapped[str] = mapped_column(unique=True) #ссылка для отправки сообщений этому пользователю
    VIP: Mapped[bool] = mapped_column(default=False)
    
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



