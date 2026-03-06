from pydantic import BaseModel,Field

class TranscationInput(BaseModel):
    
    amt: float = Field(..., gt=0)
    hour: int = Field(..., ge=0, le=23)

    state: str
    category: str
    gender: str

    date: int
    high_amt: int
    user_avg_amt: float
    deviation_amt: float
    spending_ratio: float
    last_1h_trans: int
    distance: float