import requests
from bs4 import BeautifulSoup
from ...models import DigitalFootprintItem, ItemType, User
from .base_scraper import WebScraper
from typing import List

class GoogleSearchScraper(WebScraper):
    def get_name(self) -> str:
        return "Google Search"

    def scan(self, user: User, identity: str) -> List[DigitalFootprintItem]:
        discovered_items = []
        search_query = f"{identity} site:facebook.com OR site:twitter.com OR site:linkedin.com"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        try:
            response = requests.get(f"https://www.google.com/search?q={search_query}", headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.select('div.g')

            for result in results:
                link = result.select_one('a')
                snippet = result.select_one('div.VwiC3b')

                if link and link.get('href') and not "google.com" in link.get('href'):
                    url = link.get('href')
                    title_elem = result.select_one('h3')
                    title = title_elem.get_text() if title_elem else "No Title"
                    description = snippet.get_text() if snippet else "No Description"

                    item_type = self._determine_item_type_from_url(url)
                    platform_name = self._determine_platform_name_from_url(url)
                    
                    discovered_items.append(DigitalFootprintItem(
                        type=item_type,
                        platform=platform_name,
                        url=url,
                        description=f"{title} - {description}",
                        detected_identifier=identity
                    ))
        except requests.exceptions.RequestException as e:
            print(f"Error during Google search for {identity}: {e}")
        return discovered_items
    
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
