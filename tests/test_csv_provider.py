from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import pandas as pd
import pytest

from app.data_providers.csv_provider import CSVDataProvider


def _write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    dataframe = pd.DataFrame(rows)
    dataframe.to_csv(path, index=False)


@pytest.fixture()
def csv_file(tmp_path: Path) -> Path:
    file_path = tmp_path / "data.csv"
    rows = [
        {"UF": "SP", "CNPJ": "123", "TICO_CODIGO": "1"},
        {"UF": "RJ", "CNPJ": "456", "TICO_CODIGO": "2"},
        {"UF": "RJ", "CNPJ": "789", "TICO_CODIGO": "3"},
    ]
    _write_csv(file_path, rows)
    return file_path


def test_find_rows_applies_filters_and_limit(csv_file: Path) -> None:
    provider = CSVDataProvider(data_file=csv_file)

    records = provider.find_rows({"UF": "RJ"}, limit=1)

    assert len(records) == 1
    assert records[0]["CNPJ"] == "456"


def test_find_rows_reuses_cached_dataframe(csv_file: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    provider = CSVDataProvider(data_file=csv_file)

    call_count = 0
    original_read_csv = pd.read_csv

    def counting_read_csv(*args, **kwargs):  # type: ignore[no-untyped-def]
        nonlocal call_count
        call_count += 1
        return original_read_csv(*args, **kwargs)

    monkeypatch.setattr(pd, "read_csv", counting_read_csv)

    provider.find_rows({"UF": "RJ"})
    provider.find_rows({"UF": "SP"})

    assert call_count == 1


def test_find_rows_reloads_when_file_changes(csv_file: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    provider = CSVDataProvider(data_file=csv_file)

    call_count = 0
    original_read_csv = pd.read_csv

    def counting_read_csv(*args, **kwargs):  # type: ignore[no-untyped-def]
        nonlocal call_count
        call_count += 1
        return original_read_csv(*args, **kwargs)

    monkeypatch.setattr(pd, "read_csv", counting_read_csv)

    provider.find_rows({"UF": "RJ"})
    assert call_count == 1

    updated_rows = [
        {"UF": "MG", "CNPJ": "321", "TICO_CODIGO": "9"},
    ]
    _write_csv(csv_file, updated_rows)

    records = provider.find_rows({"UF": "MG"})

    assert call_count == 2
    assert records == updated_rows
