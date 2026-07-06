import asyncio
import logging
import re
import pandas as pd

from .commands import load_commands
from .config import get_pre_files, get_post_files
from .extractors import (
    _clean_value,
    get_lte_cell_data,
    get_lte_cell_relation_data,
    get_lte_enbinfo_data,
    get_lte_eutran_freq_data,
    get_lte_eutran_freq_relation_data,
    get_lte_feature_state_data,
    get_lte_gpl_data,
    get_nr_baseline_data,
    get_nr_cell_data,
    get_nr_feature_state_data,
    get_nr_gnbinfo_data,
    get_nr_gutran_freq_relation_data,
)

log = logging.getLogger(__name__)


def _build_audit_df(pre_df: pd.DataFrame, post_df: pd.DataFrame) -> pd.DataFrame:
    merged = pre_df.merge(
        post_df,
        on=["MO", "Perameter"],
        how="left",
        suffixes=("_pre", "_post"),
    ).rename(columns={"value_pre": "pre_value", "value_post": "current_value"})

    if "Node_ID_post" in merged.columns:
        merged["Node_ID"] = merged["Node_ID_post"]
        merged.drop(columns=["Node_ID_pre", "Node_ID_post"], inplace=True, errors="ignore")

    merged["pre_value"] = merged["pre_value"].apply(_clean_value)
    merged["current_value"] = merged["current_value"].apply(_clean_value)

    def _status(r):
        if pd.isna(r["current_value"]):
            return "MISSING IN POST"
        if pd.isna(r["pre_value"]):
            return "MISSING IN PRE"
        return "OK" if r["pre_value"] == r["current_value"] else "NOT OK"

    merged["status"] = merged.apply(_status, axis=1)
    keep = [c for c in ("Node_ID", "MO", "Perameter", "pre_value", "current_value", "status") if c in merged.columns]
    return merged[keep]


def _pipe_diff_columns(merged: pd.DataFrame, value_cols: list[str], suffixes: tuple[str, str] = ("_pre", "_post")) -> pd.Series:
    """Collapse each `<col>_pre` / `<col>_post` pair in `merged` into a single
    `<col>` column, in place — matching the pre|post diff format used by
    LTE_EutranfreqRelation. Where the values differ, the collapsed column holds
    "pre|post"; where one side is missing, it holds whichever side is present.
    Returns a boolean Series, True for rows where at least one compared column differed.
    """
    pre_sfx, post_sfx = suffixes
    diff_mask = pd.Series(False, index=merged.index)

    def _norm(s: pd.Series) -> pd.Series:
        return (
            s.fillna("")
             .astype(str)
             .str.lower()
             .str.strip()
             .replace({"nan": "", "<na>": "", "none": "", "nat": ""})
        )

    for col in value_cols:
        pre_col, post_col = f"{col}{pre_sfx}", f"{col}{post_sfx}"
        if pre_col not in merged.columns or post_col not in merged.columns:
            continue

        pre_s = _norm(merged[pre_col])
        post_s = _norm(merged[post_col])
        mask = pre_s.ne(post_s)
        diff_mask |= mask

        merged[pre_col] = merged[pre_col].astype(object)
        for idx in merged[mask].index:
            pre_raw, post_raw = merged.at[idx, pre_col], merged.at[idx, post_col]
            pre_v = "" if pd.isna(pre_raw) else str(pre_raw)
            post_v = "" if pd.isna(post_raw) else str(post_raw)
            if not post_v:
                merged.at[idx, pre_col] = pre_v
            elif not pre_v:
                merged.at[idx, pre_col] = post_v
            else:
                merged.at[idx, pre_col] = f"{pre_v}|{post_v}"

        merged.drop(columns=[post_col], inplace=True)
        merged.rename(columns={pre_col: col}, inplace=True)

    return diff_mask


import re

async def nr_baseline_audit() -> pd.DataFrame:
    commands = load_commands()
    pre_files, post_files = get_pre_files(), get_post_files()
    log.info("NR GPL Audit — %d PRE file(s), %d POST file(s)", len(pre_files), len(post_files))
    pre_df, post_df = await asyncio.gather(
        get_nr_baseline_data(commands, pre_files),
        get_nr_baseline_data(commands, post_files),
    )

    if pre_df.empty:
        log.warning("NR GPL Audit: no NR data found in log files — sheet will be skipped.")
        return pd.DataFrame()
    if post_df.empty:
        log.warning("NR GPL Audit: POST file produced no data — sheet will be skipped.")
        return pd.DataFrame()
    
    def _node_name(mo_series: pd.Series) -> str | None:
        """Extract node name from MO strings like 'NRCellDU=...xxxxCTPR11_A' or with commas."""
        try:
            # Handle comma-separated values (e.g., MO,NRFreqRelation=...)
            names = (
                mo_series.apply(lambda x: str(x).split(",")[0])  # Split by comma, take MO part
                .str.split("=").str[-1]  # Take after '=' (e.g., 'KK_5_EE_T1_OM_5_xxxxCTPR11_A')
                .str.extract(r"(x*[A-Z0-9]+)_[A-Z]$", expand=False)  # Extract node name before final _[A-Z]
                .str.replace(r"^x+", "", regex=True)  # Remove leading x's
                .dropna()
            )
            return names.iloc[0] if not names.empty else None
        except Exception:
            return None

    pre_node = _node_name(pre_df["MO"])
    post_node = _node_name(post_df["MO"])

    # Rename pre MOs so they align with post cell names (cross-node swap support)
    if pre_node and post_node and pre_node != post_node:
        log.info("NR GPL Audit: cross-node rename _%s_ → _%s_ in PRE MOs", pre_node, post_node)
        pattern = rf"_(x*){re.escape(pre_node)}"
        pre_df["MO"] = pre_df["MO"].str.replace(pattern, rf"_\1{post_node}", regex=True)

    result = _build_audit_df(pre_df, post_df)
    log.info(
        "NR GPL Audit — %d rows | OK: %d | NOT OK: %d | MISSING IN POST: %d",
        len(result),
        (result["status"] == "OK").sum(),
        (result["status"] == "NOT OK").sum(),
        (result["status"] == "MISSING IN POST").sum(),
    )
    return result


