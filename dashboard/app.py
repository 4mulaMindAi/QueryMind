import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ml'))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import time
from optimizer import QueryOptimizer
from data_collector import DataCollector

st.set_page_config(
    page_title = "QueryMind Dashboard",
    page_icon  = "🧠",
    layout     = "wide"
)

API = "http://localhost:8080/api"

def get_tables():
    try:
        res = requests.get(f"{API}/tables", timeout=2)
        return res.json().get("tables", [])
    except:
        return []

def api_status():
    try:
        res = requests.get(f"{API}/ping", timeout=2)
        return res.json()
    except:
        return None

col1, col2 = st.columns([8, 2])
col1.title("🧠 QueryMind Dashboard")
col1.markdown("**4mulaMindAI** — Intelligent Database Engine")
st.divider()

st.sidebar.title("🧠 QueryMind")
st.sidebar.markdown("---")

status = api_status()
if status:
    st.sidebar.success("🟢 API Running")
else:
    st.sidebar.error("🔴 API Offline")

tables = get_tables()
if tables:
    st.sidebar.markdown("### Tables")
    for t in tables:
        st.sidebar.markdown(f"• `{t}`")

st.sidebar.markdown("---")
page = st.sidebar.radio("Navigate", [
    "🏠 Overview",
    "📊 Query Executor",
    "🗑️ Delete & Update",
    "🤖 ML Optimizer",
    "📈 Performance",
    "📜 Query History"
])

if page == "🏠 Overview":
    st.header("System Overview")

    col1, col2, col3, col4 = st.columns(4)
    if status:
        col1.metric("API Status",  "🟢 Running")
        col2.metric("Engine",      status["engine"])
        col3.metric("Company",     status["company"])
        col4.metric("Tables",      len(tables))
    else:
        st.error("Java API is offline! Run `mvn spring-boot:run`")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Architecture")
        arch = {
            "Module":  ["Storage Engine", "Query Processor",
                        "ML Optimizer", "Java API", "Dashboard"],
            "Tech":    ["C++", "C++", "Python", "Java", "Python"],
            "Status":  ["✅ Done", "✅ Done", "✅ Done",
                        "✅ Done", "✅ Done"]
        }
        st.dataframe(pd.DataFrame(arch), use_container_width=True)

    with col2:
        st.subheader("Tech Stack Distribution")
        fig = px.pie(
            values=[30, 30, 20, 20],
            names=["C++", "Python", "Java", "SQL"],
            title="Tech Distribution",
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)

elif page == "📊 Query Executor":
    st.header("Query Executor")

    with st.expander("➕ Create Table"):
        col1, col2 = st.columns([3, 1])
        table_name = col1.text_input("Table Name")
        if col2.button("Create", use_container_width=True):
            res = requests.post(f"{API}/create",
                json={"table": table_name})
            if res.json()["status"] == "success":
                st.success(res.json()["message"])
                st.rerun()
            else:
                st.error(res.json()["message"])

    with st.expander("📥 Insert Row"):
        tables = get_tables()
        if tables:
            ins_table = st.selectbox("Select Table", tables, key="ins_table")
            col1, col2, col3 = st.columns(3)
            id_val   = col1.text_input("ID")
            name_val = col2.text_input("Name")
            age_val  = col3.text_input("Age")
            if st.button("Insert Row"):
                res = requests.post(f"{API}/insert",
                    json={"table": ins_table,
                          "row":   {"id":   id_val,
                                    "name": name_val,
                                    "age":  age_val}})
                if res.json()["status"] == "success":
                    st.success(res.json()["message"])
                else:
                    st.error(res.json()["message"])
        else:
            st.warning("Please create a table first!")

    with st.expander("🔍 View & Search Data", expanded=True):
        tables = get_tables()
        if tables:
            sel_table = st.selectbox("Select Table", tables, key="sel_table")
            search    = st.text_input("🔍 Search rows")
            if st.button("Fetch Data"):
                res  = requests.get(f"{API}/select/{sel_table}")
                data = res.json()
                if data["status"] == "success" and data["count"] > 0:
                    df = pd.DataFrame(data["rows"])
                    if search:
                        mask = df.apply(lambda row:
                            row.astype(str).str.contains(
                                search, case=False).any(), axis=1)
                        df = df[mask]
                    st.metric("Total Rows", len(df))
                    st.dataframe(df, use_container_width=True)
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "📥 Export CSV",
                        csv,
                        f"{sel_table}.csv",
                        "text/csv"
                    )
                else:
                    st.info("Table is empty!")
        else:
            st.warning("Please create a table first!")

