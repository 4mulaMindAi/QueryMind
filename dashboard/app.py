import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ml'))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import json

st.set_page_config(
    page_title = "QueryMind Dashboard",
    page_icon  = "🧠",
    layout     = "wide"
)

# ════════════════════════════════════════════════════════════
# DATABASE — Streamlit Session State
# ════════════════════════════════════════════════════════════
if "users"   not in st.session_state:
    st.session_state.users   = {"admin": {"password": "querymind", "email": "admin@querymind.com"}}
if "tables"  not in st.session_state:
    st.session_state.tables  = {}
if "history" not in st.session_state:
    st.session_state.history = []

def log_history(operation, table, status):
    st.session_state.history.append({
        "operation": operation,
        "table":     table,
        "status":    status,
        "time":      time.strftime("%Y-%m-%d %H:%M:%S")
    })

# ════════════════════════════════════════════════════════════
# 🔐 LOGIN / SIGNUP
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

        with tab1:
            st.subheader("Welcome Back!")
            login_user = st.text_input("Username", key="login_user")
            login_pass = st.text_input("Password", type="password", key="login_pass")

            if st.button("Login", type="primary", use_container_width=True):
                if not login_user or not login_pass:
                    st.error("Please fill all fields!")
                elif login_user in st.session_state.users and \
                     st.session_state.users[login_user]["password"] == login_pass:
                    st.session_state.logged_in = True
                    st.session_state.username  = login_user
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password!")

            st.caption("Default: **admin** / **querymind**")

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
                elif signup_user in st.session_state.users:
                    st.error("Username already exists!")
                else:
                    st.session_state.users[signup_user] = {
                        "password": signup_pass,
                        "email":    signup_email
                    }
                    st.success("Account created! Please login.")

    st.stop()

# ════════════════════════════════════════════════════════════
# MAIN DASHBOARD
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
st.sidebar.success(f"👤 {st.session_state.username}")
st.sidebar.markdown("---")
st.sidebar.success("🟢 Engine Running")

tables = list(st.session_state.tables.keys())
if tables:
    st.sidebar.markdown("### Tables")
    for t in tables:
        count = len(st.session_state.tables[t])
        st.sidebar.markdown(f"• `{t}` ({count} rows)")

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
    col1.metric("Engine",   "QueryMind v1.0")
    col2.metric("Company",  "4mulaMindAI")
    col3.metric("Tables",   len(tables))
    col4.metric("Queries",  len(st.session_state.history))

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

    if st.button("▶️ Run Query", type="primary"):
        q = query.strip()
        qu = q.upper()

        try:
            # CREATE TABLE
            if qu.startswith("CREATE TABLE"):
                parts = q.split()
                tbl   = parts[2]
                if tbl in st.session_state.tables:
                    st.error(f"Table '{tbl}' already exists!")
                else:
                    st.session_state.tables[tbl] = []
                    log_history("CREATE", tbl, "success")
                    st.success(f"✅ Table '{tbl}' created!")
                    st.rerun()

            # SELECT
            elif qu.startswith("SELECT") and "FROM" in qu:
                parts = q.split()
                idx   = [p.upper() for p in parts].index("FROM")
                tbl   = parts[idx+1].rstrip(";")
                if tbl not in st.session_state.tables:
                    st.error(f"Table '{tbl}' not found!")
                else:
                    rows = st.session_state.tables[tbl]
                    log_history("SELECT", tbl, "success")
                    if rows:
                        df = pd.DataFrame(rows)
                        # WHERE filter
                        if "WHERE" in qu:
                            widx  = [p.upper() for p in parts].index("WHERE")
                            wcol  = parts[widx+1]
                            wval  = parts[widx+3].strip("'\"")
                            df    = df[df[wcol].astype(str) == wval]
                        st.metric("Rows", len(df))
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("Table is empty!")

            # INSERT INTO
            elif qu.startswith("INSERT INTO"):
                parts = q.split()
                tbl   = parts[2]
                raw   = q[q.find("(")+1 : q.find(")")]
                vals  = [v.strip() for v in raw.split(",")]
                keys  = ["id","name","age","col4","col5","col6","col7","col8"]
                row   = {keys[i]: vals[i] for i in range(min(len(vals), len(keys)))}
                if tbl not in st.session_state.tables:
                    st.session_state.tables[tbl] = []
                st.session_state.tables[tbl].append(row)
                log_history("INSERT", tbl, "success")
                st.success("✅ 1 row inserted!")

            # DELETE
            elif qu.startswith("DELETE FROM"):
                parts = q.split()
                tbl   = parts[2]
                if "WHERE" in qu:
                    widx  = [p.upper() for p in parts].index("WHERE")
                    wcol  = parts[widx+1]
                    wval  = parts[widx+3].strip("'\"")
                    before = len(st.session_state.tables[tbl])
                    st.session_state.tables[tbl] = [
                        r for r in st.session_state.tables[tbl]
                        if str(r.get(wcol)) != wval
                    ]
                    deleted = before - len(st.session_state.tables[tbl])
                    log_history("DELETE", tbl, "success")
                    st.success(f"✅ {deleted} row(s) deleted!")
                else:
                    st.warning("Add WHERE clause!")

            else:
                st.warning("Supported: SELECT, INSERT INTO, CREATE TABLE, DELETE FROM")

        except Exception as e:
            st.error(f"Error: {e}")

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
            if not table_name:
                st.error("Enter table name!")
            elif table_name in st.session_state.tables:
                st.error("Table already exists!")
            else:
                st.session_state.tables[table_name] = []
                log_history("CREATE", table_name, "success")
                st.success(f"Table '{table_name}' created!")
                st.rerun()

    with st.expander("📥 Insert Row — Multiple Columns"):
        tables = list(st.session_state.tables.keys())
        if tables:
            ins_table = st.selectbox("Select Table", tables, key="ins_tbl")
            num_cols  = st.number_input("Number of Columns", 1, 10, 3)
            cols      = st.columns(num_cols)
            col_names = []
            col_vals  = []
            for i, c in enumerate(cols):
                cn = c.text_input(f"Col {i+1} Name",
                    value=["id","name","age"][i] if i < 3 else f"col{i+1}",
                    key=f"cn_{i}")
                cv = c.text_input(f"Col {i+1} Value", key=f"cv_{i}")
                col_names.append(cn)
                col_vals.append(cv)

            if st.button("Insert Row"):
                row = {col_names[i]: col_vals[i] for i in range(num_cols)}
                st.session_state.tables[ins_table].append(row)
                log_history("INSERT", ins_table, "success")
                st.success("1 row inserted!")
        else:
            st.warning("Please create a table first!")

    with st.expander("🔍 View & Search Data", expanded=True):
        tables = list(st.session_state.tables.keys())
        if tables:
            sel_table = st.selectbox("Select Table", tables, key="sel_tbl")
            search    = st.text_input("🔍 Search rows")
            if st.button("Fetch Data"):
                rows = st.session_state.tables[sel_table]
                log_history("SELECT", sel_table, "success")
                if rows:
                    df = pd.DataFrame(rows)
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
    tables = list(st.session_state.tables.keys())

    if not tables:
        st.warning("Please create a table first!")
    else:
        tab1, tab2 = st.tabs(["🗑️ Delete", "✏️ Update"])

        with tab1:
            del_table = st.selectbox("Table", tables, key="del_tbl")
            col1, col2 = st.columns(2)
            del_key   = col1.text_input("Column", value="id")
            del_value = col2.text_input("Value to delete")
            if st.button("🗑️ Delete Row", type="primary"):
                before = len(st.session_state.tables[del_table])
                st.session_state.tables[del_table] = [
                    r for r in st.session_state.tables[del_table]
                    if str(r.get(del_key)) != del_value
                ]
                deleted = before - len(st.session_state.tables[del_table])
                log_history("DELETE", del_table, "success")
                st.success(f"{deleted} row(s) deleted!")

        with tab2:
            upd_table = st.selectbox("Table", tables, key="upd_tbl")
            col1, col2 = st.columns(2)
            upd_key   = col1.text_input("Find by Column", value="id")
            upd_value = col2.text_input("Find by Value")
            st.markdown("**New Values:**")
            num_upd   = st.number_input("Fields to update", 1, 10, 2)
            upd_cols  = st.columns(num_upd)
            new_data  = {}
            for i, c in enumerate(upd_cols):
                k = c.text_input("Column", key=f"uk_{i}")
                v = c.text_input("Value",  key=f"uv_{i}")
                if k and v:
                    new_data[k] = v

            if st.button("✏️ Update Row", type="primary"):
                for row in st.session_state.tables[upd_table]:
                    if str(row.get(upd_key)) == upd_value:
                        row.update(new_data)
                log_history("UPDATE", upd_table, "success")
                st.success("Row updated successfully!")

