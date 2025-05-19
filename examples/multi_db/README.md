# Multi-Database Example for Data-AI

This example demonstrates how to spin up a MySQL, PostgreSQL, MongoDB, and ClickHouse environment, load test data into each, and register them into the Data-AI agent system.

---

## Step 1: Start All Services

Launch all required databases using Docker Compose:

```bash
docker compose up -d
```

This will start:
- MySQL (port `3306`)
- PostgreSQL (port `5432`)
- ClickHouse (ports `8123`, `9000`)

---

## Step 2: Load Data

Run the script to initialize schemas and populate example data for all databases:

```bash
python load_data.py
```

This includes:
- Users, stores, orders, and products in MySQL
- Transactions in PostgreSQL
- Events in ClickHouse

---

## Step 3: Register Databases with AI Agent

Use the `data-ai` CLI to add each database:

```bash
# ClickHouse
data-ai add clickhouse+native://root:root@localhost:19000/ch-data-ai-test

# PostgreSQL
data-ai add postgresql://postgres:root@localhost/pg-data-ai-test

# MySQL
data-ai add mysql+pymysql://root:root@localhost/mysql-data-ai-test
```

Once added, the AI agent can interact with these databases, explain their structure, and answer natural language questions using SQL or domain-specific logic.

---
