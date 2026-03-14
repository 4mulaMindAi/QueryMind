import sys
import os

# ML folder ko python path me add kar rahe hain
# taaki waha ke modules import ho sake
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ml'))

# Required libraries import
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

# Supabase client create karne ke liye library
from supabase import create_client, Client

## Main interface
# Streamlit page configuration
st.set_page_config(page_title="QueryMind Dashboard", page_icon="🧠", layout="wide")

# Supabase project URL
SUPABASE_URL = "https://mrolmkndebwzgleijcxv.supabase.co"

# Supabase public API key
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1yb2xta25kZWJ3emdsZWlqY3h2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM0NzMxMTMsImV4cCI6MjA4OTA0OTExM30.4ZKu0uwhADQyZ9EO1abJVq23jj2JBN2ZFEN-D344BJE"

# Supabase client initialize
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Session state me query history store karne ke liye
if "history" not in st.session_state:
    st.session_state.history = []

# Query history log karne ka function
def log_history(op, tbl, status): ## login history
    st.session_state.history.append({
        "operation": op,  # Query type (SELECT, INSERT, etc.)
        "table": tbl,     # Table name
        "status": status, # Success ya failure
        "time": time.strftime("%Y-%m-%d %H:%M:%S")  # Current time
    })

# Login function
def db_login(username, password): ## login
    try:
        # users table me username aur password match karte hain
        res = supabase.table("users").select("*").eq("username", username).eq("password", password).execute()

        # Agar user mil gaya to login success
        return (True, res.data[0]) if res.data else (False, "Invalid username or password!")

    except Exception as e:
        return False, str(e)

# Signup function
def db_signup(username, email, password): ## signup
    try:
        # Check karte hain username already exist karta hai ya nahi
        ex = supabase.table("users").select("*").eq("username", username).execute()

        if ex.data:
            return False, "Username already exists!"

        # New user database me insert karte hain
        supabase.table("users").insert({
            "username": username,
            "email": email,
            "password": password
        }).execute()

        return True, "Account created successfully!"

    except Exception as e:
        return False, str(e)

# Password reset function
def db_reset_password(username, email, new_password): ## reset pasword
    try:
        # Username aur email verify karte hain
        res = supabase.table("users").select("*").eq("username", username).eq("email", email).execute()

        if res.data:
            # Password update karte hain
            supabase.table("users").update({"password": new_password}).eq("username", username).execute()
            return True, "Password reset successfully!"

        return False, "Username or email not found!"

    except Exception as e:
        return False, str(e)

# Database me existing tables fetch karne ka function
def db_get_tables():
    try:
        res = supabase.table("db_tables").select("*").execute()

        # Table names list me return karte hain
        return [t["name"] for t in res.data]

    except:
        return []

# New table create karne ka function
def db_create_table(name, username):
    try:
        # Check karte hain table already exist karta hai ya nahi
        ex = supabase.table("db_tables").select("*").eq("name", name).execute()

        if ex.data:
            return False, "Table already exists!"

        # New table record create
        supabase.table("db_tables").insert({
            "name": name,
            "created_by": username
        }).execute()

        return True, f"Table '{name}' created!"

    except Exception as e:
        return False, str(e)

# Table me row insert karne ka function
def db_insert_row(table_name, row):
    try:
        # Row data db_rows table me store karte hain
        supabase.table("db_rows").insert({
            "table_name": table_name,
            "row_data": row
        }).execute()

        return True, "1 row inserted!"

    except Exception as e:
        return False, str(e)

# Table ke rows fetch karne ka function
def db_select_rows(table_name):
    try:
        # Table ke rows fetch
        res = supabase.table("db_rows").select("*").eq("table_name", table_name).execute()

        # Sirf row_data return karte hain
        return [r["row_data"] for r in res.data]

    except:
        return []
# Row delete karne ka function
def db_delete_row(table_name, key, value):
    try:
        # Table ke saare rows fetch karte hain
        rows = supabase.table("db_rows").select("*").eq("table_name", table_name).execute()
        
        # Har row check karte hain
        for r in rows.data:
            # Agar column key ki value match karti hai
            if str(r["row_data"].get(key)) == value:
                # Us row ko delete kar dete hain
                supabase.table("db_rows").delete().eq("id", r["id"]).execute()
        
        return True, "Row deleted!"
    
    except Exception as e:
        return False, str(e)


