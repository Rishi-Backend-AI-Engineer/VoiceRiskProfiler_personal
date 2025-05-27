from alembic import context
from sqlalchemy import text
from sqlalchemy import engine_from_config, pool
import os
import sys
from dotenv import load_dotenv
load_dotenv()


# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import your Base metadata
from app.database import Base  # Adjust if Base is located elsewhere

# Target metadata for Alembic
target_metadata = Base.metadata

# Function to construct the database URL
def get_url():
    return (
        f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:"  # No default fallback — forces valid .env
        f"{os.getenv('POSTGRES_PASSWORD')}@"
        f"{os.getenv('POSTGRES_HOST')}:" 
        f"{os.getenv('POSTGRES_PORT')}/"
        f"{os.getenv('POSTGRES_DB')}"
    )

def run_migrations_online():
    config = context.config
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
        url=get_url()  # Inject dynamic URL
    )

    with connectable.connect() as connection:
        connection.execute(text("SET search_path TO user_schema, public"))

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema='user_schema',  # <-- ensure alembic_version is in this schema
            compare_type=True  # Optional: track type changes too
        )

        with context.begin_transaction():
            context.run_migrations()

# Entry point
if context.is_offline_mode():
    raise NotImplementedError("Offline migrations are not supported.")
else:
    run_migrations_online()
