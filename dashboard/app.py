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

# ════════════════════════════════════════════════════════════
# 🔐 LOGIN
# ════════════════════════════════════════════════════════════
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🧠 QueryMind")
    st.markdown("### 4mulaMindAI — Intelligent Database Engine")
    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])

        # ── LOGIN ──────────────────────────────────────────
        with tab1:
            st.subheader("Welcome Back!")
            login_user = st.text_input("Username", key="login_user")
            login_pass = st.text_input("Password", type="password", key="login_pass")

            if st.button("Login", type="primary", use_container_width=True):
                if not login_user or not login_pass:
                    st.error("Please fill all fields!")
                else:
                    try:
                        res  = requests.post(f"{API}/login",
                                json={"username": login_user,
                                      "password": login_pass})
                        data = res.json()
                        if data["status"] == "success":
                            st.session_state.logged_in = True
                            st.session_state.token     = data["token"]
                            st.session_state.username  = data["user"]
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error(data["message"])
                    except:
                        st.error("API is offline! Run `mvn spring-boot:run`")

            st.markdown("---")
            st.caption("Default: **admin** / **querymind**")

        # ── SIGNUP ─────────────────────────────────────────
        with tab2:
            st.subheader("Create Account")
            signup_user  = st.text_input("Username",         key="signup_user")
            signup_email = st.text_input("Email",            key="signup_email")
            signup_pass  = st.text_input("Password",         type="password", key="signup_pass")
            signup_pass2 = st.text_input("Confirm Password", type="password", key="signup_pass2")

            if st.button("Create Account", type="primary", use_container_width=True):
                if not signup_user or not signup_pass:
                    st.error("Username and password are required!")
                elif signup_pass != signup_pass2:
                    st.error("Passwords do not match!")
                elif len(signup_pass) < 6:
                    st.error("Password must be at least 6 characters!")
                else:
                    try:
                        res  = requests.post(f"{API}/signup",
                                json={"username": signup_user,
                                      "email":    signup_email,
                                      "password": signup_pass})
                        data = res.json()
                        if data["status"] == "success":
                            st.success("Account created! Please login.")
                        else:
                            st.error(data["message"])
                    except:
                        st.error("API is offline!")

    st.stop()

# ════════════════════════════════════════════════════════════
# MAIN DASHBOARD (after login)
# ════════════════════════════════════════════════════════════
col1, col2 = st.columns([8, 2])
col1.title("🧠 QueryMind Dashboard")
col1.markdown("**4mulaMindAI** — Intelligent Database Engine")
if col2.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.rerun()

st.divider()

# Sidebar
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
    "💻 SQL Query Box",
    "📊 Query Executor",
    "🗑️ Delete & Update",
    "📉 Data Visualization",
    "🤖 ML Optimizer",
    "📈 Performance",
    "📜 Query History"
])

# ════════════════════════════════════════════════════════════
# 🏠 OVERVIEW
# ════════════════════════════════════════════════════════════
if page == "🏠 Overview":
    st.header("System Overview")

    col1, col2, col3, col4 = st.columns(4)
    if status:
        col1.metric("API Status", "🟢 Running")
        col2.metric("Engine",     status["engine"])
        col3.metric("Company",    status["company"])
        col4.metric("Tables",     len(tables))
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
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)

