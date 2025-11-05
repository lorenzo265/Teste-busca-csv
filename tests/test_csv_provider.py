from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import pytest

from app.data_providers import csv_provider
from app.data_providers.csv_provider import CSVDataProvider


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    dataframe = pd.DataFrame(rows)
    dataframe.to_csv(path, index=False)


def test_find_rows_supports_aliases_and_numeric_filters(tmp_path: Path) -> None:
    data_file = tmp_path / "data.csv"
    _write_csv(
        data_file,
        [
            {
                "TICO_CODIGO": "03",
                "FLAG": "Y",
                "SUFRAMA": "12345",
                "UF": "SP",
            },
            {
                "TICO_CODIGO": "06",
                "FLAG": "N",
                "SUFRAMA": "",
                "UF": "RJ",
            },
        ],
    )

    provider = CSVDataProvider(data_file)

    flag_results = provider.find_rows({"FLAGS": "Y"})
    assert len(flag_results) == 1
    assert flag_results[0]["FLAGS"] == "Y"
    assert flag_results[0]["INSCR_SUFRAMA"] == "12345"

    contrib_results = provider.find_rows({"TICO_CODIGO": 3})
    assert len(contrib_results) == 1
    assert contrib_results[0]["TICO_CODIGO"] == "03"


def test_find_rows_raises_for_unknown_columns(tmp_path: Path) -> None:
    data_file = tmp_path / "data.csv"
    _write_csv(data_file, [{"UF": "SP"}])

    provider = CSVDataProvider(data_file)

    with pytest.raises(ValueError) as excinfo:
        provider.find_rows({"UNKNOWN": "value"})

    assert "UNKNOWN" in str(excinfo.value)


def test_dataframe_is_cached_between_calls(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    data_file = tmp_path / "data.csv"
    _write_csv(data_file, [{"UF": "SP"}])

    provider = CSVDataProvider(data_file)

    call_count = 0
    original_read_csv = csv_provider.pd.read_csv

    def tracked_read_csv(*args: Any, **kwargs: Any):
        nonlocal call_count
        call_count += 1
        return original_read_csv(*args, **kwargs)

    monkeypatch.setattr(csv_provider.pd, "read_csv", tracked_read_csv)

    provider.find_rows({})
    provider.find_rows({})

    assert call_count == 1
