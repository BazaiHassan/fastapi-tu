from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, UUID
import uuid

SQLALCHEMY_DB_URL="sqlite:///./sqlite.db"

engine = create_engine(
    SQLALCHEMY_DB_URL,
    connect_args={"check_same_thread":False}
)

Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Tables
class Expense(Base):
    __tablename__ = "expenses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)

Base.metadata.create_all(engine)

# Dependency to get database session
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()