import requests
from typing import List, Dict

from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)

BASE_URL = "https://api.isthereanydeal.com"


def search_games(keyword: str, limit: int = 10) -> List[Dict]:
    """
    Search games by keyword from ITAD.

    Returns a list of:
    {
        id: str,
        title: str,
        type: str
    }
    """
    url = f"{BASE_URL}/games/search/v1"

    params = {
        "key": settings.ITAD_API_KEY,
        "title": keyword,
        "limit": limit
    }

    logger.info(f"Searching ITAD games with keyword: {keyword}")

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()

    data = resp.json()

    results = []
    for item in data:
        results.append(
            {
                "id": item["id"],
                "title": item["title"],
                "type": item.get("type", "game"),
            }
        )

    logger.info(f"Found {len(results)} candidates from ITAD")

    return results
