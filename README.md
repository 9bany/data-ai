# Data-AI

**Data-AI** is a terminal-based intelligent agent platform that connects to multiple databases (PostgreSQL, MySQL, Redis, MongoDB, ClickHouse, BigQuery...) and transforms them into AI-powered agents capable of understanding, storing, and reasoning over your data.

## Features

- Connect to multiple databases via URI
- Automatically loads schema and metadata
- Generates vectorized knowledge from database structure
- Each database becomes an AI agent with memory
- Supports collaborative team chat between agents
- Easy CLI commands: `add`, `list`, `chat`

---

## System Overview

```
          ┌────────────┐
          │  CLI (typer) ├────────┐
          └────┬───────┘         │
               │                 ▼
         ┌─────▼─────┐      ┌─────────────┐
         │ DB Engine │─────▶ Load Metadata│
         └─────┬─────┘      └─────────────┘
               │                 │
               ▼                 ▼
        VectorStore        KnowledgeBase (JSON)
               │                 │
               ▼                 ▼
           Agent (SQLAgent)     ◀──────────┐
               │                            │
               ▼                            │
         Team Discussion <───────── User CLI Interaction
```

---

## Installation

### 1. Clone & install dependencies
```bash
git clone https://github.com/yourname/data-ai.git
cd data-ai
pip install -r requirements.txt
```

### 2. Set up your `.env`
```env
OPENAI_API_KEY=your-openai-api-key
```


## Usage

### Add a database
```bash
python src/main.py add --uri "postgresql://user:pass@localhost:5432/mydb"
```

### List all connected databases
```bash
python src/main.py list
```

### 💬 Start a collaborative AI chat
```bash
python src/main.py chat
```

Each connected database becomes an agent that understands the schema and can participate in AI-powered conversations with other databases.


## Supported Databases

| Database     | Driver                  | Status     |
|--------------|--------------------------|------------|
| PostgreSQL   | `psycopg2`               | ✅ Stable  |
| MySQL        | `mysql+pymysql`          | ✅ Stable  |
| Redis        | `redis-py`               | ✅ Basic   |
| MongoDB      | `pymongo`                | ✅ Stable  |
| ClickHouse   | `clickhouse-connect`     | ✅ Stable  |
| BigQuery     | `google-cloud-bigquery`  | ✅ Stable  |

## How Agents Work

- Automatically parse database schema
- Convert structure and metadata into vectorized knowledge
- Load knowledge into `JSONKnowledgeBase`
- Use `OpenAI GPT` models to answer, reason, and collaborate
- Agents chat as a team to reach consensus

## Contributing

1. Fork this repo
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Submit a pull request 🙌

---

## 📄 License

MIT License. Free to use, distribute, and modify.

---

## 🙏 Credits

Built with:
- [Typer](https://github.com/tiangolo/typer)
- [Rich](https://github.com/Textualize/rich)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [OpenAI](https://platform.openai.com/)
- [Qdrant / Chroma / JSON Vector DBs](https://qdrant.tech/)

---

> 💫 If you find this useful, please ⭐ the repo or share it with others!
