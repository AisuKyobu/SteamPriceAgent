from pydantic import BaseModel, Field
from typing import List, Literal

class CandidateSelection(BaseModel):
    ''' single：用户明确问某一作
        series：用户问“系列 / 全部”
        latest：用户模糊，但更可能关心最新作'''
    selection_type: Literal["single", "series", "latest"] = Field(..., description="Type of candidate selection")
    selected_ids: List[str] = Field(..., description="List of selected game IDs")
    reason: str = Field(..., description="Detailed explanation for your selection")
