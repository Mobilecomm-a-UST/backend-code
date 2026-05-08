import os
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from django.conf import settings
from django.http import FileResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from mcom_website.settings import MEDIA_ROOT, MEDIA_URL
from django.shortcuts import render

# ─────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────

main_folder = os.path.join(settings.MEDIA_ROOT, "performance_idploy")
input_path  = os.path.join(main_folder, "input")
output_path = os.path.join(main_folder, "output")

os.makedirs(input_path, exist_ok=True)
os.makedirs(output_path, exist_ok=True)

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────

OUTPUT_FILENAME     = "output_Offered Vs OA TAT.xlsx"
CATEGORIES          = ['<=12days', '13-21days', '22-30days', '>30days']
HEADER_BG           = '4472C4'
HEADER_FG           = 'FFFFFF'
TOTAL_BG            = 'D9E1F2'
ALT_ROW_BG          = 'F2F2F2'
BORDER_CLR          = '000000'

LAYERS_4G_EXCLUDE   = {"3500", "L3500", "N3500", "N2600"}
LAYERS_5G_INCLUDE   = {"3500", "L3500", "N3500"}
LAYERS_4G5G_EXCLUDE = {"N2600"}


# ─────────────────────────────────────────────
# API 1 — UPLOAD
# ─────────────────────────────────────────────

def _clear_old_files():
    """
    Delete all existing files in input and output folders.
    Guarantees both folders exist after clearing.
    """
    for folder in [input_path, output_path]:
        if os.path.exists(folder):
            for f in os.listdir(folder):
                os.remove(os.path.join(folder, f))
        os.makedirs(folder, exist_ok=True)


def _save_uploaded_file(uploaded):
    """Save uploaded file to input folder with its original name."""
    save_path = os.path.join(input_path, uploaded.name)
    with open(save_path, 'wb+') as destination:
        for chunk in uploaded.chunks():
            destination.write(chunk)
    return save_path


def _validate_file(filepath):
    """
    Read file and check all required columns exist.
    Required: Circle, On Air Date, Performance AT Offered Date, Offered Layer
    Called only once at upload time.
    Returns (df, error_message). If valid, error_message is None.
    """
    ext = os.path.splitext(filepath)[1].lower()
    if ext in ('.xlsx', '.xls'):
        df = pd.read_excel(filepath)
    elif ext == '.csv':
        df = pd.read_csv(filepath)
    else:
        return None, f"Unsupported file type: {ext}"

    # strip whitespace from all column names
    df.rename(columns={c: c.strip() for c in df.columns}, inplace=True)

    lower_map = {c.lower(): c for c in df.columns}

    required = {
        'on air date':                 'On Air Date',
        'performance at offered date': 'Performance AT Offered Date',
        'performance at status date':  'Performance AT Status Date',
        'circle':                      'Circle',
        'offered layer':               'Offered Layer',
    }

    rename = {}
    for key, canonical in required.items():
        if canonical in df.columns:
            rename[canonical] = canonical
        elif key in lower_map:
            rename[lower_map[key]] = canonical
        else:
            match = next((c for c in df.columns if key in c.lower()), None)
            if match:
                rename[match] = canonical
            else:
                return None, (
                    f"Column '{canonical}' not found. "
                    f"Available columns: {list(df.columns)}"
                )

    df.rename(columns=rename, inplace=True)

    # parse date columns — only On Air Date is mandatory
    df['On Air Date'] = pd.to_datetime(df['On Air Date'], errors='coerce').dt.date
    df['Performance AT Offered Date'] = pd.to_datetime(
        df['Performance AT Offered Date'], errors='coerce'
    ).dt.date
    for col in ('On Air Date', 'Performance AT Offered Date', 'Performance AT Status Date'):
        df[col] = pd.to_datetime(df[col], errors='coerce').dt.date

    # drop rows where On Air Date is missing — cannot process without it
    df.dropna(subset=['On Air Date'], inplace=True)

    return df, None