# Row update karne ka function
def db_update_row(table_name, key, value, new_data):
    try:
        # Table ke rows fetch
        rows = supabase.table("db_rows").select("*").eq("table_name", table_name).execute()
        
        # Har row check karte hain
        for r in rows.data:
            # Agar key ki value match kare
            if str(r["row_data"].get(key)) == value:
                
                # Old data aur new data ko merge karte hain
                updated = {**r["row_data"], **new_data}
                
                # Updated row database me save karte hain
                supabase.table("db_rows").update({"row_data": updated}).eq("id", r["id"]).execute()
        
        return True, "Row updated!"
    
    except Exception as e:
        return False, str(e)


# Session state me login status initialize
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    

## Login Interface
# Agar user logged in nahi hai to login page show hoga
if not st.session_state.logged_in:

    # App title
    st.title("🧠 QueryMind")

    # Subtitle / tagline
    st.markdown("### 4mulaMind — Intelligent Database Engine")

    # Divider line
    st.divider()

    # Centered layout banane ke liye columns
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        # Login / Signup / Reset ke tabs
        tab1, tab2, tab3 = st.tabs(["🔐 Login", "📝 Sign Up", "🔑 Forgot Password"])


# ---------------- LOGIN TAB ----------------
        with tab1:

            st.subheader("Welcome Back!")

            # Username input
            lu = st.text_input("Username", key="lu")

            # Password input
            lp = st.text_input("Password", type="password", key="lp")

            # Login button
            if st.button("Login", type="primary", use_container_width=True):

                # Validation check
                if not lu or not lp:
                    st.error("Please fill all fields!")

                else:
                    # Login function call
                    ok, res = db_login(lu, lp)

                    if ok:
                        # Login success -> session update
                        st.session_state.logged_in = True
                        st.session_state.username  = lu
                        st.rerun()
                    else:
                        st.error(res)

            # Default credentials hint
            st.caption("Default: **admin** / **querymind**")


# ---------------- SIGNUP TAB ----------------
        with tab2:

            st.subheader("Create Account")

            # User inputs
            su  = st.text_input("Username", key="su")
            se  = st.text_input("Email", key="se")
            sp  = st.text_input("Password", type="password", key="sp")
            sp2 = st.text_input("Confirm Password", type="password", key="sp2")

            # Create account button
            if st.button("Create Account", type="primary", use_container_width=True):

                if not su or not sp:
                    st.error("Username and password required!")

                elif sp != sp2:
                    st.error("Passwords do not match!")

                elif len(sp) < 6:
                    st.error("Password must be 6+ characters!")

                else:
                    # Signup function call
                    ok, msg = db_signup(su, se, sp)

                    if ok:
                        st.success(msg + " Please login.")
                    else:
                        st.error(msg)


# ---------------- RESET PASSWORD TAB ----------------
        with tab3:

            st.subheader("Reset Password")

            # Inputs
            fp_user  = st.text_input("Username", key="fp_user")
            fp_email = st.text_input("Email", key="fp_email")
            fp_new   = st.text_input("New Password", type="password", key="fp_new")
            fp_new2  = st.text_input("Confirm Password", type="password", key="fp_new2")

            # Reset button
            if st.button("Reset Password", type="primary", use_container_width=True):

                if not fp_user or not fp_email or not fp_new:
                    st.error("Please fill all fields!")

                elif fp_new != fp_new2:
                    st.error("Passwords do not match!")

                elif len(fp_new) < 6:
                    st.error("Password must be 6+ characters!")

                else:
                    # Reset password function
                    ok, msg = db_reset_password(fp_user, fp_email, fp_new)

                    if ok:
                        st.success("✅ " + msg + " Please login.")
                    else:
                        st.error(msg)

# Login page ke baad app stop ho jata hai jab tak login na ho
    st.stop()

# ---------------- DASHBOARD HEADER ----------------

col1, col2 = st.columns([8, 2])

# Dashboard title
col1.title("🧠 QueryMind Dashboard")

# Subtitle
col1.markdown("**4mulaMind** — Intelligent Database Engine")

# Logout button
if col2.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.rerun()

# Divider
st.divider()


# Database se tables fetch
tables = db_get_tables()


# ---------------- SIDEBAR ----------------

st.sidebar.title("🧠 QueryMind")

# Logged in user show
st.sidebar.success(f"👤 {st.session_state.username}")

