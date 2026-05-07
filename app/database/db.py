from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase
from app.config.app_config import getAppconfig

url = getAppconfig().database_url.get_secret_value()
engine= create_engine(url,pool_pre_ping=True)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

class Base(DeclarativeBase):
    pass

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