async def nr_cell_data_audit() -> tuple[pd.DataFrame, pd.DataFrame]:
    commands = load_commands()
    pre_files, post_files = get_pre_files(), get_post_files()
    log.info("NR Cell Data — %d PRE file(s), %d POST file(s)", len(pre_files), len(post_files))
    pre_df, post_df = await asyncio.gather(
        get_nr_cell_data(commands, pre_files),
        get_nr_cell_data(commands, post_files),
    )
    log.info("NR Cell Data PRE: %d rows x %d cols", *pre_df.shape)
    log.info("NR Cell Data POST: %d rows x %d cols", *post_df.shape)
    return pre_df, post_df


async def lte_enbinfo_audit() -> pd.DataFrame:
    commands = load_commands()
    pre_files, post_files = get_pre_files(), get_post_files()
    log.info("LTE eNBInfo Audit — %d PRE file(s), %d POST file(s)", len(pre_files), len(post_files))

    pre_df, post_df = await asyncio.gather(
        get_lte_enbinfo_data(commands, pre_files),
        get_lte_enbinfo_data(commands, post_files),
    )
    if pre_df.empty:
        log.warning("LTE eNBInfo Audit: no data in PRE files — sheet will be skipped.")
        return pd.DataFrame()
    if post_df.empty:
        log.warning("LTE eNBInfo Audit: no data in POST files — sheet will be skipped.")
        return pd.DataFrame()

    # determine which value columns to compare (all non-key cols)
    val_cols = [c for c in pre_df.columns if c not in ("Node_ID", "MO")]

    # enbinfo MO is "ENodeBFunction=1" on both nodes — merge on MO to compare
    merged = pd.merge(pre_df, post_df, on="MO", how="outer", suffixes=("_pre", "_post"), indicator=True)

    # Node_ID: prefer post (current node); fall back to pre if row missing in post
    if "Node_ID_post" in merged.columns:
        merged["Node_ID"] = merged["Node_ID_post"].fillna(merged.get("Node_ID_pre"))
        merged.drop(columns=["Node_ID_pre", "Node_ID_post"], inplace=True, errors="ignore")

    diff_mask = _pipe_diff_columns(merged, val_cols)

    merged["Status"] = "OK"
    merged.loc[diff_mask, "Status"] = "NOT OK"
    merged.loc[merged["_merge"] == "left_only", "Status"] = "Missing"
    merged.drop(columns=["_merge"], inplace=True)

    out_cols = ["Node_ID", "MO"] + val_cols + ["Status"]
    result = merged[[c for c in out_cols if c in merged.columns]]

    log.info(
        "LTE eNBInfo — %d rows | OK: %d | NOT OK: %d | Missing: %d",
        len(result),
        (result["Status"] == "OK").sum(),
        (result["Status"] == "NOT OK").sum(),
        (result["Status"] == "Missing").sum(),
    )
    return result

async def nr_gnbinfo_audit() -> pd.DataFrame:
    commands = load_commands()
    pre_files, post_files = get_pre_files(), get_post_files()
    log.info("NR gNBInfo Audit — %d PRE file(s), %d POST file(s)", len(pre_files), len(post_files))

    pre_df, post_df = await asyncio.gather(
        get_nr_gnbinfo_data(commands, pre_files),
        get_nr_gnbinfo_data(commands, post_files),
    )
    if pre_df.empty:
        log.warning("NR gNBInfo Audit: no data in PRE files — sheet will be skipped.")
        return pd.DataFrame()
    if post_df.empty:
        log.warning("NR gNBInfo Audit: no data in POST files — sheet will be skipped.")
        return pd.DataFrame()

    # determine which value columns to compare (all non-key cols)
    val_cols = [c for c in pre_df.columns if c not in ("Node_ID", "MO")]

    # gnbinfo MO is "ENodeBFunction=1" on both nodes — merge on MO to compare
    merged = pd.merge(pre_df, post_df, on="MO", how="outer", suffixes=("_pre", "_post"), indicator=True)

    # Node_ID: prefer post (current node); fall back to pre if row missing in post
    if "Node_ID_post" in merged.columns:
        merged["Node_ID"] = merged["Node_ID_post"].fillna(merged.get("Node_ID_pre"))
        merged.drop(columns=["Node_ID_pre", "Node_ID_post"], inplace=True, errors="ignore")

    diff_mask = _pipe_diff_columns(merged, val_cols)

    merged["Status"] = "OK"
    merged.loc[diff_mask, "Status"] = "NOT OK"
    merged.loc[merged["_merge"] == "left_only", "Status"] = "Missing"
    merged.drop(columns=["_merge"], inplace=True)

    out_cols = ["Node_ID", "MO"] + val_cols + ["Status"]
    result = merged[[c for c in out_cols if c in merged.columns]]

    log.info(
        "NR gNBInfo — %d rows | OK: %d | NOT OK: %d | Missing: %d",
        len(result),
        (result["Status"] == "OK").sum(),
        (result["Status"] == "NOT OK").sum(),
        (result["Status"] == "Missing").sum(),
    )
    return result


async def lte_summary_audit() -> pd.DataFrame:
    commands = load_commands()
    pre_files, post_files = get_pre_files(), get_post_files()
    log.info("LTE Summary — %d PRE file(s), %d POST file(s)", len(pre_files), len(post_files))

    cell_pre, cell_post, enb_pre, enb_post = await asyncio.gather(
        get_lte_cell_data(commands, pre_files),
        get_lte_cell_data(commands, post_files),
        get_lte_enbinfo_data(commands, pre_files),
        get_lte_enbinfo_data(commands, post_files),
    )

    # eNBId mappings: Node_ID → enbid
    pre_enb_map: dict = {}
    post_enb_map: dict = {}
    enb_col = next((c for c in ("enbid", "eNBId", "eNBID") if not enb_pre.empty and c in enb_pre.columns), None)
    if enb_col and "Node_ID" in enb_pre.columns:
        pre_enb_map = dict(zip(enb_pre["Node_ID"].astype(str), enb_pre[enb_col].astype(str)))
    if enb_col and not enb_post.empty and "Node_ID" in enb_post.columns:
        post_enb_map = dict(zip(enb_post["Node_ID"].astype(str), enb_post[enb_col].astype(str)))

    # Build cell-level rows from cell_data
    def _cell_rows(cell_df: pd.DataFrame, site_col: str, name_col: str) -> pd.DataFrame:
        if cell_df.empty or "cellId" not in cell_df.columns:
            return pd.DataFrame(columns=[site_col, name_col, "cellId"])
        out = cell_df[["Node_ID", "MO", "cellId"]].copy()
        out["cellId"] = out["cellId"].astype(str)
        return out.rename(columns={"Node_ID": site_col, "MO": name_col})

    pre_cell_id_df = _cell_rows(cell_pre, "Pre SiteId", "Pre CellName")
    post_cell_id_df = _cell_rows(cell_post, "Post SiteId", "Post CellName")

    summary = pd.merge(pre_cell_id_df, post_cell_id_df, on="cellId", how="outer").fillna("NA")
    summary = summary.sort_values(by=["Pre SiteId", "Pre CellName", "cellId"], ascending=True).reset_index(drop=True)

    summary["Pre eNBID"] = summary["Pre SiteId"].apply(lambda x: pre_enb_map.get(x, "NA") if x != "NA" else "NA")
    summary["Post eNBID"] = summary["Post SiteId"].apply(lambda x: post_enb_map.get(x, "NA") if x != "NA" else "NA")

    out_cols = ["Pre SiteId", "Pre CellName", "Pre eNBID", "cellId", "Post SiteId", "Post eNBID", "Post CellName"]
    result = summary[[c for c in out_cols if c in summary.columns]]

    log.info("LTE Summary — %d rows", len(result))
    return result


