from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

db_url = "postgresql+psycopg2://postgres:adminZ@localhost:5432/updated_ecom"
engine = create_engine(db_url)

Base = declarative_base()
LocalSession = sessionmaker(bind=engine)
session = LocalSession()

def create_table():
    Base.metadata.create_all(engine)

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()