import requests
from typing import Dict, List, Union
import logging

logger = logging.getLogger(__name__)

def get_steam_meta(appid: Union[str, int]) -> Dict:
    """
    获取Steam游戏的meta信息，辅助购买决策

    返回关键信息：
    - 近期评价（用于判断游戏质量）
    - 标签（用于了解游戏类型）
    - 发售时间（用于判断新作/老作）

    Args:
        appid: Steam应用ID

    Returns:
        Dict: 包含核心信息的字典
    """
    try:
        return _fetch_steam_data(appid)
    except Exception as e:
        logger.error(f"Failed to get Steam meta for appid {appid}: {str(e)}")
        return {}

def _fetch_steam_data(appid: Union[str, int]) -> Dict:
    """从Steam Store API获取游戏数据"""
    base_url = "https://store.steampowered.com/api/appdetails/"
    params = {
        'appids': str(appid),
        'l': 'english'  # 获取英文数据
    }

    try:
        # 设置User-Agent避免被屏蔽
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()

        if not data or str(appid) not in data:
            return {}

        app_data = data[str(appid)]

        if not app_data.get('success', False):
            return {}

        return _parse_core_info(app_data['data'])

    except Exception as e:
        logger.error(f"Steam API request failed: {str(e)}")
        return {}

def _parse_core_info(app_data: Dict) -> Dict:
    """解析核心信息，只保留决策需要的字段"""

    # 1. 评价信息 - 结合Metacritic和发行商质量推断
    metacritic = app_data.get('metacritic', {})
    metacritic_score = metacritic.get('score', 0)

    # 发行商质量作为辅助判断（知名发行商通常质量更高）
    publishers = app_data.get('publishers', [])
    is_major_publisher = any(publisher in publishers for publisher in ['Valve', 'Nintendo', 'FromSoftware', 'Square Enix', 'CD Projekt Red'])

    # 综合推断评价等级
    review_summary = _get_review_summary(metacritic_score, is_major_publisher)

    # 2. 游戏类型 - 合并genres和categories，优先保留核心类型
    genres = [g.get('description', '') for g in app_data.get('genres', []) if g.get('description')]
    categories = [c.get('description', '') for c in app_data.get('categories', []) if c.get('description')]

    # 提取关键类型标签
    priority_tags = _get_priority_tags(genres + categories)

    # 3. 发售时间
    release_date = app_data.get('release_date', {}).get('date', '')

    # 4. 游戏名称
    game_name = app_data.get('name', '')

    return {
        'name': game_name,
        'release_date': release_date,
        'reviews': {
            'summary': review_summary,
            'metacritic_score': metacritic_score,
            'confidence': _get_confidence_level(metacritic_score, is_major_publisher)
        },
        'tags': priority_tags
    }

def _get_priority_tags(all_tags: list) -> list:
    """提取优先级标签，保留最重要的类型信息"""
    # 定义优先级标签映射
    priority_mapping = {
        'JRPG': 'JRPG', 'RPG': 'RPG', 'Role-Playing': 'RPG',
        'Action': '动作', 'Adventure': '冒险',
        'Single-player': '单机', 'Multi-player': '多人',
        'Co-op': '合作', 'PvP': '对战',
        'Strategy': '策略', 'Simulation': '模拟',
        'Puzzle': '解谜', 'Platformer': '平台跳跃',
        'Shooter': '射击', 'Racing': '竞速',
        'Turn-Based': '回合制', 'Real-Time': '即时制'
    }

    priority_tags = []
    for tag in all_tags[:8]:  # 取前8个
        for key, value in priority_mapping.items():
            if key.lower() in tag.lower():
                priority_tags.append(value)
                break
        else:
            priority_tags.append(tag)

    return priority_tags[:5]  # 最多返回5个优先标签

def _get_review_summary(metacritic_score: int, is_major_publisher: bool) -> str:
    """结合Metacritic和发行商推断评价等级"""
    # 基于Metacritic的初步等级
    if metacritic_score >= 90:
        base_review = "普遍好评"
    elif metacritic_score >= 80:
        base_review = "特别好评"
    elif metacritic_score >= 70:
        base_review = "多半好评"
    elif metacritic_score >= 60:
        base_review = "褒贬不一"
    else:
        base_review = "评价不佳"

    # 知名发行商加成
    if is_major_publisher and metacritic_score >= 75:
        if metacritic_score >= 90:
            return base_review  # 已经是最高等级
        elif metacritic_score >= 80:
            return "普遍好评"  # 提升一级
        elif metacritic_score >= 70:
            return "特别好评"  # 提升一级

    return base_review

def _get_confidence_level(metacritic_score: int, is_major_publisher: bool) -> str:
    """评估评价的可信度"""
    if metacritic_score >= 80:
        return "高"
    elif metacritic_score >= 60:
        return "中" if is_major_publisher else "中低"
    else:
        return "低"

# 示例使用
if __name__ == "__main__":
    # 测试一个知名游戏的AppID
    try:
        meta = get_steam_meta("620")  # Portal 2
        print(f"游戏: {meta['name']}")
        print(f"发售日期: {meta['release_date']}")
        print(f"评价: {meta['reviews']['summary']}")
        print(f"Metacritic评分: {meta['reviews']['metacritic_score']}")
        print(f"可信度: {meta['reviews']['confidence']}")
        print(f"标签: {', '.join(meta['tags'])}")
    except Exception as e:
        print(f"错误: {e}")