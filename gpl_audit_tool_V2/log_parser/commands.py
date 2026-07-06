import json
import logging
import re
from pathlib import Path

from .config import COMMANDS_FILE, COMMANDS_CACHE_PATH

log = logging.getLogger(__name__)

_loaded_commands: dict[str, list[str]] | None = None

_SECTION_RE = re.compile(r"^(#{4,})\s*(.+?)\s*(#{4,})\s*$")
_END_RE = re.compile(r"^END\s+(?:OF\s+)?", re.IGNORECASE)
_START_PREFIX_RE = re.compile(r"^Start:\s*", re.IGNORECASE)
_HGETC_RE = re.compile(r"^hgetc\b", re.IGNORECASE)
_CONTROL_RE = re.compile(r"^(lt\s|rbs\s*$|prox|get\s|if\s|fi\s*$|exit\s*$)", re.IGNORECASE)


def _section_marker(line: str):
    m = _SECTION_RE.match(line.strip())
    if not m:
        return None
    inner = m.group(2).strip()
    if _END_RE.match(inner):
        name = _END_RE.sub("", inner).strip()
        return (True, name.upper().replace(" ", "_"))
    name = _START_PREFIX_RE.sub("", inner).strip()
    return (False, name.upper().replace(" ", "_"))


def parse_commands_file(file_path: Path | str) -> dict:
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Commands file not found: {file_path}")

    result: dict[str, list[str]] = {}
    current_section: str | None = None
    current_cmd: str | None = None

    def flush():
        nonlocal current_cmd
        if current_section and current_cmd:
            cmd = current_cmd.strip()
            if cmd:
                result.setdefault(current_section, []).append(cmd)
        current_cmd = None

    try:
        with open(file_path, encoding="utf-8") as fh:
            for raw in fh:
                line = raw.strip()

                if not line:
                    flush()
                    continue

                marker = _section_marker(line)
                if marker:
                    flush()
                    is_end, key = marker
                    current_section = None if is_end else key
                    continue

                if line.startswith("#") or _CONTROL_RE.match(line):
                    flush()
                    continue

                if current_section is None:
                    continue

                if _HGETC_RE.match(line):
                    flush()
                    current_cmd = line
                elif current_cmd is not None:
                    current_cmd += line

        flush()
    except UnicodeDecodeError as e:
        raise ValueError(f"Could not decode commands file (expected UTF-8): {e}") from e

    if not result:
        raise ValueError(f"No commands parsed from: {file_path}")

    log.info("Parsed %d sections from commands file", len(result))
    return result


def load_commands(
    commands_file: Path | str = COMMANDS_FILE,
    cache_file: Path | str = COMMANDS_CACHE_PATH,
) -> dict:
    commands_file = Path(commands_file)
    cache_file = Path(cache_file)

    global _loaded_commands
    if _loaded_commands is not None:
        return _loaded_commands

    if cache_file.exists():
        src_mtime = commands_file.stat().st_mtime if commands_file.exists() else 0
        cache_mtime = cache_file.stat().st_mtime
        if src_mtime > cache_mtime:
            log.info("Commands file is newer than cache — re-parsing.")
        else:
            try:
                with open(cache_file, encoding="utf-8") as fh:
                    data = json.load(fh)
                log.info("Loaded commands from cache: %s", cache_file)
                _loaded_commands = data
                return data
            except (json.JSONDecodeError, OSError) as e:
                log.warning("Cache corrupt or unreadable (%s), re-parsing.", e)

    commands = parse_commands_file(commands_file)

    try:
        with open(cache_file, "w", encoding="utf-8") as fh:
            json.dump(commands, fh, indent=2)
        log.info("Commands cache written to %s", cache_file)
    except OSError as e:
        log.warning("Could not write cache: %s", e)

    _loaded_commands = commands
    return commands

    return commands