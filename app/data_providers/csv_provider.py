from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "base.csv"


class CSVDataProvider:
    def __init__(self, data_file: Path = DATA_FILE) -> None:
        self._data_file = data_file

    def find_rows(self, filters: Dict[str, Any], limit: int | None = None) -> List[Dict[str, Any]]:
        dataframe = pd.read_csv(self._data_file, dtype=str, keep_default_na=False)
        dataframe = dataframe.astype(str)
        
        for key, value in filters.items():
            dataframe = dataframe[dataframe[key].astype(str) == str(value)]

        if limit is not None:
            dataframe = dataframe.head(limit)

        return dataframe.to_dict(orient="records")
