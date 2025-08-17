from sqlalchemy.orm import Session
from .. import crud, models
from ..schemas import DigitalFootprintItemUpdate, DeletionRequestCreate, DeletionRequestUpdate
from .scraping.base_scraper import WebScraper
from typing import List, Type

class DigitalFootprintService:
    def __init__(self, scraper_classes: List[Type[WebScraper]]):
        self.scrapers = [cls() for cls in scraper_classes]

    def perform_scan(self, db: Session, user: models.User):
        identities = crud.get_user_search_identities(db, user.id)
        new_items = []

        if not identities:
            return new_items

        for identity in identities:
            for scraper in self.scrapers:
                try:
                    discovered = scraper.scan(user, identity)
                    for item_data in discovered:
                        existing_item = db.query(models.DigitalFootprintItem).filter(
                            models.DigitalFootprintItem.user_id == user.id,
                            models.DigitalFootprintItem.url == item_data.url,
                            models.DigitalFootprintItem.platform == item_data.platform
                        ).first()
                        
                        if not existing_item:
                            created_item = crud.create_digital_footprint_item(db=db, item=item_data, user_id=user.id)
                            new_items.append(created_item)
                except Exception as e:
                    print(f"Error during scan with {scraper.get_name()} for identity {identity}: {e}")

        return new_items
