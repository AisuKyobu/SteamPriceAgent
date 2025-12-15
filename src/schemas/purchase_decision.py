from pydantic import BaseModel, Field
from typing import Literal

class PurchaseDecision(BaseModel):
    recommendation: Literal["buy", "wait"] = Field(...,description="Buy recommendation: 'buy' or 'wait'")
    reason: str = Field(...,description="Detailed explanation for the recommendation")
    confidence: float = Field(...,ge=0,le=1,description="Confidence level between 0 and 1")