st.sidebar.markdown("---")

# Engine status
st.sidebar.success("🟢 Engine Running")


# Tables list show
if tables:
    st.sidebar.markdown("### Tables")
    
    for t in tables:
        rows = db_select_rows(t)
        st.sidebar.markdown(f"• `{t}` ({len(rows)} rows)")


st.sidebar.markdown("---")


# Navigation menu
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

# Check if the selected page is Overview
if page == "🏠 Overview":

    # Page title
    st.header("System Overview")

    # Try to fetch total users from Supabase database
    try:
        res = supabase.table("users").select("*").execute()
        total_users = len(res.data)  # Count total users
    except:
        total_users = 0  # If database error occurs, set users to 0

    # Create 5 columns to display metrics
    col1, col2, col3, col4, col5 = st.columns(5)

    # Display system information metrics
    col1.metric("Engine",   "QueryMind v1.0")                 # Engine name
    col2.metric("Company",  "4mulaMind")                      # Company name
    col3.metric("Tables",   len(tables))                      # Number of tables
    col4.metric("Queries",  len(st.session_state.history))    # Total queries executed
    col5.metric("👥 Users", total_users)                      # Total users in system

    # Add horizontal divider
    st.divider()

    # Create two columns for Architecture and Tech Stack
    col1, col2 = st.columns(2)

    # -------- Architecture Section --------
    with col1:
        st.subheader("Architecture")

        # Dictionary representing system architecture
        arch = {
            "Module": ["Storage Engine","Query Processor","ML Optimizer","Java API","Dashboard"],
            "Tech":   ["C++","C++","Python","Java","Python"],
            "Status": ["✅ Done","✅ Done","✅ Done","✅ Done","✅ Done"]
        }

        # Convert dictionary to DataFrame and display it
        st.dataframe(pd.DataFrame(arch), use_container_width=True)

    # -------- Tech Stack Section --------
    with col2:
        st.subheader("Tech Stack")

        # Create pie chart showing technology distribution
        fig = px.pie(
            values=[30,30,20,20],
            names=["C++","Python","Java","SQL"],
            hole=0.4
        )

        # Display the pie chart
        st.plotly_chart(fig, use_container_width=True)
        
        
# -------------------- SQL Query Box Page --------------------
elif page == "💻 SQL Query Box":

    # Page title
    st.header("SQL Query Box")

    # Text area where user writes SQL queries
    query = st.text_area(
        "Enter SQL Query",
        height=120,
        placeholder="SELECT * FROM users\nINSERT INTO users VALUES (1, Alice, 22)\nCREATE TABLE products"
    )

    # Run query button
    if st.button("▶️ Run Query", type="primary"):

        # Remove extra spaces and create uppercase version for parsing
        q = query.strip()
        qu = q.upper()

        try:

            # -------- CREATE TABLE --------
            if qu.startswith("CREATE TABLE"):

                # Extract table name
                tbl = q.split()[2]

                # Call function to create table
                ok, msg = db_create_table(tbl, st.session_state.username)

                # Show success or error message
                (st.success if ok else st.error)(f"{'✅' if ok else '❌'} {msg}")

                # Log query history
                if ok:
                    log_history("CREATE", tbl, "success")
                    st.rerun()

            # -------- SELECT QUERY --------
            elif qu.startswith("SELECT") and "FROM" in qu:

                parts = q.split()

                # Extract table name after FROM
                tbl = parts[[p.upper() for p in parts].index("FROM") + 1].rstrip(";")

                # Fetch rows from database
                rows = db_select_rows(tbl)

                # Log query
                log_history("SELECT", tbl, "success")

                if rows:

                    # Convert rows to DataFrame
                    df = pd.DataFrame(rows)

                    # Handle WHERE condition if present
                    if "WHERE" in qu:
                        widx = [p.upper() for p in parts].index("WHERE")

                        df = df[
                            df[parts[widx + 1]].astype(str)
                            == parts[widx + 3].strip("'\"")
                        ]

                    # Show number of rows
                    st.metric("Rows", len(df))

                    # Display table
                    st.dataframe(df, use_container_width=True)

                else:
                    st.info("Table is empty!")

            # -------- INSERT QUERY --------
            elif qu.startswith("INSERT INTO"):

                parts = q.split()
                tbl = parts[2]

                # Extract values inside parentheses
                vals = [
                    v.strip()
                    for v in q[q.find("(") + 1 : q.find(")")].split(",")
                ]

                # Default column names
                keys = ["id", "name", "age", "col4", "col5", "col6"]

                # Create row dictionary
                row = {keys[i]: vals[i] for i in range(min(len(vals), len(keys)))}

                # Insert row into database
                ok, msg = db_insert_row(tbl, row)

                # Show result
                (st.success if ok else st.error)(f"{'✅' if ok else '❌'} {msg}")

                # Log query
                if ok:
                    log_history("INSERT", tbl, "success")

            # -------- DELETE QUERY --------
            elif qu.startswith("DELETE FROM"):

                parts = q.split()
                tbl = parts[2]

                # Check if WHERE condition exists
                if "WHERE" in qu:

                    widx = [p.upper() for p in parts].index("WHERE")

                    # Delete row using column and value
                    ok, msg = db_delete_row(
                        tbl,
                        parts[widx + 1],
                        parts[widx + 3].strip("'\""),
                    )

                    # Show result
                    (st.success if ok else st.error)(f"{'✅' if ok else '❌'} {msg}")

                    # Log query
                    if ok:
                        log_history("DELETE", tbl, "success")

                else:
                    st.warning("Add WHERE clause!")

            # Unsupported query
            else:
                st.warning("Supported: SELECT, INSERT INTO, CREATE TABLE, DELETE FROM")

        # Handle unexpected errors
        except Exception as e:
            st.error(f"Error: {e}")

    # Divider line
    st.divider()

    # -------- Example Queries --------
    st.subheader("📖 Examples")

    for label, ex in {
        "Create": "CREATE TABLE students",
        "Insert": "INSERT INTO students VALUES (1, Alice, 22)",
        "Select": "SELECT * FROM students",
        "Delete": "DELETE FROM students WHERE id = 1",
    }.items():
        st.code(ex, language="sql")
        
