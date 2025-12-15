from langchain.agents import create_agent
from langchain.messages import HumanMessage
from schemas.candidate_selection import CandidateSelection
from pathlib import Path
from typing import Any, Dict, List
import os

from utils.logger import get_logger

logger = get_logger(__name__)

class CandidateSelectorAgent:
    def __init__(self, llm: Any):
        prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "candidate_selector.txt")
        prompt_text = Path(prompt_path).read_text(encoding="utf-8")
        agent = create_agent(
            model=llm,
            system_prompt=prompt_text,
            response_format=CandidateSelection
        )
        self.agent = agent
        
    def select(self, user_query: str,candidates: List[Dict]) -> CandidateSelection:
        """
        candidates: list of dicts with keys: id, title, type
        """
        try:
            result = self.agent.invoke({"messages":
                HumanMessage(f"User query: {user_query}\nCandidates: {candidates}")})
        except Exception as e:
            raise RuntimeError(f"Error during CandidateSelectorAgent making: {str(e)}") from e
        
        structured_response = result.get("structured_response", {})
        logger.info(f"Candidate selection: {structured_response}")

        return structured_response
