# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.core.config import settings

# Créez votre URL de base de données dans votre fichier .env
# Par exemple: DATABASE_URL="postgresql://user:password@localhost:5432/digital_cleanse_db"
SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dépendance pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
