<!-- @format -->

# QueryMind 🧠

An intelligent relational database engine built from scratch.
Storage engine in C++, ML optimizer in Python, and REST API in Java.

---

## What is QueryMind?

QueryMind is a fully custom database engine that stores data on disk,
parses SQL queries, and uses Machine Learning to optimize query execution.
No external database libraries used — everything built from ground up.

---

## Architecture
```
Python Dashboard  →  Visualization & Analytics
ML Optimizer      →  Intelligent Query Planning
Java Middleware   →  REST API Layer
C++ Core Engine   →  Storage & Query Execution
```

## Modules

| Module          | Tech   | Status    |
| --------------- | ------ | --------- |
| Storage Engine  | C++    | ✅ Done   |
| Query Processor | C++    | ✅ Done   |
| ML Optimizer    | Python | ✅ Done   |
| Java Middleware | Java   | 🔄 In Progress |
| Dashboard       | Python | ⏳ Pending |

---

## How to Run
```bash
# Compile C++ Engine
g++ -std=c++17 src/main.cpp -o queryMind
./queryMind

# Run ML Optimizer
source ml/venv/bin/activate
python3 ml/optimizer.py
```

---

## Tech Stack

- C++ — Storage Engine & Query Processor
- Python — ML Optimizer & Dashboard
- Java — REST API Middleware

---

## Progress

- [x] Page Structure
- [x] Disk Manager
- [x] Buffer Pool + LRU
- [x] B+ Tree Index
- [x] SQL Lexer
- [x] SQL Parser
- [x] Execution Engine
- [x] Terminal UI
- [x] ML Data Collector
- [x] ML Random Forest Optimizer
- [ ] Java Middleware
- [ ] Web Dashboard