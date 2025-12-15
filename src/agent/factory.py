from langchain_deepseek import ChatDeepSeek

from agent.game_entity_resolver import GameEntityResolver
from agent.candidate_selector import CandidateSelectorAgent
from agent.decision import PurchaseDecisionAgent
from config.settings import Settings


def create_llm():
    return ChatDeepSeek(
        model="deepseek-chat",
        temperature=0.2,
        api_key=Settings.DEEPSEEK_API_KEY
    )


def create_agents():
    llm = create_llm()

    return {
        "resolver": GameEntityResolver(llm),
        "selector": CandidateSelectorAgent(llm),
        "decision": PurchaseDecisionAgent(llm),
    }
