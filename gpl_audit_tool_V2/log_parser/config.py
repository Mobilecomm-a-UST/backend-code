import contextvars
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

PRE_DIR = BASE_DIR / "input" / "pre"
POST_DIR = BASE_DIR / "input" / "post"
COMMANDS_FILE = BASE_DIR / "commands" / "GPL_Audit_command_NR_Updated.txt"
COMMANDS_CACHE_PATH = BASE_DIR / "commands" / "commands_cache.json"

OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "GPL_AUDIT.xlsx"

SHEETS: list[tuple[str, str]] = [
    ("Summary", "lte_summary"),
    ("eNBInfo", "lte_enbinfo"),
    ("gNBInfo", "nr_gnbinfo"),
    ("LTE_CELL_DATA", "LTE_CELL_DATA"),
    ("NR_CELL_DATA", "cell_post"),
    ("LTE_GPL_AUDIT", "lte_gpl"),
    ("NR_GPL_AUDIT", "nr_gpl_audit"),
    ("FEATURESTATE", "lte_feature_state"),
    ("FREQ_AUDIT", "lte_eutran_freq"),
    ("LTE_EutranfreqRelation", "lte_eutran_freq_relation"),
    ("NR_GutranfreqRelation", "nr_gutran_freq_relation"),
    ("CellRelation", "lte_cell_relation"),
]

# Runtime overrides — set by the GUI (or main()) before running.
#
# These used to be plain module-level globals, which are shared process-wide
# across threads AND across concurrent asyncio tasks. If two runs ever
# overlap in the same process (e.g. the GUI's background thread starts a new
# run, or two runs are launched close together), the second run's file
# selection / output path would silently clobber the first run's globals
# mid-flight — one run would then mix its own data with the other run's file
# list. ContextVar gives each asyncio Task (and each thread, which starts
# with its own top-level context) an isolated copy, so overlapping runs can
# never see each other's settings.
_pre_files_var: "contextvars.ContextVar[list[Path] | None]" = contextvars.ContextVar("pre_files", default=None)
_post_files_var: "contextvars.ContextVar[list[Path] | None]" = contextvars.ContextVar("post_files", default=None)
_output_file_var: "contextvars.ContextVar[Path | None]" = contextvars.ContextVar("output_file", default=None)
_session_dir_var: "contextvars.ContextVar[Path | None]" = contextvars.ContextVar("session_dir", default=None)


def set_pre_files(files: list[Path]) -> None:
    _pre_files_var.set(files)


def set_post_files(files: list[Path]) -> None:
    _post_files_var.set(files)


def set_output_file(path: Path) -> None:
    _output_file_var.set(path)


def set_session_dir(path: Path) -> None:
    _session_dir_var.set(path)


def get_session_dir() -> Path | None:
    return _session_dir_var.get()


def get_pre_files() -> list[Path]:
    files = _pre_files_var.get()
    if files is not None:
        return files
    files = sorted(PRE_DIR.glob("*.txt"))
    if not files:
        raise FileNotFoundError(f"No .txt files found in PRE directory: {PRE_DIR}")
    return files


def get_post_files() -> list[Path]:
    files = _post_files_var.get()
    if files is not None:
        return files
    files = sorted(POST_DIR.glob("*.txt"))
    if not files:
        raise FileNotFoundError(f"No .txt files found in POST directory: {POST_DIR}")
    return files


def get_output_file() -> Path:
    return _output_file_var.get() or OUTPUT_FILE
