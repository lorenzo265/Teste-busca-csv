from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class RecordSchema(BaseModel):
    UF: Optional[str] = None
    CNPJ: Optional[str] = None
    CEP: Optional[str] = None
    IE: Optional[str] = None
    FLAGS: Optional[str] = None
    IND_ORGAO_GOVERNAMENTAL: Optional[str] = None
    COD_NATUREZA_JURIDICA: Optional[str] = None
    TICO_CODIGO: Optional[int] = None
    ENTE_FEDERATIVO: Optional[str] = None
    INSCR_SUFRAMA: Optional[str] = None

    model_config = ConfigDict(extra="ignore")



class SearchRequest(BaseModel):
    UF: Optional[str] = None
    CNPJ: Optional[str] = None
    CEP: Optional[str] = None
    IE: Optional[str] = None
    FLAGS: Optional[str] = None
    IND_ORGAO_GOVERNAMENTAL: Optional[str] = None
    COD_NATUREZA_JURIDICA: Optional[str] = None
    TICO_CODIGO: Optional[int] = None
    ENTE_FEDERATIVO: Optional[str] = None
    INSCR_SUFRAMA: Optional[str] = None
    Contribuinte: Optional[bool] = None
    Quantity: Optional[int] = Field(default=None, gt=0)

    model_config = ConfigDict(extra="allow")



class SearchResponse(BaseModel):
    count: int
    results: List[RecordSchema]


class ExportRequest(BaseModel):
    data: List[RecordSchema]
    format: Literal["xlsx", "csv"] = "xlsx"


class SchemaResponse(BaseModel):
    fields: Dict[str, str] = Field(
        default_factory=lambda: {
            "UF": "string",
            "CNPJ": "string",
            "CEP": "string",
            "IE": "string",
            "FLAGS": "string",
            "IND_ORGAO_GOVERNAMENTAL": "string",
            "COD_NATUREZA_JURIDICA": "string",
            "TICO_CODIGO": "int",
            "ENTE_FEDERATIVO": "string",
            "INSCR_SUFRAMA": "string",
            "Contribuinte": "boolean",
            "Quantity": "int",
        }
    )


@dataclass
class ExportedFile:
    content: bytes
    media_type: str
    filename: str