# ---------------- Query Executor Page ----------------
elif page == "📊 Query Executor":

    # Page title
    st.header("Query Executor")

    # -------- Create Table Section --------
    with st.expander("➕ Create Table"):

        # Create two columns for input and button
        col1, col2 = st.columns([3,1])

        # Input field for table name
        tname = col1.text_input("Table Name")

        # Button to create table
        if col2.button("Create", use_container_width=True):

            # Call database function to create table
            ok, msg = db_create_table(tname, st.session_state.username)

            # Show success or error message
            (st.success if ok else st.error)(msg)

            # Log query history
            if ok:
                log_history("CREATE", tname, "success")
                st.rerun()

    # -------- Insert Row Section --------
    with st.expander("📥 Insert Row"):

        # Check if tables exist
        if tables:

            # Select table to insert data
            ins_t = st.selectbox("Table", tables, key="ins_t")

            # Select number of columns
            nc = st.number_input("Columns", 1, 10, 3)

            # Create dynamic columns for inputs
            cols = st.columns(nc)

            cnames, cvals = [], []

            # Loop for column names and values
            for i, c in enumerate(cols):

                # Column name input
                cnames.append(
                    c.text_input(
                        f"Col {i+1}",
                        value=["id","name","age"][i] if i < 3 else f"col{i+1}",
                        key=f"cn{i}"
                    )
                )

                # Column value input
                cvals.append(c.text_input(f"Val {i+1}", key=f"cv{i}"))

            # Insert button
            if st.button("Insert Row"):

                # Create dictionary for row data
                row = {cnames[i]: cvals[i] for i in range(nc)}

                # Insert row in database
                ok, msg = db_insert_row(ins_t, row)

                # Show result
                (st.success if ok else st.error)(msg)

                # Log history
                if ok:
                    log_history("INSERT", ins_t, "success")

        else:
            st.warning("Create a table first!")

