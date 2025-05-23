from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import Client, Recording
from datetime import datetime
import os, shutil, uuid
import psycopg2

Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"status": "Voice Risk Profiler API Running 🚀"}


@app.get("/test-db")
def test_db():
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "db"),
            database=os.getenv("POSTGRES_DB", "postgres"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", "password")
        )
        conn.close()
        return {"status": "Connection successful! ✅"}
    except Exception as e:
        return {"status": "Connection failed ❌", "error": str(e)}


@app.post("/upload_audio/")
def upload_audio(
    client_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        audio_id = str(uuid.uuid4())
        file_path = f"/code/audio/{audio_id}.wav"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        new_recording = Recording(
            session_id=audio_id,
            client_id=client_id,
            audio_file_path=file_path,
            recorded_on=datetime.utcnow()
        )

        db.add(new_recording)
        db.commit()

        return {
            "msg": "File uploaded successfully 🎤✅",
            "audio_id": audio_id,
            "file_path": file_path
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
