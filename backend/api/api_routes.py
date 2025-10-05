import json
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Sequence
import csv
import io

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException

from backend.src.orchestrators.data_base_orchestrator import DataBaseOrchestrator
from backend.src.orchestrators.prediction_orchestrator import PredictionOrchestrator

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

ALLOWED_EXTENSIONS = {".xls", ".xlsx", ".xlsm", ".csv"}


class ExampleDataOrchestrator(DataBaseOrchestrator):
    """Adaptateur minimal pour exposer le snapshot JSON d'exemple."""

    def __init__(self, example_path: Path) -> None:
        super().__init__()
        self._example_path = example_path

    def get_dataset_snapshot(self) -> Dict[str, Any]:
        try:
            raw_content = self._example_path.read_text(encoding="utf-8")
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail="Jeu de données introuvable sur le serveur.") from exc

        try:
            payload: Dict[str, Any] = json.loads(raw_content)
        except json.JSONDecodeError as exc:
            raise HTTPException(status_code=500, detail="Jeu de données corrompu.") from exc
        return payload


example_data_orchestrator = ExampleDataOrchestrator(
    Path(__file__).resolve().parents[1] / "src" / "exemple_json_data.json"
)


@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API"}


@app.get("/api/hello")
def hello():
    return {"message": "Hello from FastAPI!"}


@app.get("/api/datasets/example")
def get_example_dataset():
    """Retourne un snapshot JSON conforme à `exemple_json_data`."""

    return example_data_orchestrator.get_dataset_snapshot()


def _serialize_value(value: Any) -> Any:
    """Convert Excel/CSV cell values to JSON serialisable items."""

    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return value


def _structure_table(rows: List[Sequence[Any]]) -> dict:
    if not rows:
        return {"columns": [], "rows": []}

    first_row = list(rows[0])
    if not any(first_row):
        header = [f"column_{idx + 1}" for idx in range(len(first_row))]
    else:
        header = []
        for idx, column in enumerate(first_row):
            if isinstance(column, str) and column.strip():
                header.append(column.strip())
            else:
                header.append(f"column_{idx + 1}")

    data_rows = []
    for raw_row in rows[1:]:
        row = list(raw_row)
        record = {}
        for idx, column_name in enumerate(header):
            value = row[idx] if idx < len(row) else None
            record[column_name] = _serialize_value(value)
        data_rows.append(record)

    return {
        "columns": header,
        "rows": data_rows,
    }


def _extract_excel(binary_file) -> dict:
    binary_file.seek(0)
    workbook = load_workbook(filename=binary_file, data_only=True)
    sheet = workbook.active
    rows = [list(row) for row in sheet.iter_rows(values_only=True)]
    return _structure_table(rows)


def _extract_csv(binary_file) -> dict:
    binary_file.seek(0)
    raw_bytes = binary_file.read()

    decoded_text = None
    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            decoded_text = raw_bytes.decode(encoding)
            break
        except UnicodeDecodeError:
            continue

    if decoded_text is None:
        raise ValueError("Impossible de décoder le fichier CSV.")

    reader = csv.reader(io.StringIO(decoded_text))
    rows = [row for row in reader]
    return _structure_table(rows)


@app.post("/api/upload-excel")
async def upload_excel(file: UploadFile = File(...)):
    """Reçoit un fichier Excel ou CSV et renvoie son contenu sous forme JSON."""

    if not file.filename:
        raise HTTPException(status_code=400, detail="Nom de fichier manquant.")

    extension = Path(file.filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Format non pris en charge. Veuillez fournir un fichier Excel ou CSV (.xls, .xlsx, .xlsm, .csv).",
        )

    try:
        if extension == ".csv":
            payload = _extract_csv(file.file)
        else:
            payload = _extract_excel(file.file)
    except InvalidFileException as exc:
        raise HTTPException(status_code=400, detail="Fichier Excel invalide ou corrompu.") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except csv.Error as exc:
        raise HTTPException(status_code=400, detail="Fichier CSV invalide.") from exc
    except Exception as exc:  # pragma: no cover - unexpected loader failure
        raise HTTPException(status_code=500, detail="Impossible de lire le fichier fourni.") from exc
    finally:
        await file.close()

        prediction_orchestrator = PredictionOrchestrator()

    return {
        "message": "Fichier analysé avec succès.",
        "filename": file.filename,
        "result": prediction_orchestrator.process_and_predict(payload),

    }
