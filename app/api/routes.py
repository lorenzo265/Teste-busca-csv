from fastapi import APIRouter, HTTPException, Response

from app.models.schemas import ExportRequest, SchemaResponse, SearchRequest, SearchResponse
from app.services.export_service import ExportService
from app.services.search_service import SearchService

api_router = APIRouter()

search_service = SearchService()
export_service = ExportService()


@api_router.post("/search", response_model=SearchResponse)
def search_records(request: SearchRequest) -> SearchResponse:
    results = search_service.search_records(request)
    return SearchResponse(count=len(results), results=results)


@api_router.post("/export")
def export_records(request: ExportRequest) -> Response:
    try:
        exported = export_service.export_records(request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    response = Response(content=exported.content, media_type=exported.media_type)
    response.headers.update({"Content-Disposition": f"attachment; filename={exported.filename}"})
    return response


@api_router.get("/schema", response_model=SchemaResponse)
def get_schema() -> SchemaResponse:
    return SchemaResponse()
