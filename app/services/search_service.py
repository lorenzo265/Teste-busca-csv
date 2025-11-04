from __future__ import annotations

from typing import List

from app.data_providers.csv_provider import CSVDataProvider
from app.domain.query_normalizer import NormalizedQuery, normalize_search_query
from app.models.schemas import RecordSchema, SearchRequest


class SearchService:
    def __init__(self, data_provider: CSVDataProvider | None = None) -> None:
        self._data_provider = data_provider or CSVDataProvider()

    def search_records(self, request: SearchRequest) -> List[RecordSchema]:
        normalized: NormalizedQuery = normalize_search_query(request)
        records = self._data_provider.find_rows(normalized.filters, normalized.limit)
        return [RecordSchema(**record) for record in records]
