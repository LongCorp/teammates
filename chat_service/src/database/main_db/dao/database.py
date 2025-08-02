from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import MAIN_DB_URL


engine = create_async_engine(url=MAIN_DB_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)