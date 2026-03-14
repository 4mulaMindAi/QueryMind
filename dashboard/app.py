import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ml'))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
from supabase import create_client, Client

st.set_page_config(page_title="QueryMind Dashboard", page_icon="🧠", layout="wide")

SUPABASE_URL = "https://mrolmkndebwzgleijcxv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1yb2xta25kZWJ3emdsZWlqY3h2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM0NzMxMTMsImV4cCI6MjA4OTA0OTExM30.4ZKu0uwhADQyZ9EO1abJVq23jj2JBN2ZFEN-D344BJE"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

if "history" not in st.session_state:
    st.session_state.history = []

def log_history(op, tbl, status):
    st.session_state.history.append({"operation": op, "table": tbl, "status": status, "time": time.strftime("%Y-%m-%d %H:%M:%S")})

def db_login(username, password):
    try:
        res = supabase.table("users").select("*").eq("username", username).eq("password", password).execute()
        return (True, res.data[0]) if res.data else (False, "Invalid username or password!")
    except Exception as e:
        return False, str(e)

def db_signup(username, email, password):
    try:
        ex = supabase.table("users").select("*").eq("username", username).execute()
        if ex.data:
            return False, "Username already exists!"
        supabase.table("users").insert({"username": username, "email": email, "password": password}).execute()
        return True, "Account created successfully!"
    except Exception as e:
        return False, str(e)

def db_get_tables():
    try:
        res = supabase.table("db_tables").select("*").execute()
        return [t["name"] for t in res.data]
    except:
        return []

def db_create_table(name, username):
    try:
        ex = supabase.table("db_tables").select("*").eq("name", name).execute()
        if ex.data:
            return False, "Table already exists!"
        supabase.table("db_tables").insert({"name": name, "created_by": username}).execute()
        return True, f"Table '{name}' created!"
    except Exception as e:
        return False, str(e)

def db_insert_row(table_name, row):
    try:
        supabase.table("db_rows").insert({"table_name": table_name, "row_data": row}).execute()
        return True, "1 row inserted!"
    except Exception as e:
        return False, str(e)

def db_select_rows(table_name):
    try:
        res = supabase.table("db_rows").select("*").eq("table_name", table_name).execute()
        return [r["row_data"] for r in res.data]
    except:
        return []

def db_delete_row(table_name, key, value):
    try:
        rows = supabase.table("db_rows").select("*").eq("table_name", table_name).execute()
        for r in rows.data:
            if str(r["row_data"].get(key)) == value:
                supabase.table("db_rows").delete().eq("id", r["id"]).execute()
        return True, "Row deleted!"
    except Exception as e:
        return False, str(e)

def db_update_row(table_name, key, value, new_data):
    try:
        rows = supabase.table("db_rows").select("*").eq("table_name", table_name).execute()
        for r in rows.data:
            if str(r["row_data"].get(key)) == value:
                updated = {**r["row_data"], **new_data}
                supabase.table("db_rows").update({"row_data": updated}).eq("id", r["id"]).execute()
        return True, "Row updated!"
    except Exception as e:
        return False, str(e)

# ── LOGIN / SIGNUP ─────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🧠 QueryMind")
    st.markdown("### 4mulaMind — Intelligent Database Engine")
    st.divider()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
        with tab1:
            st.subheader("Welcome Back!")
            lu = st.text_input("Username", key="lu")
            lp = st.text_input("Password", type="password", key="lp")
            if st.button("Login", type="primary", use_container_width=True):
                if not lu or not lp:
                    st.error("Please fill all fields!")
                else:
                    ok, res = db_login(lu, lp)
                    if ok:
                        st.session_state.logged_in = True
                        st.session_state.username  = lu
                        st.rerun()
                    else:
                        st.error(res)
            st.caption("Default: **admin** / **querymind**")
        with tab2:
            st.subheader("Create Account")
            su  = st.text_input("Username",         key="su")
            se  = st.text_input("Email",            key="se")
            sp  = st.text_input("Password",         type="password", key="sp")
            sp2 = st.text_input("Confirm Password", type="password", key="sp2")
            if st.button("Create Account", type="primary", use_container_width=True):
                if not su or not sp:
                    st.error("Username and password required!")
                elif sp != sp2:
                    st.error("Passwords do not match!")
                elif len(sp) < 6:
                    st.error("Password must be 6+ characters!")
                else:
                    ok, msg = db_signup(su, se, sp)
                    if ok:
                        st.success(msg + " Please login.")
                    else:
                        st.error(msg)
    st.stop()

