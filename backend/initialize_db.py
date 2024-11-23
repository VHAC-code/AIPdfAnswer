from database import engine
from models import Base
import uvicorn


# Function to create tables
def init_db():
    """
    Create all database tables based on models defined in models.py.
    """
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    try:
        uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    except KeyboardInterrupt:
        print("\nApplication shutdown requested by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    init_db()
