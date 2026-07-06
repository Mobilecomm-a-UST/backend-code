"""
Generate AMOS correction scripts from the GPL_AUDIT.xlsx and zip them,
with a separate sub-folder per node.
"""
import asyncio
import logging
import os
import zipfile
from datetime import datetime
from pathlib import Path

import pandas as pd

log = logging.getLogger(__name__)

# ── AMOS command templates ─────────────────────────────────────────────────────

_GERAN_FREQ_TEMPLATE = """\
crn GeraNetwork=1,GeranFrequency={arfcnValueGeranDl}
arfcnValueGeranDl {arfcnValueGeranDl}
end"""

_EUTRAN_FREQ_TEMPLATE = """\
crn ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency={arfcnValueEUtranDl}
arfcnValueEUtranDl {arfcnValueEUtranDl}
end"""

_CELL_RELATION_TEMPLATE = """\
crn {EUtranCellName},EUtranCellRelation
neighborCellRef {neighborCellRef}
end"""


# ── helpers ───────────────────────────────────────────────────────────────────

def _write_script(lines: list[str], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(str(ln) for ln in lines))
    log.info("Written: %s", path)


def _melt_notok(df: pd.DataFrame, drop_cols: set) -> pd.DataFrame:
    """Melt to per-parameter rows, keeping only rows that have a pre|post diff (contain '|')."""
    if df.empty:
        return pd.DataFrame(columns=["MO", "Relation Parameter", "Value"])
    keep = [c for c in df.columns if c not in drop_cols or c == "MO"]
    d = df[keep].copy()
    melted = d.melt(id_vars=["MO"], var_name="Relation Parameter", value_name="Value")
    melted = melted[melted["Value"].astype(str).str.contains(r"\|", regex=True, na=False)]
    melted["Value"] = melted["Value"].apply(lambda x: str(x).split("|")[0])
    return melted.reset_index(drop=True)


def _melt_all(df: pd.DataFrame, drop_cols: set) -> pd.DataFrame:
    """Melt all value columns, excluding drop_cols."""
    if df.empty:
        return pd.DataFrame(columns=["MO", "Relation Parameter", "Value"])
    keep = [c for c in df.columns if c not in drop_cols or c == "MO"]
    d = df[keep].copy()
    melted = d.melt(id_vars=["MO"], var_name="Relation Parameter", value_name="Value")
    melted = melted[melted["MO"].notna()].drop_duplicates(subset=["MO", "Relation Parameter"])
    return melted.reset_index(drop=True)


def _to_int(val):
    try:
        return int(str(val).split("|")[0])
    except (ValueError, TypeError):
        return val


