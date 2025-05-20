# Data-AI: AI Agents for Your Databases
> ⚠️ **Warning:** This project is under active development. Expect breaking changes, incomplete features, and evolving APIs.

Data-AI is a command-line tool that transforms your databases into AI-powered agents. Each agent understands your schema, stores vectorized knowledge, and participates in collaborative or routed AI conversations.

## Features

- Connect to multiple databases via URI
- Automatically loads schema and metadata
- Generates vectorized knowledge from database structure
- Each database becomes an AI agent with memory
- Supports collaborative/Coordinative team chat between agents
- Simple CLI commands: `add`, `list`, `chat`, `delete`

---

## System Overview

![system overview](./docs/assets/1000000.png)

---

## Installation

### 1. Clone the repository
```bash
git clone git@github.com:9bany/data-ai.git
cd data-ai
pip install -e .
```

### 2. Configure environment variables
Create a `.env` file in the project root or export variables directly:
```bash
export OPENAI_API_KEY=your-openai-api-key       # Required for OpenAI GPT
export GOOGLE_API_KEY=your-google-api-key       # Optional for Google GenAI
export ANTHROPIC_API_KEY=your-anthropic-api-key # Optional for Anthropic
export GROQ_API_KEY=your-groq-api-key           # Optional for Groq
```


## Usage
Once installed, the CLI is available as `data-ai`. You can also run `python src/main.py <command>` directly.

### Add a database
```bash
data-ai add --uri "postgresql://user:pass@localhost:5432/mydb" --name mydb
```

### List all registered databases
```bash
data-ai list
```

### 💬 Start an AI chat
```bash
data-ai chat --work-mode collaborate --show-member-response
```

### Delete a database agent
```bash
data-ai delete mydb
```

Each connected database becomes an agent that understands the schema and can participate in AI-powered conversations with other databases.

## Examples
- [Multiple database](https://github.com/9bany/data-ai/tree/master/examples/multi_db)

## Supported Databases

| Database     | Driver                  | Status     |
|--------------|--------------------------|------------|
| PostgreSQL   | `psycopg2-binary`        | ✅ Stable  |
| MySQL        | `mysql+pymysql`          | ✅ Stable  |
| ClickHouse   | `clickhouse-sqlalchemy`  | ✅ Stable  |
| BigQuery     | `google-cloud-bigquery`  | 🚧 Unstable  |

## URI Database format
- Mysql: `mysql+pymysql://<user>:<password>@<host>:<port>/<database>`
- PostgreSQL: `postgresql://<user>:<password>@<host>:<port>/<database>`
- Clickhouse: `clickhouse<+driver>://<user>:<password>@<host>:<port>/<database>[?key=value..]`

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
