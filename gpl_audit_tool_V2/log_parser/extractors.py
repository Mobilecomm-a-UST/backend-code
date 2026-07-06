import logging
import re
from pathlib import Path

import pandas as pd

from .reader import parse_all_commands_multi

log = logging.getLogger(__name__)


def _clean_value(val):
    if pd.isna(val):
        return val
    return re.sub(r"\s*\([^)]*\)", "", str(val)).strip()


async def get_nr_baseline_data(
    commands: dict,
    file_paths: list[Path | str],
    key: str = "NR_GPL_AUDIT",
) -> pd.DataFrame:
    nr_commands = commands.get(key)
    if not nr_commands:
        log.warning("Section '%s' not found in commands — skipping.", key)
        return pd.DataFrame()

    all_dfs = await parse_all_commands_multi(nr_commands, file_paths)

    frames = []
    for cmd, df in all_dfs.items():
        if df.empty:
            continue
        if "MO" not in df.columns:
            log.warning("'MO' column missing for command: %s", cmd)
            continue
        id_vars = [c for c in ("Node_ID", "MO") if c in df.columns]
        frames.append(df.melt(id_vars=id_vars, var_name="Perameter"))

    if not frames:
        log.warning("No valid data extracted from %s [%s]", file_paths, key)
        return pd.DataFrame()

    return pd.concat(frames, axis=0, ignore_index=True)


async def get_nr_cell_data(
    commands: dict,
    file_paths: list[Path | str],
    key: str = "NR_CELL_DATA",
) -> pd.DataFrame:
    nr_commands = commands.get(key)
    if not nr_commands:
        log.warning("Section '%s' not found in commands — skipping.", key)
        return pd.DataFrame()

    all_dfs = await parse_all_commands_multi(nr_commands, file_paths)

    frames = []
    for cmd, df in all_dfs.items():
        if df.empty:
            continue
        if "MO" not in df.columns:
            log.warning("'MO' column missing for command: %s", cmd)
            continue
        frames.append(df)

    if not frames:
        log.warning("No valid data extracted from %s [%s]", file_paths, key)
        return pd.DataFrame()

    result = frames[0].reset_index(drop=True)
    for i, df in enumerate(frames[1:], 1):
        df = df.reset_index(drop=True).rename(columns={"MO": f"MO_{i}"})
        df = df.drop(columns=["Node_ID"], errors="ignore")
        result = pd.concat([result, df], axis=1)
    return result


async def get_lte_gpl_data(
    commands: dict,
    file_paths: list[Path | str],
    key: str = "LTE_GPL_AUDIT",
) -> pd.DataFrame:
    lte_commands = commands.get(key)
    if not lte_commands:
        log.warning("Section '%s' not found in commands — skipping.", key)
        return pd.DataFrame()

    all_dfs = await parse_all_commands_multi(lte_commands, file_paths)

    frames = []
    for cmd, df in all_dfs.items():
        if df.empty:
            continue
        if "MO" not in df.columns:
            log.warning("'MO' column missing for command: %s", cmd)
            continue
        id_vars = [c for c in ("Node_ID", "MO") if c in df.columns]
        frames.append(df.melt(id_vars=id_vars, var_name="Perameter"))

    if not frames:
        log.warning("No valid data extracted from %s [%s]", file_paths, key)
        return pd.DataFrame()

    return pd.concat(frames, axis=0, ignore_index=True)


async def _get_lte_wide_data(
    commands: dict,
    file_paths: list[Path | str],
    key: str,
) -> pd.DataFrame:
    """Concat all DataFrames for a section vertically (wide / non-melted)."""
    lte_commands = commands.get(key)
    if not lte_commands:
        log.warning("Section '%s' not found in commands — skipping.", key)
        return pd.DataFrame()

    all_dfs = await parse_all_commands_multi(lte_commands, file_paths)
    

    frames = []
    for cmd, df in all_dfs.items():
        if df.empty:
            continue
        if "MO" not in df.columns:
            log.warning("'MO' column missing for command: %s", cmd)
            continue
        frames.append(df)

    if not frames:
        log.warning("No valid data extracted from %s [%s]", file_paths, key)
        return pd.DataFrame()

    return pd.concat(frames, axis=0, ignore_index=True)


async def get_lte_enbinfo_data(
    commands: dict,
    file_paths: list[Path | str],
    key: str = "ENBINFO_AUDIT",
) -> pd.DataFrame:
    return await _get_lte_wide_data(commands, file_paths, key)

async def get_nr_gnbinfo_data(
    commands: dict,
    file_paths: list[Path | str],
    key: str = "GNBINFO_AUDIT",
) -> pd.DataFrame:
    df = await _get_lte_wide_data(commands, file_paths, key)
    if not df.empty:
        # hgetc splits some MOs (e.g. GNBCUUPFunction, whose pLMNId is a
        # struct attribute) across two physical output lines: one line has
        # gNBId/gNBIdLength populated with mcc/mnc blank, the next has it the
        # other way round. Coalesce rows sharing the same Node_ID+MO into one
        # logical row, keeping the first non-blank value per column.
        group_cols = [c for c in ("Node_ID", "MO") if c in df.columns]
        if group_cols:
            def _coalesce(s: pd.Series):
                for v in s:
                    if pd.notna(v) and str(v).strip() != "":
                        return v
                return s.iloc[0]

            df = df.groupby(group_cols, as_index=False, sort=False).agg(_coalesce)
    return df




