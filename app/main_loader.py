import joblib
def load_model():
    pipeline = joblib.load(r"D:\Real-Time Fraud Detection Dashboard\fraud_model_complete.pkl")
    return pipeline
