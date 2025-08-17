from src.database import Base, engine

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Base de données initialisée avec succès!")

if __name__ == "__main__":
    init_db()
