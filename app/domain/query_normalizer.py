from __future__ import annotations

from typing import Any, Dict, NamedTuple

from app.models.schemas import SearchRequest

ALLOWED_FILTER_FIELDS = {
    "UF",
    "CNPJ",
    "CEP",
    "IE",
    "FLAGS",
    "IND_ORGAO_GOVERNAMENTAL",
    "COD_NATUREZA_JURIDICA",
    "TICO_CODIGO",
    "ENTE_FEDERATIVO",
    "INSCR_SUFRAMA",
}


class NormalizedQuery(NamedTuple):
    filters: Dict[str, Any]
    limit: int | None


def normalize_search_query(request: SearchRequest) -> NormalizedQuery:
    payload = request.dict(exclude_unset=True)

    limit = payload.pop("Quantity", None)
    contrib = payload.pop("Contribuinte", None)

    filters: Dict[str, Any] = {
        key: value
        for key, value in payload.items()
        if key in ALLOWED_FILTER_FIELDS and value is not None
    }

    if contrib is not None:
        filters["TICO_CODIGO"] = 3 if contrib else 6

    limit_value = None
    if isinstance(limit, int):
        limit_value = max(limit, 1)

    return NormalizedQuery(filters=filters, limit=limit_value)
