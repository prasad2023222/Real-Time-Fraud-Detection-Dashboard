from pydantic import BaseModel, Field, constr, confloat, conint

StateStr = constr(pattern=r"^[A-Z]{2}$")
CategoryStr = constr(min_length=1, max_length=64)
GenderStr = constr(pattern=r"^[MF]$")

class TranscationInput(BaseModel):
    amt: confloat(gt=0, le=100000)          # cap max amount
    hour: conint(ge=0, le=23)
    state: StateStr
    category: CategoryStr
    gender: GenderStr
    date: conint(ge=1, le=31)
    high_amt: conint(ge=0, le=1)
    user_avg_amt: confloat(gt=0, le=100000)
    deviation_amt: confloat(ge=0, le=100000)
    spending_ratio: confloat(gt=0, le=100)
    last_1h_trans: conint(ge=0, le=500)
    distance: confloat(ge=0, le=20000)