# -------- View & Search Section --------
    with st.expander("🔍 View & Search", expanded=True):

        if tables:

            # Select table to view
            sel_t = st.selectbox("Table", tables, key="sel_t")

            # Search input
            search = st.text_input("🔍 Search")

            # Button to fetch data
            if st.button("Fetch Data"):

                # Fetch rows from database
                rows = db_select_rows(sel_t)

                # Log query
                log_history("SELECT", sel_t, "success")

                if rows:

                    # Convert rows to DataFrame
                    df = pd.DataFrame(rows)

                    # Apply search filter
                    if search:
                        df = df[
                            df.apply(
                                lambda r: r.astype(str)
                                .str.contains(search, case=False)
                                .any(),
                                axis=1
                            )
                        ]

                    # Display row count
                    st.metric("Rows", len(df))

                    # Display table
                    st.dataframe(df, use_container_width=True)

                    # Export CSV option
                    st.download_button(
                        "📥 Export CSV",
                        df.to_csv(index=False),
                        f"{sel_t}.csv",
                        "text/csv"
                    )

                else:
                    st.info("Table is empty!")

        else:
            st.warning("Create a table first!")


# ---------------- Delete & Update Page ----------------
elif page == "🗑️ Delete & Update":

    # Page title
    st.header("Delete & Update")

    # If no tables exist
    if not tables:
        st.warning("Create a table first!")

    else:

        # Tabs for delete and update
        tab1, tab2 = st.tabs(["🗑️ Delete", "✏️ Update"])

        # -------- Delete Row --------
        with tab1:

            # Select table
            dt = st.selectbox("Table", tables, key="dt")

            # Column and value input
            c1, c2 = st.columns(2)

            dk = c1.text_input("Column", value="id")
            dv = c2.text_input("Value")

            # Delete button
            if st.button("🗑️ Delete", type="primary"):

                # Delete row
                ok, msg = db_delete_row(dt, dk, dv)

                # Show result
                (st.success if ok else st.error)(msg)

                # Log history
                if ok:
                    log_history("DELETE", dt, "success")

        # -------- Update Row --------
        with tab2:

            # Select table
            ut = st.selectbox("Table", tables, key="ut")

            # Column and value to find
            c1, c2 = st.columns(2)

            uk = c1.text_input("Find Column", value="id")
            uv = c2.text_input("Find Value")

            # Number of fields to update
            nu = st.number_input("Fields", 1, 10, 2)

            # Dynamic inputs
            uc = st.columns(nu)
            nd = {}

            for i, c in enumerate(uc):

                k = c.text_input("Col", key=f"uk{i}")
                v = c.text_input("Val", key=f"uv{i}")

                # Add to update dictionary
                if k and v:
                    nd[k] = v

            # Update button
            if st.button("✏️ Update", type="primary"):

                # Update row in database
                ok, msg = db_update_row(ut, uk, uv, nd)

                # Show result
                (st.success if ok else st.error)(msg)

                # Log history
                if ok:
                    log_history("UPDATE", ut, "success")
# ---------------- Data Visualization Page ----------------
elif page == "📉 Data Visualization":

    # Page title
    st.header("Data Visualization")

    # Agar koi table nahi hai to warning
    if not tables:
        st.warning("Create a table first!")
    else:

        # Dropdown se table select karna
        sel = st.selectbox("Table", tables)

        # Selected table ka data fetch karna
        rows = db_select_rows(sel)

        if rows:

            # Rows ko pandas DataFrame me convert karna
            df = pd.DataFrame(rows)

            # Data table display karna
            st.dataframe(df, use_container_width=True)

            # UI divider
            st.divider()

            # Page ko 2 columns me divide karna
            c1, c2 = st.columns(2)

            # -------- Bar Chart Section --------
            with c1:
                st.subheader("Bar Chart")

                # X axis column select karna
                xc = st.selectbox("X", df.columns, key="bx")

                # Y axis column select karna
                yc = st.selectbox("Y", df.columns, key="by")

                try:
                    # Plotly bar chart render karna
                    st.plotly_chart(
                        px.bar(df, x=xc, y=yc, color=xc),
                        use_container_width=True
                    )
                except:
                    st.warning("Select valid columns!")

            # -------- Pie Chart Section --------
            with c2:
                st.subheader("Pie Chart")

                # Pie chart ke liye column select
                pc = st.selectbox("Column", df.columns, key="pc")

                try:
                    # Plotly pie chart render
                    st.plotly_chart(
                        px.pie(df, names=pc, hole=0.3),
                        use_container_width=True
                    )
                except:
                    st.warning("Could not render!")

        else:
            # Agar table empty ho
            st.info("Table is empty!")


