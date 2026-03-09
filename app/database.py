from sqlalchemy import create_engine
DB_url="postgresql://postgres:prasad%400203@localhost:5432/fraud_db"

engine=create_engine(DB_url)