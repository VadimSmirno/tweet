from config import name_db, username, password, host
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import  sessionmaker

DATABASE_URL = f"postgresql+asyncpg://{username}:{password}@{host}/{name_db}"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)  # type: ignore

session = async_session()