def _zip_output(output_dir: Path, zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _dirs, files in os.walk(output_dir):
            for file in files:
                abs_path = Path(root) / file
                if abs_path == zip_path:
                    continue
                zf.write(abs_path, abs_path.relative_to(output_dir))
    log.info("Zipped → %s", zip_path)


# ── per-node script writer (runs in thread pool) ───────────────────────────────

def _write_node_scripts(
    node: str,
    node_dir: Path,
    ts: str,
    gpl_df: pd.DataFrame,
    feat_df: pd.DataFrame,
    eutran_freq_df: pd.DataFrame,
    freq_rel_notok: pd.DataFrame,
    freq_rel_missing: pd.DataFrame,
    cell_rel_notok: pd.DataFrame,
    cell_rel_missing: pd.DataFrame,
    valid_frequencies: list,
) -> None:

    # ── GPL Parameter Correction ──────────────────────────────────────────────
    gpl_lines = [
        f"##################### GPL Parameter Correction Commands {node} ####################",
    ]
    for _, row in gpl_df.iterrows():
        if pd.notna(row.get("Pre-existing Value")) and pd.notna(row.get("MO")):
            value = str(row["Pre-existing Value"]).split()[0]
            gpl_lines.append(f"set {row['MO']}$ {row['Parameter']} {value}")

    gpl_lines.append(
        f"\n##################### LTE Feature Correction Commands {node} ####################"
    )
    for _, row in feat_df.iterrows():
        if pd.notna(row.get("Pre Existing FeatureState")) and pd.notna(row.get("CXC ID")):
            gpl_lines.append(f"set {row['CXC ID']}$ featureState {_to_int(row['Pre Existing FeatureState'])}")

    _write_script(gpl_lines, node_dir / f"{node}_GPL_Correction_Script_{ts}.txt")
    # ── Relation Correction ───────────────────────────────────────────────────
    rel_lines: list[str] = []

    # EutranFrequency missing (crn create commands)
    for _, row in eutran_freq_df.iterrows():
        mo = str(row.get("MO", ""))
        if mo.startswith("GeraNetwork=1,GeranFrequency="):
            try:
                rel_lines.append(_GERAN_FREQ_TEMPLATE.format(arfcnValueGeranDl=int(row.get("arfcnValueGeranDl", 0))))
            except (ValueError, TypeError):
                pass
        elif mo.startswith("ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency="):
            try:
                rel_lines.append(_EUTRAN_FREQ_TEMPLATE.format(arfcnValueEUtranDl=int(row.get("arfcnValueEUtranDl", 0))))
            except (ValueError, TypeError):
                pass

    # EutranFreqRelation NOT OK (set commands)
    rel_lines.append(
        f"\n\n##################### Eutran Frequency Relation Correction Commands {node} ####################\n"
    )
    _FR_DROP = {"cellId", "Status", "Node_ID", "duplicates_mask"}
    for _, row in _melt_notok(freq_rel_notok, _FR_DROP).iterrows():
        if pd.notna(row.get("MO")):
            rel_lines.append(f"set {row['MO']}$ {row['Relation Parameter']} {row['Value']}")

    # EutranFreqRelation Missing (crn create commands)
    rel_lines.append(
        f"\n\n##################### Creating Eutran Frequency Relation Missing Commands {node} ####################\n"
    )
    _FR_MISS_DROP = {"cellId", "Status", "Node_ID", "duplicates_mask", "eutranFrequencyRef"}
    fr_miss_melt = _melt_all(freq_rel_missing, _FR_MISS_DROP)
    valid_freq_str = [str(f) for f in valid_frequencies]
    for mo, group in fr_miss_melt.groupby("MO"):
        parts = str(mo).split(",")
        freq_val = parts[1].split("=")[1] if len(parts) > 1 and "=" in parts[1] else ""
        if freq_val in valid_freq_str:
            rel_lines.append(f"\ncrn {mo}")
            for _, r in group.iterrows():
                rel_lines.append(f"{r['Relation Parameter']} {r['Value']}")
            rel_lines.append("end")

    # CellRelation NOT OK (set commands)
    rel_lines.append(
        f"\n\n######################################################## Cell Relation {node} ####################################################\n"
    )
    _CR_PARAM_COLS = [
        "cellIndividualOffsetEUtran", "coverageIndicator", "loadBalancing",
        "qOffsetCellEUtran", "reportDlActivity", "sCellCandidate",
        "sCellPriority", "sleepModeCovCellCandidate",
    ]
    if not cell_rel_notok.empty:
        cols = ["MO"] + [c for c in _CR_PARAM_COLS if c in cell_rel_notok.columns]
        cr_melt = cell_rel_notok[cols].melt(id_vars=["MO"], var_name="Relation Parameter", value_name="Value")
        cr_melt["Value"] = cr_melt["Value"].apply(lambda x: str(x).split("|")[0] if "|" in str(x) else x)
        cr_melt.drop_duplicates(subset=["MO", "Relation Parameter"], inplace=True)
        for _, row in cr_melt.iterrows():
            rel_lines.append(f"set {row['MO']}$ {row['Relation Parameter']} {_to_int(row['Value'])}")

    # CellRelation Missing (crn create commands)
    rel_lines.append(
        f"\n\n###############################################CELL RELATION MISSING {node} #########################################################\n"
    )
    for _, row in cell_rel_missing.iterrows():
        mo_cell = str(row.get("MO", ""))
        nbr = str(row.get("neighborCellRef", ""))
        if mo_cell and nbr:
            rel_lines.append(_CELL_RELATION_TEMPLATE.format(EUtranCellName=mo_cell, neighborCellRef=nbr))

    _write_script(rel_lines, node_dir / f"{node}_Relation_Correction_Script_{ts}.txt")


# ── public entry point ─────────────────────────────────────────────────────────

async def generate_correction_scripts(
    excel_path: Path, output_dir: Path, ts: str | None = None
) -> Path:
    """
    Read GPL_AUDIT.xlsx, generate per-node AMOS correction scripts directly
    into output_dir (no per-node sub-folders), then zip the whole directory.

    output_dir is expected to already be named after the site/node (e.g.
    output/KK-NLCTPR12-1/).  The Excel file should already be written there
    before this is called.  The zip is placed at
    output_dir.parent/{output_dir.name}.zip.

    Returns the path to the zip file.
    """
    if ts is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir.mkdir(parents=True, exist_ok=True)

    xl = pd.ExcelFile(excel_path)
    sheet_names = xl.sheet_names

    def _parse(sheet: str) -> pd.DataFrame:
        return xl.parse(sheet) if sheet in sheet_names else pd.DataFrame()

    (gpl_df, feat_df, eutran_freq_df,
     freq_rel_df, cell_rel_df, cell_data_df) = await asyncio.gather(
        asyncio.to_thread(_parse, "LTE_GPL_AUDIT"),
        asyncio.to_thread(_parse, "LTE_FeatureState"),
        asyncio.to_thread(_parse, "LTE_Eutranfrequency"),
        asyncio.to_thread(_parse, "LTE_EutranfreqRelation"),
        asyncio.to_thread(_parse, "LTE_CellRelation"),
        asyncio.to_thread(_parse, "LTE_CELL_DATA"),
    )

    # ── filter rows ───────────────────────────────────────────────────────────
    feat_notok = feat_df[feat_df.get("Feature setting Status", pd.Series(dtype=str)) == "NOT OK"].copy() if not feat_df.empty else pd.DataFrame()

    # EutranFrequency status column may be 'status' or 'Status'
    _status_col = "status" if "status" in eutran_freq_df.columns else "Status"
    eutran_freq_missing = eutran_freq_df[
        eutran_freq_df[_status_col] == "Missing in Post"
    ].copy() if not eutran_freq_df.empty and _status_col in eutran_freq_df.columns else pd.DataFrame()

    freq_rel_notok   = freq_rel_df[freq_rel_df["Status"] == "NOT OK"].copy()  if "Status" in freq_rel_df.columns else pd.DataFrame()
    freq_rel_missing = freq_rel_df[freq_rel_df["Status"] == "Missing"].copy() if "Status" in freq_rel_df.columns else pd.DataFrame()

    cell_rel_notok   = cell_rel_df[cell_rel_df["Status"] == "NOT OK"].copy()  if "Status" in cell_rel_df.columns else pd.DataFrame()
    cell_rel_missing = cell_rel_df[cell_rel_df["Status"] == "Missing"].copy() if "Status" in cell_rel_df.columns else pd.DataFrame()

    gpl_mask = (
        (gpl_df["Parameter Setting Status"] != "OK") & gpl_df["Current value"].notna()
    ) if not gpl_df.empty and "Parameter Setting Status" in gpl_df.columns else pd.Series(dtype=bool)
    gpl_notok = gpl_df[gpl_mask].copy() if not gpl_mask.empty else pd.DataFrame()

    valid_frequencies = cell_data_df["earfcndl"].dropna().unique().tolist() if "earfcndl" in cell_data_df.columns else []

    # ── discover post node names from any available sheet ─────────────────────
    post_nodes: list[str] = []
    for df in (gpl_notok, feat_df, freq_rel_df, cell_rel_df):
        if not df.empty and "Node_ID" in df.columns:
            candidates = df["Node_ID"].dropna().unique().tolist()
            candidates = [n for n in candidates if n not in ("", "cell not found in post", "Cell is not Found in Post")]
            if candidates:
                post_nodes = candidates
                break

    if not post_nodes:
        log.warning("No post nodes found in audit data — correction scripts skipped.")
        return output_dir / f"GPL_AUDIT_{ts}.zip"

    log.info("Generating correction scripts for nodes: %s", post_nodes)

    # ── per-node tasks ─────────────────────────────────────────────────────────
    tasks = []
    for node in post_nodes:
        # Scripts go directly into output_dir (flat — no sub-folder per node).
        # output_dir is already named after the site, e.g. output/KK-NLCTPR12-1/

        def _node_slice(df: pd.DataFrame, node_val: str, extra: list[str] | None = None) -> pd.DataFrame:
            if df.empty or "Node_ID" not in df.columns:
                return df.copy() if not df.empty else pd.DataFrame()
            values = [node_val] + (extra or [])
            return df[df["Node_ID"].isin(values)].copy()

        tasks.append(asyncio.to_thread(
            _write_node_scripts,
            node, output_dir, ts,
            _node_slice(gpl_notok, node),
            _node_slice(feat_notok, node) if not feat_notok.empty else pd.DataFrame(),
            _node_slice(eutran_freq_missing, node) if not eutran_freq_missing.empty else pd.DataFrame(),
            _node_slice(freq_rel_notok, node),
            _node_slice(freq_rel_missing, node),
            _node_slice(cell_rel_notok, node, ["cell not found in post"]),
            _node_slice(cell_rel_missing, node, ["cell not found in post"]),
            valid_frequencies,
        ))

    await asyncio.gather(*tasks)

    # ── zip the entire session folder ─────────────────────────────────────────
    zip_path = output_dir.parent / f"{output_dir.name}.zip"
    await asyncio.to_thread(_zip_output, output_dir, zip_path)

    return zip_path