async def lte_gpl_audit() -> pd.DataFrame:
    commands = load_commands()
    pre_files, post_files = get_pre_files(), get_post_files()
    log.info("LTE GPL Audit — %d PRE file(s), %d POST file(s)", len(pre_files), len(post_files))

    pre_df, post_df, cell_post = await asyncio.gather(
        get_lte_gpl_data(commands, pre_files),
        get_lte_gpl_data(commands, post_files),
        get_lte_cell_data(commands, post_files),
    )

    if pre_df.empty:
        log.warning("LTE GPL Audit: no LTE data found in log files — sheet will be skipped.")
        return pd.DataFrame()
    if post_df.empty:
        log.warning("LTE GPL Audit: POST file produced no data — sheet will be skipped.")
        return pd.DataFrame()

    # Align column names to old format
    pre_df = pre_df.rename(columns={"Perameter": "Parameter", "value": "Value"})
    post_df = post_df.rename(columns={"Perameter": "Parameter", "value": "Value"})

    # Build cellId map from POST cell_data {MO: cellId}
    cell_id_map: dict = {}
    if not cell_post.empty and "cellId" in cell_post.columns:
        cell_id_map = dict(zip(cell_post["MO"], cell_post["cellId"]))

    # Extract node name from MO: "EUtranCellFDD=KK_E_F1_OM_CTPR12A_A" → "CTPR12"
    def _node_name(mo_series: pd.Series) -> str | None:
        try:
            names = (
                mo_series.str.split("=").str[-1]
                .str.split("_")
                .apply(lambda p: p[4][:-1] if isinstance(p, list) and len(p) > 4 else None)
                .dropna()
            )
            return names.iloc[0] if not names.empty else None
        except Exception:
            return None

    pre_node = _node_name(pre_df["MO"])
    post_node = _node_name(post_df["MO"])

    # Rename pre MOs so they align with post cell names (cross-node swap support)
    if pre_node and post_node and pre_node != post_node:
        log.info("LTE GPL Audit: cross-node rename _%s_ → _%s_ in PRE MOs", pre_node, post_node)
        pre_df["MO"] = pre_df["MO"].str.replace(f"_{pre_node}", f"_{post_node}", regex=False)

    # Add cellId using the first MO component as the lookup key
    pre_df["cellId"] = pre_df["MO"].apply(lambda x: cell_id_map.get(str(x).split(",")[0], 0))
    post_df["cellId"] = post_df["MO"].apply(lambda x: cell_id_map.get(str(x).split(",")[0], 0))

    # Carry pre value into a named column before merge
    pre_df = pre_df.assign(**{"Pre-existing Value": pre_df["Value"]})

    merged = pd.merge(
        left=pre_df,
        right=post_df,
        how="left",
        on=["MO", "cellId", "Parameter"],
        suffixes=("_pre", "_post"),
        indicator=True,
    )

    # Node_ID: use post value; if cell missing in post, mark it
    if "Node_ID_post" in merged.columns:
        merged["Node_ID"] = merged["Node_ID_post"].fillna("Cell is not Found in Post")
        merged.drop(columns=["Node_ID_pre", "Node_ID_post"], inplace=True, errors="ignore")

    merged["Current value"] = merged["Value_post"]
    merged.drop(columns=["Value_pre", "Value_post"], inplace=True, errors="ignore")
    merged.drop_duplicates(subset=["MO", "Parameter"], inplace=True)

    merged["Parameter Setting Status"] = merged.apply(
        lambda row: (
            "OK"
            if row["Current value"] == row["Pre-existing Value"]
            else (
                "Missing"
                if pd.isna(row["Current value"]) or pd.isna(row["Pre-existing Value"])
                else "NOT OK"
            )
        ),
        axis=1,
    )
    merged["Current value"] = merged["Current value"].fillna("NA")

    def _band(mo: str) -> str:
        if "_F1_" in mo: return "L2100"
        if "_F3_" in mo: return "L1800"
        if "_F8_" in mo: return "L900"
        if "_T1_" in mo or "_T2_" in mo: return "L23"
        return "Band Error"

    merged["Band"] = merged["MO"].apply(_band)

    out_cols = ["Node_ID", "MO", "cellId", "Parameter", "Pre-existing Value",
                "Current value", "_merge", "Parameter Setting Status", "Band"]
    result = merged[[c for c in out_cols if c in merged.columns]]

    log.info(
        "LTE GPL Audit — %d rows | OK: %d | NOT OK: %d | Missing: %d",
        len(result),
        (result["Parameter Setting Status"] == "OK").sum(),
        (result["Parameter Setting Status"] == "NOT OK").sum(),
        (result["Parameter Setting Status"] == "Missing").sum(),
    )
    return result


