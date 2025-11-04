from pathlib import Path

import pytest

from app.data_providers.csv_provider import CSVDataProvider


pd = pytest.importorskip("pandas")


@pytest.fixture()
def sample_csv(tmp_path: Path) -> Path:
    data = pd.DataFrame(
        [
            {
                "UF": "SP",
                "CNPJ": "111",
                "TICO_CODIGO": 3,
                "ENTE_FEDERATIVO": "Municipio",
            },
            {
                "UF": "RJ",
                "CNPJ": "222",
                "TICO_CODIGO": 6,
                "ENTE_FEDERATIVO": "Estado",
            },
        ]
    )
    file_path = tmp_path / "dataset.csv"
    data.to_csv(file_path, index=False)
    return file_path


def test_filters_records(sample_csv: Path):
    provider = CSVDataProvider(data_file=sample_csv)

    results = provider.find_rows({"UF": "SP", "TICO_CODIGO": 3})

    assert len(results) == 1
    assert results[0]["CNPJ"] == "111"


def test_limit_is_applied(sample_csv: Path):
    provider = CSVDataProvider(data_file=sample_csv)

    results = provider.find_rows({}, limit=1)

    assert len(results) == 1
