import joblib
import os 
from dotenv import load_dotenv

load_dotenv()

MODEL_PATH=os.getenv("MODEL_PATH")

def load_model():
    if not MODEL_PATH:
        raise RuntimeError("MODEL_PATH is not set")
    pipeline=joblib.load(MODEL_PATH)
    return pipeline



    
    #pipeline = joblib.load(r"D:\Real-Time Fraud Detection Dashboard\fraud_model_complete.pkl")
    #return pipeline