async def lte_feature_state_audit() -> pd.DataFrame:
    commands = load_commands()
    pre_files, post_files = get_pre_files(), get_post_files()
    log.info("LTE FeatureState Audit — %d PRE file(s), %d POST file(s)", len(pre_files), len(post_files))

    pre_df, post_df = await asyncio.gather(
        get_lte_feature_state_data(commands, pre_files),
        get_lte_feature_state_data(commands, post_files),
    )
    if pre_df.empty:
        log.warning("LTE FeatureState Audit: no data in PRE files — sheet will be skipped.")
        return pd.DataFrame()
    if post_df.empty:
        log.warning("LTE FeatureState Audit: no data in POST files — sheet will be skipped.")
        return pd.DataFrame()

    # Strip parenthetical suffix e.g. "ACTIVATED (1)" → "ACTIVATED"
    for col in ("featureState", "licenseState"):
        for _df in (pre_df, post_df):
            if col in _df.columns:
                _df[col] = _df[col].astype(str).str.split().str[0]

    # Rename MO → CXC ID to match reference output
    pre_df = pre_df.rename(columns={"MO": "CXC ID"})
    post_df = post_df.rename(columns={"MO": "CXC ID"})

    # Rename pre state columns to final output names
    pre_df = pre_df.rename(columns={
        "featureState": "Pre Existing FeatureState",
        "licenseState": "Pre Existing LicenseState",
    })

    # Merge on CXC ID + description (Node_ID excluded from key → cross-node handled)
    merge_on = ["CXC ID"]
    if "description" in pre_df.columns and "description" in post_df.columns:
        merge_on.append("description")

    merged = pd.merge(
        left=pre_df,
        right=post_df,
        on=merge_on,
        how="left",
        suffixes=("_pre", "_post"),
    )

    # Node_ID: use post (current node); fall back to pre if cell not found in post
    if "Node_ID_post" in merged.columns:
        merged["Node_ID"] = merged["Node_ID_post"].fillna(merged.get("Node_ID_pre", ""))
        merged.drop(columns=["Node_ID_pre", "Node_ID_post"], inplace=True, errors="ignore")

    merged["Current FeatureState"] = merged["featureState"].astype(str)
    merged["Current LicenseState"] = merged["licenseState"].astype(str)
    merged.drop(columns=["featureState", "licenseState"], inplace=True, errors="ignore")

    def _feat_status(row):
        curr_feat = str(row.get("Current FeatureState", "nan"))
        pre_feat  = str(row.get("Pre Existing FeatureState", "nan"))
        curr_lic  = str(row.get("Current LicenseState", "nan"))
        pre_lic   = str(row.get("Pre Existing LicenseState", "nan"))
        if curr_feat in ("nan", "") or curr_lic in ("nan", ""):
            return "Missing"
        return "OK" if curr_feat == pre_feat and curr_lic == pre_lic else "NOT OK"

    merged["Feature setting Status"] = merged.apply(_feat_status, axis=1)

    out_cols = [
        "Node_ID", "CXC ID", "description",
        "Pre Existing FeatureState", "Pre Existing LicenseState",
        "Current FeatureState", "Current LicenseState",
        "Feature setting Status",
    ]
    result = merged[[c for c in out_cols if c in merged.columns]]

    log.info(
        "LTE FeatureState — %d rows | OK: %d | NOT OK: %d | Missing: %d",
        len(result),
        (result["Feature setting Status"] == "OK").sum(),
        (result["Feature setting Status"] == "NOT OK").sum(),
        (result["Feature setting Status"] == "Missing").sum(),
    )
    return result


async def nr_feature_state_audit() -> pd.DataFrame:
    commands = load_commands()
    pre_files, post_files = get_pre_files(), get_post_files()
    log.info("NR FeatureState Audit — %d PRE file(s), %d POST file(s)", len(pre_files), len(post_files))

    pre_df, post_df = await asyncio.gather(
        get_nr_feature_state_data(commands, pre_files),
        get_nr_feature_state_data(commands, post_files),
    )
    if pre_df.empty:
        log.warning("NR FeatureState Audit: no data in PRE files — sheet will be skipped.")
        return pd.DataFrame()
    if post_df.empty:
        log.warning("NR FeatureState Audit: no data in POST files — sheet will be skipped.")
        return pd.DataFrame()

    # Strip parenthetical suffix e.g. "ACTIVATED (1)" → "ACTIVATED"
    for col in ("featureState", "licenseState"):
        for _df in (pre_df, post_df):
            if col in _df.columns:
                _df[col] = _df[col].astype(str).str.split().str[0]

    # Rename MO → CXC ID to match reference output
    pre_df = pre_df.rename(columns={"MO": "CXC ID"})
    post_df = post_df.rename(columns={"MO": "CXC ID"})

    # Rename pre state columns to final output names
    pre_df = pre_df.rename(columns={
        "featureState": "Pre Existing FeatureState",
        "licenseState": "Pre Existing LicenseState",
    })

    # Merge on CXC ID + description (Node_ID excluded from key → cross-node handled)
    merge_on = ["CXC ID"]
    if "description" in pre_df.columns and "description" in post_df.columns:
        merge_on.append("description")

    merged = pd.merge(
        left=pre_df,
        right=post_df,
        on=merge_on,
        how="left",
        suffixes=("_pre", "_post"),
    )

    # Node_ID: use post (current node); fall back to pre if cell not found in post
    if "Node_ID_post" in merged.columns:
        merged["Node_ID"] = merged["Node_ID_post"].fillna(merged.get("Node_ID_pre", ""))
        merged.drop(columns=["Node_ID_pre", "Node_ID_post"], inplace=True, errors="ignore")

    merged["Current FeatureState"] = merged["featureState"].astype(str)
    merged["Current LicenseState"] = merged["licenseState"].astype(str)
    merged.drop(columns=["featureState", "licenseState"], inplace=True, errors="ignore")

    def _feat_status(row):
        curr_feat = str(row.get("Current FeatureState", "nan"))
        pre_feat  = str(row.get("Pre Existing FeatureState", "nan"))
        curr_lic  = str(row.get("Current LicenseState", "nan"))
        pre_lic   = str(row.get("Pre Existing LicenseState", "nan"))
        if curr_feat in ("nan", "") or curr_lic in ("nan", ""):
            return "Missing"
        return "OK" if curr_feat == pre_feat and curr_lic == pre_lic else "NOT OK"

    merged["Feature setting Status"] = merged.apply(_feat_status, axis=1)

    out_cols = [
        "Node_ID", "CXC ID", "description",
        "Pre Existing FeatureState", "Pre Existing LicenseState",
        "Current FeatureState", "Current LicenseState",
        "Feature setting Status",
    ]
    result = merged[[c for c in out_cols if c in merged.columns]]

    log.info(
        "NR FeatureState — %d rows | OK: %d | NOT OK: %d | Missing: %d",
        len(result),
        (result["Feature setting Status"] == "OK").sum(),
        (result["Feature setting Status"] == "NOT OK").sum(),
        (result["Feature setting Status"] == "Missing").sum(),
    )
    return result


