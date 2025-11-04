import pytest

from app.domain.query_normalizer import normalize_search_query
from app.models.schemas import SearchRequest


def test_contribuinte_sets_default_tico_when_missing():
    request = SearchRequest(UF="SP", Contribuinte=True, Quantity=5)

    normalized = normalize_search_query(request)

    assert normalized.filters["UF"] == "SP"
    assert normalized.filters["TICO_CODIGO"] == 3
    assert normalized.limit == 5


def test_contribuinte_false_sets_expected_tico():
    request = SearchRequest(Contribuinte=False)

    normalized = normalize_search_query(request)

    assert normalized.filters["TICO_CODIGO"] == 6
    assert normalized.limit is None


def test_explicit_tico_is_not_overridden_by_contribuinte():
    request = SearchRequest(TICO_CODIGO=8, Contribuinte=True, Quantity=1)

    normalized = normalize_search_query(request)

    assert normalized.filters["TICO_CODIGO"] == 8
    assert normalized.limit == 1


def test_ignores_unknown_fields():
    request = SearchRequest.parse_obj({"UF": "RJ", "Unknown": "value"})

    normalized = normalize_search_query(request)

    assert normalized.filters == {"UF": "RJ"}


@pytest.mark.parametrize("quantity", [None, 1, 5])
def test_limit_values(quantity):
    request = SearchRequest(Quantity=quantity) if quantity is not None else SearchRequest()

    normalized = normalize_search_query(request)

    expected = quantity if quantity is not None else None
    assert normalized.limit == expected
