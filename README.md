## Real‑Time Fraud Detection Dashboard

This project is an end‑to‑end **real‑time fraud monitoring system** built around a production‑style architecture:

- **FastAPI** backend exposing a fraud scoring API backed by a trained ML model
- **PostgreSQL** for persisting scored transactions
- **Streamlit** dashboard for real‑time monitoring and investigation
- **Docker** container for the API for easy deployment

The goal was to build something that looks and behaves like a system you would ship into a real payments / fintech environment, not just a notebook demo.

---

### Project Structure

```text
Real-Time Fraud Detection Dashboard/
├─ app/
│  ├─ main.py                # FastAPI application (fraud scoring API)
│  ├─ schemas.py             # Pydantic request/response models
│  ├─ preprocessor.py        # Feature engineering / preprocessing pipeline
│  ├─ main_loader.py         # Model loading logic (joblib + MODEL_PATH)
│  ├─ database.py            # SQLAlchemy engine / DB configuration
│  ├─ dashboard.py           # Streamlit dashboard (monitoring + KPIs)
│  ├─ transaction_checker.py # Streamlit helper to send test transactions to the API
│  └─ test_transcation.py    # Basic tests / experimentation around transactions
├─ fraud_final_model_complete.pkl  # Serialized ML pipeline (primary model)
├─ fraud_model_complete.pkl        # Alternate / earlier model version
├─ Business_Value.md         # Business impact narrative (for recruiters/stakeholders)
├─ requirements.txt          # Python dependencies
├─ Dockerfile                # Container image for the FastAPI service
├─ .env                      # Local configuration (DB_URL, MODEL_PATH, API_KEY, etc.)
├─ index.py                  # Vercel / entrypoint export for FastAPI app
└─ README.md                 # Project documentation (this file)
```

---

### 1. High‑Level Architecture

- **Fraud Detection API (`app/main.py`)**
  - Implements a **FastAPI** service with:
    - `GET /home` – health check
    - `POST /predict` – scores a single transaction
  - Loads a serialized model pipeline (`fraud_final_model_complete.pkl`) via `app/main_loader.py`.
  - Validates request payloads using Pydantic schemas (`app/schemas.py`).
  - Applies a preprocessing pipeline (`app/preprocessor.py`) before scoring.
  - Persists every scored transaction into a **PostgreSQL** table via SQLAlchemy (`app/database.py`).
  - Protects the scoring endpoint with an optional **API key** (`API_KEY` header).

- **Model Serving**
  - The trained model pipeline is stored as a pickle file at the project root (for example `fraud_final_model_complete.pkl`).
  - `MODEL_PATH` is configurable via environment variable (see **Environment configuration**).

- **Analytics Dashboard (`app/dashboard.py`)**
  - Built with **Streamlit** for quick iteration and rich UI.
  - Two main views:
    - **Landing / Hero** – a product‑style marketing view that communicates value to stakeholders.
    - **Monitor** – real‑time fraud analytics driven from the `transactions` table:
      - Overall KPIs: total transactions, fraud volume, normal volume, fraud rate.
      - Model metrics (F1, precision, recall, ROC AUC) from the stored pipeline metadata, tuned for an **imbalanced dataset**:
        - `F1` ≈ **0.850**
        - `Precision` ≈ **0.885**
        - `Recall` ≈ **0.817**
        - `ROC AUC` ≈ **0.845**
      - Distribution visualizations powered by Plotly:
        - Fraud vs normal breakdown
        - Fraud by state
        - Fraud probability histogram
      - Recent transactions table for detailed investigation.
    - **Check a transaction** – an embedded tool (implemented in `app/transaction_checker.py`) to send ad‑hoc transactions to the `/predict` API and inspect the response.

- **Persistence Layer**
  - PostgreSQL via SQLAlchemy.
  - A `transactions` table stores features and model outputs for each scored transaction, enabling:
    - Historical analysis and drift detection.
    - KPI computation.
    - Ad‑hoc querying for investigations.

- **Containerization (`Dockerfile`)**
  - Production‑oriented Python 3.11 image.
  - Installs system dependencies for **psycopg2** and numerical libraries.
  - Installs application dependencies from `requirements.txt`.
  - Runs the FastAPI app behind Uvicorn with multiple workers:
    - `uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --workers 4`

---

### 2. Key Features

- **Real‑time scoring API**
  - Single `/predict` endpoint that:
    - Preprocesses incoming transactions.
    - Produces `fraud_prediction` and `fraud_probability`.
    - Logs a unique `request_id` per call for observability.
    - Optionally enforces API key authentication (`x-api-key`).
  - Designed to be easily fronted by a gateway or message bus in a larger system.

- **Production‑style data capture**
  - Every scored transaction is written to PostgreSQL, which:
    - Provides an auditable ledger of model decisions.
    - Supports building offline reports and retraining datasets.

- **Operator‑friendly UI**
  - Streamlit dashboard optimized for **risk / data teams**:
    - At‑a‑glance KPIs and model performance.
    - Visual breakdowns that highlight hotspots (e.g., fraud by state).
    - Interactive exploration of recent transactions.
    - Built‑in “what‑if” tester for single transactions.

