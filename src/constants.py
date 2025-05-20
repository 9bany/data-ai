from os.path import join
from pathlib import Path

# Default user ID used by the system
USER_ID = "root"

# Root directory under user's home for all app data
ROOT_DIR = str(Path.home()) + "/data-ai"

# File path to store in-memory database representations
DB_MEM_FILE = join(ROOT_DIR, "db-mem")

# File path to store registered database connection info
DB_STORE_FILE = join(ROOT_DIR, "db-store")

# File path for storing vectorized knowledge base
DB_VECTOR_FILE = join(ROOT_DIR, "db-vector")

# Path to store image outputs (e.g., for visualizations)
IMAGES_PATH = join(ROOT_DIR, "images")

# Model used to analyze database schema and generate metadata
ANALYZE_MODEL_NAME = "openai:gpt-4o"

# Model used for individual database agent interactions
MEMBER_MODEL_NAME = "openai:gpt-3.5-turbo"

# Model used for the team leader agent to synthesize group responses
TEAM_LEADER_MODEL_NAME = "openai:o4-mini"