# ════════════════════════════════════════════════════════════
# 💻 SQL QUERY BOX
# ════════════════════════════════════════════════════════════
elif page == "💻 SQL Query Box":
    st.header("SQL Query Box")
    st.markdown("Write SQL queries and execute them directly!")

    query = st.text_area("Enter SQL Query", height=120,
        placeholder="SELECT * FROM users\nINSERT INTO users VALUES (1, Alice, 22)\nCREATE TABLE products")

    col1, col2 = st.columns([1, 5])
    run = col1.button("▶️ Run Query", type="primary")

    if run and query.strip():
        q = query.strip().upper()

        try:
            # CREATE TABLE
            if q.startswith("CREATE TABLE"):
                parts     = query.strip().split()
                tbl       = parts[2]
                res       = requests.post(f"{API}/create",
                                json={"table": tbl})
                data      = res.json()
                if data["status"] == "success":
                    st.success(f"✅ {data['message']}")
                else:
                    st.error(data["message"])

            # SELECT * FROM table
            elif q.startswith("SELECT") and "FROM" in q:
                parts = query.strip().split()
                tbl   = parts[parts.index("FROM") + 1] if "FROM" in [p.upper() for p in parts] else None
                if not tbl:
                    idx = [p.upper() for p in parts].index("FROM")
                    tbl = parts[idx + 1]
                tbl   = tbl.rstrip(";")
                res   = requests.get(f"{API}/select/{tbl}")
                data  = res.json()
                if data["status"] == "success":
                    if data["count"] > 0:
                        st.metric("Rows returned", data["count"])
                        st.dataframe(pd.DataFrame(data["rows"]),
                                     use_container_width=True)
                    else:
                        st.info("Table is empty!")
                else:
                    st.error(data["message"])

            # INSERT INTO table VALUES (...)
            elif q.startswith("INSERT INTO"):
                parts = query.strip().split()
                tbl   = parts[2]
                # Extract values between ( )
                raw   = query[query.find("(")+1 : query.find(")")]
                vals  = [v.strip() for v in raw.split(",")]
                row   = {}
                if len(vals) >= 1: row["id"]   = vals[0]
                if len(vals) >= 2: row["name"]  = vals[1]
                if len(vals) >= 3: row["age"]   = vals[2]
                # Extra columns
                keys = ["id","name","age","col4","col5","col6"]
                for i, v in enumerate(vals):
                    if i < len(keys):
                        row[keys[i]] = v

                res  = requests.post(f"{API}/insert",
                           json={"table": tbl, "row": row})
                data = res.json()
                if data["status"] == "success":
                    st.success(f"✅ {data['message']}")
                else:
                    st.error(data["message"])

            # DELETE FROM table WHERE col = val
            elif q.startswith("DELETE FROM"):
                parts = query.strip().split()
                tbl   = parts[2]
                if "WHERE" in [p.upper() for p in parts]:
                    idx   = [p.upper() for p in parts].index("WHERE")
                    col   = parts[idx+1]
                    val   = parts[idx+3].strip("'\"")
                    res   = requests.post(f"{API}/delete",
                                json={"table": tbl,
                                      "key":   col,
                                      "value": val})
                    data  = res.json()
                    if data["status"] == "success":
                        st.success("✅ Row deleted!")
                    else:
                        st.error(data["message"])
                else:
                    st.warning("Add WHERE clause: DELETE FROM table WHERE id = 1")

            else:
                st.warning("Supported: SELECT, INSERT INTO, CREATE TABLE, DELETE FROM")

        except Exception as e:
            st.error(f"Error: {e}")

    # Query examples
    st.divider()
    st.subheader("📖 Query Examples")
    examples = {
        "Create table":  "CREATE TABLE students",
        "Insert row":    "INSERT INTO students VALUES (1, Alice, 22)",
        "Select all":    "SELECT * FROM students",
        "Delete row":    "DELETE FROM students WHERE id = 1",
    }
    for label, ex in examples.items():
        st.code(ex, language="sql")

# ════════════════════════════════════════════════════════════
# 📊 QUERY EXECUTOR
# ════════════════════════════════════════════════════════════
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

    with st.expander("📥 Insert Row — Multiple Columns"):
        tables = get_tables()
        if tables:
            ins_table = st.selectbox("Select Table", tables, key="ins_tbl")

            st.markdown("**Define Columns:**")
            num_cols  = st.number_input("Number of Columns", 1, 10, 3)
            cols      = st.columns(num_cols)
            col_names = []
            col_vals  = []

            for i, c in enumerate(cols):
                cn = c.text_input(f"Column {i+1} Name",
                                   value=["id","name","age"][i] if i < 3 else f"col{i+1}",
                                   key=f"cn_{i}")
                cv = c.text_input(f"Column {i+1} Value", key=f"cv_{i}")
                col_names.append(cn)
                col_vals.append(cv)

            if st.button("Insert Row"):
                row = {col_names[i]: col_vals[i] for i in range(num_cols)}
                res = requests.post(f"{API}/insert",
                        json={"table": ins_table, "row": row})
                if res.json()["status"] == "success":
                    st.success(res.json()["message"])
                else:
                    st.error(res.json()["message"])
        else:
            st.warning("Please create a table first!")

    with st.expander("🔍 View & Search Data", expanded=True):
        tables = get_tables()
        if tables:
            sel_table = st.selectbox("Select Table", tables, key="sel_tbl")
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
                    st.download_button("📥 Export CSV", csv,
                                       f"{sel_table}.csv", "text/csv")
                else:
                    st.info("Table is empty!")
        else:
            st.warning("Please create a table first!")

