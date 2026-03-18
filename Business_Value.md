## Business Value – Real‑Time Fraud Detection Dashboard

### 1. Problem This Solves

Financial institutions, payment processors, and marketplaces lose significant revenue to:

- **Card‑not‑present fraud** and account takeovers
- **False positives** that block good customers
- **Slow incident response**, where fraud is discovered hours or days after it happens

Most teams already have models somewhere, but:

- Scores are not **operationalized** in real time.
- There is no **single place** for risk / ops to monitor what the model is doing.
- Data for **audit, RCA, and retraining** is spread across logs, databases, and notebooks.

This project turns a raw fraud model into a **production‑style, observable service** that risk, data, and engineering teams can actually use day‑to‑day.

---

### 2. Concrete Business Value

- **Reduce realized fraud losses**
  - Real‑time scoring API lets products **block or step‑up authenticate** high‑risk transactions *before* they settle.
  - Probability output supports **risk‑based rules** (e.g., auto‑block above 0.9, route to manual review between 0.7–0.9).
  - The current model is tuned for an **imbalanced fraud dataset**, delivering:
    - **F1** ≈ 0.850
    - **Precision** ≈ 0.885 (fewer false alarms and costly manual reviews)
    - **Recall** ≈ 0.817 (captures a large share of fraudulent activity)
    - **ROC AUC** ≈ 0.845 (strong ranking power for thresholding)

- **Lower false positives and customer friction**
  - Operators can see, in one dashboard, how many transactions are being flagged and at what probability.
  - This visibility enables **data‑driven threshold tuning** instead of guesswork, reducing unnecessary declines.

- **Faster fraud investigation and incident response**
  - Every scored transaction is stored in PostgreSQL with the key features and model outputs.
  - The dashboard surfaces:
    - Recent transactions
    - Fraud distribution by geography / category
    - Probability distributions
  - This shortens the loop from “we suspect a problem” to **“we know exactly where and why”**.

- **Regulatory and audit readiness**
  - Persisting model decisions and inputs creates a **clear audit trail**:
    - What decision was taken?
    - With what probability?
    - On which features?
  - This is increasingly important for **model risk management** and regulatory reviews.

- **Faster iteration on models**
  - Because inputs and outputs are stored consistently, data scientists can:
    - Pull fresh, labeled datasets for retraining.
    - Compare performance over time (drift, degradation).
  - The system becomes a platform for **continuous improvement**, not a one‑off model drop.

---

### 3. Who Uses This (Personas)

- **Risk / Fraud Operations**
  - Monitors live KPIs (fraud rate, flagged vs normal, hotspots by state).
  - Uses the “Check a transaction” tool to run **what‑if scenarios** during investigations.
  - Adjusts downstream rules/thresholds based on current model behavior.

- **Data Science / Analytics**
  - Treats the API + DB as a **closed loop**:
    - Model → decision → storage → analysis → better model.
  - Uses the stored transaction data for performance monitoring, drift analysis, and retraining.

- **Engineering / Platform**
  - Integrates the FastAPI service behind existing gateways, queues, or orchestration.
  - Benefits from a **containerized, configurable** service that is straightforward to deploy and observe.

---

### 4. How This Project Demonstrates Business Thinking

This is not just a model demo. It intentionally shows:

- **End‑to‑end ownership** – from model artifact to API, storage, and visual monitoring.
- Focus on **operational KPIs** (fraud rate, distribution, recent transactions), not just accuracy metrics.
- **Config‑driven design** so the same pattern can be lifted into different environments (local, staging, production).
- A UI that speaks the language of **risk and business stakeholders**, not only engineers.

In a real organization, this project can be used as:

- A starting point for a production fraud detection service.
- An **internal tool for fraud analysts**.
- A template for other ML‑driven decisioning systems (credit risk, collections, KYC, etc.).

---

### Where This Value Lives in the Repo

- **Real‑time scoring service**: `app/main.py` (`POST /predict`)
- **Model artifact**: `fraud_final_model_complete.pkl` (configurable via `MODEL_PATH`)
- **Audit trail / analytics store**: PostgreSQL via `DB_URL` (`app/database.py`)
- **Monitoring + KPIs UI**: `app/dashboard.py`