# ---------------- ML Optimizer Page ----------------
elif page == "🤖 ML Optimizer":

    # Page title
    st.header("ML Query Optimizer")

    # Page layout
    c1, c2 = st.columns(2)

    # -------- Train Model Section --------
    with c1:

        st.subheader("Train Model")

        # Training samples select karna
        samples = st.slider("Samples", 500, 2000, 1000)

        # Train button
        if st.button("🚀 Train", type="primary"):

            with st.spinner("Training..."):
                try:
                    # Data generator import
                    from data_collector import DataCollector

                    # ML optimizer import
                    from optimizer import QueryOptimizer

                    # Training dataset generate karna
                    DataCollector().generate_training_data(samples)

                    # Model train karna
                    opt = QueryOptimizer()
                    opt.train()

                    # Model session me store karna
                    st.session_state["optimizer"] = opt

                    st.success(f"Trained on {samples} samples!")

                except Exception as e:
                    st.error(f"Error: {e}")

# -------- Prediction Section --------
    with c2:

        st.subheader("Predict")

        # Table size input
        ts = st.slider("Table Size", 100, 10000, 1000)

        # WHERE condition checkbox
        hw = st.checkbox("WHERE condition?")

        # Index checkbox
        hi = st.checkbox("Index?")

        # Query type select
        qt = st.selectbox("Query Type", ["SELECT","INSERT"])

        # Predict button
        if st.button("🔮 Predict"):

            # Agar model train nahi hua
            if "optimizer" not in st.session_state:
                st.warning("Train model first!")

            else:
                import numpy as np

                # Model load
                opt = st.session_state["optimizer"]

                # Feature array create karna
                f = np.array([[0 if qt=="SELECT" else 1, ts, int(hw), int(hi)]])

                # Prediction
                t = opt.model.predict(f)[0]

                # Estimated execution time show
                st.metric("Estimated Time", f"{t:.2f} ms")

                # Optimization suggestion
                if hw and not hi and ts > 1000:
                    st.error("⚠️ Add INDEX!")

                elif hi:
                    st.success("✅ Optimized!")

                else:
                    st.info("ℹ️ Looks good!")


# ---------------- Performance Analytics Page ----------------
elif page == "📈 Performance":

    # Page title
    st.header("Performance Analytics")

    # Page layout
    c1, c2 = st.columns(2)

    # -------- Query Execution Time Graph --------
    with c1:

        fig = px.bar(
            pd.DataFrame({
                "Query":["SELECT *","SELECT WHERE","INSERT","SELECT+Index"],
                "Time(ms)":[45,12,8,3]
            }),
            x="Query",
            y="Time(ms)",
            title="Execution Time",
            color="Time(ms)",
            color_continuous_scale="RdYlGn_r"
        )

        st.plotly_chart(fig, use_container_width=True)

    # -------- Index Impact Graph --------
    with c2:

        fig2 = px.bar(
            pd.DataFrame({
                "Scenario":["No Index 1K","Index 1K","No Index 10K","Index 10K"],
                "Time(ms)":[45,3,450,5]
            }),
            x="Scenario",
            y="Time(ms)",
            title="Index Impact",
            color="Time(ms)",
            color_continuous_scale="RdYlGn_r"
        )

        st.plotly_chart(fig2, use_container_width=True)

    # -------- Real-time Monitor --------
    st.subheader("📡 Real-time Monitor")

    # Placeholder chart
    ph = st.empty()

    # Start monitoring
    if st.button("▶️ Start"):

        import random

        for i in range(20):

            fig3 = go.Figure()

            # Random query execution times generate
            fig3.add_trace(
                go.Scatter(
                    y=[random.randint(1,50) for _ in range(5)],
                    mode="lines+markers",
                    line=dict(color="#00ff88")
                )
            )

            fig3.update_layout(title="Live Query Times (ms)")

            ph.plotly_chart(fig3, use_container_width=True)

            time.sleep(0.5)


# ---------------- Query History Page ----------------
elif page == "📜 Query History":

    # Page title
    st.header("Query History")

    # Refresh button
    if st.button("🔄 Refresh"):
        st.rerun()

    # Agar history exist karti hai
    if st.session_state.history:

        # History ko DataFrame me convert
        df = pd.DataFrame(st.session_state.history)

        # Total queries metric
        st.metric("Total", len(df))

        # Table display
        st.dataframe(df, use_container_width=True)

        # Query distribution pie chart
        st.plotly_chart(
            px.pie(df, names="operation", title="Query Distribution"),
            use_container_width=True
        )

    else:
        st.info("No queries yet!")