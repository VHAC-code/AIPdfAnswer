from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL
DATABASE_URL = "sqlite:///./documents.db"

# Create the database engine with additional configurations
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False},  # Necessary for SQLite in multi-threaded environments
    pool_pre_ping=True,  # Checks connections before using them
    pool_size=5,  # Maximum number of connections in the pool
    max_overflow=10  # Overflow beyond pool_size before rejecting connections
)

# Define a base class for models
Base = declarative_base()

# Create a local session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    """
    Yields a database session. Automatically rolls back on exceptions and closes properly.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        print(f"Database session rollback due to: {e}")
        raise
    finally:
        db.close()
