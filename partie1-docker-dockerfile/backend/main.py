# =========================
# Imports
# =========================
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import joblib
import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from contextlib import contextmanager
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
import time

# =========================
# FastAPI app
# =========================
app = FastAPI(
    title="API Backend IA - Penguins Prediction",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Database configuration (NO startup connection!)
# =========================
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://bd_user:password123@localhost:5432/bd_manchot"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# =========================
# Database dependency
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================
# Database model
# =========================
class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    features = Column(String, nullable=False)
    prediction = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


def wait_for_db(engine, retries=10, delay=3):
    """Attend que la DB soit prête avant de créer les tables"""
    for i in range(retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Database ready!")
            return True
        except OperationalError as e:
            print(f"DB not ready, retry {i+1}/{retries}: {e}")
            time.sleep(delay)
    raise RuntimeError("Database not ready after retries")

# =========================
# Create tables (safe & idempotent)
# =========================
try:
    wait_for_db(engine)
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"DB init failed: {e}")

# =========================
# Load ML model + scaler (async safe)
# =========================
MODEL_PATH = "models/penguins_model.pkl"
SCALER_PATH = "models/penguins_scaler.pkl"

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
except Exception as e:
    print(f"Model loading failed: {e}")
    model = None
    scaler = None

# =========================
# Pydantic schema
# =========================
class PredictRequest(BaseModel):
    features: list[float]

class PredictionResponse(BaseModel):
    prediction: str
    label: str

# =========================
# Routes
# =========================
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Backend IA - Penguins !"}

@app.get("/health")
def health_check():
    """Healthcheck sans DB - critique pour Docker Swarm"""
    return {"status": "healthy"}

'''@app.post("/predict", response_model=PredictionResponse)
def predict(data: PredictRequest, db: Session = Depends(get_db)):
    """Prediction avec gestion d'erreur DB"""
    if model is None or scaler is None:
        raise HTTPException(status_code=503, detail="ML models not loaded")
    
    try:
        # ML prediction
        X = np.array([data.features])
        X_scaled = scaler.transform(X)
        prediction = model.predict(X_scaled)[0]
        
        # DB save (non-bloquant)
        try:
            record = Prediction(features=str(data.features), prediction=prediction)
            db.add(record)
            db.commit()
        except Exception as db_err:
            db.rollback()
            print(f"DB save failed (non-critical): {db_err}")
            # Continue sans crash !
        
        return {"prediction": prediction, "label": prediction}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")'''


@app.post("/predict", response_model=PredictionResponse)
def predict(data: PredictRequest, db: Session = Depends(get_db)):
    """Prediction avec gestion d'erreur DB"""
    if model is None or scaler is None:
        raise HTTPException(status_code=503, detail="ML models not loaded")
    
    try:
        print(f"Received features: {data.features}")
        X = np.array([data.features])
        print(f"Input array: {X}, shape: {X.shape}")
        
        X_scaled = scaler.transform(X)
        print(f"Scaled input: {X_scaled}")
        
        prediction = model.predict(X_scaled)[0]
        print(f"Predicted: {prediction}")
        
        # DB save
        try:
            record = Prediction(features=str(data.features), prediction=prediction)
            db.add(record)
            db.commit()
        except Exception as db_err:
            db.rollback()
            # Log complet de l'erreur
            import traceback
            print("DB save failed (non-critical):")
            traceback.print_exc()
        
        return {"prediction": prediction, "label": prediction}
    
    except Exception as e:
        print(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")



@app.get("/predictions")
def get_predictions(db: Session = Depends(get_db)):
    """Récupère les prédictions avec gestion d'erreur"""
    try:
        records = db.query(Prediction).all()
        return [
            {
                "id": r.id, 
                "features": r.features, 
                "prediction": r.prediction, 
                "created_at": r.created_at
            }
            for r in records
        ]
    except Exception as e:
        print(f"DB query failed: {e}")
        raise HTTPException(status_code=503, detail="Database temporarily unavailable")

