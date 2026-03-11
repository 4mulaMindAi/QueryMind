import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ml'))

import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import json
from optimizer import QueryOptimizer
from data_collector import DataCollector

# Page config
st.set_page_config(
    page_title="QueryMind Dashboard",
    page_icon="🧠",
    layout="wide"
)

# Header
st.title("🧠 QueryMind Dashboard")
st.markdown("**4mulaMindAI** — Intelligent Database Engine")
st.divider()

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "🏠 Overview",
    "📊 Query Executor",
    "🤖 ML Optimizer",
    "📈 Performance"
])

API = "http://localhost:8080/api"

# ─── Overview Page ───────────────────────────────────────────
if page == "🏠 Overview":
    st.header("System Overview")

    col1, col2, col3, col4 = st.columns(4)

    # API status check
    try:
        res = requests.get(f"{API}/ping", timeout=2)
        data = res.json()
        col1.metric("API Status",  "🟢 Running")
        col2.metric("Engine",      data["engine"])
        col3.metric("Company",     data["company"])
        col4.metric("Port",        "8080")
    except:
        col1.metric("API Status", "🔴 Offline")
        st.error("Java API chal nahi rahi! `mvn spring-boot:run` chalaao!")

    st.divider()
    st.subheader("Architecture")
    
    arch = {
        "Module":  ["Storage Engine", "Query Processor", "ML Optimizer", "Java API", "Dashboard"],
        "Tech":    ["C++",            "C++",             "Python",       "Java",     "Python"],
        "Status":  ["✅ Done",         "✅ Done",          "✅ Done",       "✅ Done",   "🔄 Building"]
    }
    st.dataframe(pd.DataFrame(arch), use_container_width=True)

# ─── Query Executor Page ─────────────────────────────────────
elif page == "📊 Query Executor":
    st.header("Query Executor")

    # Table banao
    with st.expander("➕ Create Table"):
        table_name = st.text_input("Table Name")
        if st.button("Create"):
            res = requests.post(f"{API}/create", 
                json={"table": table_name})
            st.success(res.json()["message"])

    # Row insert karo
    with st.expander("📥 Insert Row"):
        ins_table = st.text_input("Table Name ", key="ins")
        col1, col2, col3 = st.columns(3)
        id_val   = col1.text_input("ID")
        name_val = col2.text_input("Name")
        age_val  = col3.text_input("Age")

        if st.button("Insert"):
            res = requests.post(f"{API}/insert",
                json={"table": ins_table, 
                      "row": {"id": id_val, 
                              "name": name_val, 
                              "age": age_val}})
            st.success(res.json()["message"])

    # Data dekho
    with st.expander("🔍 Select Data", expanded=True):
        sel_table = st.text_input("Table Name  ", key="sel")
        if st.button("Fetch"):
            res  = requests.get(f"{API}/select/{sel_table}")
            data = res.json()
            if data["status"] == "success":
                st.metric("Total Rows", data["count"])
                st.dataframe(pd.DataFrame(data["rows"]), 
                           use_container_width=True)
            else:
                st.error(data["message"])

# ─── ML Optimizer Page ───────────────────────────────────────
elif page == "🤖 ML Optimizer":
    st.header("ML Query Optimizer")

    if st.button("🚀 Train Model"):
        with st.spinner("Training..."):
            collector = DataCollector()
            collector.generate_training_data(1000)
            optimizer = QueryOptimizer()
            optimizer.train()
            st.session_state["optimizer"] = optimizer
        st.success("Model trained!")

    st.divider()
    st.subheader("Predict Query Performance")

    col1, col2 = st.columns(2)
    table_size = col1.slider("Table Size",    100, 10000, 1000)
    has_where  = col1.checkbox("Has WHERE condition?")
    has_index  = col2.checkbox("Has Index?")
    query_type = col2.selectbox("Query Type", ["SELECT", "INSERT"])

    if st.button("🔮 Predict"):
        if "optimizer" not in st.session_state:
            st.warning("Pehle model train karo!")
        else:
            opt = st.session_state["optimizer"]
            qt  = 0 if query_type == "SELECT" else 1
            opt.predict(qt, table_size, 
                       int(has_where), int(has_index))
            st.info("Check terminal for prediction!")

# ─── Performance Page ────────────────────────────────────────
elif page == "📈 Performance":
    st.header("Performance Analytics")

    # Sample performance data
    data = {
        "Query":    ["SELECT *", "SELECT WHERE", "INSERT", "SELECT + Index"],
        "Time(ms)": [45,         12,              8,        3]
    }
    df = pd.DataFrame(data)

    fig = px.bar(df, x="Query", y="Time(ms)",
                 title="Query Execution Time Comparison",
                 color="Time(ms)",
                 color_continuous_scale="RdYlGn_r")
    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("Index Impact")

    index_data = {
        "Scenario":  ["No Index\n(1K rows)", "With Index\n(1K rows)", 
                      "No Index\n(10K rows)", "With Index\n(10K rows)"],
        "Time(ms)":  [45, 3, 450, 5]
    }
    fig2 = px.bar(pd.DataFrame(index_data), 
                  x="Scenario", y="Time(ms)",
                  title="Index Impact on Query Performance",
                  color="Time(ms)",
                  color_continuous_scale="RdYlGn_r")
    st.plotly_chart(fig2, use_container_width=True)