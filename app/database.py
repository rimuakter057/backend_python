#connection database
from sqlalchemy import create_engine
# for all  model class  basemodel
from sqlalchemy.ext.declarative import declarative_base
#database session
from sqlalchemy.orm import sessionmaker

SQLALChEMY_DATABASE_URL = "postgresql://postgres:1234@localhost/test_first"

engine = create_engine(SQLALChEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()