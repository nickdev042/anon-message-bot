from app.database.models import async_session, User
from sqlalchemy import or_, and_, select
import secrets
import string

def generate_unique_link_code(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits  # a-zA-Z0-9
    return ''.join(secrets.choice(characters) for _ in range(length))

async def create_user_profile(TG_id):
    """Создание пользователя в бд (вызывается только по команде /start)"""
    try:
       async with async_session() as session:
           
            # Генерация уникального кода
            code = generate_unique_link_code()

            # Опционально: проверка на уникальность
            # Если в базе должно быть уникальное поле link_code — лучше проверить, нет ли уже такого
            existing = await session.scalar(
                select(User).where(User.link_code == code)
            )
            while existing:
                code = generate_unique_link_code()
                existing = await session.scalar(
                    select(User).where(User.link_code == code)
                )
            new_user = User(
                tg_id=TG_id,
                link_code = code
                )

            session.add(new_user)
            await session.commit()
    except Exception as e:
        print(f"Ошибка при создании пользователя: {e}")
        await session.rollback()
    
    return code
    
async def get_link(tg_id):
    async with async_session() as session:
        result = await session.execute(
            select(User.link_code).where(User.tg_id == tg_id)
        )
        link_code = result.scalar()
        return link_code

async def check_user_exists(TG_id) -> bool:
    """Проверка существования"""
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == TG_id))
        return user is not None
    
async def check_user_VIP(TG_id) -> bool:
    async with async_session() as session:
        result = await session.scalar(select(User.VIP).where(User.tg_id == TG_id))
        return result if result is not None else False   

async def check_user_link(code) -> str:
    async with async_session() as session:
        result = await session.execute(
            select(User.tg_id)
               .where(
                  and_(
                      User.link_code == code
                      )
                  )
        )
        User_receiver = result.scalar()  
        return User_receiver