import numpy as np 
import pandas as pd

def preprocess_input(input_data:dict,pipeline:dict):
    state_te=pipeline["state_te"]
    category_te=pipeline["category_te"]
    global_mean=pipeline["global_mean"]
    features=pipeline["feature_columns"]

    df=pd.DataFrame([input_data])

    df["log_amount"]=np.log1p(df["amt"])
    df["is_night"]=df["hour"].apply(lambda x: 1 if x>=22 or x<=5 else 0)

    # Target encoding
    df["state_te"] = df["state"].map(state_te).fillna(global_mean)
    df["category_te"] = df["category"].map(category_te).fillna(global_mean)

    # One-hot gender
    df["gender_M"] = 1 if df["gender"].iloc[0] == "M" else 0

    # Drop raw columns
    df = df.drop(["state", "category", "gender"], axis=1)

    
    print("MODEL FEATURES:", features)

    # Ensure column order matches training
    df = df[features]

    return df



