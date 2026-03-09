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

| Module          | Tech   | Status         |
| --------------- | ------ | -------------- |
| Storage Engine  | C++    | 🔄 In Progress |
| Query Processor | C++    | ⏳ Pending     |
| ML Optimizer    | Python | ⏳ Pending     |
| Java Middleware | Java   | ⏳ Pending     |
| Dashboard       | Python | ⏳ Pending     |

---

## How to Run

```bash
# Compile
g++ -std=c++17 src/main.cpp -o queryMind

# Run
./queryMind
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
- [ ] SQL Parser
- [ ] ML Query Optimizer