@api_view(['POST', 'GET', 'DELETE'])
def upload_file(request):
    try:
        os.makedirs(input_path, exist_ok=True)
        os.makedirs(output_path, exist_ok=True)

        if request.method == 'POST':
            files = request.FILES.getlist('file')
            if not files:
                return Response(
                    {'error': 'No files uploaded'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            uploaded = files[0]
            ext      = os.path.splitext(uploaded.name)[1].lower()
            if ext not in ('.xlsx', '.xls', '.csv'):
                return Response(
                    {'error': f"Unsupported type '{ext}'. Use .xlsx, .xls, or .csv."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            _clear_old_files()

            save_path = _save_uploaded_file(uploaded)
            df, error = _validate_file(save_path)

            if error:
                os.remove(save_path)
                return Response({'error': error}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            return Response({
                'status':    True,
                'message':   'File saved successfully',
                'filename':  uploaded.name,
                'rows_read': len(df),
            }, status=status.HTTP_200_OK)


        elif request.method == 'GET':
            # check input file
            input_file_info = None
            if os.path.exists(input_path):
                input_files = os.listdir(input_path)
                if input_files:
                    input_file_info = {
                        'filename': input_files[0],
                        'status':   'ready',
                    }

            # check output files
            output_files = []

            offered_file = os.path.join(output_path, "output_Offered Vs OA TAT.xlsx")
            status_file  = os.path.join(output_path, "output_Performance vs OA TAT.xlsx")

            if os.path.exists(offered_file):
                output_files.append({
                    'report_type':  'offered',
                    'filename':     'output_Offered Vs OA TAT.xlsx',
                    'download_url': request.build_absolute_uri(
                        f"{settings.MEDIA_URL.rstrip('/')}/performance_idploy/output/output_Offered Vs OA TAT.xlsx"
                    ),
                })

            if os.path.exists(status_file):
                output_files.append({
                    'report_type':  'status',
                    'filename':     'output_Performance vs OA TAT.xlsx',
                    'download_url': request.build_absolute_uri(
                        f"{settings.MEDIA_URL.rstrip('/')}/performance_idploy/output/output_Performance vs OA TAT.xlsx"
                    ),
                })

            return Response({
                'status':       True,
                'message':      'Files found' if input_file_info else 'No files found',
                'input_file':   input_file_info,
                'output_files': output_files,
            }, status=status.HTTP_200_OK)


        elif request.method == 'DELETE':
            if not os.path.exists(input_path) and not os.path.exists(output_path):
                return Response(
                    {'error': 'Folder does not exist'},
                    status=status.HTTP_404_NOT_FOUND,
                )

            deleted_files = _delete_all_files()

            return Response({
                'status':        True,
                'message':       'Files deleted successfully',
                'deleted_files': deleted_files,
            }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





# ─────────────────────────────────────────────
# API 2 — GET MONTHS
# ─────────────────────────────────────────────

def _get_input_df():
    """
    Read the already-validated file from input folder.
    Parse date columns back to date objects after reading.
    Returns (df, error_message).
    """
    if not os.path.exists(input_path):
        return None, "No input file found. Upload first via POST /idploy/upload/"

    for f in os.listdir(input_path):
        filepath = os.path.join(input_path, f)
        ext      = os.path.splitext(filepath)[1].lower()

        if ext in ('.xlsx', '.xls'):
            df = pd.read_excel(filepath)
        elif ext == '.csv':
            df = pd.read_csv(filepath)
        else:
            continue

        # parse date columns back to date objects
        df['On Air Date'] = pd.to_datetime(
            df['On Air Date'], errors='coerce'
        ).dt.date
        df['Performance AT Offered Date'] = pd.to_datetime(
            df['Performance AT Offered Date'], errors='coerce'
        ).dt.date

        for col in ('On Air Date', 'Performance AT Offered Date', 'Performance AT Status Date'):
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.date

        return df, None

    return None, "No input file found. Upload first via POST /idploy/upload/"


def _bucket_start(month_label):
    """'Dec 2025' -> date(2025, 11, 26) — 26th of previous month."""
    dt   = pd.to_datetime(month_label, format='%b %Y')
    prev = dt - relativedelta(months=1)
    return date(prev.year, prev.month, 26)


def _bucket_end(month_label):
    """'Dec 2025' -> date(2025, 12, 25) — 25th of current month."""
    dt = pd.to_datetime(month_label, format='%b %Y')
    return date(dt.year, dt.month, 25)


def _get_available_months(df):
    """
    Derive month bucket labels from On Air Date column.
    26th rollover rule:
      day >= 26 -> current month label
      day <  26 -> previous month label
    Returns sorted list e.g. ['Nov 2025', 'Dec 2025', 'Jan 2026']
    """
    def _to_label(d):
        if d.day >= 26:
            return d.strftime('%b %Y')
        prior = date(d.year, d.month, 1) - relativedelta(months=1)
        return prior.strftime('%b %Y')

    labels = df['On Air Date'].dropna().apply(_to_label)
    return sorted(set(labels), key=lambda x: pd.to_datetime(x, format='%b %Y'))


@api_view(['GET'])
def get_months(request):
    """
    GET /idploy/months/
    Returns available month bucket labels from the uploaded file.
    User picks one label and passes it to POST /idploy/generate-offered/
    """
    df, error = _get_input_df()
    if error:
        return Response({'error': error}, status=status.HTTP_404_NOT_FOUND)

    try:
        months = _get_available_months(df)
    except Exception as exc:
        return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    result = [{
        'label': m,
        'start': _bucket_start(m).strftime('%d-%b-%Y'),
        'end':   _bucket_end(m).strftime('%d-%b-%Y'),
    } for m in months]

    return Response({
        'months':    result,
        'next_step': 'POST /idploy/generate-offered/ with body {"month": "<label>"}',
    }, status=status.HTTP_200_OK)


# ─────────────────────────────────────────────
# API 3 — GENERATE + DOWNLOAD
# ─────────────────────────────────────────────

def _apply_layer_filter(df, case):
    """
    Filter DataFrame rows based on Offered Layer column.
    case '4G'    — exclude rows where Offered Layer is in LAYERS_4G_EXCLUDE
    case '5G'    — include only rows where Offered Layer is in LAYERS_5G_INCLUDE
    case '4G+5G' — exclude rows where Offered Layer is in LAYERS_4G5G_EXCLUDE
    """
    df      = df.copy()
    col     = 'Offered Layer'
    df[col] = df[col].astype(str).str.strip()

    if case == '4G':
        return df[~df[col].isin(LAYERS_4G_EXCLUDE)].copy()
    elif case == '5G':
        return df[df[col].isin(LAYERS_5G_INCLUDE)].copy()
    elif case == '4G+5G':
        return df[~df[col].isin(LAYERS_4G5G_EXCLUDE)].copy()
    else:
        raise ValueError(f"Unknown layer case: {case}")


def _classify(days):
    """
    Classify day difference into one of the 4 categories.
    0 and negatives also fall into <=12days.
    """
    if days <= 12:
        return '<=12days'
    elif days <= 21:
        return '13-21days'
    elif days <= 30:
        return '22-30days'
    else:
        return '>30days'


def _process_data(df, month_label, layer_case, date_col='Performance AT Offered Date'):
    """
    Step 1: Apply Offered Layer filter first.
    Step 2: Filter On Air Date within bucket (26th prev -> 25th current).
    Step 3: Split into pending (blank date_col) and filled.
    Step 4: Compute diff = date_col - On Air Date (days).
            Keep 0 and negatives — counted in <=12days.
            Only drop rows where diff could not be computed at all.
    Step 5: Classify diff into category.
    Step 6: Count per circle alphabetically + Grand Total.

    date_col: column to use for diff calculation.
              'Performance AT Offered Date' or 'Performance AT Status Date'
    """
    start = _bucket_start(month_label)
    end   = _bucket_end(month_label)

    # Step 1 — layer filter first
    df_layer = _apply_layer_filter(df, layer_case)

    # Step 2 — filter On Air Date within bucket
    mask_oa = (df_layer['On Air Date'] >= start) & (df_layer['On Air Date'] <= end)
    df_oa   = df_layer[mask_oa].copy()

    if df_oa.empty:
        available = _get_available_months(df)
        raise ValueError(
            f"No data found for '{month_label}' with layer '{layer_case}'. "
            f"Available months: {available}"
        )

    # Step 3 — split into pending and filled using date_col ← FIXED
    mask_blank = df_oa[date_col].isna()
    df_pending = df_oa[mask_blank].copy()
    df_filled  = df_oa[~mask_blank].copy()

    # Step 4 — compute diff using date_col ← FIXED
    df_filled['_diff'] = (
        df_filled[date_col] - df_filled['On Air Date']
    ).apply(lambda x: x.days if hasattr(x, 'days') else None)

    df_filled = df_filled[df_filled['_diff'].notna()]

    # Step 5 — classify
    df_filled['_category'] = df_filled['_diff'].apply(_classify)

    # Step 6 — count per circle alphabetically
    all_circles = sorted(df_oa['Circle'].dropna().unique())

    result_circles = {}
    grand          = {c: 0 for c in CATEGORIES}
    grand_pending  = 0
    grand_total    = 0

    for circle in all_circles:
        df_c    = df_filled[df_filled['Circle'] == circle]
        counts  = df_c['_category'].value_counts()
        row     = {cat: int(counts.get(cat, 0)) for cat in CATEGORIES}

        pending = int((df_pending['Circle'] == circle).sum())
        total   = sum(row.values()) + pending

        pct_lt12  = round(
            row['<=12days'] / total * 100, 1
        ) if total > 0 else 0.0

        pct_lt21  = round(
            (row['<=12days'] + row['13-21days']) / total * 100, 1
        ) if total > 0 else 0.0

        pct_22_30 = round(
            row['22-30days'] / total * 100, 1
        ) if total > 0 else 0.0

        result_circles[circle] = {
            **row,
            'Pending':  pending,
            'Total':    total,
            '%<12':     pct_lt12,
            '%<21':     pct_lt21,
            '%<22-30':  pct_22_30,
        }

        for cat in CATEGORIES:
            grand[cat] += row[cat]
        grand_pending += pending
        grand_total   += total

    grand_pct_lt12  = round(
        grand['<=12days'] / grand_total * 100, 1
    ) if grand_total > 0 else 0.0

    grand_pct_lt21  = round(
        (grand['<=12days'] + grand['13-21days']) / grand_total * 100, 1
    ) if grand_total > 0 else 0.0

    grand_pct_22_30 = round(
        grand['22-30days'] / grand_total * 100, 1
    ) if grand_total > 0 else 0.0

    return {
        'month':       month_label,
        'start':       start.strftime('%d-%b-%Y'),
        'end':         end.strftime('%d-%b-%Y'),
        'circles':     result_circles,
        'grand_total': {
            **grand,
            'Pending':  grand_pending,
            'Total':    grand_total,
            '%<12':     grand_pct_lt12,
            '%<21':     grand_pct_lt21,
            '%<22-30':  grand_pct_22_30,
        },
    }


def _write_sheet(ws, result, thin):
    """
    Write data into a single worksheet.
    Called once per layer case — 4G, 5G, 4G+5G.
    """
    ALL_COLS = CATEGORIES + ['Pending', 'Total','%<12', '%<21', '%<22-30']

    def _hdr_cell(cell, value, bg=HEADER_BG, fg=HEADER_FG):
        cell.value     = value
        cell.font      = Font(name='Arial', bold=True, color=fg, size=10)
        cell.fill      = PatternFill('solid', start_color=bg)
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        cell.border    = thin

    def _data_cell(cell, value, bold=False, bg=None):
        cell.value     = value
        cell.font      = Font(name='Arial', bold=bold, size=10)
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.border    = thin
        if bg:
            cell.fill = PatternFill('solid', start_color=bg)

    # Row 1 — month label spanning all columns A to I
    ws.merge_cells('A1:J1')
    _hdr_cell(ws['A1'], result['month'])

    # Row 2 — column headers
    _hdr_cell(ws['A2'], 'Circle')
    for col_idx, col_name in enumerate(ALL_COLS, start=2):
        _hdr_cell(ws.cell(row=2, column=col_idx), col_name)

    

    # Data rows
    row = 3
    for i, (circle, counts) in enumerate(result['circles'].items()):
        
        _data_cell(ws.cell(row=row, column=1), circle, bg='FFFFFF')
        for col_idx, col_name in enumerate(ALL_COLS, start=2):
            val = counts.get(col_name)
            # show blank instead of 0 for category counts and pending
            if col_name not in ('%<21', '%<22-30', 'Total') and val == 0:
                val = None
            _data_cell(ws.cell(row=row, column=col_idx), val, bg='FFFFFF')
        row += 1

    # Grand Total row
    grand = result['grand_total']
    _data_cell(ws.cell(row=row, column=1), 'Grand Total', bold=True, bg=TOTAL_BG)
    for col_idx, col_name in enumerate(ALL_COLS, start=2):
        val = grand.get(col_name)
        if col_name not in ('%<12','%<21', '%<22-30', 'Total') and val == 0:
            val = None
        _data_cell(ws.cell(row=row, column=col_idx), val, bold=True, bg=TOTAL_BG)

    # Column widths
    col_widths = {
        'A': 10,   # Circle
        'B': 10,   # <=12days
        'C': 11,   # 13-21days
        'D': 11,   # 22-30days
        'E': 10,   # >30days
        'F': 10,   # Pending
        'G': 8,    # Total
        'H': 8,    # %<12 
        'I': 8,    # %<21
        'J': 10,   # %<22-30
    }
    for col_letter, width in col_widths.items():
        ws.column_dimensions[col_letter].width = width

    ws.row_dimensions[1].height = 20
    ws.row_dimensions[2].height = 30


def _write_output_excel(results, out_filepath):
    """
    Write one Excel file with 3 sheets — 4G, 5G, 4G+5G.
    results is a dict: {'4G': result_dict, '5G': result_dict, '4G+5G': result_dict}
    """
    wb = Workbook()

    # remove default empty sheet
    wb.remove(wb.active)

    side = Side(style='thin', color=BORDER_CLR)
    thin = Border(left=side, right=side, top=side, bottom=side)

    for sheet_name in ['4G', '5G', '4G+5G']:
        ws = wb.create_sheet(title=sheet_name)
        _write_sheet(ws, results[sheet_name], thin)

    wb.save(out_filepath)


def _delete_all_files():
    """Delete all input and output files."""
    deleted = []
    for folder in [input_path, output_path]:
        if os.path.exists(folder):
            for f in os.listdir(folder):
                os.remove(os.path.join(folder, f))
                deleted.append(f)
    return deleted


@api_view(['POST'])
def generate_offered(request):
    """
    POST /idploy/generate-offered/
    Body (JSON): { "month": "Dec 2025" }
    Processes data for all 3 layer cases (4G, 5G, 4G+5G),
    writes one Excel with 3 sheets, returns JSON + download URL.
    """
    month_label = request.data.get('month', '').strip()
    if not month_label:
        return Response(
            {'error': 'Provide month in body. Example: {"month": "Dec 2025"}'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    df, error = _get_input_df()
    if error:
        return Response({'error': error}, status=status.HTTP_404_NOT_FOUND)

    out_file = os.path.join(output_path, OUTPUT_FILENAME)

    try:
        results = {
            '4G':    _process_data(df, month_label, '4G'),
            '5G':    _process_data(df, month_label, '5G'),
            '4G+5G': _process_data(df, month_label, '4G+5G'),
        }
        _write_output_excel(results, out_file)

    except ValueError as ve:
        return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as exc:
        return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    file_relative_path = f"performance_idploy/output/{OUTPUT_FILENAME}"
    download_url = request.build_absolute_uri(
        f"{settings.MEDIA_URL.rstrip('/')}/{file_relative_path}"
    )

    return Response({
        'status':     True,
        'message':    'Report generated successfully.',
        'month':      month_label,
        'date_range': f"{results['4G']['start']} to {results['4G']['end']}",
        'data': {
            '4G': {
                'circles':     results['4G']['circles'],
                'grand_total': results['4G']['grand_total'],
            },
            '5G': {
                'circles':     results['5G']['circles'],
                'grand_total': results['5G']['grand_total'],
            },
            '4G+5G': {
                'circles':     results['4G+5G']['circles'],
                'grand_total': results['4G+5G']['grand_total'],
            },
        },
        'download_url': download_url,
    }, status=status.HTTP_200_OK)


# ─────────────────────────────────────────────
# API 5 — GENERATE STATUS DATE REPORT
# ─────────────────────────────────────────────

@api_view(['POST'])
def generate_performance(request):
    """
    POST /idploy/generate-performance/
    Body (JSON): { "month": "Dec 2025" }

    Same logic as generate_offered but uses
    'Performance AT Status Date' column instead of
    'Performance AT Offered Date' for diff calculation.

    Reuses all existing helpers — _get_input_df, _apply_layer_filter,
    _process_data, _write_output_excel — no duplication.
    """
    month_label = request.data.get('month', '').strip()
    if not month_label:
        return Response(
            {'error': 'Provide month in body. Example: {"month": "Dec 2025"}'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    df, error = _get_input_df()
    if error:
        return Response({'error': error}, status=status.HTTP_404_NOT_FOUND)

    out_file = os.path.join(output_path, "output_Performance vs OA TAT.xlsx")

    try:
        # same _process_data — just passing different date_col
        results = {
            '4G':    _process_data(df, month_label, '4G',    'Performance AT Status Date'),
            '5G':    _process_data(df, month_label, '5G',    'Performance AT Status Date'),
            '4G+5G': _process_data(df, month_label, '4G+5G', 'Performance AT Status Date'),
        }
        _write_output_excel(results, out_file)

    except ValueError as ve:
        return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as exc:
        return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    file_relative_path = "performance_idploy/output/output_Performance vs OA TAT.xlsx"
    download_url = request.build_absolute_uri(
        f"{settings.MEDIA_URL.rstrip('/')}/{file_relative_path}"
    )

    return Response({
        'status':     True,
        'message':    'Status date report generated successfully.',
        'month':      month_label,
        'date_range': f"{results['4G']['start']} to {results['4G']['end']}",
        'data': {
            '4G': {
                'circles':     results['4G']['circles'],
                'grand_total': results['4G']['grand_total'],
            },
            '5G': {
                'circles':     results['5G']['circles'],
                'grand_total': results['5G']['grand_total'],
            },
            '4G+5G': {
                'circles':     results['4G+5G']['circles'],
                'grand_total': results['4G+5G']['grand_total'],
            },
        },
        'download_url': download_url,
    }, status=status.HTTP_200_OK)

# ─────────────────────────────────────────────
# API 4 — CLEANUP
# ─────────────────────────────────────────────

@api_view(['DELETE'])
def cleanup(request):
    """
    DELETE /idploy/cleanup/
    Manually delete all input and output files without downloading.
    Use this to reset at any point in the flow.
    """
    deleted = _delete_all_files()
    return Response({
        'message':       'Cleanup complete.',
        'deleted_files': deleted,
    }, status=status.HTTP_200_OK)





