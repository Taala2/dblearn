from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings

# Create SQLModel engine
engine = create_engine(
    settings.DATABASE_URL, 
    echo=False,  # Set to True for SQL query logging
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
)

def create_db_and_tables():
    """Create database tables on application startup."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency for database session."""
    with Session(engine) as session:
        yield session