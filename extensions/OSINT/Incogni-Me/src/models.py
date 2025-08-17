# app/models.py
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Table
from sqlalchemy.orm import relationship
from src.database import Base
import datetime
import enum

# Enums (Python enums, mappés à des types de BDD)
class ItemType(str, enum.Enum):
    SOCIAL_PROFILE = "SOCIAL_PROFILE"
    FORUM_ACCOUNT = "FORUM_ACCOUNT"
    ECOMMERCE = "ECOMMERCE"
    MENTION = "MENTION"
    DATA_BREACH = "DATA_BREACH"
    NEWSLETTER = "NEWSLETTER"

class ItemStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    POTENTIAL_RISK = "POTENTIAL_RISK"
    RESOLVED = "RESOLVED"
    PENDING_DELETION = "PENDING_DELETION"
    IGNORED = "IGNORED"

class RequestType(str, enum.Enum):
    DELETE = "DELETE"
    DEACTIVATE = "DEACTIVATE"
    UPDATE_PRIVACY = "UPDATE_PRIVACY"
    UNSUBSCRIBE = "UNSUBSCRIBE"
    REPORT_HACKED = "REPORT_HACKED"
    RECTIFY_DATA = "RECTIFY_DATA"

class RequestStatus(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    MANUAL_REQUIRED = "MANUAL_REQUIRED"


# Table d'association pour les identifiants de recherche de l'utilisateur
user_search_identities = Table(
    'user_search_identities',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('identity_value', String, primary_key=True)
)


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now, nullable=False)

    # Relation Many-to-Many via table d'association
    search_identities = relationship(
        "UserSearchIdentity",
        collection_class=set,
        back_populates="user",
        cascade="all, delete-orphan"
    )

    digital_footprint_items = relationship("DigitalFootprintItem", back_populates="user", cascade="all, delete-orphan")

class UserSearchIdentity(Base):
    __tablename__ = "user_search_identities"
    __table_args__ = {'extend_existing': True}

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    identity_value = Column(String, primary_key=True)

    user = relationship("User", back_populates="search_identities")


class DigitalFootprintItem(Base):
    __tablename__ = "digital_footprint_items"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    type = Column(Enum(ItemType), nullable=False)
    platform = Column(String, nullable=False)
    url = Column(String, nullable=False, unique=True) # Une URL unique par utilisateur pourrait être pertinente
    description = Column(String)
    detected_identifier = Column(String)
    status = Column(Enum(ItemStatus), default=ItemStatus.ACTIVE, nullable=False)
    detected_at = Column(DateTime, default=datetime.datetime.now, nullable=False)
    last_checked_at = Column(DateTime, default=datetime.datetime.now, nullable=False)

    user = relationship("User", back_populates="digital_footprint_items")
    deletion_requests = relationship("DeletionRequest", back_populates="item", cascade="all, delete-orphan")


class DeletionRequest(Base):
    __tablename__ = "deletion_requests"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("digital_footprint_items.id"), nullable=False)
    
    request_type = Column(Enum(RequestType), nullable=False)
    status = Column(Enum(RequestStatus), default=RequestStatus.PENDING, nullable=False)
    notes = Column(String)
    requested_at = Column(DateTime, default=datetime.datetime.now, nullable=False)
    last_updated_at = Column(DateTime, default=datetime.datetime.now, nullable=False)

    item = relationship("DigitalFootprintItem", back_populates="deletion_requests")
