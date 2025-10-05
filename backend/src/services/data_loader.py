from __future__ import annotations
import pandas as pd
import io
import os
import json
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional, Sequence

@dataclass
class DataLoadError:
    field: Optional[str]
    code: str
    message: str

    def to_json(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class DataLoadResult:
    ok: bool
    rows: List[Dict[str, Any]]
    errors: List[DataLoadError]
    columns: List[str]
    source_name: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ok": self.ok,
            "rows": self.rows,
            "errors": [error.to_json() for error in self.errors],
            "columns": self.columns,
            "source_name": self.source_name,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)



class DataLoader:
    """Charge un dataset CSV/XLS/XLSX et vérifie uniquement la présence des colonnes nécessaires."""

    def __init__(
        self,
        required_columns: Optional[Sequence[str]] = None,
    ) -> None:
        self.required_columns = list(required_columns) if required_columns else []


    def load_file(self, path: str) -> DataLoadResult:
        source_name = os.path.basename(path) if path else None
        try:
            if not path or not os.path.exists(path):
                return self._error_result("file_not_found", f"Fichier introuvable: {path}", source_name)

            ext = os.path.splitext(path)[1].lower()
            if ext == ".csv":
                df = pd.read_csv(path)
            elif ext in (".xls", ".xlsx"):
                df = pd.read_excel(path)
            else:
                return self._error_result("unsupported_type", f"Type non supporté: {ext}", source_name)

            return self._validate(df, source_name)
        except Exception as exc:
            return self._error_result("load_failure", f"Erreur de chargement: {exc}", source_name)

    def load_bytes(self, content: bytes, filename: str) -> DataLoadResult:
        source_name = filename
        try:
            ext = os.path.splitext(filename)[1].lower()
            buffer = io.BytesIO(content)

            if ext == ".csv":
                df = pd.read_csv(buffer)
            elif ext in (".xls", ".xlsx"):
                df = pd.read_excel(buffer)
            else:
                return self._error_result("unsupported_type", f"Type non supporté: {ext}", source_name)

            return self._validate(df, source_name)
        except Exception as exc:
            return self._error_result("load_failure", f"Erreur de chargement: {exc}", source_name)

    def _validate(self, df: pd.DataFrame, source_name: Optional[str]) -> DataLoadResult:
        df.columns = [str(c).strip() for c in df.columns]
        errors: List[DataLoadError] = []

        missing = [col for col in self.required_columns if col not in df.columns]
        if missing:
            errors.append(DataLoadError(None, "missing_columns", f"Colonnes manquantes: {', '.join(missing)}"))

        return DataLoadResult(
            ok=len(errors) == 0,
            rows=df.to_dict(orient="records"),
            errors=errors,
            columns=list(df.columns),
            source_name=source_name,
        )
        
    def _error_result(self, code: str, message: str, source_name: Optional[str]) -> DataLoadResult:
        return DataLoadResult(
            ok=False,
            rows=[],
            errors=[DataLoadError(None, code, message)],
            columns=[],
            source_name=source_name,
        )


if __name__ == "__main__":
    required_cols = ["pl_orbper", "pl_rade", "pl_tranmid", "st_teff"]

    loader = DataLoader(required_columns=required_cols)

    # === Cas 1 : Fichier inexistant
    res = loader.load_file("fichier_inexistant.csv")
    print(res.to_json())

    # === Cas 2 : Colonnes manquantes
    df_missing = pd.DataFrame({
        "pl_orbper": [365],
        "st_teff": [5778]
    })
    df_missing.to_csv("test_missing.csv", index=False)
    res = loader.load_file("test_missing.csv")
    print(res.to_json())

    # === Cas 3 : Données valides
    df_valid = pd.DataFrame({
        "pl_orbper": [365, 420],
        "pl_rade": [1.0, 1.2],
        "pl_tranmid": [2458330.5, 2458331.2],
        "st_teff": [5778, 5800],
        "extra_col": ["ok", "ok"]
    })
    df_valid.to_csv("test_valid.csv", index=False)
    res = loader.load_file("test_valid.csv")
    print(res.to_json())

    # === Cas 4 : Upload (bytes)
    buffer = io.BytesIO()
    df_valid.to_csv(buffer, index=False)
    buffer.seek(0)
    bytes_data = buffer.read()
    res = loader.load_bytes(bytes_data, "upload.csv")
    print(res.to_json())
