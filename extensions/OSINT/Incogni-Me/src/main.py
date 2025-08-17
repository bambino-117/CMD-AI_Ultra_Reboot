# extensions/incogni_me/src/main.py
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from src import models, crud, schemas
from src.database import engine, Base, get_db
from src.security import create_access_token, decode_access_token, get_password_hash
from src.core.config import settings
from .user_service import UserService
from .services.footprint_service import DigitalFootprintService
from .services.scraping.google_scraper import GoogleSearchScraper
# Importez ici tous vos scrapers

# Création des tables de la BDD (à faire une seule fois ou via des migrations)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Digital Cleanse API")

# Initialisation des services avec les dépendances nécessaires
# IMPORTANT: Passez vos classes de scrapers ici.
footprint_service = DigitalFootprintService(scraper_classes=[GoogleSearchScraper]) 
user_service = UserService()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dépendance pour l'utilisateur actuel
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = decode_access_token(token)
    if token_data is None:
        raise credentials_exception
    user = crud.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

# --- Endpoints d'Authentification ---
@app.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = user_service.register_user(db, user)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Email already registered")
    return db_user

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- Endpoints Utilisateur ---
@app.get("/users/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@app.post("/users/me/identities", response_model=schemas.UserResponse)
def add_user_identity(identity: schemas.SearchIdentityAdd, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_service.add_identity(db, current_user.id, identity.identity_value)
    # Recharger l'utilisateur pour avoir les identités à jour
    db.refresh(current_user) 
    return current_user


# --- Endpoints Empreinte Numérique et Scan ---
@app.post("/footprint/scan", response_model=List[schemas.DigitalFootprintItemResponse])
def start_scan(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Lance un scan de la présence numérique pour l'utilisateur connecté."""
    new_items = footprint_service.perform_scan(db, current_user)
    return new_items

@app.get("/footprint/items", response_model=List[schemas.DigitalFootprintItemResponse])
def get_user_footprint(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Récupère tous les éléments de l'empreinte numérique de l'utilisateur."""
    items = footprint_service.get_user_footprint_items(db, current_user)
    return items

@app.patch("/footprint/items/{item_id}", response_model=schemas.DigitalFootprintItemResponse)
def update_item_status(item_id: int, update_data: schemas.DigitalFootprintItemUpdate, 
                       current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Met à jour le statut d'un élément de l'empreinte numérique."""
    item = footprint_service.update_item_status(db, item_id, current_user.id, update_data)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found or not owned by user")
    return item

# --- Endpoints Requêtes de Suppression ---
@app.post("/footprint/items/{item_id}/request", response_model=schemas.DeletionRequestResponse)
def create_deletion_request(item_id: int, request_data: schemas.DeletionRequestCreate,
                            current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Crée une nouvelle demande de suppression ou de gestion pour un élément."""
    if request_data.item_id != item_id: # S'assurer de la cohérence de l'ID
        raise HTTPException(status_code=400, detail="Item ID in path and body do not match")

    request = footprint_service.create_deletion_request(db, request_data, current_user.id)
    if not request:
        raise HTTPException(status_code=404, detail="Item not found or not owned by user")
    return request

@app.get("/footprint/items/{item_id}/requests", response_model=List[schemas.DeletionRequestResponse])
def get_item_deletion_requests(item_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Récupère toutes les demandes de suppression/gestion pour un élément donné."""
    requests = footprint_service.get_requests_for_item(db, item_id, current_user.id)
    return requests

@app.patch("/requests/{request_id}", response_model=schemas.DeletionRequestResponse)
def update_request_status(request_id: int, update_data: schemas.DeletionRequestUpdate,
                          current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Met à jour le statut d'une demande de suppression."""
    # Note: Dans une vraie application, vous voudriez aussi vérifier que l'utilisateur a le droit de modifier cette requête
    request = footprint_service.update_deletion_request(db, request_id, update_data)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    return request