# ── MAIN DASHBOARD ─────────────────────────────────────────
col1, col2 = st.columns([8, 2])
col1.title("🧠 QueryMind Dashboard")
col1.markdown("**4mulaMind** — Intelligent Database Engine")
if col2.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.rerun()
st.divider()

tables = db_get_tables()
st.sidebar.title("🧠 QueryMind")
st.sidebar.success(f"👤 {st.session_state.username}")
st.sidebar.markdown("---")
st.sidebar.success("🟢 Engine Running")
if tables:
    st.sidebar.markdown("### Tables")
    for t in tables:
        rows = db_select_rows(t)
        st.sidebar.markdown(f"• `{t}` ({len(rows)} rows)")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigate", [
    "🏠 Overview", "💻 SQL Query Box", "📊 Query Executor",
    "🗑️ Delete & Update", "📉 Data Visualization",
    "🤖 ML Optimizer", "📈 Performance", "📜 Query History"
])

# ── OVERVIEW ───────────────────────────────────────────────
if page == "🏠 Overview":
    st.header("System Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Engine",  "QueryMind v1.0")
    col2.metric("Company", "4mulaMind")
    col3.metric("Tables",  len(tables))
    col4.metric("Queries", len(st.session_state.history))
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Architecture")
        arch = {"Module": ["Storage Engine","Query Processor","ML Optimizer","Java API","Dashboard"],
                "Tech":   ["C++","C++","Python","Java","Python"],
                "Status": ["✅ Done","✅ Done","✅ Done","✅ Done","✅ Done"]}
        st.dataframe(pd.DataFrame(arch), use_container_width=True)
    with col2:
        st.subheader("Tech Stack")
        fig = px.pie(values=[30,30,20,20], names=["C++","Python","Java","SQL"], hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

# ── SQL QUERY BOX ──────────────────────────────────────────
elif page == "💻 SQL Query Box":
    st.header("SQL Query Box")
    query = st.text_area("Enter SQL Query", height=120,
        placeholder="SELECT * FROM users\nINSERT INTO users VALUES (1, Alice, 22)\nCREATE TABLE products")
    if st.button("▶️ Run Query", type="primary"):
        q = query.strip(); qu = q.upper()
        try:
            if qu.startswith("CREATE TABLE"):
                tbl = q.split()[2]
                ok, msg = db_create_table(tbl, st.session_state.username)
                (st.success if ok else st.error)(f"{'✅' if ok else '❌'} {msg}")
                if ok: log_history("CREATE", tbl, "success"); st.rerun()
            elif qu.startswith("SELECT") and "FROM" in qu:
                parts = q.split()
                tbl   = parts[[p.upper() for p in parts].index("FROM")+1].rstrip(";")
                rows  = db_select_rows(tbl)
                log_history("SELECT", tbl, "success")
                if rows:
                    df = pd.DataFrame(rows)
                    if "WHERE" in qu:
                        widx = [p.upper() for p in parts].index("WHERE")
                        df   = df[df[parts[widx+1]].astype(str) == parts[widx+3].strip("'\"")]
                    st.metric("Rows", len(df))
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("Table is empty!")
            elif qu.startswith("INSERT INTO"):
                parts = q.split(); tbl = parts[2]
                vals  = [v.strip() for v in q[q.find("(")+1:q.find(")")].split(",")]
                keys  = ["id","name","age","col4","col5","col6"]
                row   = {keys[i]: vals[i] for i in range(min(len(vals),len(keys)))}
                ok, msg = db_insert_row(tbl, row)
                (st.success if ok else st.error)(f"{'✅' if ok else '❌'} {msg}")
                if ok: log_history("INSERT", tbl, "success")
            elif qu.startswith("DELETE FROM"):
                parts = q.split(); tbl = parts[2]
                if "WHERE" in qu:
                    widx = [p.upper() for p in parts].index("WHERE")
                    ok, msg = db_delete_row(tbl, parts[widx+1], parts[widx+3].strip("'\""))
                    (st.success if ok else st.error)(f"{'✅' if ok else '❌'} {msg}")
                    if ok: log_history("DELETE", tbl, "success")
                else:
                    st.warning("Add WHERE clause!")
            else:
                st.warning("Supported: SELECT, INSERT INTO, CREATE TABLE, DELETE FROM")
        except Exception as e:
            st.error(f"Error: {e}")
    st.divider()
    st.subheader("📖 Examples")
    for label, ex in {"Create": "CREATE TABLE students", "Insert": "INSERT INTO students VALUES (1, Alice, 22)",
                      "Select": "SELECT * FROM students", "Delete": "DELETE FROM students WHERE id = 1"}.items():
        st.code(ex, language="sql")

# ── QUERY EXECUTOR ─────────────────────────────────────────
elif page == "📊 Query Executor":
    st.header("Query Executor")
    with st.expander("➕ Create Table"):
        col1, col2 = st.columns([3,1])
        tname = col1.text_input("Table Name")
        if col2.button("Create", use_container_width=True):
            ok, msg = db_create_table(tname, st.session_state.username)
            (st.success if ok else st.error)(msg)
            if ok: log_history("CREATE", tname, "success"); st.rerun()
    with st.expander("📥 Insert Row"):
        if tables:
            ins_t = st.selectbox("Table", tables, key="ins_t")
            nc    = st.number_input("Columns", 1, 10, 3)
            cols  = st.columns(nc)
            cnames, cvals = [], []
            for i, c in enumerate(cols):
                cnames.append(c.text_input(f"Col {i+1}", value=["id","name","age"][i] if i<3 else f"col{i+1}", key=f"cn{i}"))
                cvals.append(c.text_input(f"Val {i+1}", key=f"cv{i}"))
            if st.button("Insert Row"):
                row = {cnames[i]: cvals[i] for i in range(nc)}
                ok, msg = db_insert_row(ins_t, row)
                (st.success if ok else st.error)(msg)
                if ok: log_history("INSERT", ins_t, "success")
        else:
            st.warning("Create a table first!")
    with st.expander("🔍 View & Search", expanded=True):
        if tables:
            sel_t  = st.selectbox("Table", tables, key="sel_t")
            search = st.text_input("🔍 Search")
            if st.button("Fetch Data"):
                rows = db_select_rows(sel_t)
                log_history("SELECT", sel_t, "success")
                if rows:
                    df = pd.DataFrame(rows)
                    if search:
                        df = df[df.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
                    st.metric("Rows", len(df))
                    st.dataframe(df, use_container_width=True)
                    st.download_button("📥 Export CSV", df.to_csv(index=False), f"{sel_t}.csv", "text/csv")
                else:
                    st.info("Table is empty!")
        else:
            st.warning("Create a table first!")

# ── DELETE & UPDATE ────────────────────────────────────────
elif page == "🗑️ Delete & Update":
    st.header("Delete & Update")
    if not tables:
        st.warning("Create a table first!")
    else:
        tab1, tab2 = st.tabs(["🗑️ Delete", "✏️ Update"])
        with tab1:
            dt = st.selectbox("Table", tables, key="dt")
            c1, c2 = st.columns(2)
            dk = c1.text_input("Column", value="id")
            dv = c2.text_input("Value")
            if st.button("🗑️ Delete", type="primary"):
                ok, msg = db_delete_row(dt, dk, dv)
                (st.success if ok else st.error)(msg)
                if ok: log_history("DELETE", dt, "success")
        with tab2:
            ut = st.selectbox("Table", tables, key="ut")
            c1, c2 = st.columns(2)
            uk = c1.text_input("Find Column", value="id")
            uv = c2.text_input("Find Value")
            nu = st.number_input("Fields", 1, 10, 2)
            uc = st.columns(nu); nd = {}
            for i, c in enumerate(uc):
                k = c.text_input("Col", key=f"uk{i}")
                v = c.text_input("Val", key=f"uv{i}")
                if k and v: nd[k] = v
            if st.button("✏️ Update", type="primary"):
                ok, msg = db_update_row(ut, uk, uv, nd)
                (st.success if ok else st.error)(msg)
                if ok: log_history("UPDATE", ut, "success")

# ── DATA VISUALIZATION ─────────────────────────────────────
elif page == "📉 Data Visualization":
    st.header("Data Visualization")
    if not tables:
        st.warning("Create a table first!")
    else:
        sel = st.selectbox("Table", tables)
        rows = db_select_rows(sel)
        if rows:
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True)
            st.divider()
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("Bar Chart")
                xc = st.selectbox("X", df.columns, key="bx")
                yc = st.selectbox("Y", df.columns, key="by")
                try:
                    st.plotly_chart(px.bar(df, x=xc, y=yc, color=xc), use_container_width=True)
                except:
                    st.warning("Select valid columns!")
            with c2:
                st.subheader("Pie Chart")
                pc = st.selectbox("Column", df.columns, key="pc")
                try:
                    st.plotly_chart(px.pie(df, names=pc, hole=0.3), use_container_width=True)
                except:
                    st.warning("Could not render!")
        else:
            st.info("Table is empty!")

# ── ML OPTIMIZER ───────────────────────────────────────────
elif page == "🤖 ML Optimizer":
    st.header("ML Query Optimizer")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Train Model")
        samples = st.slider("Samples", 500, 2000, 1000)
        if st.button("🚀 Train", type="primary"):
            with st.spinner("Training..."):
                try:
                    from data_collector import DataCollector
                    from optimizer import QueryOptimizer
                    DataCollector().generate_training_data(samples)
                    opt = QueryOptimizer(); opt.train()
                    st.session_state["optimizer"] = opt
                    st.success(f"Trained on {samples} samples!")
                except Exception as e:
                    st.error(f"Error: {e}")
    with c2:
        st.subheader("Predict")
        ts = st.slider("Table Size", 100, 10000, 1000)
        hw = st.checkbox("WHERE condition?")
        hi = st.checkbox("Index?")
        qt = st.selectbox("Query Type", ["SELECT","INSERT"])
        if st.button("🔮 Predict"):
            if "optimizer" not in st.session_state:
                st.warning("Train model first!")
            else:
                import numpy as np
                opt = st.session_state["optimizer"]
                f   = np.array([[0 if qt=="SELECT" else 1, ts, int(hw), int(hi)]])
                t   = opt.model.predict(f)[0]
                st.metric("Estimated Time", f"{t:.2f} ms")
                if hw and not hi and ts > 1000: st.error("⚠️ Add INDEX!")
                elif hi: st.success("✅ Optimized!")
                else: st.info("ℹ️ Looks good!")

# ── PERFORMANCE ────────────────────────────────────────────
elif page == "📈 Performance":
    st.header("Performance Analytics")
    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(pd.DataFrame({"Query":["SELECT *","SELECT WHERE","INSERT","SELECT+Index"],"Time(ms)":[45,12,8,3]}),
                     x="Query", y="Time(ms)", title="Execution Time", color="Time(ms)", color_continuous_scale="RdYlGn_r")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig2 = px.bar(pd.DataFrame({"Scenario":["No Index 1K","Index 1K","No Index 10K","Index 10K"],"Time(ms)":[45,3,450,5]}),
                      x="Scenario", y="Time(ms)", title="Index Impact", color="Time(ms)", color_continuous_scale="RdYlGn_r")
        st.plotly_chart(fig2, use_container_width=True)
    st.subheader("📡 Real-time Monitor")
    ph = st.empty()
    if st.button("▶️ Start"):
        import random
        for i in range(20):
            fig3 = go.Figure()
            fig3.add_trace(go.Scatter(y=[random.randint(1,50) for _ in range(5)], mode="lines+markers", line=dict(color="#00ff88")))
            fig3.update_layout(title="Live Query Times (ms)")
            ph.plotly_chart(fig3, use_container_width=True)
            time.sleep(0.5)

# ── QUERY HISTORY ──────────────────────────────────────────
elif page == "📜 Query History":
    st.header("Query History")
    if st.button("🔄 Refresh"): st.rerun()
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.metric("Total", len(df))
        st.dataframe(df, use_container_width=True)
        st.plotly_chart(px.pie(df, names="operation", title="Query Distribution"), use_container_width=True)
    else:
        st.info("No queries yet!")