# ════════════════════════════════════════════════════════════
# 📉 DATA VISUALIZATION
# ════════════════════════════════════════════════════════════
elif page == "📉 Data Visualization":
    st.header("Data Visualization")
    tables = list(st.session_state.tables.keys())

    if not tables:
        st.warning("Please create a table and insert data first!")
    else:
        sel_table = st.selectbox("Select Table", tables)
        rows      = st.session_state.tables[sel_table]

        if rows:
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True)
            st.divider()

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Bar Chart")
                x_col = st.selectbox("X Axis", df.columns, key="bx")
                y_col = st.selectbox("Y Axis", df.columns, key="by")
                try:
                    fig = px.bar(df, x=x_col, y=y_col,
                                 title=f"{y_col} by {x_col}",
                                 color=x_col)
                    st.plotly_chart(fig, use_container_width=True)
                except:
                    st.warning("Select valid columns!")

            with col2:
                st.subheader("Pie Chart")
                pie_col = st.selectbox("Column", df.columns, key="pc")
                try:
                    fig2 = px.pie(df, names=pie_col,
                                  title=f"Distribution of {pie_col}",
                                  hole=0.3)
                    st.plotly_chart(fig2, use_container_width=True)
                except:
                    st.warning("Could not render pie chart!")
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
                try:
                    from data_collector import DataCollector
                    from optimizer import QueryOptimizer
                    collector = DataCollector()
                    collector.generate_training_data(samples)
                    optimizer = QueryOptimizer()
                    optimizer.train()
                    st.session_state["optimizer"] = optimizer
                    st.success(f"Model trained on {samples} samples!")
                except Exception as e:
                    st.error(f"Error: {e}")

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
            "Query":    ["SELECT *", "SELECT WHERE", "INSERT", "SELECT + Index"],
            "Time(ms)": [45, 12, 8, 3]
        }
        fig = px.bar(pd.DataFrame(data), x="Query", y="Time(ms)",
                     title="Query Execution Time Comparison",
                     color="Time(ms)", color_continuous_scale="RdYlGn_r")
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
                      color="Time(ms)", color_continuous_scale="RdYlGn_r")
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

    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.metric("Total Queries", len(df))
        st.dataframe(df, use_container_width=True)
        fig = px.pie(df, names="operation",
                     title="Query Type Distribution")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No queries executed yet!")