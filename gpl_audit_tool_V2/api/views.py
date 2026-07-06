"""
REST endpoints wrapping the existing GPL comparison engine (log_parser/ +
main.py, unmodified) so it can be driven from Postman instead of the
Tkinter GUI.

Flow:
    1. POST /api/gpl-audit/run/
       multipart/form-data with:
         - pre_files  : one or more PRE .txt log files
         - post_files : one or more POST .txt log files
       Runs the full audit pipeline synchronously and returns JSON with a
       job_id, a per-sheet summary of the generated Excel report, and
       download links.

    2. GET /api/gpl-audit/download/<job_id>/
       Downloads the correction-scripts zip (Excel + AMOS scripts) for
       that job.

    3. GET /api/gpl-audit/download-excel/<job_id>/
       Downloads just the generated .xlsx report for that job.

    4. GET /api/gpl-audit/health/
       Simple liveness check.
"""
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

from log_parser.config import (
    set_output_file,
    set_pre_files,
    set_post_files,
)
from main import main as run_gpl_audit_pipeline

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
    """Lightweight per-sheet summary (name/row count/columns) of the report,
    used purely so the run/ response gives the caller something useful
    without having to download the file first."""
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
    """GET /api/gpl-audit/health/ — simple liveness probe."""

    def get(self, request, *args, **kwargs):
        return Response({"status": "ok"})


class RunGPLAuditView(APIView):
    """POST /api/gpl-audit/run/ — upload PRE/POST logs, run the comparison."""

    def post(self, request, *args, **kwargs):
        pre_files = request.FILES.getlist("pre_files")
        post_files = request.FILES.getlist("post_files")

        if not pre_files or not post_files:
            return Response(
                {
                    "error": (
                        "Both 'pre_files' and 'post_files' are required "
                        "as multipart/form-data — attach one or more files "
                        "under each field name."
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

            # These are contextvars (see log_parser/config.py) — they must be
            # set in the SAME thread that then calls asyncio.run(...) below,
            # exactly like log_parser's own GUI worker thread does, otherwise
            # the pipeline silently falls back to the default input/ folders.
            set_pre_files(pre_paths)
            set_post_files(post_paths)
            set_output_file(output_dir / "GPL_AUDIT.xlsx")

            try:
                zip_path: Path = asyncio.run(run_gpl_audit_pipeline())
            except SystemExit:
                # main() calls sys.exit(1) on bad/unparseable input instead
                # of raising — catch it here so one bad upload can't kill
                # the whole Django process.
                return Response(
                    {
                        "job_id": job_id,
                        "error": (
                            "Parsing failed — check that the uploaded files "
                            "are valid GPL audit log exports."
                        ),
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
                        f"/api/gpl-audit/download-excel/{job_id}/"
                    ),
                    "download_zip_url": request.build_absolute_uri(
                        f"/api/gpl-audit/download/{job_id}/"
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


class DownloadZipView(APIView):
    """GET /api/gpl-audit/download/<job_id>/ — the full correction-scripts zip."""

    def get(self, request, job_id, *args, **kwargs):
        output_dir = JOBS_ROOT / job_id / "output"
        zip_path = next(output_dir.glob("*.zip"), None) if output_dir.exists() else None
        if not zip_path or not zip_path.exists():
            raise Http404("Zip result not found for this job_id.")
        return FileResponse(open(zip_path, "rb"), as_attachment=True, filename=zip_path.name)


class DownloadExcelView(APIView):
    """GET /api/gpl-audit/download-excel/<job_id>/ — just the .xlsx report."""

    def get(self, request, job_id, *args, **kwargs):
        output_dir = JOBS_ROOT / job_id / "output"
        excel_path = next(output_dir.rglob("*.xlsx"), None) if output_dir.exists() else None
        if not excel_path or not excel_path.exists():
            raise Http404("Excel result not found for this job_id.")
        return FileResponse(open(excel_path, "rb"), as_attachment=True, filename=excel_path.name)
