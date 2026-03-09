import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from datetime import datetime

# ---------- DB CONFIG ----------
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL=os.getenv("DB_URL")
if not DB_URL:
    raise RuntimeError("DB_URL is not set")

engine=create_engine(DB_URL)

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Fraud Radar",
    page_icon="💳",
    layout="wide",
)

# ---------- SIMPLE PAGE STATE ----------
if "page" not in st.session_state:
    st.session_state.page = "landing"

# ---------- CUSTOM CSS FOR HERO ----------
st.markdown(
    """
    <style>
    .hero-container {
        position: relative;
        height: 100vh;
        padding: 0 5%;
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: linear-gradient(120deg, #050816 0%, #111827 40%, #020617 100%);
        color: #f9fafb;
        overflow: hidden;
    }
    .hero-left {
        max-width: 40%;
        z-index: 2;
    }
    .hero-title {
        font-size: 3.2rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        letter-spacing: 0.03em;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: #9ca3af;
        margin-bottom: 1.5rem;
    }
    .hero-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.25rem 0.8rem;
        border-radius: 999px;
        background: rgba(15, 118, 110, 0.18);
        color: #a5f3fc;
        font-size: 0.8rem;
        margin-bottom: 0.8rem;
    }
    .hero-cta {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.65rem 1.6rem;
        border-radius: 999px;
        border: none;
        background: #22c55e;
        color: #022c22;
        font-weight: 600;
        font-size: 0.95rem;
        cursor: pointer;
        box-shadow: 0 12px 30px rgba(34, 197, 94, 0.35);
    }
    .hero-cta:hover {
        background: #16a34a;
    }
    .hero-right {
        position: relative;
        flex: 1;
        display: flex;
        justify-content: flex-end;
        z-index: 1;
    }
    .hero-card {
        width: 320px;
        height: 620px;
        border-radius: 30px;
        background: radial-gradient(circle at top, #0f172a 0%, #020617 45%, #0b1120 100%);
        border: 1px solid rgba(148, 163, 184, 0.2);
        box-shadow: 0 25px 80px rgba(15, 23, 42, 0.85);
        padding: 1.25rem;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        color: #e5e7eb;
    }
    .hero-card-header {
        font-size: 0.88rem;
        font-weight: 600;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.8rem;
    }
    .mini-metric {
        font-size: 0.8rem;
        display: flex;
        flex-direction: column;
        gap: 0.15rem;
    }
    .mini-metric-label {
        color: #9ca3af;
        font-size: 0.7rem;
    }
    .mini-metric-value {
        font-weight: 700;
    }
    .sparkline {
        height: 120px;
        border-radius: 14px;
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.12), rgba(8, 47, 73, 0.2));
        margin-top: 0.4rem;
    }
    .hero-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.78rem;
        color: #9ca3af;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- DASHBOARD VIEW ----------
def show_dashboard() -> None:
    st.markdown("## 💳 Real-Time Fraud Detection Dashboard")
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    query = "SELECT * FROM transactions ORDER BY created_at DESC"
    df = pd.read_sql(query, engine)

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    total = len(df)
    fraud_count = int(df["fraud_prediction"].sum()) if "fraud_prediction" in df.columns else 0
    fraud_rate = (fraud_count / total * 100) if total else 0
    normal_count = total - fraud_count

    with col1:
        st.metric("Total Transactions", total)
    with col2:
        st.metric("Fraud", fraud_count)
    with col3:
        st.metric("Normal", normal_count)
    with col4:
        st.metric("Fraud Rate %", f"{fraud_rate:.1f}%")

    # Alerts
    if total and fraud_rate > 10:
        st.error("⚠️ Fraud rate is above 10%. Review recent activity.")
    elif total and fraud_rate > 5:
        st.warning("Fraud rate is elevated. Monitor transactions.")

    # Charts
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Fraud vs Normal")
        if "fraud_prediction" in df.columns:
            counts = df["fraud_prediction"].value_counts()
            fig_pie = px.pie(
                values=counts.values,
                names=["Normal" if k == 0 else "Fraud" for k in counts.index],
                color_discrete_sequence=["#22c55e", "#ef4444"],
            )
            st.plotly_chart(fig_pie, use_container_width=True)

    with chart_col2:
        st.subheader("Fraud by State")
        if "state" in df.columns and "fraud_prediction" in df.columns:
            fraud_by_state = df.groupby("state")["fraud_prediction"].sum().reset_index()
            fraud_by_state.columns = ["state", "fraud_count"]
            fig_bar = px.bar(
                fraud_by_state,
                x="state",
                y="fraud_count",
                color="fraud_count",
                color_continuous_scale="Reds",
            )
            st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("Fraud Probability Distribution")
    if "fraud_probability" in df.columns:
        fig_hist = px.histogram(df, x="fraud_probability", nbins=30)
        st.plotly_chart(fig_hist, use_container_width=True)

    with st.expander("📋 Recent Transactions", expanded=False):
        st.dataframe(df, use_container_width=True)

# ---------- LANDING (HERO) VIEW ----------
def show_landing() -> None:
    # Fake hero stats (optional: replace with real aggregates)
    daily_tx = "12.4K"
    fraud_today = "126"
    blocked_pct = "89%"

    st.markdown(
        f"""
        <div class="hero-container">
          <div class="hero-left">
            <div class="hero-pill">
              <span>●</span>
              <span>Live anomaly monitoring</span>
            </div>
            <div class="hero-title">
              Real‑Time Fraud Radar
            </div>
            <div class="hero-subtitle">
              Track risky payments as they happen, investigate suspicious behavior,
              and stop fraud before it settles — all in one live command center.
            </div>
            <p style="font-size:0.9rem; color:#9ca3af; margin-bottom:1.6rem;">
              Designed for risk teams that need second‑by‑second visibility into global transactions.
            </p>
          </div>

          <div class="hero-right">
            <div class="hero-card">
              <div>
                <div class="hero-card-header">
                  <span>Live fraud overview</span>
                  <span style="font-size:0.7rem; color:#9ca3af;">{datetime.now().strftime('%H:%M')}</span>
                </div>
                <div style="display:flex; justify-content:space-between; gap:0.75rem;">
                  <div class="mini-metric">
                    <span class="mini-metric-label">Today</span>
                    <span class="mini-metric-value">{daily_tx}</span>
                    <span style="color:#22c55e; font-size:0.7rem;">+8.3% vs yesterday</span>
                  </div>
                  <div class="mini-metric">
                    <span class="mini-metric-label">Flagged</span>
                    <span class="mini-metric-value" style="color:#f97316;">{fraud_today}</span>
                    <span style="color:#f97316; font-size:0.7rem;">High risk traffic</span>
                  </div>
                  <div class="mini-metric">
                    <span class="mini-metric-label">Blocked</span>
                    <span class="mini-metric-value" style="color:#22c55e;">{blocked_pct}</span>
                    <span style="color:#22c55e; font-size:0.7rem;">Auto rules</span>
                  </div>
                </div>
                <div class="sparkline"></div>
              </div>

              <div class="hero-footer">
                <span>Latency &lt; 300ms</span>
                <span>Global · 24/7 monitoring</span>
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # CTA button under hero
    st.markdown("<div style='margin-top:-140px; padding: 0 5%;'>", unsafe_allow_html=True)
    if st.button("Open live dashboard", key="open_dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- ROUTER ----------
if st.session_state.page == "landing":
    show_landing()
else:
    show_dashboard()