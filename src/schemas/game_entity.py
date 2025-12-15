from pydantic import BaseModel, Field


class GameEntity(BaseModel):
    game_name: str = Field(..., description="Canonical Steam game name")
    is_dlc: bool = Field(False, description="Whether this refers to a DLC")
    confidence: float = Field(..., ge=0, le=1)
