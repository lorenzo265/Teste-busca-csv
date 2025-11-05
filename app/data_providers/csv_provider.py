from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import os

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "base.csv"


class CSVDataProvider:
    def __init__(self, data_file: Path = DATA_FILE) -> None:
        self._data_file = Path(data_file)
        self._dataframe_cache: pd.DataFrame | None = None
        self._last_modified_ns: int | None = None

    def _load_dataframe(self) -> pd.DataFrame:
        modified_ns = os.stat(self._data_file).st_mtime_ns

        if self._dataframe_cache is None or self._last_modified_ns != modified_ns:
            dataframe = pd.read_csv(self._data_file, dtype=str, keep_default_na=False)
            self._dataframe_cache = dataframe.astype(str)
            self._last_modified_ns = modified_ns

        return self._dataframe_cache

    def find_rows(self, filters: Dict[str, Any], limit: int | None = None) -> List[Dict[str, Any]]:
        dataframe = self._load_dataframe()
        filtered_dataframe = dataframe

        for key, value in filters.items():
            filtered_dataframe = filtered_dataframe[filtered_dataframe[key].astype(str) == str(value)]

        if limit is not None:
            filtered_dataframe = filtered_dataframe.head(limit)

        return filtered_dataframe.copy().to_dict(orient="records")
