import requests
from datetime import datetime, timedelta
from typing import Union
from schemas.steam_result import SteamInfo
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)

# Steam API 基础配置
STORE_API_BASE = "https://store.steampowered.com/api"
REVIEW_API_BASE = "https://store.steampowered.com/appreviews"

# 评测等级映射
RATING_MAP = {
    "Overwhelmingly Positive": "好评如潮",
    "Very Positive": "特别好评",
    "Positive": "好评",
    "Mostly Positive": "多半好评",
    "Mixed": "褒贬不一",
    "Mostly Negative": "多半差评",
    "Negative": "差评",
    "Very Negative": "特别差评",
    "Overwhelmingly Negative": "差评如潮"
}


def get_steam_info(app_id: Union[str, int]) -> SteamInfo:
    """
    查询Steam游戏信息并返回归一化的结构化数据

    Args:
        app_id: Steam游戏的appID

    Returns:
        SteamInfo: 归一化的游戏信息对象
    """

    logger.info(f"Querying Steam info for App ID: {app_id}")

    # 获取商店基础数据
    store_data = _fetch_store_data(app_id)
    app_id_str = str(app_id)
    game_data = store_data[app_id_str]["data"]

    # 提取核心数据
    tags = _extract_tags(game_data)
    release_type = _judge_release_type(game_data)
    recent_rating = _get_recent_rating(app_id, settings.STEAM_API_KEY)

    logger.info(f"Successfully fetched Steam info for App ID: {app_id}")

    return SteamInfo(
        recent_rating=recent_rating,
        tags=tags,
        release_type=release_type
    )


def _fetch_store_data(app_id: Union[str, int]) -> dict:
    """获取Steam商店的游戏基础数据"""
    url = f"{STORE_API_BASE}/appdetails"
    params = {
        "appids": app_id,
        "l": "schinese",
        "cc": "cn"
    }

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def _extract_tags(game_data: dict) -> list:
    """提取游戏标签（优先玩家标签，其次官方分类）"""
    # 优先获取玩家投票的标签（取前10）
    user_tags = game_data.get("tags", [])
    if user_tags:
        return [tag["description"] for tag in user_tags[:10]]

    # 提取官方类型和分类
    tags = []
    genres = game_data.get("genres", [])
    if genres:
        tags.extend([genre["description"] for genre in genres])

    categories = game_data.get("categories", [])
    if categories:
        tags.extend([category["description"] for category in categories])

    # 去重并取前10
    tags = list(dict.fromkeys(tags))[:10]
    return tags


def _judge_release_type(game_data: dict) -> str:
    """根据发售日期判断是新作还是老作（一年内为新作）"""
    release_date_str = game_data.get("release_date", {}).get("date", "")
    if not release_date_str:
        raise ValueError("Game release date not found")

    release_date_str = release_date_str.replace(" ", "")
    release_date = None

    # 解析中文格式（2011年4月19日）
    try:
        release_date = datetime.strptime(release_date_str, "%Y年%m月%d日")
    except ValueError:
        # 解析ISO格式（2024-12-15）
        try:
            release_date = datetime.strptime(release_date_str, "%Y-%m-%d")
        except ValueError as e:
            raise ValueError(f"Unsupported release date format: {release_date_str}") from e

    # 判定新作/老作
    one_year_ago = datetime.now() - timedelta(days=365)
    return "新作" if release_date >= one_year_ago else "老作"


def _get_recent_rating(app_id: Union[str, int], api_key: str) -> str:
    """获取游戏近期评测等级"""
    url = f"{REVIEW_API_BASE}/{app_id}"
    params = {
        "json": 1,
        "filter": "recent",
        "language": "all",
        "review_type": "all",
        "purchase_type": "all",
        "num_per_page": 0,
        "key": api_key
    }

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    review_data = resp.json()

    if not review_data.get("success"):
        raise ValueError(f"Failed to get review data for App ID: {app_id}")

    review_summary = review_data.get("query_summary", {})
    rating_en = review_summary.get("review_score_desc", "No Rating")
    return RATING_MAP.get(rating_en, "暂无评价")