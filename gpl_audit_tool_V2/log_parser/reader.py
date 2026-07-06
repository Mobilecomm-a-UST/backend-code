import asyncio
import logging
import re
from pathlib import Path

import pandas as pd

log = logging.getLogger(__name__)

_PROMPT_RE = re.compile(r"^([A-Z0-9][A-Z0-9-]+)>\s*(.*)$")
# hgetc brackets each output table (and, when it pages results by MO type,
# each page) with a dots-only separator line, e.g. "...." or "..................".
_DOTS_RE = re.compile(r"^\.+$")

# Different sites/operators sometimes type the same hgetc query with or
# without regex anchors (e.g. "hgetc enodebfunction=1 ..." vs
# "hgetc ^enodebfunction=1$ ..."). Match commands ignoring that cosmetic
# difference so real log files aren't silently dropped from a section.
_ANCHOR_TRANS = str.maketrans("", "", "^$")


def _normalize_command(cmd: str) -> str:
    return cmd.translate(_ANCHOR_TRANS)

# Every audit section asks for a different subset of commands out of the same
# handful of physical log files. Parsing is keyed per physical file (not per
# requested command list) so each file is read and scanned exactly once no
# matter how many audit sections need data out of it — concurrent callers
# requesting different command subsets from the same file share one parse.
_file_parse_cache: dict[tuple, "asyncio.Future"] = {}


def clear_parse_cache() -> None:
    """Reset the parse cache. Call at the start of each parser run (the GUI
    can invoke the parser multiple times with different files in one process)."""
    _file_parse_cache.clear()


def _read_lines_sync(file_path: Path) -> list[str]:
    if not file_path.exists():
        raise FileNotFoundError(f"Log file not found: {file_path}")
    with open(file_path, "r", encoding="utf-8") as fh:
        return fh.read().splitlines()


def _build_df(headers_raw: str, rows_raw: list[str]) -> pd.DataFrame:
    if not headers_raw:
        return pd.DataFrame()
    headers = [h.strip() for h in headers_raw.split(";") if h.strip()]
    records = []
    for row in rows_raw:
        values = [v.strip() for v in row.split(";")]
        values = values[: len(headers)] + [""] * max(0, len(headers) - len(values))
        records.append(dict(zip(headers, values)))
    return pd.DataFrame(records)


def _parse_file_sync(file_path: Path, start_header: str) -> dict[str, pd.DataFrame]:
    """Single pass over one log file: every 'NODE_ID> <command>' block found
    becomes one entry, keyed by the literal command text. Runs in a worker
    thread (via asyncio.to_thread) — plain synchronous I/O and string/regex
    work, no per-line coroutine overhead.
    """
    results: dict[str, pd.DataFrame] = {}
    active_cmd: str | None = None
    header_found = False
    header_complete = False
    headers_raw = ""
    rows_raw: list[str] = []
    current_row = ""
    current_node_id = ""
    # hgetc re-prints a fresh "MO;col1;col2..." header line whenever the
    # attribute set changes mid-command — e.g. a combined FDD/TDD cell query
    # pages FDD rows (earfcndl/earfcnul/dlChannelBandwidth/...) separately
    # from TDD rows (earfcn/channelBandwidth/...), each under its own header.
    # Every such page is parsed against its OWN header and collected here;
    # pages are concatenated by column name (not position) at flush time so
    # differing schemas never zip values into the wrong column.
    pages: list[tuple[str, list[str]]] = []

    def _close_page():
        nonlocal headers_raw, rows_raw, current_row
        if current_row:
            rows_raw.append(current_row)
            current_row = ""
        if headers_raw:
            pages.append((headers_raw, rows_raw))
        headers_raw = ""
        rows_raw = []

    def flush():
        nonlocal active_cmd, header_found, header_complete, pages
        if active_cmd:
            _close_page()
            frames = [f for h, r in pages for f in [_build_df(h, r)] if not f.empty]
            df = pd.concat(frames, axis=0, ignore_index=True) if frames else pd.DataFrame()
            if not df.empty and current_node_id:
                df.insert(0, "Node_ID", current_node_id)
            results[active_cmd] = df
        active_cmd = None
        header_found = header_complete = False
        pages = []

    try:
        lines = _read_lines_sync(file_path)
    except UnicodeDecodeError as e:
        raise ValueError(f"Could not decode log file (expected UTF-8): {file_path} — {e}") from e

    for line in lines:
        m = _PROMPT_RE.match(line)
        if m:
            flush()
            current_node_id = m.group(1)
            cmd_text = m.group(2).strip()
            active_cmd = cmd_text or None
            continue

        if active_cmd is None or not line.strip():
            continue

        if _DOTS_RE.match(line.strip()):
            continue

        if not header_found:
            if line.startswith(start_header):
                header_found = True
                headers_raw = line
            continue

        first_field = line.split(";")[0].strip()
        is_new_record = "=" in first_field

        # hgetc pages large result sets by MO type, reprinting a
        # "MO;col1;col2..." header line before each page — sometimes with the
        # SAME columns (just a page break), sometimes with a DIFFERENT column
        # set (e.g. FDD vs TDD cells). Close out the page seen so far and
        # start a new one parsed against this fresh header line.
        if header_complete and not is_new_record and line.startswith(start_header):
            _close_page()
            headers_raw = line
            header_complete = False
            continue

        if not header_complete:
            if not is_new_record:
                headers_raw += line
                continue
            header_complete = True

        if is_new_record:
            if current_row:
                rows_raw.append(current_row)
            current_row = line
        else:
            current_row += line

    flush()
    return results


def _get_file_future(file_path: Path | str, start_header: str) -> "asyncio.Future":
    key = (str(Path(file_path)), start_header)
    future = _file_parse_cache.get(key)
    if future is None:
        future = asyncio.ensure_future(asyncio.to_thread(_parse_file_sync, Path(file_path), start_header))
        _file_parse_cache[key] = future
    return future


async def parse_all_commands_multi(
    commands: list[str],
    file_paths: list[Path | str],
    start_header: str = "MO",
) -> dict[str, pd.DataFrame]:
    """Return {command: DataFrame} for the requested commands, concatenated
    across all file_paths on axis=0.

    Each physical file is parsed once in total (for every command it
    contains) and cached — multiple audit sections requesting different
    command subsets from the same files share that single parse instead of
    each re-reading and re-scanning the files from disk.
    """
    if not file_paths:
        raise ValueError("file_paths list is empty")
    if not commands:
        raise ValueError("commands list is empty")

    per_file_results = await asyncio.gather(
        *[_get_file_future(fp, start_header) for fp in file_paths]
    )

    merged: dict[str, pd.DataFrame] = {}
    total = len(commands)
    wanted = {_normalize_command(c) for c in commands}
    for fp, file_results in zip(file_paths, per_file_results):
        matched = 0
        # iterate in file-scan order (dict insertion order), not requested-list
        # order, so row order matches a section-scoped scan of the same file.
        for cmd, df in file_results.items():
            if _normalize_command(cmd) not in wanted:
                continue
            matched += 1
            if df.empty:
                continue
            if cmd not in merged:
                merged[cmd] = df
            else:
                merged[cmd] = pd.concat([merged[cmd], df], axis=0, ignore_index=True)

        if matched == 0:
            log.warning("No commands matched in: %s", fp)
        elif matched < total:
            log.warning("%d/%d commands not found in: %s", total - matched, total, fp)
        else:
            log.info("All %d commands matched in: %s", total, fp)

    return merged