from pydantic import BaseModel, Field

class PriceInfo(BaseModel):
    current_price: float = Field(..., description="Current lowest price")
    historical_low: float = Field(..., description="Historical lowest price")
    discount_percent: int = Field(..., ge=0, le=100)
    store: str = Field(..., description="Store name, e.g. Steam")