async def lte_eutran_freq_audit() -> pd.DataFrame:
    commands = load_commands()
    pre_files, post_files = get_pre_files(), get_post_files()
    log.info("LTE Eutranfrequency Audit — %d PRE file(s), %d POST file(s)", len(pre_files), len(post_files))

    pre_df, post_df = await asyncio.gather(
        get_lte_eutran_freq_data(commands, pre_files),
        get_lte_eutran_freq_data(commands, post_files),
    )
    if pre_df.empty:
        log.warning("LTE Eutranfrequency Audit: no data in PRE files — sheet will be skipped.")
        return pd.DataFrame()
    if post_df.empty:
        log.warning("LTE Eutranfrequency Audit: no data in POST files — sheet will be skipped.")
        return pd.DataFrame()

    # require the column in BOTH — if it's only in post we can't compare
    val_cols = [c for c in ("arfcnValueEUtranDl", "arfcn", "arfcnValueGeranDl") if c in pre_df.columns and c in post_df.columns]

    # how="left": only pre-existing frequencies are audited — a frequency
    # newly added in post with no pre counterpart isn't a regression.
    merged = pre_df.merge(post_df, on=["MO"], how="left", suffixes=("_pre", "_post"), indicator=True)

    if "Node_ID_post" in merged.columns:
        merged["Node_ID"] = merged["Node_ID_post"].fillna(merged.get("Node_ID_pre"))
        merged.drop(columns=["Node_ID_pre", "Node_ID_post"], inplace=True, errors="ignore")

    # A given MO only populates ONE of these three arfcn* columns (its own
    # frequency type — EUtran / GUtranSyncSignal / Geran); the others are
    # blank on both sides for that row, so the pipe-diff helper naturally
    # treats them as a non-diff instead of a false mismatch.
    diff_mask = _pipe_diff_columns(merged, val_cols)

    merged["status"] = "OK"
    merged.loc[diff_mask, "status"] = "NOT OK"
    merged.loc[merged["_merge"] == "left_only", "status"] = "Missing in Post"
    merged.drop(columns=["_merge"], inplace=True)

    out_cols = ["Node_ID", "MO"] + val_cols + ["status"]
    result = merged[[c for c in out_cols if c in merged.columns]]

    log.info(
        "LTE Eutranfrequency — %d rows | OK: %d | NOT OK: %d | Missing: %d",
        len(result),
        (result["status"] == "OK").sum(),
        (result["status"] == "NOT OK").sum(),
        (result["status"] == "Missing in Post").sum(),
    )
    return result


