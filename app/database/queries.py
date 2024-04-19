import logging
from sqlalchemy import select, insert

from database.models import Users, Base
from database.config import db_session, engine
import tg_bot.exceptions as exceptions


log = logging.getLogger(__name__)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def select_user(tg_id: int):
    """Select user in database by tg_id"""
    async with db_session() as session:
        query = select(Users).filter_by(tg_id=tg_id)
        result = await session.execute(query)
        return result.one_or_none()

async def create_user(username: str, tg_id: int):
    """Create new user if he is not in database already."""
    log.info(f"Start add user in database: username - "
                f"{username}, tg_id - {tg_id}")
    try:
        async with db_session() as session:
            user = Users(username=username, tg_id=tg_id)
            session.add(user)
            await session.commit()
    except Exception as error:
        error_message = "Got an error when try to add user to database"
        log.warning(error_message)
        raise exceptions.CreateUserError(error_message)
    log.info(f"User add succesfull")
    return user

async def update_messages_count(tg_id: int):
    """Update user messages_count by tg_id."""
    log.info(f"start update user messages_count by tg_id: {tg_id}")
    try:
        async with db_session() as session:
            user = select(Users).filter_by(tg_id=tg_id)
            user = await session.execute(user)
            user = user.scalar()
            user.messages_count += 1
            await session.commit()
    except Exception as error:
        error_message = "Got error when try to update messages_count by tg_id"
        log.warning(error_message)
        raise exceptions.UpdateMessagesCountError(error_message)
    return user

async def update_nav_moves_count(tg_id: int):
    """Update user nav_moves_count by tg_id."""
    log.info(f"start update user nav_moves_count by tg_id: {tg_id}")
    try:
        async with db_session() as session:
            user = select(Users).filter_by(tg_id=tg_id)
            user = await session.execute(user)
            user = user.scalar()
            user.nav_moves_count += 1
            await session.commit()
    except Exception as error:
        error_message = "Got error when try to update nav_moves_count by tg_id"
        log.warning(error_message)
        raise exceptions.UpdateNavMovesCountError(error_message)
    return user