async def get_lte_feature_state_data(
    commands: dict,
    file_paths: list[Path | str],
    key: str = "FEATURESTATE_AUDIT",
) -> pd.DataFrame:
    df = await _get_lte_wide_data(commands, file_paths, key)
    # The section mixes a broad "Lm=1,FeatureState" command with individual CXC
    # commands that overlap — deduplicate keeping the first occurrence per MO.
    if not df.empty:
        df = df.drop_duplicates(subset=["MO"], keep="first").reset_index(drop=True)
    return df


async def get_nr_feature_state_data(
    commands: dict,
    file_paths: list[Path | str],
    key: str = "NR_FEATURESTATE_AUDIT",
) -> pd.DataFrame:
    df = await _get_lte_wide_data(commands, file_paths, key)
    # The section batches several "CXCxxxxxxx$" hgetc commands whose CXC ranges
    # overlap slightly — deduplicate keeping the first occurrence per MO.
    if not df.empty:
        df = df.drop_duplicates(subset=["MO"], keep="first").reset_index(drop=True)
    return df


async def get_lte_eutran_freq_data(
    commands: dict,
    file_paths: list[Path | str],
    key: str = "EUTRANFREQUENCY_AUDIT",
) -> pd.DataFrame:
    return await _get_lte_wide_data(commands, file_paths, key)


async def get_lte_eutran_freq_relation_data(
    commands: dict,
    file_paths: list[Path | str],
    key: str = "EUTRANFREQRELATION_AUDIT",
) -> pd.DataFrame:
    df = await _get_lte_wide_data(commands, file_paths, key)
    if not df.empty:
        # Command 2 uses EutranFreqToQciProfileRelation@ (a child object), so its
        # MO column has an extra ",EutranFreqToQciProfileRelation=N" suffix.
        # Strip it so all 4 commands align to the same parent EUtranFreqRelation MO,
        # then groupby.first() merges columns across commands into one row per MO.
        df["MO"] = df["MO"].str.replace(
            r",EutranFreqToQciProfileRelation=\S+$", "", regex=True
        )
        df = df.groupby("MO", as_index=False).first()
    return df

async def get_nr_gutran_freq_relation_data(
    commands: dict,
    file_paths: list[Path | str],
    key: str = "GUTRANFREQRELATION_AUDIT",
) -> pd.DataFrame:
    df = await _get_lte_wide_data(commands, file_paths, key)
    if not df.empty:
        # Command 2 uses EutranFreqToQciProfileRelation@ (a child object), so its
        # MO column has an extra ",EutranFreqToQciProfileRelation=N" suffix.
        # Strip it so all 4 commands align to the same parent EUtranFreqRelation MO,
        # then groupby.first() merges columns across commands into one row per MO.
        df["MO"] = df["MO"].str.replace(
            r",EutranFreqToQciProfileRelation=\S+$", "", regex=True
        )
        df = df.groupby("MO", as_index=False).first()
    return df


async def get_lte_cell_relation_data(
    commands: dict,
    file_paths: list[Path | str],
    key: str = "CELLRELATION_AUDIT",
) -> pd.DataFrame:
    df = await _get_lte_wide_data(commands, file_paths, key)
    
    
    if not df.empty:
        # The section includes EUtranCell and ExternalGeranCell rows alongside
        # EUtranCellRelation rows.  Keep only the relation rows.
        df = df[df["MO"].str.contains("EUtranCellRelation", na=False)].reset_index(drop=True)
        # The audit dump batches both a "_PRE"/"_POST" file and an "_NR_5G_PRE"/
        # "_NR_5G_POST" file, and both contain the same LTE CellRelation section —
        # dedupe by MO like get_lte_eutran_freq_relation_data does.
        df = df.drop_duplicates(subset=["MO"], keep="first").reset_index(drop=True)
        # earfcndl/physicalLayerCellIdGroup/physicalLayerSubCellId/tac come from
        # the section's EUtranCellFDD command, and rimAssociationStatus/rimCapable
        # from its ExternalGeranCell command — both filtered out above, so these
        # columns are always empty once only EUtranCellRelation rows remain.
        df = df.drop(columns=[
            "earfcndl", "physicalLayerCellIdGroup", "physicalLayerSubCellId", "tac",
            "rimAssociationStatus", "rimCapable",
        ], errors="ignore")
    return df


async def get_lte_cell_data(
    commands: dict,
    file_paths: list[Path | str],
    key: str = "LTE_CELL_DATA",
) -> pd.DataFrame:
    lte_commands = commands.get(key)
    
    if not lte_commands:
        log.warning("Section '%s' not found in commands — skipping.", key)
        return pd.DataFrame()

    all_dfs = await parse_all_commands_multi(lte_commands, file_paths)
    
    

    frames = []
    for cmd, df in all_dfs.items():
        if df.empty:
            continue
        if "MO" not in df.columns:
            log.warning("'MO' column missing for command: %s", cmd)
            continue
        frames.append(df)

    if not frames:
        log.warning("No valid data extracted from %s [%s]", file_paths, key)
        return pd.DataFrame()

    result = frames[0].reset_index(drop=True)
    for i, df in enumerate(frames[1:], 1):
        df = df.reset_index(drop=True).rename(columns={"MO": f"MO_{i}"})
        df = df.drop(columns=["Node_ID"], errors="ignore")
        result = pd.concat([result, df], axis=1)
    
    return result