async def lte_eutran_freq_relation_audit() -> pd.DataFrame:
    commands = load_commands()
    pre_files, post_files = get_pre_files(), get_post_files()
    log.info("LTE EutranfreqRelation Audit — %d PRE file(s), %d POST file(s)", len(pre_files), len(post_files))

    pre_df, post_df, cell_post = await asyncio.gather(
        get_lte_eutran_freq_relation_data(commands, pre_files),
        get_lte_eutran_freq_relation_data(commands, post_files),
        get_lte_cell_data(commands, post_files),
    )
    if pre_df.empty:
        log.warning("LTE EutranfreqRelation Audit: no data in PRE files — sheet will be skipped.")
        return pd.DataFrame()
    if post_df.empty:
        log.warning("LTE EutranfreqRelation Audit: no data in POST files — sheet will be skipped.")
        return pd.DataFrame()

    for _df in (pre_df, post_df):
        if "lbBnrPolicy" in _df.columns:
            _df["lbBnrPolicy"] = _df["lbBnrPolicy"].astype(str).str.split().str[0]

    # post cell_data maps: MO → cellId, cellId → Node_ID
    cell_id_map: dict = {}
    cell_node_map: dict = {}
    if not cell_post.empty and "cellId" in cell_post.columns:
        cell_id_map = dict(zip(cell_post["MO"].astype(str), cell_post["cellId"].astype(str)))
        if "Node_ID" in cell_post.columns:
            cell_node_map = dict(zip(cell_post["cellId"].astype(str), cell_post["Node_ID"].astype(str)))

    # cross-node rename (same pattern as GPL audit)
    # NOTE: EutranFreqRelation MOs are compound ("cell,relation=N"), so take the
    # first comma-component before extracting the node name — otherwise
    # str.split("=")[-1] picks the numeric relation ID, not the cell name.
    def _node_name(mo_series: pd.Series):
        try:
            names = (
                mo_series.apply(lambda x: str(x).split(",")[0])
                .str.split("=").str[-1]
                .str.split("_")
                .apply(lambda p: p[4][:-1] if isinstance(p, list) and len(p) > 4 else None)
                .dropna()
            )
            return names.iloc[0] if not names.empty else None
        except Exception:
            return None

    pre_node = _node_name(pre_df["MO"])
    post_node = _node_name(post_df["MO"])
    if pre_node and post_node and pre_node != post_node:
        log.info("LTE EutranfreqRelation: cross-node rename _%s_ → _%s_ in PRE MOs", pre_node, post_node)
        pre_df["MO"] = pre_df["MO"].str.replace(f"_{pre_node}", f"_{post_node}", regex=False)

    # add cellId using post mapping (after rename so MOs match post names)
    for _df in (pre_df, post_df):
        _df.drop(columns=["cellId"], errors="ignore", inplace=True)
    pre_df.insert(1, "cellId", pre_df["MO"].apply(lambda x: cell_id_map.get(str(x).split(",")[0], "")))
    post_df.insert(1, "cellId", post_df["MO"].apply(lambda x: cell_id_map.get(str(x).split(",")[0], "")))

    # type consistency for integer columns
    for col in pre_df.select_dtypes(include="int64").columns:
        if col in post_df.columns:
            post_df[col] = post_df[col].astype("int64")

    merged = pd.merge(
        left=pre_df, right=post_df,
        on=["MO", "cellId"], how="left",
        suffixes=("_x", "_y"),
    )

    # float64 → Int64 (preserves NA)
    for col in merged.select_dtypes(include="float64").columns:
        merged[col] = (
            pd.to_numeric(merged[col], errors="coerce")
            .replace([float("inf"), float("-inf")], pd.NA)
            .astype("Int64")
        )

    # eutranFrequencyRef: keep post, fall back to pre if missing
    if "eutranFrequencyRef_y" in merged.columns and "eutranFrequencyRef_x" in merged.columns:
        merged["eutranFrequencyRef_y"] = merged["eutranFrequencyRef_y"].fillna(merged["eutranFrequencyRef_x"])
        merged.drop(columns=["eutranFrequencyRef_x"], inplace=True)
        merged.rename(columns={"eutranFrequencyRef_y": "eutranFrequencyRef"}, inplace=True)

    # Node_ID: use post value, mark cells not found
    if "Node_ID_y" in merged.columns:
        merged["Node_ID_y"] = merged["Node_ID_y"].fillna("Cell is not Found in Post")
        merged["Node_ID_x"] = merged["Node_ID_y"]
        merged.drop(columns=["Node_ID_y"], inplace=True)
        merged.rename(columns={"Node_ID_x": "Node_ID"}, inplace=True)

    # Normalize cross-node reference columns on the pre side: replace the pre
    # node name with the post node name so that refs like qciProfileRef that
    # embed "ManagedElement=KK-NLCTPR11-1,..." compare equal when the actual
    # profile name is the same on both nodes.
    if pre_node and post_node and pre_node != post_node:
        ref_cols_x = [
            c for c in merged.columns
            if c.endswith("Ref_x") and c != "eutranFrequencyRef_x"
        ]
        for rc in ref_cols_x:
            merged[rc] = merged[rc].astype(str).str.replace(pre_node, post_node, regex=False)

    merged["duplicates_mask"] = merged.duplicated(subset=merged.columns.tolist())
    merged.insert(3, "Status", "OK")

    def _norm(s: pd.Series) -> pd.Series:
        # fillna first so float/pandas NA become '' before astype(str),
        # then normalise remaining null-like strings ('nan', '<na>', 'none')
        return (
            s.fillna("")
             .astype(str)
             .str.lower()
             .str.strip()
             .replace({"nan": "", "<na>": "", "none": "", "nat": ""})
        )

    skip = {"MO", "Node_ID", "eutranFrequencyRef", "cellId"}
    for col in pre_df.columns:
        if col in skip:
            continue
        pre_col, post_col = f"{col}_x", f"{col}_y"
        if pre_col not in merged.columns or post_col not in merged.columns:
            continue
        pre_s = _norm(merged[pre_col])
        post_s = _norm(merged[post_col])
        mask = pre_s.ne(post_s)
        merged.loc[mask, "Status"] = "NOT OK"
        if mask.any():
            merged[pre_col] = merged[pre_col].astype(object)
            for idx in merged[mask].index:
                pre_v = str(merged.at[idx, pre_col])
                post_v = str(merged.at[idx, post_col])
                if post_v in ("nan", "0", "<na>", "<NA>", ""):
                    merged.at[idx, pre_col] = pre_v
                else:
                    merged.at[idx, pre_col] = f"{pre_v}|{post_v}"

    merged["Status"] = merged.apply(
        lambda row: "Missing" if row.get("Node_ID") == "Cell is not Found in Post" else row["Status"],
        axis=1,
    )

    # final Node_ID from cellId lookup, then sort
    merged["Node_ID"] = merged["cellId"].apply(lambda x: cell_node_map.get(str(x), ""))
    merged.sort_values(by=["Node_ID"], inplace=True)

    merged = merged[[c for c in merged.columns if not c.endswith("_y")]]
    merged.rename(columns={c: c[:-2] for c in merged.columns if c.endswith("_x")}, inplace=True)

    log.info(
        "LTE EutranfreqRelation — %d rows | OK: %d | NOT OK: %d | Missing: %d",
        len(merged),
        (merged["Status"] == "OK").sum(),
        (merged["Status"] == "NOT OK").sum(),
        (merged["Status"] == "Missing").sum(),
    )
    return merged

async def nr_gutran_freq_relation_audit() -> pd.DataFrame:
    commands = load_commands()
    pre_files, post_files = get_pre_files(), get_post_files()
    log.info("NR GutranfreqRelation Audit — %d PRE file(s), %d POST file(s)", len(pre_files), len(post_files))

    pre_df, post_df, cell_post = await asyncio.gather(
        get_nr_gutran_freq_relation_data(commands, pre_files),
        get_nr_gutran_freq_relation_data(commands, post_files),
        get_lte_cell_data(commands, post_files),
    )
    if pre_df.empty:
        log.warning("NR GutranfreqRelation Audit: no data in PRE files — sheet will be skipped.")
        return pd.DataFrame()
    if post_df.empty:
        log.warning("NR GutranfreqRelation Audit: no data in POST files — sheet will be skipped.")
        return pd.DataFrame()

    log.info(
        "NR GutranfreqRelation — %d rows in PRE | %d rows in POST",
        len(pre_df),
        len(post_df),
    )

    def _node_name(mo_series: pd.Series):
        try:
            names = (
                mo_series.apply(lambda x: str(x).split(",")[0])
                .str.split("=").str[-1]
                .str.split("_")
                .apply(lambda p: p[4][:-1] if isinstance(p, list) and len(p) > 4 else None)
                .dropna()
            )
            return names.iloc[0] if not names.empty else None
        except Exception:
            return None

    pre_node = _node_name(pre_df["MO"])
    post_node = _node_name(post_df["MO"])
    if pre_node and post_node and pre_node != post_node:
        log.info("NR GutranfreqRelation: cross-node rename _%s_ → _%s_ in PRE MOs", pre_node, post_node)
        pre_df["MO"] = pre_df["MO"].str.replace(f"_{pre_node}", f"_{post_node}", regex=False)

    val_cols = [c for c in pre_df.columns if c not in ("MO", "Node_ID")]

    merged = pd.merge(
        left=pre_df,
        right=post_df,
        on=["MO"],
        how="outer",
        suffixes=("_pre", "_post"),
        indicator=True,
    )

    if "Node_ID_post" in merged.columns:
        merged["Node_ID"] = merged["Node_ID_post"].fillna(merged.get("Node_ID_pre"))
        merged.drop(columns=["Node_ID_pre", "Node_ID_post"], inplace=True, errors="ignore")

    diff_mask = _pipe_diff_columns(merged, val_cols)

    merged["Status"] = "OK"
    merged.loc[diff_mask, "Status"] = "NOT OK"
    merged.loc[merged["_merge"] == "left_only", "Status"] = "Missing"
    merged.drop(columns=["_merge"], inplace=True)

    out_cols = ["Node_ID", "MO"] + val_cols + ["Status"]
    result = merged[[c for c in out_cols if c in merged.columns]]

    log.info(
        "NR GutranfreqRelation — %d rows | OK: %d | NOT OK: %d | Missing: %d",
        len(result),
        (result["Status"] == "OK").sum(),
        (result["Status"] == "NOT OK").sum(),
        (result["Status"] == "Missing").sum(),
    )

    return result




