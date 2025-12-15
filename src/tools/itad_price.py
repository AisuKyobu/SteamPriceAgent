import requests
from typing import List, Dict, Union
from schemas.price_result import PriceInfo
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)

BASE_URL = "https://api.isthereanydeal.com"


def game_price(game_ids: List[Dict]) -> List[PriceInfo]:
    """
    Get game price information (current lowest price, historical low, discount, etc.) from ITAD.

    Args:
        game_ids: List of game dicts containing "id" (ITAD game id) and other optional fields

    Returns:
        List[PriceInfo]: List of price information objects for each game
    """

    # Build request URL and parameters
    url = f"{BASE_URL}/games/overview/v2"
    params = {
        "key": settings.ITAD_API_KEY,
        "country": "CN",
        "shops": "61"  # Steam shop ID, adjust if needed
    }

    logger.info(f"Querying price info for game IDs: {game_ids}")

    # Send POST request with game ids
    resp = requests.post(url, params=params, json=game_ids, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    # Process price data
    price_results = []
    price_data_list = data.get("prices", [])
    if not price_data_list:
        logger.info("No price data found for the provided game IDs")
        return price_results

    for game_id in game_ids:
        # Find matching price data for the game
        match_price_data = next((p for p in price_data_list if p["id"] == game_id), None)
        if not match_price_data:
            logger.warning(f"No price data found for game ID: {game_id}")
            continue

        # Extract price details
        current_price = match_price_data["current"]["price"]["amount"]
        historical_low = match_price_data["lowest"]["price"]["amount"]
        discount_percent = match_price_data["current"]["cut"]
        store = match_price_data["current"]["shop"]["name"]

        # Create PriceInfo object
        price_info = PriceInfo(
            current_price=current_price,
            historical_low=historical_low,
            discount_percent=discount_percent,
            store=store
        )
        price_results.append(price_info)

    logger.info(f"Successfully fetched price info for {len(price_results)} games")
    return price_results