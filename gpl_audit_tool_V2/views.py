"""Django views for the V2 GPL audit API."""

from __future__ import annotations

import asyncio
import traceback
import uuid
from pathlib import Path

import pandas as pd
from django.conf import settings
from django.http import FileResponse, Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from gpl_audit_tool_V2.log_parser.config import (
    set_output_file,
    set_pre_files,
    set_post_files,
)
from gpl_audit_tool_V2.main import main as run_gpl_audit_pipeline

JOBS_ROOT = Path(settings.MEDIA_ROOT) / "gpl_audit_jobs"


def _save_uploaded_files(files, dest_dir: Path) -> list[Path]:
    dest_dir.mkdir(parents=True, exist_ok=True)
    saved = []
    for f in files:
        target = dest_dir / f.name
        with open(target, "wb") as out:
            for chunk in f.chunks():
                out.write(chunk)
        saved.append(target)
    return saved


def _excel_summary(excel_path: Path) -> list[dict]:
    """Return a lightweight per-sheet summary for the generated report."""
    try:
        xl = pd.ExcelFile(excel_path)
    except Exception:
        return []

    sheets = []
    for name in xl.sheet_names:
        try:
            df = xl.parse(name)
            sheets.append(
                {
                    "sheet": name,
                    "rows": int(len(df)),
                    "columns": list(map(str, df.columns)),
                }
            )
        except Exception:
            sheets.append({"sheet": name, "rows": None, "columns": []})
    return sheets


class HealthCheckView(APIView):
    """Simple liveness probe."""

    def get(self, request, *args, **kwargs):
        return Response({"status": "ok"})


class RunGPLAuditView(APIView):
    """Upload PRE/POST logs and run the comparison pipeline."""

    def post(self, request, *args, **kwargs):
        pre_files = request.FILES.getlist("pre_files")
        post_files = request.FILES.getlist("post_files")

        if not pre_files or not post_files:
            return Response(
                {
                    "error": (
                        "Both 'pre_files' and 'post_files' are required as multipart/form-data."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        job_id = uuid.uuid4().hex
        job_dir = JOBS_ROOT / job_id
        pre_dir = job_dir / "input" / "pre"
        post_dir = job_dir / "input" / "post"
        output_dir = job_dir / "output"

        try:
            pre_paths = _save_uploaded_files(pre_files, pre_dir)
            post_paths = _save_uploaded_files(post_files, post_dir)

            set_pre_files(pre_paths)
            set_post_files(post_paths)
            set_output_file(output_dir / "GPL_AUDIT.xlsx")

            try:
                zip_path: Path = asyncio.run(run_gpl_audit_pipeline())
            except SystemExit:
                return Response(
                    {
                        "job_id": job_id,
                        "error": "Parsing failed — check that the uploaded files are valid GPL audit log exports.",
                    },
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )

            excel_path = next(output_dir.rglob("*.xlsx"), None)
            sheets = _excel_summary(excel_path) if excel_path else []

            return Response(
                {
                    "job_id": job_id,
                    "status": "completed",
                    "sheets": sheets,
                    "excel_filename": excel_path.name if excel_path else None,
                    "zip_filename": zip_path.name if zip_path else None,
                    "download_excel_url": request.build_absolute_uri(
                        f"/gpl_audit_V2/download-excel/{job_id}/"
                    ),
                    "download_zip_url": request.build_absolute_uri(
                        f"/gpl_audit_V2/download/{job_id}/"
                    ),
                },
                status=status.HTTP_200_OK,
            )

        except FileNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            traceback.print_exc()
            return Response(
                {"error": f"Unexpected error: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


def _find_job_output_file(job_id: str, suffix: str) -> Path | None:
    job_dir = JOBS_ROOT / job_id
    if not job_dir.exists():
        return None

    matches = sorted(job_dir.rglob(f"*{suffix}"))
    return matches[0] if matches else None


class DownloadZipView(APIView):
    """Download the generated correction-scripts zip."""

    def get(self, request, job_id, *args, **kwargs):
        zip_path = _find_job_output_file(job_id, ".zip")
        if not zip_path or not zip_path.exists():
            raise Http404("Zip result not found for this job_id.")
        return FileResponse(open(zip_path, "rb"), as_attachment=True, filename=zip_path.name)


class DownloadExcelView(APIView):
    """Download the generated Excel report."""

    def get(self, request, job_id, *args, **kwargs):
        excel_path = _find_job_output_file(job_id, ".xlsx")
        if not excel_path or not excel_path.exists():
            raise Http404("Excel result not found for this job_id.")
        return FileResponse(open(excel_path, "rb"), as_attachment=True, filename=excel_path.name)