async def lte_cell_relation_audit() -> pd.DataFrame:
    commands = load_commands()
    pre_files, post_files = get_pre_files(), get_post_files()
    log.info("LTE CellRelation Audit — %d PRE file(s), %d POST file(s)", len(pre_files), len(post_files))

    pre_df, post_df, cell_pre, cell_post, enb_pre, enb_post = await asyncio.gather(
        get_lte_cell_relation_data(commands, pre_files),
        get_lte_cell_relation_data(commands, post_files),
        get_lte_cell_data(commands, pre_files),
        get_lte_cell_data(commands, post_files),
        get_lte_enbinfo_data(commands, pre_files),
        get_lte_enbinfo_data(commands, post_files),
    )
    if pre_df.empty:
        log.warning("LTE CellRelation Audit: no data in PRE files — sheet will be skipped.")
        return pd.DataFrame()
    if post_df.empty:
        log.warning("LTE CellRelation Audit: no data in POST files — sheet will be skipped.")
        return pd.DataFrame()

    # cell MO → cellId maps for pre and post
    pre_cell_id_map: dict = {}
    post_cell_id_map: dict = {}
    cell_node_map: dict = {}
    if not cell_pre.empty and "cellId" in cell_pre.columns:
        pre_cell_id_map = dict(zip(cell_pre["MO"].astype(str), cell_pre["cellId"].astype(str)))
    if not cell_post.empty and "cellId" in cell_post.columns:
        post_cell_id_map = dict(zip(cell_post["MO"].astype(str), cell_post["cellId"].astype(str)))
        if "Node_ID" in cell_post.columns:
            cell_node_map = dict(zip(cell_post["cellId"].astype(str), cell_post["Node_ID"].astype(str)))

    reversed_pre_map = {v: k for k, v in pre_cell_id_map.items()}   # pre cellId → cell MO
    reversed_post_map = {v: k for k, v in post_cell_id_map.items()}  # post cellId → cell MO

    # noughbourCellId = last segment after "-" in the relation MO
    # cellId = serving cell MO (first comma-delimited component) → mapped to cellId
    for _df in (pre_df, post_df):
        _df.drop(columns=["noughbourCellId", "cellId"], errors="ignore", inplace=True)
    pre_df.insert(2, "noughbourCellId", pre_df["MO"].apply(lambda mo: str(mo).split("-")[-1]))
    pre_df.insert(3, "cellId", pre_df["MO"].apply(lambda mo: pre_cell_id_map.get(str(mo).split(",")[0], "")))
    post_df.insert(2, "noughbourCellId", post_df["MO"].apply(lambda mo: str(mo).split("-")[-1]))
    post_df.insert(3, "cellId", post_df["MO"].apply(lambda mo: post_cell_id_map.get(str(mo).split(",")[0], "")))

    # eNBId filtering: keep only intra-eNB relations (neighbour eNBId == local eNBId).
    # The eNBId sits at position [1] after splitting the relation MO on "-":
    #   EUtranCellRelation=1-213895-30  →  split[1] = "213895"
    enb_col = next((c for c in ("eNBId", "enbid", "eNBID") if not enb_pre.empty and c in enb_pre.columns), None)
    pre_enb_ids: list[str] = []
    post_enb_ids: list[str] = []
    if enb_col:
        pre_enb_ids  = enb_pre[enb_col].astype(str).unique().tolist()
        post_enb_ids = enb_post[enb_col].astype(str).unique().tolist() if not enb_post.empty else []

    def _enb_id_from_mo(mo: str) -> str:
        try:
            return str(mo).split("-")[1]
        except (AttributeError, IndexError):
            return ""

    if pre_enb_ids:
        pre_df = pre_df[pre_df["MO"].apply(_enb_id_from_mo).isin(pre_enb_ids)].reset_index(drop=True)
        log.info("CellRelation: PRE filtered to %d intra-eNB rows (eNBIds: %s)", len(pre_df), pre_enb_ids)
    if post_enb_ids:
        post_df = post_df[post_df["MO"].apply(_enb_id_from_mo).isin(post_enb_ids)].reset_index(drop=True)
        log.info("CellRelation: POST filtered to %d intra-eNB rows (eNBIds: %s)", len(post_df), post_enb_ids)

    # cross-node rename
    def _node_name(mo_series: pd.Series):
        try:
            names = (
                mo_series.apply(lambda x: str(x).split(",")[0])
                .str.split("=").str[-1]
                .str.split("_")
                .apply(lambda p: p[4][:-1] if isinstance(p, list) and len(p) > 4 else None)
                .dropna()
            )
            return names.iloc[0] if not names.empty else None
        except Exception:
            return None

    pre_node = _node_name(pre_df["MO"])
    post_node = _node_name(post_df["MO"])

    # integer columns: strip parenthetical and convert
    int_cols = [
        "cellIndividualOffsetEUtran", "coverageIndicator", "loadBalancing",
        "qOffsetCellEUtran", "reportDlActivity", "sCellCandidate",
        "sCellPriority", "sleepModeCovCellCandidate",
    ]

    def _to_int(val):
        try:
            return int(str(val).split()[0])
        except (ValueError, TypeError, AttributeError):
            return None

    for col in int_cols:
        for _df in (pre_df, post_df):
            if col in _df.columns:
                _df[col] = _df[col].apply(_to_int)

    if pre_node and post_node and pre_node != post_node:
        log.info("LTE CellRelation: cross-node rename _%s_ → _%s_ in PRE", pre_node, post_node)
        # reverse cellId → cell name, rename node, then remap to post cellId
        pre_df["cellId"] = pre_df["cellId"].apply(lambda x: reversed_pre_map.get(str(x), str(x)))
        pre_df["noughbourCellId"] = pre_df["noughbourCellId"].apply(lambda x: reversed_pre_map.get(str(x), str(x)))

        pre_df["cellId"] = pre_df["cellId"].str.replace(f"_{pre_node}", f"_{post_node}", regex=False)
        pre_df["MO"] = pre_df["MO"].str.replace(pre_node, post_node, regex=False)
        pre_df["noughbourCellId"] = pre_df["noughbourCellId"].str.replace(f"_{pre_node}", f"_{post_node}", regex=False)

        pre_df["cellId"] = pre_df["cellId"].apply(lambda x: post_cell_id_map.get(x, ""))
        pre_df["noughbourCellId"] = pre_df["noughbourCellId"].apply(lambda x: post_cell_id_map.get(x, ""))

    pre_df["Node_ID"] = pre_df["cellId"].apply(lambda x: cell_node_map.get(str(x), ""))

    # replace the neighbour-cell segment in MO with new noughbourCellId
    def _fix_mo_neighbour(row):
        mo = str(row["MO"])
        nbr = str(row["noughbourCellId"]) if row["noughbourCellId"] else None
        if not nbr:
            return mo
        old_nbr = mo.split("-")[-1]
        return mo[: mo.rfind("-") + 1] + nbr if old_nbr else mo

    pre_df["MO"] = pre_df.apply(_fix_mo_neighbour, axis=1)

    # Replace pre eNBIds with post eNBIds inside the relation segment of the MO.
    # e.g.  EUtranCellRelation=1-213895-30  →  1-213896-30  (if eNBId changed)
    if pre_enb_ids and post_enb_ids and pre_enb_ids != post_enb_ids:
        def _replace_enb_ids(mo: str) -> str:
            for pre_id, post_id in zip(pre_enb_ids, post_enb_ids):
                mo = mo.replace(f"-{pre_id}-", f"-{post_id}-")
            return mo
        pre_df["MO"] = pre_df["MO"].apply(_replace_enb_ids)
        log.info("CellRelation: replaced eNBIds %s → %s in PRE MOs", pre_enb_ids, post_enb_ids)

    merged = (
        pd.merge(left=pre_df, right=post_df, how="left", on=["MO", "cellId"])
        .drop_duplicates(subset=["MO", "cellId"])
    )

    # keep ref columns from pre when post is missing
    for ref_col in ("neighborCellRef", "noughbourCellId"):
        xc, yc = f"{ref_col}_x", f"{ref_col}_y"
        if xc in merged.columns and yc in merged.columns:
            merged[yc] = merged[yc].fillna(merged[xc])
            merged[xc] = merged[yc]

    if "Node_ID_y" in merged.columns:
        merged["Node_ID_y"] = merged["Node_ID_y"].fillna("cell not found in post")
        merged["Node_ID_x"] = merged["Node_ID_y"]
        merged.drop(columns=["Node_ID_y"], inplace=True)
        merged.rename(columns={"Node_ID_x": "Node_ID"}, inplace=True)

    # ensure int cols are numeric after merge (avoids float/int mismatch NOT OK)
    for col in int_cols:
        for sfx in ("_x", "_y"):
            c = f"{col}{sfx}"
            if c in merged.columns:
                merged[c] = pd.to_numeric(merged[c], errors="coerce").fillna(0).astype(int)

    merged.insert(3, "Status", "OK")

    def _norm(s: pd.Series) -> pd.Series:
        # fillna first so float/pandas NA become '' before astype(str),
        # then normalise remaining null-like strings ('nan', '<na>', 'none')
        return (
            s.fillna("")
             .astype(str)
             .str.lower()
             .str.strip()
             .replace({"nan": "", "<na>": "", "none": "", "nat": ""})
        )

    skip = {"MO", "Node_ID", "neighborCellRef", "cellId", "noughbourCellId"}
    for col in pre_df.columns:
        if col in skip:
            continue
        pre_col, post_col = f"{col}_x", f"{col}_y"
        if pre_col not in merged.columns or post_col not in merged.columns:
            continue
        pre_s = _norm(merged[pre_col])
        post_s = _norm(merged[post_col])
        mask = pre_s.ne(post_s)
        merged.loc[mask, "Status"] = "NOT OK"
        if mask.any():
            merged[pre_col] = merged[pre_col].astype(object)
            for idx in merged[mask].index:
                pre_v = str(merged.at[idx, pre_col])
                post_v = str(merged.at[idx, post_col])
                merged.at[idx, pre_col] = pre_v if post_v in ("nan", "") else f"{pre_v}|{post_v}"

    merged["Status"] = merged.apply(
        lambda row: "Missing" if row.get("Node_ID") == "cell not found in post" else row["Status"],
        axis=1,
    )

    merged["Node_ID"] = merged["cellId"].apply(lambda x: cell_node_map.get(str(x), ""))
    merged.sort_values(by=["Node_ID"], inplace=True)

    merged = merged[[c for c in merged.columns if not c.endswith("_y")]]
    merged.rename(columns={c: c[:-2] for c in merged.columns if c.endswith("_x")}, inplace=True)

    # neighborCellRef: derive from post reversed mapping via noughbourCellId
    if "noughbourCellId" in merged.columns:
        merged["neighborCellRef"] = merged["noughbourCellId"].apply(
            lambda x: reversed_post_map.get(str(x), "")
        )

    # for Missing rows, strip the "|post" part from int cols (only pre value is valid)
    for col in int_cols:
        if col in merged.columns:
            merged.loc[merged["Status"] == "Missing", col] = (
                merged.loc[merged["Status"] == "Missing", col]
                .apply(lambda x: int(str(x).split("|")[0]) if "|" in str(x) else x)
            )

    log.info(
        "LTE CellRelation — %d rows | OK: %d | NOT OK: %d | Missing: %d",
        len(merged),
        (merged["Status"] == "OK").sum(),
        (merged["Status"] == "NOT OK").sum(),
        (merged["Status"] == "Missing").sum(),
    )
    return merged


async def lte_cell_data_audit() -> tuple[pd.DataFrame, pd.DataFrame]:
    commands = load_commands()
    pre_files, post_files = get_pre_files(), get_post_files()
    log.info("LTE Cell Data — %d PRE file(s), %d POST file(s)", len(pre_files), len(post_files))
    pre_df, post_df = await asyncio.gather(
        get_lte_cell_data(commands, pre_files),
        get_lte_cell_data(commands, post_files),
    )
    log.info("LTE Cell Data PRE: %d rows x %d cols", *pre_df.shape)
    log.info("LTE Cell Data POST: %d rows x %d cols", *post_df.shape)
    return pre_df, post_df