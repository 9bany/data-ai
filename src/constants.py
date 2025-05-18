from os.path import join
from pathlib import Path

ROOT_DIR = str(Path.home()) + "/data-ai"
DB_MEM_FILE=join(ROOT_DIR, "db-mem")
DB_STORE_FILE=join(ROOT_DIR, "db-store")
DB_VECTOR_FILE=join(ROOT_DIR, "db-vector")
IMAGES_PATH=join(ROOT_DIR, "images")
USER_ID="root"