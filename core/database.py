from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from core.config import settings
from core.base import Base
import sys
import os

# Use an in-memory SQLite database when running under pytest to keep tests isolated
is_testing = "PYTEST_CURRENT_TEST" in os.environ or "pytest" in sys.modules

if is_testing:
    # Use StaticPool so the in-memory SQLite database is shared across connections
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool)
else:
    engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Use the project's Declarative `Base` so model metadata is shared
Base = Base

# During tests, ensure all model modules are imported and create tables
if is_testing:
    import importlib
    import os

    models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    try:
        for fname in os.listdir(models_dir):
            if fname.endswith(".py") and fname != "__init__.py":
                mod_name = fname[:-3]
                importlib.import_module(f"models.{mod_name}")
    except Exception:
        pass

    # create all tables for the in-memory test database
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()