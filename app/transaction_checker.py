from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests
import streamlit as st


def render_transaction_checker(*, default_api_url: Optional[str] = None) -> None:
    api_url = (os.getenv("API_URL") or default_api_url or "http://localhost:8000").rstrip("/")
    api_key = os.getenv("API_KEY")

    st.subheader("Send a transaction to the API")
    st.caption(f"API: {api_url}")

    with st.form("tx_form", clear_on_submit=False):
        col_a, col_b = st.columns(2)
        with col_a:
            amt = st.number_input("Amount (amt)", min_value=0.0, value=100.0, step=1.0)
            state = st.text_input("State", value="CA")
            category = st.text_input("Category", value="shopping")
        with col_b:
            gender = st.selectbox("Gender", options=["M", "F"], index=0)
            hour = st.number_input("Hour (0-23)", min_value=0, max_value=23, value=12, step=1)

        submitted = st.form_submit_button("Predict fraud risk")

    if not submitted:
        return

    payload: Dict[str, Any] = {
        "amt": float(amt),
        "state": state,
        "category": category,
        "gender": gender,
        "hour": int(hour),
    }

    headers = {"content-type": "application/json"}
    if api_key:
        headers["x-api-key"] = api_key

    try:
        resp = requests.post(f"{api_url}/predict", json=payload, headers=headers, timeout=20)
        if resp.ok:
            data = resp.json()
            st.success("Prediction received")
            st.json(data)
            return

        st.error(f"API error: {resp.status_code}")
        try:
            st.json(resp.json())
        except Exception:
            st.code(resp.text)
    except requests.RequestException as e:
        st.error("Could not reach the API. Check that it is running and API_URL is correct.")
        st.code(str(e))

