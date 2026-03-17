FROM python:3.11-slim AS base

WORKDIR /app

# System deps for psycopg2 and building some libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project (code + model)
COPY . .

# Expose API port
EXPOSE 8000

# Use environment PORT if provided (Heroku/Render), else 8000
ENV PORT=8000

# Production-style Uvicorn command
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --workers 4"]