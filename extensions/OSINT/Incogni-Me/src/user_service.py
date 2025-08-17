# app/services/user_service.py
from sqlalchemy.orm import Session
from .models import User
from .crud import create_user, get_user_by_email, add_user_search_identity
from .schemas import UserCreate
from .core.security import verify_password

class UserService:
    def register_user(self, db: Session, user: UserCreate):
        db_user = get_user_by_email(db, user.email)
        if db_user:
            return None
        return create_user(db=db, user=user)

    def authenticate_user(self, db: Session, email: str, password: str):
        user = get_user_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    def add_identity(self, db: Session, user_id: int, identity_value: str):
        return add_user_search_identity(db, user_id, identity_value)

# app/services/scraping/base_scraper.py
from abc import ABC, abstractmethod
from typing import List
from .models import User, DigitalFootprintItem

class WebScraper(ABC):
    @abstractmethod
    def scan(self, user: User, identity: str) -> List[DigitalFootprintItem]:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

# app/services/scraping/google_scraper.py (Exemple simplifié)
import requests
from bs4 import BeautifulSoup
from .models import DigitalFootprintItem, ItemType
from .services.scraping.base_scraper import WebScraper
from .models import User
from typing import List

class GoogleSearchScraper(WebScraper):
    def get_name(self) -> str:
        return "Google Search"

    def scan(self, user: User, identity: str) -> List[DigitalFootprintItem]:
        discovered_items = []
        search_query = f"{identity} site:facebook.com OR site:twitter.com OR site:linkedin.com" # Simplifié

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        try:
            response = requests.get(f"https://www.google.com/search?q={search_query}", headers=headers, timeout=10)
            response.raise_for_status() # Lève une exception pour les codes d'erreur HTTP

            soup = BeautifulSoup(response.text, 'html.parser')
            # Ceci est un sélecteur très basique pour les résultats Google, il peut changer!
            results = soup.select('div.g') 

            for result in results:
                link = result.select_one('a')
                snippet = result.select_one('div.VwiC3b') # Description du résultat

                if link and link.get('href') and not "google.com" in link.get('href'):
                    url = link.get('href')
                    title_elem = result.select_one('h3')
                    title = title_elem.get_text() if title_elem else "No Title"
                    description = snippet.get_text() if snippet else "No Description"

                    item_type = self._determine_item_type_from_url(url)
                    platform_name = self._determine_platform_name_from_url(url)
                    
                    # Note: L'utilisateur n'est pas passé au constructeur, il est attribué par le service
                    discovered_items.append(DigitalFootprintItem(
                        type=item_type,
                        platform=platform_name,
                        url=url,
                        description=f"{title} - {description}",
                        detected_identifier=identity
                    ))
        except requests.exceptions.RequestException as e:
            print(f"Error during Google search for {identity}: {e}")
            # Gérer l'erreur (logger, etc.)
        return discovered_items
    
    # Fonctions utilitaires pour déterminer le type et la plateforme (similaires à l'exemple Java)
    def _determine_item_type_from_url(self, url: str) -> ItemType:
        if "facebook.com" in url or "twitter.com" in url or "linkedin.com" in url or "instagram.com" in url:
            return ItemType.SOCIAL_PROFILE
        if "reddit.com" in url or "forum." in url:
            return ItemType.FORUM_ACCOUNT
        return ItemType.MENTION

    def _determine_platform_name_from_url(self, url: str) -> str:
        if "facebook.com" in url: return "Facebook"
        if "twitter.com" in url: return "X (Twitter)"
        if "linkedin.com" in url: return "LinkedIn"
        if "reddit.com" in url: return "Reddit"
        if "instagram.com" in url: return "Instagram"
        return "Unknown"

# app/services/footprint_service.py
from sqlalchemy.orm import Session
from . import crud, models
from .schemas import DigitalFootprintItemUpdate, DeletionRequestCreate, DeletionRequestUpdate
from .services.scraping.base_scraper import WebScraper
from typing import List, Type

class DigitalFootprintService:
    def __init__(self, scraper_classes: List[Type[WebScraper]]):
        self.scrapers = [cls() for cls in scraper_classes] # Instancier les scrapers

    def perform_scan(self, db: Session, user: models.User):
        identities = crud.get_user_search_identities(db, user.id)
        new_items = []

        if not identities:
            return new_items

        for identity in identities:
            for scraper in self.scrapers:
                try:
                    # Les items retournés n'ont pas encore de user_id, ils seront attribués par le crud.
                    discovered = scraper.scan(user, identity)
                    for item_data in discovered:
                        # Vérifier si l'item existe déjà pour éviter les doublons
                        existing_item = db.query(models.DigitalFootprintItem).filter(
                            models.DigitalFootprintItem.user_id == user.id,
                            models.DigitalFootprintItem.url == item_data.url,
                            models.DigitalFootprintItem.platform == item_data.platform
                        ).first()
                        
                        if not existing_item:
                            # Utiliser crud.create_digital_footprint_item en lui passant l'ID de l'utilisateur
                            # et les données nécessaires.
                            created_item = crud.create_digital_footprint_item(db=db, item=item_data, user_id=user.id)
                            new_items.append(created_item)
                except Exception as e:
                    print(f"Error during scan with {scraper.get_name()} for identity {identity}: {e}")
                    # Log l'erreur

        return new_items
    
    def get_user_footprint_items(self, db: Session, user: models.User):
        return crud.get_digital_footprint_items(db, user.id)

    def update_item_status(self, db: Session, item_id: int, user_id: int, status_update: DigitalFootprintItemUpdate):
        return crud.update_digital_footprint_item_status(db, item_id, user_id, status_update.status)

    def create_deletion_request(self, db: Session, request: DeletionRequestCreate, user_id: int):
        # Vérifier que l'item appartient bien à l'utilisateur avant de créer la requête
        item = crud.get_digital_footprint_item(db, request.item_id, user_id)
        if not item:
            return None # Ou lever une HTTPException
        
        return crud.create_deletion_request(db, request)

    def update_deletion_request(self, db: Session, request_id: int, request_update: DeletionRequestUpdate):
        return crud.update_deletion_request_status(db, request_id, request_update.status, request_update.notes)

    def get_requests_for_item(self, db: Session, item_id: int, user_id: int):
        # Vérifier que l'item appartient bien à l'utilisateur
        item = crud.get_digital_footprint_item(db, item_id, user_id)
        if not item:
            return [] # Ou lever une HTTPException
        return crud.get_deletion_requests_for_item(db, item_id)