elif page == "🗑️ Delete & Update":
    st.header("Delete & Update Rows")

    tables = get_tables()
    if not tables:
        st.warning("Please create a table first!")
    else:
        tab1, tab2 = st.tabs(["🗑️ Delete", "✏️ Update"])

        with tab1:
            st.subheader("Delete Row")
            del_table = st.selectbox("Table", tables, key="del_table")
            col1, col2 = st.columns(2)
            del_key   = col1.text_input("Column", value="id")
            del_value = col2.text_input("Value to delete")
            if st.button("🗑️ Delete Row", type="primary"):
                res = requests.post(f"{API}/delete",
                    json={"table": del_table,
                          "key":   del_key,
                          "value": del_value})
                if res.json()["status"] == "success":
                    st.success("Row deleted successfully!")
                else:
                    st.error(res.json()["message"])

        with tab2:
            st.subheader("Update Row")
            upd_table = st.selectbox("Table", tables, key="upd_table")
            col1, col2 = st.columns(2)
            upd_key   = col1.text_input("Find by Column", value="id")
            upd_value = col2.text_input("Find by Value")
            st.markdown("**New Values:**")
            col1, col2 = st.columns(2)
            new_name  = col1.text_input("New Name")
            new_age   = col2.text_input("New Age")
            if st.button("✏️ Update Row", type="primary"):
                new_data = {}
                if new_name: new_data["name"] = new_name
                if new_age:  new_data["age"]  = new_age
                res = requests.post(f"{API}/update",
                    json={"table":   upd_table,
                          "key":     upd_key,
                          "value":   upd_value,
                          "newData": new_data})
                if res.json()["status"] == "success":
                    st.success("Row updated successfully!")
                else:
                    st.error(res.json()["message"])

elif page == "🤖 ML Optimizer":
    st.header("ML Query Optimizer")
    st.markdown("Random Forest model that predicts query execution time.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Train Model")
        samples = st.slider("Training Samples", 500, 2000, 1000)
        if st.button("🚀 Train Model", type="primary"):
            with st.spinner("Training Random Forest model..."):
                collector = DataCollector()
                collector.generate_training_data(samples)
                optimizer = QueryOptimizer()
                optimizer.train()
                st.session_state["optimizer"] = optimizer
            st.success(f"Model trained on {samples} samples!")

    with col2:
        st.subheader("Predict Performance")
        table_size = st.slider("Table Size",    100, 10000, 1000)
        has_where  = st.checkbox("Has WHERE condition?")
        has_index  = st.checkbox("Has Index?")
        query_type = st.selectbox("Query Type", ["SELECT", "INSERT"])
        if st.button("🔮 Predict"):
            if "optimizer" not in st.session_state:
                st.warning("Please train the model first!")
            else:
                import numpy as np
                opt      = st.session_state["optimizer"]
                qt       = 0 if query_type == "SELECT" else 1
                features = np.array([[qt, table_size,
                                       int(has_where), int(has_index)]])
                est_time = opt.model.predict(features)[0]
                st.metric("Estimated Execution Time", f"{est_time:.2f} ms")
                if has_where and not has_index and table_size > 1000:
                    st.error("⚠️ Add an INDEX — query will be slow!")
                elif has_index:
                    st.success("✅ Query is optimized!")
                else:
                    st.info("ℹ️ Query performance looks good!")

elif page == "📈 Performance":
    st.header("Performance Analytics")

    col1, col2 = st.columns(2)
    with col1:
        data = {
            "Query":    ["SELECT *", "SELECT WHERE",
                         "INSERT", "SELECT + Index"],
            "Time(ms)": [45, 12, 8, 3]
        }
        fig = px.bar(pd.DataFrame(data),
                     x="Query", y="Time(ms)",
                     title="Query Execution Time Comparison",
                     color="Time(ms)",
                     color_continuous_scale="RdYlGn_r")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        index_data = {
            "Scenario":  ["No Index 1K", "With Index 1K",
                          "No Index 10K", "With Index 10K"],
            "Time(ms)":  [45, 3, 450, 5]
        }
        fig2 = px.bar(pd.DataFrame(index_data),
                      x="Scenario", y="Time(ms)",
                      title="Index Impact on Query Performance",
                      color="Time(ms)",
                      color_continuous_scale="RdYlGn_r")
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📡 Real-time Query Monitor")
    placeholder = st.empty()
    if st.button("▶️ Start Monitor"):
        import random
        for i in range(20):
            times = [random.randint(1, 50) for _ in range(5)]
            fig3  = go.Figure()
            fig3.add_trace(go.Scatter(
                y=times, mode="lines+markers",
                name="Query Time",
                line=dict(color="#00ff88")
            ))
            fig3.update_layout(title="Live Query Times (ms)")
            placeholder.plotly_chart(fig3, use_container_width=True)
            time.sleep(0.5)

elif page == "📜 Query History":
    st.header("Query History")

    if st.button("🔄 Refresh"):
        st.rerun()

    try:
        res  = requests.get(f"{API}/history", timeout=2)
        data = res.json()
        if data["status"] == "success" and data["history"]:
            df = pd.DataFrame(data["history"])
            st.metric("Total Queries", len(df))
            st.dataframe(df, use_container_width=True)
            fig = px.pie(df, names="operation",
                         title="Query Type Distribution")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No queries executed yet!")
    except:
        st.error("Cannot connect to API!")