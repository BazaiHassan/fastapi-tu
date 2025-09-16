# core/migrations/env.py
from logging.config import fileConfig
import os
import sys
from importlib import import_module
from sqlalchemy import engine_from_config, pool
from alembic import context

# ✅ Import Base — now SAFE
from core.src.db import Base
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)
else:
    print("Warning: .env file not found. Using global env vars.")

DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in environment")

config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- NUCLEAR CLEANUP ---
print(">>> CLEANING UP: Clearing Base.metadata and sys.modules")
Base.metadata.clear()

# Full module paths
model_modules = [
    "core.user.models",
    "core.expense.models",
    "core.category.models",
    "core.budget.models",
]

for module_name in model_modules:
    if module_name in sys.modules:
        print(f">>> Removing {module_name} from sys.modules")
        del sys.modules[module_name]

print(">>> Tables BEFORE imports:", list(Base.metadata.tables.keys()))

# --- IMPORT MODELS ---
for module_name in model_modules:
    print(f">>> Importing {module_name}...")
    import_module(module_name)

print(">>> Tables AFTER imports:", list(Base.metadata.tables.keys()))

target_metadata = Base.metadata

# --- MIGRATION FUNCTIONS ---
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()