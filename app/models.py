# app/models.py

from sqlalchemy import Column, String, Date, Numeric, TIMESTAMP
import uuid
from database import Base


class Client(Base):
    __tablename__ = "clients"

    client_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date)
    mobile = Column(String, nullable=False)
    annual_income = Column(Numeric)
    created_at = Column(TIMESTAMP, nullable=False)

class Recording(Base):
    __tablename__ = "recording_sessions"

    session_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String, nullable=False)
    audio_file_path = Column(String, nullable=False)
    recorded_on = Column(TIMESTAMP)
