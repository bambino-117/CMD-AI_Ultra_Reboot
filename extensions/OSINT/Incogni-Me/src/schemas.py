# app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Set
from datetime import datetime
from src.models import ItemType, ItemStatus, RequestType, RequestStatus

# --- Utilisateur ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    search_identities: Set[str] = set() # Pour affichage
    
    class Config:
        from_attributes = True # Ancien orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- Identifiants de Recherche ---
class SearchIdentityAdd(BaseModel):
    identity_value: str

# --- Élément d'Empreinte Numérique ---
class DigitalFootprintItemCreate(BaseModel):
    type: ItemType
    platform: str
    url: str
    description: Optional[str] = None
    detected_identifier: Optional[str] = None

class DigitalFootprintItemResponse(BaseModel):
    id: int
    user_id: int
    type: ItemType
    platform: str
    url: str
    description: Optional[str] = None
    detected_identifier: Optional[str] = None
    status: ItemStatus
    detected_at: datetime
    last_checked_at: datetime

    class Config:
        from_attributes = True

class DigitalFootprintItemUpdate(BaseModel):
    status: ItemStatus # Pour mettre à jour le statut d'un item

# --- Requête de Suppression/Gestion ---
class DeletionRequestCreate(BaseModel):
    item_id: int
    request_type: RequestType

class DeletionRequestResponse(BaseModel):
    id: int
    item_id: int
    request_type: RequestType
    status: RequestStatus
    notes: Optional[str] = None
    requested_at: datetime
    last_updated_at: datetime

    class Config:
        from_attributes = True

class DeletionRequestUpdate(BaseModel):
    status: RequestStatus
    notes: Optional[str] = None
