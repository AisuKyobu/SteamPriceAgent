import requests
from schemas.price_result import PriceInfo
from dotenv import load_dotenv

load_dotenv()


class IsAnyDealClient:
    BASE_URL = "https://api.isthereanydeal.com"

    def __init__(self):
        if not self.api_key:
            raise RuntimeError("IsThereAnyDeal_API_KEY not set")

    def get_price_info(self, game_name: str) -> PriceInfo:
        """
        Query isanydeal and return normalized price info.
        """
        # 1. 搜索 plain（isanydeal 的唯一标识）
        search_resp = requests.get(
            f"{self.BASE_URL}/games/search/v1",
            params={
                "key": self.api_key,
                "q": game_name,
            },
            timeout=10,
        )
        search_resp.raise_for_status()
        search_data = search_resp.json()

        if not search_data:
            raise ValueError(f"No game found for: {game_name}")

        plain = search_data[0]["plain"]

        # 2. 查询价格
        price_resp = requests.get(
            f"{self.BASE_URL}/games/prices/v2",
            params={
                "key": self.api_key,
                "plains": plain,
                "shops": "steam",
            },
            timeout=10,
        )
        price_resp.raise_for_status()
        price_data = price_resp.json()

        game_price = price_data[plain][0]

        return PriceInfo(
            current_price=game_price["price"]["amount"],
            historical_low=game_price["lowest"]["amount"],
            discount_percent=game_price["price"]["cut"],
            store="Steam",
        )
