# schemas/steam_result.py
from pydantic import BaseModel, Field
from typing import List, Literal, Optional

# 定义 Steam 近期评价的字面量类型（限定可选值，提升数据规范性）
SteamRating = Literal[
    "好评如潮", "特别好评", "好评", "多半好评", "褒贬不一",
    "多半差评", "差评", "特别差评", "差评如潮", "暂无评价"
]

# 定义发售类型的字面量类型
ReleaseType = Literal["新作", "老作", "暂无数据"]

class SteamInfo(BaseModel):
    """Steam game information model"""
    recent_rating: SteamRating = Field(...,description="Steam recent review rating level")
    tags: List[str] = Field(...,description="List of Steam user-voted game tags, like:['解谜', '合作', '科幻']")
    release_type: ReleaseType = Field(...,description="Game release type, determined by release date：新作（近1年）、老作（超1年）、暂无数据")
    store: Literal["Steam"] = Field(default="Steam",description="Steam store")