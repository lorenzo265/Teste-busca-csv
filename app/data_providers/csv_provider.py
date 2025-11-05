from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "base.csv"

_COLUMN_ALIASES: Dict[str, str] = {
    "FLAG": "FLAGS",
    "SUFRAMA": "INSCR_SUFRAMA",
}


class CSVDataProvider:
    def __init__(self, data_file: Path = DATA_FILE) -> None:
        self._data_file = data_file
        self._dataframe: pd.DataFrame | None = None
        self._dataframe_mtime: float | None = None

    def _load_dataframe(self) -> pd.DataFrame:
        mtime = self._data_file.stat().st_mtime

        if self._dataframe is not None and self._dataframe_mtime == mtime:
            return self._dataframe

        dataframe = pd.read_csv(self._data_file, dtype=str, keep_default_na=False)

        rename_map = {
            alias: canonical
            for alias, canonical in _COLUMN_ALIASES.items()
            if alias in dataframe.columns and canonical not in dataframe.columns
        }
        if rename_map:
            dataframe = dataframe.rename(columns=rename_map)

        self._dataframe = dataframe
        self._dataframe_mtime = mtime
        return dataframe

    def _canonical_column(self, column: str) -> str:
        return _COLUMN_ALIASES.get(column, column)

    def find_rows(self, filters: Dict[str, Any], limit: int | None = None) -> List[Dict[str, Any]]:
        dataframe = self._load_dataframe()
        filtered = dataframe

        for key, value in filters.items():
            column = self._canonical_column(key)

            if column not in filtered.columns:
                raise ValueError(f"Column '{key}' is not available in the data source.")

            if column == "TICO_CODIGO":
                series = pd.to_numeric(filtered[column], errors="coerce")
                filter_value = pd.to_numeric([value], errors="coerce")[0]

                if pd.isna(filter_value):
                    filtered = filtered[series.isna()]
                else:
                    filtered = filtered[series == filter_value]
                continue

            filtered = filtered[filtered[column].astype(str) == str(value)]

        if limit is not None:
            filtered = filtered.head(limit)

        return filtered.to_dict(orient="records")
