from __future__ import annotations

from io import BytesIO

import pandas as pd

from app.models.schemas import ExportRequest, ExportedFile


class ExportService:
    CSV_MEDIA_TYPE = "text/csv"
    XLSX_MEDIA_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    def export_records(self, request: ExportRequest) -> ExportedFile:
        data_frame = pd.DataFrame([record.dict(exclude_none=True) for record in request.data])

        if request.format == "csv":
            content = data_frame.to_csv(index=False).encode("utf-8")
            return ExportedFile(content=content, media_type=self.CSV_MEDIA_TYPE, filename="export.csv")

        if request.format == "xlsx":
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                data_frame.to_excel(writer, index=False)
            return ExportedFile(
                content=buffer.getvalue(),
                media_type=self.XLSX_MEDIA_TYPE,
                filename="export.xlsx",
            )

        raise ValueError("Unsupported export format")
