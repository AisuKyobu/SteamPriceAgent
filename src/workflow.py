from langchain_deepseek import ChatDeepSeek

from agent.game_entity_resolver import GameEntityResolver
from agent.decision import PurchaseDecisionAgent
from schemas.price_result import PriceInfo
from agent.candidate_selector import CandidateSelectorAgent
from tools.itad_price import game_price
from tools.itad_search import search_games

from config.settings import Settings
from utils.logger import setup_logging,get_logger

logger = get_logger(__name__)

def create_llm():
    return ChatDeepSeek(
        model="deepseek-chat",
        temperature=0.2,
        api_key=Settings.DEEPSEEK_API_KEY
    )


def steam_price_workflow(user_query: str):
    """
    High-level workflow orchestrating:
    - entity resolution
    - candidate selection
    - price aggregation
    - purchase decision
    """
    llm = create_llm()
    
    resolver = GameEntityResolver(llm)
    decision_agent = PurchaseDecisionAgent(llm)
    selector = CandidateSelectorAgent(llm)
    # 1. 搜索候选游戏
    game_entity = resolver.resolve(user_query)
    
    if game_entity.confidence <= 0.2:
        logger.info("No game candidates found")
        return "未找到相关游戏,游戏名错误或游戏不存在"
    
    candidates = search_games(game_entity.game_name)
    
    if not candidates:
        logger.info("No game candidates found")
        return "未找到相关游戏"

    # 2. 候选筛选
    
    selection = selector.select(user_query, candidates)

    if not selection.selected_ids:
        logger.info("No game selected by candidate selector")
        return "无法确定具体游戏"

    # 3. 查询价格
    price_infos = game_price(selection.selected_ids)

    if not price_infos:
        logger.info("No price info available")
        return "暂无价格信息"

    # 4. 决策
    decisions = decision_agent.decide(price_infos)

    return str(decisions)

def main():
    setup_logging()
    user_query = input("请输入你想查询的游戏： ")
    logger.info(steam_price_workflow(user_query))

if __name__ == "__main__":
    main()
