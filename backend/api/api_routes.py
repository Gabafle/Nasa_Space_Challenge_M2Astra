from datetime import datetime
from pathlib import Path
import shutil

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Mon API", version="1.0.0")

# Configuration CORS pour permettre les requetes depuis le frontend
origins = [
    "http://localhost:3000",  # Vue dev server
    "http://localhost:5173",  # Vite dev server (par defaut)
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory used to persist Excel files uploaded from the frontend
UPLOADS_DIR = Path(__file__).resolve().parents[2] / "uploads"
ALLOWED_EXCEL_EXTENSIONS = {".xls", ".xlsx", ".xlsm"}


@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API"}


@app.get("/api/hello")
def hello():
    return {"message": "Hello from FastAPI!"}


@app.post("/api/upload-excel")
async def upload_excel(file: UploadFile = File(...)):
    """Receive an Excel file and persist it under uploads/."""

    if not file.filename:
        raise HTTPException(status_code=400, detail="Nom de fichier manquant.")

    extension = Path(file.filename).suffix.lower()
    if extension not in ALLOWED_EXCEL_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Format non pris en charge. Veuillez fournir un fichier Excel (.xls, .xlsx, .xlsm).",
        )

    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    safe_name = Path(file.filename).name
    destination = UPLOADS_DIR / f"{timestamp}_{safe_name}"

    try:
        file.file.seek(0)
        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except OSError as exc:
        raise HTTPException(status_code=500, detail="Impossible de sauvegarder le fichier.") from exc
    finally:
        await file.close()

    return {
        "message": "Fichier Excel recus avec succes.",
        "filename": destination.name,
        "original_filename": safe_name,
    }
