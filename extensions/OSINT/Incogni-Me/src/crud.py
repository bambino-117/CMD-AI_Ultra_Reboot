# extensions/incogni_me/src/crud.py
from typing import Optional
from sqlalchemy.orm import Session
from src.models import User, DigitalFootprintItem, DeletionRequest, ItemStatus, RequestStatus, ItemType, RequestType, UserSearchIdentity
from src.schemas import UserCreate, DigitalFootprintItemCreate, DigitalFootprintItemUpdate, DeletionRequestCreate, DeletionRequestUpdate
from src.core.security import get_password_hash

# --- Opérations Utilisateur ---
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def add_user_search_identity(db: Session, user_id: int, identity_value: str):
    user = get_user_by_id(db, user_id)
    if user:
        # Vérifier si l'identité existe déjà pour cet utilisateur
        existing_identity = db.query(UserSearchIdentity).filter(
            UserSearchIdentity.user_id == user_id,
            UserSearchIdentity.identity_value == identity_value
        ).first()
        if not existing_identity:
            new_identity = UserSearchIdentity(user_id=user_id, identity_value=identity_value)
            db.add(new_identity)
            db.commit()
            db.refresh(new_identity)
            return new_identity
    return None

def get_user_search_identities(db: Session, user_id: int) -> set[str]:
    user = get_user_by_id(db, user_id)
    if user:
        return {identity.identity_value for identity in user.search_identities}
    return set()

# --- Opérations Empreinte Numérique ---
def create_digital_footprint_item(db: Session, item: DigitalFootprintItemCreate, user_id: int):
    db_item = DigitalFootprintItem(**item.dict(), user_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_digital_footprint_items(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(DigitalFootprintItem).filter(DigitalFootprintItem.user_id == user_id).offset(skip).limit(limit).all()

def get_digital_footprint_item(db: Session, item_id: int, user_id: int):
    return db.query(DigitalFootprintItem).filter(DigitalFootprintItem.id == item_id, DigitalFootprintItem.user_id == user_id).first()

def update_digital_footprint_item_status(db: Session, item_id: int, user_id: int, new_status: ItemStatus):
    db_item = get_digital_footprint_item(db, item_id, user_id)
    if db_item:
        db_item.status = new_status
        db.commit()
        db.refresh(db_item)
    return db_item

# --- Opérations Requêtes de Suppression ---
def create_deletion_request(db: Session, request: DeletionRequestCreate):
    db_request = DeletionRequest(
        item_id=request.item_id,
        request_type=request.request_type,
        status=RequestStatus.PENDING # Toujours démarrer en PENDING
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

def get_deletion_requests_for_item(db: Session, item_id: int):
    return db.query(DeletionRequest).filter(DeletionRequest.item_id == item_id).all()

def update_deletion_request_status(db: Session, request_id: int, new_status: RequestStatus, notes: Optional[str] = None):
    db_request = db.query(DeletionRequest).filter(DeletionRequest.id == request_id).first()
    if db_request:
        db_request.status = new_status
        if notes is not None:
            db_request.notes = notes
        db.commit()
        db.refresh(db_request)
    return db_request
