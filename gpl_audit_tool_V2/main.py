import asyncio
import logging
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

from .log_parser.corrections import generate_correction_scripts
from .log_parser.audits import (
    lte_cell_data_audit,
    lte_cell_relation_audit,
    lte_enbinfo_audit,
    lte_eutran_freq_audit,
    lte_eutran_freq_relation_audit,
    lte_feature_state_audit,
    lte_gpl_audit,
    lte_summary_audit,
    nr_baseline_audit,
    nr_cell_data_audit,
    nr_feature_state_audit,
    nr_gnbinfo_audit,
    nr_gutran_freq_relation_audit,
)
from .log_parser.output import write_excel
from .log_parser.reader import clear_parse_cache

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger(__name__)


def _site_name_from_files(files: list[Path]) -> str:
    """Extract site/node name from post file names.

    e.g. "KK-NLCTPR12-1_GPL_AUDIT_POST.txt" -> "KK-NLCTPR12-1"
    """
    names: list[str] = []
    for f in files:
        stem = f.stem
        upper = stem.upper()
        cut = len(stem)
        for sfx in ("_GPL_AUDIT_POST", "_GPL_AUDIT_PRE", "_GPL_AUDIT", "_POST", "_PRE"):
            idx = upper.find(sfx)
            if idx != -1:
                cut = idx
                break
        name = stem[:cut] if cut < len(stem) else stem.split("_")[0]
        if name and name not in names:
            names.append(name)
    return "_".join(names) if names else "AUDIT"


def _parameter_status_summary(sections: list[tuple[str, pd.DataFrame, str]]) -> pd.DataFrame:
    """Roll up per-audit parameter counts (total / OK / NOT OK / Missing) for
    the Summary sheet. `sections` is a list of (label, audit_df, status_column).
    """
    rows = []
    for label, df, status_col in sections:
        if df.empty or status_col not in df.columns:
            rows.append({"Audit Section": label, "Total Parameters": 0, "OK": 0, "NOT OK": 0, "Missing": 0})
            continue
        status = df[status_col].astype(str).str.upper()
        rows.append({
            "Audit Section": label,
            "Total Parameters": len(df),
            "OK": int((status == "OK").sum()),
            "NOT OK": int((status == "NOT OK").sum()),
            "Missing": int(status.str.contains("MISS").sum()),
        })
    return pd.DataFrame(rows)


async def main() -> Path:
    from .log_parser.config import (
        get_post_files,
        get_output_file,
        set_output_file,
        set_session_dir,
    )

    clear_parse_cache()

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    post_files = get_post_files()
    site = _site_name_from_files(post_files)

    # session folder: {output_parent}/{site}_GPL_AUDIT_{ts}/
    # Every run gets its own folder — excel + correction scripts all land inside.
    base_dir = get_output_file().parent
    session_dir = base_dir / f"{site}_GPL_AUDIT_{ts}"
    session_dir.mkdir(parents=True, exist_ok=True)

    # Excel lands inside session folder with the standard name
    excel_path = session_dir / f"{site}_GPL_AUDIT_{ts}.xlsx"
    set_output_file(excel_path)
    set_session_dir(session_dir)

    start = datetime.now()
    try:
        (
            lte_summary,
            lte_enbinfo,
            nr_gnbinfo,
            nr_gpl,
            (_, nr_cell_post),
            lte_gpl,
            (_, lte_cell_post),
            lte_feat,
            nr_feat,
            lte_freq,
            lte_freq_rel,
            lte_cell_rel,
            nr_gutran_freq_rel,
        ) = await asyncio.gather(
            lte_summary_audit(),
            lte_enbinfo_audit(),
            nr_gnbinfo_audit(),
            nr_baseline_audit(),
            nr_cell_data_audit(),
            lte_gpl_audit(),
            lte_cell_data_audit(),
            lte_feature_state_audit(),
            nr_feature_state_audit(),
            lte_eutran_freq_audit(),
            lte_eutran_freq_relation_audit(),
            lte_cell_relation_audit(),
            nr_gutran_freq_relation_audit()
        )
    except FileNotFoundError as e:
        log.error("Input file not found: %s", e)
        sys.exit(1)
    except Exception as e:
        log.exception("Unexpected error during parsing: %s", e)
        sys.exit(1)

    summary_counts = _parameter_status_summary(
        [
            ("LTE_GPL_AUDIT", lte_gpl, "Parameter Setting Status"),
            ("NR_GPL_AUDIT", nr_gpl, "status"),
            ("EUTRANFREQRELATION", lte_freq_rel, "Status"),
            ("FEATURESTATE", lte_feat, "Feature setting Status"),
            ("CellRelation", lte_cell_rel, "Status"),
        ]
    )

    write_excel(
        {
            "lte_summary": lte_summary,
            "lte_summary_counts": summary_counts,
            "lte_enbinfo": lte_enbinfo,
            "nr_gnbinfo": nr_gnbinfo,
            "nr_gpl_audit": nr_gpl,
            "cell_post": nr_cell_post,
            "lte_gpl": lte_gpl,
            "LTE_CELL_DATA": lte_cell_post,
            "lte_feature_state": lte_feat,
            "nr_feature_state": nr_feat,
            "lte_eutran_freq": lte_freq,
            "lte_eutran_freq_relation": lte_freq_rel,
            "nr_gutran_freq_relation": nr_gutran_freq_rel,
            "lte_cell_relation": lte_cell_rel,
        }
    )

    zip_path = await generate_correction_scripts(excel_path, session_dir, ts)
    log.info("All output → %s", session_dir)
    log.info("Zip       → %s", zip_path)
    log.info("Done in %s", datetime.now() - start)
    return zip_path


if __name__ == "__main__":
    asyncio.run(main())
