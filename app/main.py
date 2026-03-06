from fastapi import FastAPI, HTTPException
from app.schemas import TranscationInput
from app.main_loader import load_model
from app.preprocessor import preprocess_input
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pipeline = load_model()
model = pipeline["model"]

app = FastAPI(title="Fraud Detection API", version="1.0")

@app.get("/home")
def health_check():
    return {"status": "Api is running"}

@app.post("/predict")
def predict_fraud(transcation: TranscationInput):
    try:
        logger.info(f"received transcation: {transcation}")
        df = preprocess_input(transcation.dict(), pipeline)
        probability = model.predict_proba(df)[0][1]
        prediction = int(probability > 0.4)

        return {
            "fraud_probability": float(probability),
            "is_fraud": prediction,
        }
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed")
