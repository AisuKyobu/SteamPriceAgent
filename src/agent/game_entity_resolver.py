from langchain.agents import create_agent
from langchain.messages import HumanMessage
from schemas.game_entity import GameEntity
from pathlib import Path
from typing import Any
from config.settings import Settings
from utils.logger import get_logger
import os

logger = get_logger(__name__)
#查询游戏名称的实体解析器
class GameEntityResolver:
    def __init__(self, llm: Any):
        prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "game_entity_resolver.txt")
        prompt_text = Path(prompt_path).read_text(encoding="utf-8")
        agent = create_agent(
            model=llm,
            system_prompt=prompt_text,
            response_format=GameEntity
        )
        self.agent = agent
        
    def resolve(self, user_query: str) -> GameEntity:
        try:
            result = self.agent.invoke({"messages":HumanMessage(user_query)})
        except Exception as e:
            raise RuntimeError(f"Error during game name recognition for query '{user_query}': {str(e)}") from e
        
        structured_response = result.get("structured_response", {})
        logger.info(f"Resolved game entity: {structured_response}")
        return structured_response