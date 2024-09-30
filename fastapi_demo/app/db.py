from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .setting import get_settings

setting = get_settings()
username = setting.username
password = setting.password
host = setting.host
db_name = setting.database

sync_engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{db_name}",
                            pool_pre_ping=True, max_overflow=-1, pool_size=16, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)


# Dependency
def get_db_sync():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