- **Configurable, environment‑driven setup**
  - Core runtime behavior is driven from `.env`:
    - Database connection string (`DB_URL`).
    - Model path (`MODEL_PATH`).
    - API key (`API_KEY`).
  - This allows the same codebase to be reused across local, staging, and production without changes.

---

### 3. Technology Stack

- **Backend**
  - Python 3.11
  - FastAPI
  - Uvicorn
  - Pydantic
  - SQLAlchemy
  - psycopg2

- **ML / Data**
  - scikit‑learn
  - pandas
  - numpy
  - joblib (for model serialization)

- **Dashboard / Visualization**
  - Streamlit
  - Plotly Express

- **Infra / Tooling**
  - Docker (containerized API)
  - PostgreSQL

---

### 4. Getting Started (Local)

#### 4.1. Clone and create a virtual environment

```bash
git clone <your-repo-url> "Real-Time Fraud Detection Dashboard"
cd "Real-Time Fraud Detection Dashboard"

python -m venv venv
venv\Scripts\activate  # on Windows

pip install --upgrade pip
pip install -r requirements.txt
```

#### 4.2. Environment configuration

Create a `.env` file at the project root (if not already present):

```env
DB_URL=postgresql+psycopg2://username:password@localhost:5432/fraud_db
MODEL_PATH=fraud_final_model_complete.pkl
API_KEY=your-secure-api-key
```

- `DB_URL` – SQLAlchemy‑compatible connection string to PostgreSQL.
- `MODEL_PATH` – path to the serialized model file. For local development, keeping `fraud_final_model_complete.pkl` at the project root and using a relative path works well.
- `API_KEY` – optional; if set, clients must send `x-api-key` with this value to call `/predict`.

#### 4.3. Start the API

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The health check is available at:

- `GET http://localhost:8000/home`

Sample `curl` for prediction:

```bash
curl -X POST "http://localhost:8000/predict" ^
  -H "Content-Type: application/json" ^
  -H "x-api-key: your-secure-api-key" ^
  -d "{\"amt\": 123.45, \"state\": \"CA\", \"category\": \"shopping\", \"gender\": \"F\", \"hour\": 14}"
```

#### 4.4. Start the dashboard

In a separate terminal with the same virtual environment:

```bash
streamlit run app/dashboard.py
```

The dashboard will be available at `http://localhost:8501`.

Make sure your PostgreSQL instance is running and `DB_URL` is correct; otherwise, the dashboard will not be able to load transaction data.

---

### 5. Running with Docker (API)

The included `Dockerfile` is designed for the API service:

```bash
docker build -t fraud-api .

docker run --rm -p 8000:8000 ^
  -e PORT=8000 ^
  -e MODEL_PATH=/app/fraud_final_model_complete.pkl ^
  -e DB_URL=postgresql+psycopg2://username:password@host.docker.internal:5432/fraud_db ^
  -e API_KEY=your-secure-api-key ^
  fraud-api
```

Notes:

- `host.docker.internal` allows the container to connect to a database running on the host machine (Windows/macOS).
- The model file is copied into the image at `/app` by the Dockerfile, so `MODEL_PATH=/app/fraud_final_model_complete.pkl` is appropriate in containerized deployments.

You can then point remote clients or the Streamlit app at the containerized API (e.g., `API_URL=http://localhost:8000`).

---

### 6. Design Choices and Trade‑offs

- **FastAPI for serving**
  - Chosen for its performance, async capabilities, and excellent OpenAPI integration.
  - Works well as a microservice that can be scaled independently of the UI.

- **Streamlit for the dashboard**
  - Prioritized **development velocity** and **interactivity** over a fully custom frontend.
  - Ideal for internal risk / data teams and iterative experimentation.

- **PostgreSQL as the system of record**
  - A relational store provides strong guarantees for financial data and is a familiar tool for analysts.
  - The `transactions` table doubles as an audit log and a source for retraining data.

- **Serialized scikit‑learn pipeline**
  - Keeps the training code outside the serving path while allowing a straightforward `joblib.load` at inference time.
  - The pipeline can include both preprocessing and the final estimator.

- **Environment‑first configuration**
  - Everything that changes by environment (DB, model path, API keys) is configured via `.env` / env vars.
  - This pattern translates directly to Docker, CI/CD, and cloud environment variables.

---

### 7. How This Reflects My Experience

This project is intentionally structured to resemble how production fraud systems are built:

- Clear separation between **serving**, **analytics**, and **storage**.
- Environment‑driven configuration with minimal hard‑coded paths.
- Containerization for reproducible deployments.
- A dashboard focused on **operational KPIs** (fraud rate, distribution by geography/category, probability distribution) that risk teams actually care about.

It is designed so that:

- It can be extended with additional models or signals (e.g., device fingerprints, velocity features).
- It can be wired into a message queue or event bus for true streaming inference.
- It can be integrated into existing authentication, observability, and CI/CD pipelines with minimal friction.

If you’re evaluating this repository, I recommend starting by:

- Reviewing `app/main.py` for the API surface and data flow.
- Inspecting `app/dashboard.py` for how business‑level insights are surfaced.
- Looking at `Dockerfile` and `.env` usage to see how the service would be deployed and configured in a real environment.
