from langchain.agents import create_agent
from langchain.messages import HumanMessage
from schemas.price_result import PriceInfo
from schemas.purchase_decision import PurchaseDecision
from pathlib import Path
from typing import Any
from dotenv import load_dotenv
import os

load_dotenv()

class PurchaseDecisionAgent:
    def __init__(self, llm: Any):
        prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "decision.txt")
        prompt_text = Path(prompt_path).read_text(encoding="utf-8")
        agent = create_agent(
            model=llm,
            system_prompt=prompt_text,
            response_format=PurchaseDecision
        )
        self.agent = agent
        
    def decide(self, price_info: PriceInfo) -> dict:
        try:
            result = self.agent.invoke({"messages":HumanMessage(price_info.model_dump_json())})
        except Exception as e:
            raise RuntimeError(f"Error during purchase decision making: {str(e)}") from e
        
        structured_response = result.get("structured_response", {})

        return structured_response
