from sqlmodel import SQLModel, Session, create_engine
from .config import settings
postgres_url = f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(postgres_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def drop_db_and_tables():
    SQLModel.metadata.drop_all(engine)

def get_session():
    with Session(engine) as session:
        yield session