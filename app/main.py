from fastapi import FastAPI, HTTPException
from app.schemas import TranscationInput
from app.main_loader import load_model
from app.preprocessor import preprocess_input
import logging
from app.database import engine
import pandas as pd
from fastapi import Depends,Header,Request
import uuid

import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

def verify_api_key(x_api_key:str=Header(None)):
    if not API_KEY:
        return 

    if x_api_key!=API_KEY:
        raise HTTPException(status_code=401,detail="Invalid API KEY")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pipeline = load_model()
model = pipeline["model"]



app = FastAPI(title="Fraud Detection API", version="1.0")

@app.get("/home")
def health_check():
    return {"status": "Api is running"}

@app.post("/predict")
def predict_fraud(transaction: TranscationInput,request=Request,_:None=Depends(verify_api_key)):
    request_id=str(uuid.uuid4())
    try:
        logger.info("request_id=%s ip=%s playload=%s",request_id,request.clinet.host,transaction.dict())


        processed = preprocess_input(transaction.dict(), pipeline)
        prediction = model.predict(processed)[0]
        probability = model.predict_proba(processed)[0][1]

        record = {
            "amt": transaction.amt,
            "state": transaction.state,
            "category": transaction.category,
            "gender": transaction.gender,
            "hour": transaction.hour,
            "fraud_prediction": int(prediction),
            "fraud_probability": float(probability)
            }

        df = pd.DataFrame([record])

        df.to_sql("transactions", engine, if_exists="append", index=False)

        return {
            "request_id":request_id,
            "fraud_prediction": int(prediction),
            "fraud_probability": float(probability)
            }



    except Exception as e:
        logger.exception("request_id=%s Prediction error:",request_id)
        raise HTTPException(status_code=500, detail="Prediction failed")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)