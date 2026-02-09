'''
data base config
'''

'''
╭──────────────────────────────────────────────╮
│                  Import Modules              │
╰──────────────────────────────────────────────╯
'''
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from core.config import settings


engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,                    # database adress
    pool_pre_ping=True,                                  # ✅ جلوگیری از stale connection
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

session = SessionLocal()

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()