# ════════════════════════════════════════════════════════════
# 🗑️ DELETE & UPDATE
# ════════════════════════════════════════════════════════════
elif page == "🗑️ Delete & Update":
    st.header("Delete & Update Rows")

    tables = get_tables()
    if not tables:
        st.warning("Please create a table first!")
    else:
        tab1, tab2 = st.tabs(["🗑️ Delete", "✏️ Update"])

        with tab1:
            del_table = st.selectbox("Table", tables, key="del_tbl")
            col1, col2 = st.columns(2)
            del_key   = col1.text_input("Column", value="id")
            del_value = col2.text_input("Value")
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
            upd_table = st.selectbox("Table", tables, key="upd_tbl")
            col1, col2 = st.columns(2)
            upd_key   = col1.text_input("Find by Column", value="id")
            upd_value = col2.text_input("Find by Value")

            st.markdown("**New Values (fill what you want to update):**")
            num_upd   = st.number_input("Number of fields", 1, 10, 2)
            upd_cols  = st.columns(num_upd)
            new_data  = {}
            for i, c in enumerate(upd_cols):
                k = c.text_input(f"Column", key=f"uk_{i}")
                v = c.text_input(f"Value",  key=f"uv_{i}")
                if k and v:
                    new_data[k] = v

            if st.button("✏️ Update Row", type="primary"):
                res = requests.post(f"{API}/update",
                        json={"table":   upd_table,
                              "key":     upd_key,
                              "value":   upd_value,
                              "newData": new_data})
                if res.json()["status"] == "success":
                    st.success("Row updated successfully!")
                else:
                    st.error(res.json()["message"])

# ════════════════════════════════════════════════════════════
# 📉 DATA VISUALIZATION
# ════════════════════════════════════════════════════════════
elif page == "📉 Data Visualization":
    st.header("Data Visualization")

    tables = get_tables()
    if not tables:
        st.warning("Please create a table and insert data first!")
    else:
        sel_table = st.selectbox("Select Table", tables)
        res       = requests.get(f"{API}/select/{sel_table}")
        data      = res.json()

        if data["status"] == "success" and data["count"] > 0:
            df      = pd.DataFrame(data["rows"])
            st.dataframe(df, use_container_width=True)

            num_cols = df.select_dtypes(include="object").columns.tolist()

            st.divider()
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Bar Chart")
                if len(df.columns) >= 2:
                    x_col = st.selectbox("X Axis", df.columns, key="bx")
                    y_col = st.selectbox("Y Axis", df.columns, key="by")
                    try:
                        fig = px.bar(df, x=x_col, y=y_col,
                                     title=f"{y_col} by {x_col}",
                                     color=x_col)
                        st.plotly_chart(fig, use_container_width=True)
                    except:
                        st.warning("Select numeric column for Y axis")

            with col2:
                st.subheader("Pie Chart")
                pie_col = st.selectbox("Column", df.columns, key="pc")
                try:
                    fig2 = px.pie(df, names=pie_col,
                                  title=f"Distribution of {pie_col}",
                                  hole=0.3)
                    st.plotly_chart(fig2, use_container_width=True)
                except:
                    st.warning("Could not render pie chart")

            st.subheader("Scatter Plot")
            col1, col2 = st.columns(2)
            sx = col1.selectbox("X Axis", df.columns, key="sx")
            sy = col2.selectbox("Y Axis", df.columns, key="sy")
            try:
                fig3 = px.scatter(df, x=sx, y=sy,
                                  title=f"{sy} vs {sx}",
                                  color=df.columns[0])
                st.plotly_chart(fig3, use_container_width=True)
            except:
                st.warning("Select valid columns for scatter plot")
        else:
            st.info("Table is empty! Insert data first.")

# ════════════════════════════════════════════════════════════
# 🤖 ML OPTIMIZER
# ════════════════════════════════════════════════════════════
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
        table_size = st.slider("Table Size", 100, 10000, 1000)
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

# ════════════════════════════════════════════════════════════
# 📈 PERFORMANCE
# ════════════════════════════════════════════════════════════
elif page == "📈 Performance":
    st.header("Performance Analytics")

    col1, col2 = st.columns(2)
    with col1:
        data = {
            "Query":    ["SELECT *", "SELECT WHERE",
                         "INSERT", "SELECT + Index"],
            "Time(ms)": [45, 12, 8, 3]
        }
        fig = px.bar(pd.DataFrame(data), x="Query", y="Time(ms)",
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

# ════════════════════════════════════════════════════════════
# 📜 QUERY HISTORY
# ════════════════════════════════════════════════════════════
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