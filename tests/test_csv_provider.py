import pandas as pd
from pathlib import Path
from typing import Dict, List, Any

class CSVDataProvider:
    def __init__(self, data_file: Path):
        self.data_file = Path(data_file)

    def find_rows(self, filters: Dict[str, Any], limit: int | None = None) -> List[dict]:
        df = pd.read_csv(self.data_file)

        # aplica filtros
        for key, value in filters.items():
            # pula campos de controle
            if key in ("Quantity",):
                continue

            # converte tudo pra string pra evitar 3 vs "3"
            df = df[df[key].astype(str) == str(value)]

        if limit:
            df = df.head(limit)

        return df.to_dict(orient="records")
