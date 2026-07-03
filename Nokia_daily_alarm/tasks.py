import os
import win32com.client
import pythoncom
import requests
import zipfile
import py7zr
import shutil
from datetime import datetime
from celery import shared_task
from mcom_website.settings import MEDIA_ROOT
from mailapp.tasks import send_email
import pandas as pd  # make sure this is your Celery email task
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import os
from premailer import transform
from universal_alarm.models import OldvsNew
from datetime import datetime
import re

current_time = datetime.now().strftime("%d %B %Y, %I:%M %p")

save_directory = os.path.join(MEDIA_ROOT, "NOKIA_OUTPUT", "attachments")
LAST_PROCESSED_FILE = os.path.join(MEDIA_ROOT, "NOKIA_OUTPUT", "last_mail.txt")

def get_summary_counts(excel_path):
    sheets = pd.read_excel(excel_path, sheet_name=None)

    # ================= SHEETS =================
    cells_4g = sheets.get("4G_Status")
    cells_5g = sheets.get("5G_Status")

    alarm_df = sheets.get("Alarm_Output")
    old_new_4g_df = sheets.get("4G Old vs New")
    old_new_5g_df = sheets.get("5G Old vs New")
    # ================= BOTH LOCK / UNLOCK COUNT =================
    cells_set_4g = set()
    sites_set_4g = set()

    cells_set_5g = set()
    sites_set_5g = set()

    both_locked_cells_4g = set()
    both_unlocked_cells_4g = set()
    both_locked_sites_4g = set()
    both_unlocked_sites_4g = set()

    both_locked_cells_5g = set()
    both_unlocked_cells_5g = set()
    both_locked_sites_5g = set()
    both_unlocked_sites_5g = set()


    # ================= 4G OLD VS NEW =================
    if old_new_4g_df is not None:

        for _, row in old_new_4g_df.iterrows():

            old_cell = str(
                row.get("MV Cell Name_old", "")
            ).strip()

            new_cell = str(
                row.get("MV Cell Name_new", "")
            ).strip()

            old_site = str(
                row.get("Site Id_old", "")
            ).strip()

            new_site = str(
                row.get("Site Id_new", "")
            ).strip()

            lock_status = str(
                row.get("Lock Status", "")
            ).strip()

            # total unique new cells
            if new_cell != "":
                cells_set_4g.add(new_cell)

            # total sites
            if old_site != "":
                sites_set_4g.add(old_site)

            if new_site != "":
                sites_set_4g.add(new_site)

            # Both Locked
            if (
                old_cell != ""
                and new_cell != ""
                and lock_status == "Both Locked"
            ):

                both_locked_cells_4g.update(
                    [old_cell, new_cell]
                )

                both_locked_sites_4g.add(
                    (old_site, new_site)
                )

            # Both Unlocked
            elif (
                old_cell != ""
                and new_cell != ""
                and lock_status == "Both Unlocked"
            ):

                both_unlocked_cells_4g.update(
                    [old_cell, new_cell]
                )

                both_unlocked_sites_4g.add(
                    (old_site, new_site)
                )


    print("Total UNIQUE Cells 4G:", len(cells_set_4g))
    print("Both Locked Cells 4G:", len(both_locked_cells_4g))
    print("Both Unlocked Cells 4G:", len(both_unlocked_cells_4g))
    print("Both Locked Sites 4G:", len(both_locked_sites_4g))
    print("Both Unlocked Sites 4G:", len(both_unlocked_sites_4g))


    # ================= 5G OLD VS NEW =================
    if old_new_5g_df is not None:

        for _, row in old_new_5g_df.iterrows():

            old_cell = str(
                row.get("Cell Name_old", "")
            ).strip()

            new_cell = str(
                row.get("Cell Name_new", "")
            ).strip()

            old_site = str(
                row.get("Site Name_old", "")
            ).strip()

            new_site = str(
                row.get("Site Name_new", "")
            ).strip()

            lock_status = str(
                row.get("Lock Status", "")
            ).strip()

            # total unique new cells
            if new_cell != "":
                cells_set_5g.add(new_cell)

            # total sites
            if old_site != "":
                sites_set_5g.add(old_site)

            if new_site != "":
                sites_set_5g.add(new_site)

            # Both Locked
            if (
                old_cell != ""
                and new_cell != ""
                and lock_status == "Both Locked"
            ):

                both_locked_cells_5g.update(
                    [old_cell, new_cell]
                )

                both_locked_sites_5g.add(
                    (old_site, new_site)
                )

            # Both Unlocked
            elif (
                old_cell != ""
                and new_cell != ""
                and lock_status == "Both Unlocked"
            ):

                both_unlocked_cells_5g.update(
                    [old_cell, new_cell]
                )

                both_unlocked_sites_5g.add(
                    (old_site, new_site)
                )


    print("Total UNIQUE Cells 5G:", len(cells_set_5g))
    print("Both Locked Cells 5G:", len(both_locked_cells_5g))
    print("Both Unlocked Cells 5G:", len(both_unlocked_cells_5g))
    print("Both Locked Sites 5G:", len(both_locked_sites_5g))
    print("Both Unlocked Sites 5G:", len(both_unlocked_sites_5g))
    # ================= 4G UNIQUE NEW SITE =================
    total_sites_4g = set()

    if alarm_df is not None:

        for _, row in alarm_df.iterrows():

            status = str(
                row.get("4G Alarm Status", "")
            ).strip().lower()

            if status == "new site":

                site = row.get("SiteId", "")
                mrbts = row.get("MRBTS", "")

                if (
                    pd.notna(site)
                    and pd.notna(mrbts)
                ):

                    site = str(site).strip().upper()
                    mrbts = str(mrbts).strip().upper()

                    if (
                        site != ""
                        and mrbts != ""
                    ):
                        total_sites_4g.add(
                            (site, mrbts)
                        )

    print(
        "Total Unique NEW SITE 4G:",
        len(total_sites_4g)
    )
    # ================= 5G UNIQUE NEW SITE =================
    total_sites_5g = set()

    if alarm_df is not None:

        for _, row in alarm_df.iterrows():

            status = str(
                row.get("5G Alarm Status", "")
            ).strip().lower()

            if status == "new site":

                site = row.get("SiteId", "")
                nrbts = row.get("NRBTS", "")

                if (
                    pd.notna(site)
                    and pd.notna(nrbts)
                ):

                    site = str(site).strip().upper()
                    nrbts = str(nrbts).strip().upper()

                    if (
                        site != ""
                        and nrbts != ""
                    ):
                        total_sites_5g.add(
                            (site, nrbts)
                        )

    print(
        "Total Unique NEW SITE 5G:",
        len(total_sites_5g)
    )
    # ================= NO ALARM 4G (ONLY NEW SITE) =================
    No_Alarm_4G = 0

    if (
        "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms" in alarm_df.columns
        and "MRBTS" in alarm_df.columns
        and "4G Alarm Status" in alarm_df.columns
    ):

        No_Alarm_4G = alarm_df[
            (
                alarm_df[
                    "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms"
                ]
                .astype(str)
                .str.strip()
                == "No Alarms"
            )
            &
            (
                alarm_df["MRBTS"]
                .astype(str)
                .str.strip() != ""
            )
            &
            (
                alarm_df["4G Alarm Status"]
                .astype(str)
                .str.strip()
                == "New Site"
            )
        ]["SiteId"].nunique()


    # ================= NO ALARM 5G (ONLY NEW SITE) =================
    NO_Alarm_5G = 0

    if (
        "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms" in alarm_df.columns
        and "5G Alarms" in alarm_df.columns
        and "5G Alarm Status" in alarm_df.columns
    ):

        NO_Alarm_5G = alarm_df[
            (
                alarm_df[
                    "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms"
                ]
                .astype(str)
                .str.strip()
                == "No Alarms"
            )
            &
            (
                alarm_df["5G Alarms"]
                .astype(str)
                .str.strip() != ""
            )
            &
            (
                alarm_df["5G Alarm Status"]
                .astype(str)
                .str.strip()
                == "New Site"
            )
        ]["SiteId"].nunique()
    
    # ================= SITE DOWN 4G - NEW SITE =================
    site_down_4g_new = 0

    if (
        "Alarm Bucket" in alarm_df.columns
        and "MRBTS" in alarm_df.columns
        and "4G Alarm Status" in alarm_df.columns
    ):

        site_down_4g_new = alarm_df[
            (
                alarm_df["Alarm Bucket"]
                .astype(str)
                .str.contains(
                    "SITE DOWN",
                    case=False,
                    na=False
                )
            )
            &
            (
                alarm_df["MRBTS"]
                .astype(str)
                .str.strip() != ""
            )
            &
            (
                alarm_df["4G Alarm Status"]
                .astype(str)
                .str.strip()
                == "New Site"
            )
        ]["SiteId"].nunique()


    # ================= SITE DOWN 4G - OLD SITE =================
    site_down_4g_old = 0

    if (
        "Alarm Bucket" in alarm_df.columns
        and "MRBTS" in alarm_df.columns
        and "4G Alarm Status" in alarm_df.columns
    ):

        site_down_4g_old = alarm_df[
            (
                alarm_df["Alarm Bucket"]
                .astype(str)
                .str.contains(
                    "SITE DOWN",
                    case=False,
                    na=False
                )
            )
            &
            (
                alarm_df["MRBTS"]
                .astype(str)
                .str.strip() != ""
            )
            &
            (
                alarm_df["4G Alarm Status"]
                .astype(str)
                .str.strip()
                == "OLD Site"
            )
        ]["SiteId"].nunique()


    # ================= SITE DOWN 5G - NEW SITE =================
    site_down_5g_new = 0

    if (
        "Alarm Bucket" in alarm_df.columns
        and "5G Alarms" in alarm_df.columns
        and "5G Alarm Status" in alarm_df.columns
    ):

        site_down_5g_new = alarm_df[
            (
                alarm_df["Alarm Bucket"]
                .astype(str)
                .str.contains(
                    "SITE DOWN",
                    case=False,
                    na=False
                )
            )
            &
            (
                alarm_df["5G Alarms"]
                .astype(str)
                .str.strip() != ""
            )
            &
            (
                alarm_df["5G Alarm Status"]
                .astype(str)
                .str.strip()
                == "New Site"
            )
        ]["SiteId"].nunique()


    # ================= SITE DOWN 5G - OLD SITE =================
    site_down_5g_old = 0

    if (
        "Alarm Bucket" in alarm_df.columns
        and "5G Alarms" in alarm_df.columns
        and "5G Alarm Status" in alarm_df.columns
    ):

        site_down_5g_old = alarm_df[
            (
                alarm_df["Alarm Bucket"]
                .astype(str)
                .str.contains(
                    "SITE DOWN",
                    case=False,
                    na=False
                )
            )
            &
            (
                alarm_df["5G Alarms"]
                .astype(str)
                .str.strip() != ""
            )
            &
            (
                alarm_df["5G Alarm Status"]
                .astype(str)
                .str.strip()
                == "OLD Site"
            )
        ]["SiteId"].nunique()


    print("4G Site Down NEW:", site_down_4g_new)
    print("4G Site Down OLD:", site_down_4g_old)

    print("5G Site Down NEW:", site_down_5g_new)
    print("5G Site Down OLD:", site_down_5g_old)
    
    # ================= SA 4G (NEW SITE ONLY) =================
    sa_4g = 0

    if (
        "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms" in alarm_df.columns
        and "MRBTS" in alarm_df.columns
        and "4G Alarm Status" in alarm_df.columns
    ):

        sa_4g = alarm_df[
            (
                alarm_df[
                    "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms"
                ]
                .astype(str)
                .str.strip()
                == "SA"
            )
            &
            (
                alarm_df["MRBTS"]
                .astype(str)
                .str.strip() != ""
            )
            &
            (
                alarm_df["4G Alarm Status"]
                .astype(str)
                .str.strip()
                == "New Site"
            )
        ]["SiteId"].nunique()


    # ================= NSA 4G (NEW SITE ONLY) =================
    nsa_4g = 0

    if (
        "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms" in alarm_df.columns
        and "MRBTS" in alarm_df.columns
        and "4G Alarm Status" in alarm_df.columns
    ):

        nsa_4g = alarm_df[
            (
                alarm_df[
                    "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms"
                ]
                .astype(str)
                .str.strip()
                == "NSA"
            )
            &
            (
                alarm_df["MRBTS"]
                .astype(str)
                .str.strip() != ""
            )
            &
            (
                alarm_df["4G Alarm Status"]
                .astype(str)
                .str.strip()
                == "New Site"
            )
        ]["SiteId"].nunique()


    # ================= SA 5G (NEW SITE ONLY) =================
    sa_5g = 0

    if (
        "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms" in alarm_df.columns
        and "5G Alarms" in alarm_df.columns
        and "5G Alarm Status" in alarm_df.columns
    ):

        sa_5g = alarm_df[
            (
                alarm_df[
                    "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms"
                ]
                .astype(str)
                .str.strip()
                == "SA"
            )
            &
            (
                alarm_df["5G Alarms"]
                .astype(str)
                .str.strip() != ""
            )
            &
            (
                alarm_df["5G Alarm Status"]
                .astype(str)
                .str.strip()
                == "New Site"
            )
        ]["SiteId"].nunique()


    # ================= NSA 5G (NEW SITE ONLY) =================
    nsa_5g = 0

    if (
        "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms" in alarm_df.columns
        and "5G Alarms" in alarm_df.columns
        and "5G Alarm Status" in alarm_df.columns
    ):

        nsa_5g = alarm_df[
            (
                alarm_df[
                    "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms"
                ]
                .astype(str)
                .str.strip()
                == "NSA"
            )
            &
            (
                alarm_df["5G Alarms"]
                .astype(str)
                .str.strip() != ""
            )
            &
            (
                alarm_df["5G Alarm Status"]
                .astype(str)
                .str.strip()
                == "New Site"
            )
        ]["SiteId"].nunique()
        
    # ================= 4G SA Alarm Bucket (NEW SITE ONLY) =================
    hw_alarm_4g = 0
    soft_alarm_4g = 0

    if (
        "Alarm Bucket" in alarm_df.columns
        and "MRBTS" in alarm_df.columns
        and "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms" in alarm_df.columns
        and "4G Alarm Status" in alarm_df.columns
    ):

        sa_4g_df = alarm_df[
            (
                alarm_df[
                    "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms"
                ]
                .astype(str)
                .str.strip()
                .str.upper()
                == "SA"
            )
            &
            (
                alarm_df["MRBTS"]
                .astype(str)
                .str.strip()
                != ""
            )
            &
            (
                alarm_df["4G Alarm Status"]
                .astype(str)
                .str.strip()
                == "New Site"
            )
        ]

        site_alarm_map = {}

        for _, row in sa_4g_df.iterrows():

            site_id = str(
                row.get("SiteId", "")
            ).strip()

            alarm_bucket = str(
                row.get("Alarm Bucket", "")
            ).strip().upper()

            if not site_id:
                continue

            # Priority Logic
            if "HW ALARM" in alarm_bucket:
                site_alarm_map[site_id] = "HW"

            elif (
                "SOFT ALARM" in alarm_bucket
                and site_id not in site_alarm_map
            ):
                site_alarm_map[site_id] = "SOFT"

        hw_alarm_4g = sum(
            1 for v in site_alarm_map.values()
            if v == "HW"
        )

        soft_alarm_4g = sum(
            1 for v in site_alarm_map.values()
            if v == "SOFT"
        )
    # ================= 5G SA Alarm Bucket (NEW SITE ONLY) =================
    hw_alarm_5g = 0
    soft_alarm_5g = 0

    if (
        "Alarm Bucket" in alarm_df.columns
        and "5G Alarms" in alarm_df.columns
        and "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms" in alarm_df.columns
        and "5G Alarm Status" in alarm_df.columns
    ):

        sa_5g_df = alarm_df[
            (
                alarm_df[
                    "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms"
                ]
                .astype(str)
                .str.strip()
                .str.upper()
                == "SA"
            )
            &
            (
                alarm_df["5G Alarms"]
                .astype(str)
                .str.strip()
                != ""
            )
            &
            (
                alarm_df["5G Alarm Status"]
                .astype(str)
                .str.strip()
                == "New Site"
            )
        ]

        site_alarm_map = {}

        for _, row in sa_5g_df.iterrows():

            site_id = str(
                row.get("SiteId", "")
            ).strip()

            alarm_bucket = str(
                row.get("Alarm Bucket", "")
            ).strip().upper()

            if not site_id:
                continue

            # Priority Logic
            if "HW ALARM" in alarm_bucket:
                site_alarm_map[site_id] = "HW"

            elif (
                "SOFT ALARM" in alarm_bucket
                and site_id not in site_alarm_map
            ):
                site_alarm_map[site_id] = "SOFT"

        hw_alarm_5g = sum(
            1 for v in site_alarm_map.values()
            if v == "HW"
        )

        soft_alarm_5g = sum(
            1 for v in site_alarm_map.values()
            if v == "SOFT"
        )
    print("HW Alarm 4G:", hw_alarm_4g)
    print("Soft Alarm 4G:", soft_alarm_4g)

    print("HW Alarm 5G:", hw_alarm_5g)
    print("Soft Alarm 5G:", soft_alarm_5g)
    
    # ================= 4G CELL COUNT (NEW SITE) =================
    cells_count_4g = 0

    if cells_4g is not None:

        cells_count_4g = cells_4g[
            (
                cells_4g["4G Alarm Status"]
                .astype(str)
                .str.strip()
                .str.lower()
                == "new site"
            )
            &
            (
                cells_4g["MV Cell Name"]
                .astype(str)
                .str.strip() != ""
            )
        ]["MV Cell Name"].nunique()

    print("Total NEW SITE Cells 4G:", cells_count_4g)
    # ================= 5G CELL COUNT (NEW SITE) =================
    cells_count_5g = 0

    if cells_5g is not None:

        cells_count_5g = cells_5g[
            (
                cells_5g["5G Alarm Status"]
                .astype(str)
                .str.strip()
                .str.lower()
                == "new site"
            )
            &
            (
                cells_5g["Cell Name"]
                .astype(str)
                .str.strip() != ""
            )
        ]["Cell Name"].nunique()

    print("Total NEW SITE Cells 5G:", cells_count_5g)
    # ================= TOTAL LOCKED / UNLOCKED =================

    total_both_locked_cells = len(both_locked_cells_4g) + len(both_locked_cells_5g)
    total_both_unlocked_cells = len(both_unlocked_cells_4g) + len(both_unlocked_cells_5g)

    total_both_locked_sites = len(both_locked_sites_4g) + len(both_locked_sites_5g)
    total_both_unlocked_sites = len(both_unlocked_sites_4g) + len(both_unlocked_sites_5g)
    total_sites_locked_unlocked = total_both_locked_sites + total_both_unlocked_sites
    
    
    return {
        "total_4g_sites": len(total_sites_4g),
        "total_5g_sites": len(total_sites_5g),

        "Cells_4G": int(cells_count_4g),
        "Cells_5G": int(cells_count_5g),

        "no_alarm_4g": int(No_Alarm_4G),
        "no_alarm_5g": int(NO_Alarm_5G),

        # Site Down New / Old Separate
        "site_down_4g": int(site_down_4g_new),
        "old_down_4g": int(site_down_4g_old),

        "site_down_5g": int(site_down_5g_new),
        "old_down_5g": int(site_down_5g_old),

        # SA / NSA
        "sa_4g": int(sa_4g),
        "nsa_4g": int(nsa_4g),

        "sa_5g": int(sa_5g),
        "nsa_5g": int(nsa_5g),

        # HW / SOFT Alarm
        "hw_alarm_4g": int(hw_alarm_4g),
        "soft_alarm_4g": int(soft_alarm_4g),

        "hw_alarm_5g": int(hw_alarm_5g),
        "soft_alarm_5g": int(soft_alarm_5g),
        "Both_Locked_Cells": int(total_both_locked_cells),
        "Both_Unlocked_Cells": int(total_both_unlocked_cells),

        "Both_Locked_Sites": int(total_both_locked_sites),
        "Both_Unlocked_Sites": int(total_both_unlocked_sites),
        "Total_Locked_Unlocked_Sites": int(total_sites_locked_unlocked),

        "Total_No_of_Cells": int(cells_count_4g + cells_count_5g)

    }

    # # ================= 4G UNIQUE SITE COUNT =================
    # total_4g_sites = 0

    # if (
    #     "MRBTS" in alarm_df.columns
    #     and "SiteId" in alarm_df.columns
    # ):

    #     sites_4g = (
    #         alarm_df[
    #             alarm_df["MRBTS"]
    #             .astype(str)
    #             .str.strip()
    #             != ""
    #         ]["SiteId"]
    #         .astype(str)
    #         .str.strip()
    #     )

    #     total_4g_sites = sites_4g.nunique()

    # # ================= 5G UNIQUE SITE COUNT =================
    # total_5g_sites = 0

    # if (
    #     "5G Alarms" in alarm_df.columns
    #     and "SiteId" in alarm_df.columns
    # ):

    #     sites_5g = (
    #         alarm_df[
    #             alarm_df["5G Alarms"]
    #             .astype(str)
    #             .str.strip()
    #             != ""
    #         ]["SiteId"]
    #         .astype(str)
    #         .str.strip()
    #     )

    #     total_5g_sites = sites_5g.nunique()

    # print("Unique 4G Sites:", total_4g_sites)
    # print("Unique 5G Sites:", total_5g_sites)

    # No_Alarm_4G = 0
    # if (
    #     "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms" in alarm_df.columns
    #     and "MRBTS" in alarm_df.columns
    # ):
    #     No_Alarm_4G = alarm_df[
    #         (alarm_df["No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms"]
    #         .astype(str)
    #         .str.strip()
    #         == "No Alarms")
    #         &
    #         (alarm_df["MRBTS"].astype(str).str.strip() != "")
    #     ]["SiteId"].nunique()
        
    # NO_Alarm_5G = 0
    # if (
    #     "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms" in alarm_df.columns
    #     and "5G Alarms" in alarm_df.columns
    # ):
    #     NO_Alarm_5G = alarm_df[
    #         (alarm_df["No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms"]
    #         .astype(str)
    #         .str.strip() == "No Alarms")
    #         &
    #         (alarm_df["5G Alarms"].astype(str).str.strip() != "")
    #     ]["SiteId"].nunique()
        
    # site_down_4g = 0
    # if (
    #     "Alarm Bucket" in alarm_df.columns
    #     and "MRBTS" in alarm_df.columns
    # ):
    #     site_down_4g = alarm_df[
    #         (alarm_df["Alarm Bucket"].astype(str).str.contains("timeout", case=False, na=False))
    #         &
    #         (alarm_df["MRBTS"].astype(str).str.strip() != "")
    #     ]["SiteId"].nunique()
    
    # site_down_5g = 0
    # if (
    #     "Alarm Bucket" in alarm_df.columns
    #     and "5G Alarms" in alarm_df.columns
    # ):
    #     site_down_5g = alarm_df[
    #         (alarm_df["Alarm Bucket"].astype(str).str.contains("timeout", case=False, na=False))
    #         &
    #         (alarm_df["5G Alarms"].astype(str).str.strip() != "")
    #     ]["SiteId"].nunique()
        
    # sa_4g = 0
    # if (
    #     "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms" in alarm_df.columns
    #     and "MRBTS" in alarm_df.columns
    # ):
    #     sa_4g = alarm_df[
    #         (alarm_df["No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms"]
    #         .astype(str)
    #         .str.strip() == "SA")
    #         &
    #         (alarm_df["MRBTS"].astype(str).str.strip() != "")
    #     ]["SiteId"].nunique()
    
    # nsa_4g = 0
    # if (
    #     "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms" in alarm_df.columns
    #     and "MRBTS" in alarm_df.columns
    # ):
    #     nsa_4g = alarm_df[
    #         (alarm_df["No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms"]
    #         .astype(str)
    #         .str.strip() == "NSA")
    #         &
    #         (alarm_df["MRBTS"].astype(str).str.strip() != "")
    #     ]["SiteId"].nunique()
        
    # sa_5g = 0
    # if (
    #     "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms" in alarm_df.columns
    #     and "5G Alarms" in alarm_df.columns
    # ):
    #     sa_5g = alarm_df[
    #         (alarm_df["No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms"]
    #         .astype(str)
    #         .str.strip() == "SA")
    #         &
    #         (alarm_df["5G Alarms"].astype(str).str.strip() != "")
    #     ]["SiteId"].nunique()
        
    # nsa_5g = 0
    # if (
    #     "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms" in alarm_df.columns
    #     and "5G Alarms" in alarm_df.columns
    # ):
    #     nsa_5g = alarm_df[
    #         (alarm_df["No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms"]
    #         .astype(str)
    #         .str.strip() == "NSA")
    #         &
    #         (alarm_df["5G Alarms"].astype(str).str.strip() != "")
    #     ]["SiteId"].nunique()

    # # ================= 4G SA Alarm Bucket (Priority Based) =================
    # hw_alarm_4g = 0
    # soft_alarm_4g = 0

    # if (
    #     "Alarm Bucket" in alarm_df.columns
    #     and "MRBTS" in alarm_df.columns
    #     and "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms" in alarm_df.columns
    # ):

    #     sa_4g_df = alarm_df[
    #         (
    #             alarm_df[
    #                 "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms"
    #             ]
    #             .astype(str)
    #             .str.strip()
    #             .str.upper()
    #             == "SA"
    #         )
    #         &
    #         (
    #             alarm_df["MRBTS"]
    #             .astype(str)
    #             .str.strip()
    #             != ""
    #         )
    #     ]

    #     site_alarm_map = {}

    #     for _, row in sa_4g_df.iterrows():

    #         site_id = str(
    #             row.get("SiteId", "")
    #         ).strip()

    #         alarm_bucket = str(
    #             row.get("Alarm Bucket", "")
    #         ).strip().upper()

    #         if not site_id:
    #             continue

    #         # Priority Logic
    #         if "HW ALARM" in alarm_bucket:
    #             site_alarm_map[site_id] = "HW"

    #         elif (
    #             "SOFT ALARM" in alarm_bucket
    #             and site_id not in site_alarm_map
    #         ):
    #             site_alarm_map[site_id] = "SOFT"

    #     hw_alarm_4g = sum(
    #         1 for v in site_alarm_map.values()
    #         if v == "HW"
    #     )

    #     soft_alarm_4g = sum(
    #         1 for v in site_alarm_map.values()
    #         if v == "SOFT"
    #     )


    # # ================= 5G SA Alarm Bucket (Priority Based) =================
    # hw_alarm_5g = 0
    # soft_alarm_5g = 0

    # if (
    #     "Alarm Bucket" in alarm_df.columns
    #     and "5G Alarms" in alarm_df.columns
    #     and "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms" in alarm_df.columns
    # ):

    #     sa_5g_df = alarm_df[
    #         (
    #             alarm_df[
    #                 "No Alarms/Service Affecting Alarms/Non-Service Affecting Alarms"
    #             ]
    #             .astype(str)
    #             .str.strip()
    #             .str.upper()
    #             == "SA"
    #         )
    #         &
    #         (
    #             alarm_df["5G Alarms"]
    #             .astype(str)
    #             .str.strip()
    #             != ""
    #         )
    #     ]

    #     site_alarm_map = {}

    #     for _, row in sa_5g_df.iterrows():

    #         site_id = str(
    #             row.get("SiteId", "")
    #         ).strip()

    #         alarm_bucket = str(
    #             row.get("Alarm Bucket", "")
    #         ).strip().upper()

    #         if not site_id:
    #             continue

    #         # Priority Logic
    #         if "HW ALARM" in alarm_bucket:
    #             site_alarm_map[site_id] = "HW"

    #         elif (
    #             "SOFT ALARM" in alarm_bucket
    #             and site_id not in site_alarm_map
    #         ):
    #             site_alarm_map[site_id] = "SOFT"

    #     hw_alarm_5g = sum(
    #         1 for v in site_alarm_map.values()
    #         if v == "HW"
    #     )

    #     soft_alarm_5g = sum(
    #         1 for v in site_alarm_map.values()
    #         if v == "SOFT"
    #     )


    # print("HW Alarm 4G:", hw_alarm_4g)
    # print("Soft Alarm 4G:", soft_alarm_4g)

    # print("HW Alarm 5G:", hw_alarm_5g)
    # print("Soft Alarm 5G:", soft_alarm_5g)
    # return {
    #     "total_4g_sites": int(total_4g_sites),
    #     "total_5g_sites": int(total_5g_sites),
    #     "no_alarm_4g": int(No_Alarm_4G),
    #     "no_alarm_5g": int(NO_Alarm_5G),
    #     "site_down_4g": int(site_down_4g),
    #     "site_down_5g": int(site_down_5g),
    #     "sa_4g": int(sa_4g),
    #     "nsa_4g": int(nsa_4g),
    #     "sa_5g": int(sa_5g),
    #     "nsa_5g": int(nsa_5g),
    #     "hw_alarm_4g": int(hw_alarm_4g),
    #     "soft_alarm_4g": int(soft_alarm_4g),
    #     "hw_alarm_5g": int(hw_alarm_5g),
    #     "soft_alarm_5g": int(soft_alarm_5g),

    # }

def is_new_mail(unique_id):
    if not os.path.exists(LAST_PROCESSED_FILE):
        return True
    with open(LAST_PROCESSED_FILE, "r") as f:
        last_id = f.read().strip()
    return unique_id != last_id

def save_last_mail(unique_id):
    if not os.path.exists(os.path.dirname(LAST_PROCESSED_FILE)):
        os.makedirs(os.path.dirname(LAST_PROCESSED_FILE))
    with open(LAST_PROCESSED_FILE, "w") as f:
        f.write(unique_id)
 
@shared_task
def outlook_mail(expected_subject="Nokia Alarm"):
    # pythoncom.CoInitialize()
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.Folders.Item("Prerna.PramodKumar@ust.com").Folders["Inbox"]
 
    messages = inbox.Items
    messages.Sort("[ReceivedTime]", True)
    latest_mail = messages.GetFirst()
 
    if not latest_mail:
        return None
 
    unique_id = f"{latest_mail.Subject}|{latest_mail.SenderEmailAddress}|{latest_mail.ReceivedTime}"
    if not is_new_mail(unique_id):
        print("⚠️ Already processed this mail, skipping...")
        return None
 
    subject = str(latest_mail.Subject)
    print(f"Latest mail => {subject}")
 
    if expected_subject.lower() in subject.lower():
        if latest_mail.Attachments.Count > 0:
            # 🔹 Clean old attachments before saving new one-----
            if os.path.exists(save_directory):
                for old_file in os.listdir(save_directory):
                    old_path = os.path.join(save_directory, old_file)
                    if os.path.isfile(old_path):
                        os.remove(old_path)
                    elif os.path.isdir(old_path):
                        shutil.rmtree(old_path)
 
            for att in latest_mail.Attachments:
                if att.FileName.endswith((".zip", ".7z")):
                    if not os.path.exists(save_directory):
                        os.makedirs(save_directory)    
                    file_path = os.path.join(save_directory, att.FileName)
                    att.SaveAsFile(file_path)
                    print(" Zip downloaded:", file_path)
 
                    save_last_mail(unique_id)
                    process_daily_circle_logs(
                        file_path,
                        to_address=latest_mail.To,
                        cc_mails=latest_mail.CC,
                    )
 
                    return {
                        "file_path": file_path,
                        "to": latest_mail.To,
                        "cc": latest_mail.CC,
                        "subject": subject,
                        "received_time": str(latest_mail.ReceivedTime),
                    }
    return None

def process_daily_circle_logs(file_path, to_address=None, cc_mails=None):
    print("Processing Nokia Alarm ZIP...")

    output_root = os.path.join(MEDIA_ROOT, "NOKIA_OUTPUT")
    if os.path.exists(output_root):
        for item in os.listdir(output_root):
            # Skip attachments folder
            # if item == "attachments":
            # Don't delete important files/folders
            if item in ["attachments", "last_mail.txt"]:
                continue
                    
            item_path = os.path.join(output_root, item)
            try:
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                elif os.path.isfile(item_path):
                    os.remove(item_path)
            except Exception as e:
                print(f"Failed to delete {item_path}: {e}")

    extract_dir = os.path.splitext(file_path)[0]
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
    os.makedirs(extract_dir, exist_ok=True)
    if file_path.endswith(".zip"):
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)

    elif file_path.endswith(".7z"):
        with py7zr.SevenZipFile(file_path, mode="r") as z:
            z.extractall(extract_dir)

    print("ZIP Extracted:", extract_dir)

    mapping_file_path = None
    for root, dirs, files in os.walk(extract_dir):
        for file_name in files:
            lower_name = file_name.lower()
            if (
                "mapping" in lower_name
                and file_name.endswith((".xlsx", ".xls", ".csv"))
            ):
                mapping_file_path = os.path.join(root, file_name)
                break

    if not mapping_file_path:

        print("Mapping file not found")
        return
    print("Mapping File:", mapping_file_path)

    alarm_files = []
    for root, dirs, files in os.walk(extract_dir):
        for file_name in files:
            # skip mapping file
            if "mapping" in file_name.lower():
                continue
            if file_name.endswith((".csv", ".xlsx", ".xls")):
                file_path = os.path.join(root, file_name)
                alarm_files.append(file_path)
    print("Alarm Files Count:", len(alarm_files))
    if not alarm_files:
        print("No alarm files found")
        return

    files_payload = []
    # alarm files
    for alarm_path in alarm_files:
        files_payload.append(
            (
                "alarm_file",
                (
                    os.path.basename(alarm_path),
                    open(alarm_path, "rb")
                )
            )
        )

    # mapping file
    files_payload.append(
        (
            "mapping_file",
            (
                os.path.basename(mapping_file_path),
                open(mapping_file_path, "rb")
            )
        )
    )

    response = requests.post(
        "http://127.0.0.1:8001/daily_alarm/Nokia/",
        files=files_payload
    )
    print("API STATUS:", response.status_code)

    try:
        response_data = response.json()
        print(response_data)
    except Exception as e:
        print("Invalid response:", str(e))
        return
    
    if response.status_code == 200:

        print("Circle wise output generated")

        reply_subject = "📊 Nokia Alarm Output"
        circle_mail_map = {
            "MP": [
                "Ravikant.Vishwakarma@ust.com",
                "Giriraj.Soni@ust.com",
                "Himanshu.Lokhande@ust.com",
                "Santosh.Khare@ust.com",
                "Pradeep.SinghRajabat@ust.com",
                "Shubham.Mishra3@ust.com",
                "Kamal.Kishor@ust.com",
                "Rakesh.Jat@ust.com",
                "Deepak.Rathi1@ust.com",
                "TES_IN_PAG@UST.com",
                "TES_IN_SOFT_AT@UST.com",
                "Amit.Rai@ust.com",
                "Chandan.Kumar2@ust.com",
                "Shashank.Rai@ust.com"
            ],
            "BIH": [
                "Kundan.KumarSingh@ust.com",
                "Chandan.KumarSingh@ust.com",
                "Bipul.Ranjan@ust.com",
                "Vishnu.Singh@ust.com",
                "Avnish.Mishra@ust.com",
                "Sonu.Singh3@ust.com",
                "Neheru.Dalai@ust.com",
                "Ravi.Kumar4@ust.com",
                "Santosh.Kumar2@ust.com",
                "Gyan.Prakash2@ust.com",
                "Bharat.Kumar@ust.com",
                "Vikram.Thakur@ust.com",
                "Asish.Yadav@ust.com",
                "TES_IN_PAG@UST.com",
                "TES_IN_SOFT_AT@UST.com",
                "Amit.Rai@ust.com",
                "Chandan.Kumar2@ust.com",
                "Rahul.Kumar7@ust.com",
                "Shashank.Rai@ust.com"
            ],
            "JRK": [
                "Kundan.KumarSingh@ust.com",
                "Chandan.KumarSingh@ust.com",
                "Bipul.Ranjan@ust.com",
                "Vishnu.Singh@ust.com",
                "Avnish.Mishra@ust.com",
                "Sonu.Singh3@ust.com",
                "Neheru.Dalai@ust.com",
                "Ravi.Kumar4@ust.com",
                "Santosh.Kumar2@ust.com",
                "Gyan.Prakash2@ust.com",
                "Bharat.Kumar@ust.com",
                "Vikram.Thakur@ust.com",
                "Asish.Yadav@ust.com",
                "TES_IN_PAG@UST.com",
                "TES_IN_SOFT_AT@UST.com",
                "Amit.Rai@ust.com",
                "Chandan.Kumar2@ust.com",
                "Rahul.Kumar7@ust.com",
                "Shashank.Rai@ust.com"
            ],
            "UPE": [
                "Harsh.Srivastava@ust.com",
                "Anurag.Singh@ust.com",
                "Onkar.Sony@ust.com",
                "Rishabh.Singh@ust.com",
                "Saurabh.Verma@ust.com",
                "Rahul.Yadav2@ust.com",
                "Rakesh.Dubey@ust.com",
                "Shubham.Gupta2@ust.com",
                "Aditya.Kumar3@ust.com",
                "Shailesh.Srivastava@ust.com",
                "Ankush.Chauhan@ust.com",
                "TES_IN_PAG@UST.com",
                "TES_IN_SOFT_AT@UST.com",
                "Amit.Rai@ust.com",
                "Chandan.Kumar2@ust.com",
                "Rahul.Kumar7@ust.com",
                "PankajKumar.Nayak@ust.com",
                "Gaurav.KanwalSingh@ust.com",
                "Vineet.KumarSingh@ust.com",
                "MukeshKumar.Singh@ust.com",
                "Shailesh.Yadav@ust.com",
                "Shashank.Rai@ust.com"
            ],
            "ORI": [
                "Sanjeev.Das@ust.com",
                "Rakesh.Dora@ust.com",
                "Devi.Mohanty@ust.com",
                "Sarthak.Pasayat@ust.com",
                "Jayadeba.Pradhan@ust.com",
                "Bhaskar.Nayak@ust.com",
                "Bichitra.Mallik@ust.com",
                "NaliniPrasad.Pradhan@ust.com",
                "Biswaranjan.Jena@ust.com",
                "Bapuji.Sahoo@ust.com",
                "Sworajya.Behera@ust.com",
                "Piyush.Patri@ust.com",
                "TES_IN_PAG@UST.com",
                "TES_IN_SOFT_AT@UST.com",
                "Amit.Rai@ust.com",
                "Chandan.Kumar2@ust.com",
                "Shashank.Rai@ust.com"
            ],
            "MAH": [
                "Vikas.Ray@ust.com",
                "KalyanBhimrav.Shinde@ust.com",
                "GopalBhikan.Sonar@ust.com",
                "TES_IN_PAG@UST.com",
                "TES_IN_SOFT_AT@UST.com",
                "Amit.Rai@ust.com",
                "Chandan.Kumar2@ust.com",
                "Narender.Yadav@ust.com",
                "PayghanBhagwat.Bharat@ust.com",
                "Shashank.Rai@ust.com",
                "Deepak.Dubey@ust.com"
            ],
            "WB": [
                "Amit.Kumar4@ust.com",
                "Sushovan.Pal@ust.com",
                "Tanuj.Singh@ust.com",
                "Masud.Rana@ust.com",
                "TES_IN_PAG@UST.com",
                "TES_IN_SOFT_AT@UST.com",
                "Amit.Rai@ust.com",
                "Chandan.Kumar2@ust.com",
                "Shashank.Rai@ust.com",
                "DeependraSingh.Yadav@ust.com",
                "Amit.Hui@ust.com",
                "AkhileshKumar.Yadav@ust.com"
            ],
            "MUM": [
                "Rajkumar.Prajapati@ust.com",
                "Aman.Kashyap@ust.com",
                "Arvind.Verma@ust.com",
                "pramod.rane@ust.com",
                "Chandraveer.Goaswami@ust.com",
                "TES_IN_PAG@UST.com",
                "TES_IN_SOFT_AT@UST.com",
                "Amit.Rai@ust.com",
                "Chandan.Kumar2@ust.com",
                "Shashank.Rai@ust.com"
            ],
            # "MUM":[
            #     "Abhinav.Verma@ust.com",
            # ],
            # "UPE":[
            #     "Abhinav.Verma@ust.com",
            # ],
            # "WB":[
            #     "Abhinav.Verma@ust.com",
            # ],
            # "MAH":[
            #     "Abhinav.Verma@ust.com",
            # ],
            # "ORI":[
            #     "Abhinav.Verma@ust.com",
            # ],
            # "JRK":[
            #     "Abhinav.Verma@ust.com",
            # ]
        }

        body = (
            "Hi Team,\n\n"
            "PFA Nokia Alarm Circle Wise Output.\n\n"
            "Regards,\n"
            "Developer Team\n"
            "(Automated Mail)"
        )
        

        # to_address = ';'.join([
        #     # "Abhinav.Verma@ust.com",
        #     # "Shashank.Rai@ust.com",
        #     # "Gaurav.KanwalSingh@ust.com",
        #     # "Varun.Sharma@ust.com",
        #     # "Amit.Rai@ust.com",
        #     # "Mohit.Batra@ust.com"
            
        #     "MP":["Ravikant.Vishwakarma@ust.com";"Giriraj.Soni@ust.com"]
        #     "BIH":["Kundan.KumarSingh@ust.com","Chandan.KumarSingh@ust.com","Bipul.Ranjan@ust.com"]
        #     "JRK":["Kundan.KumarSingh@ust.com","Chandan.KumarSingh@ust.com","Bipul.Ranjan@ust.com"]
        #     "UPE":["Harsh.Srivastava@ust.com","Anurag.Singh@ust.com"]
        #     "ORI":["Sanjeev.Das@ust.com","Rakesh.Dora@ust.com"]
        #     "JRK":["Kundan.KumarSingh@ust.com","Chandan.KumarSingh@ust.com","Bipul.Ranjan@ust.com"]
        #     "JRK":["Kundan.KumarSingh@ust.com","Chandan.KumarSingh@ust.com","Bipul.Ranjan@ust.com"]
            
            
        # ])

        # cc_mails = ';'.join([
        #     ""
        # ])

        # Root folder where circle files are saved
        nokia_output_root = os.path.join(
            MEDIA_ROOT,
            "NOKIA_OUTPUT",
            "OUTPUT"
        )

        # Loop through circle folders
        for circle in os.listdir(nokia_output_root):

            circle_path = os.path.join(
                nokia_output_root,
                circle
            )

            # skip files like attachments, txt
            if not os.path.isdir(circle_path):
                continue

            # find excel in circle folder
            for file in os.listdir(circle_path):

                if file.endswith(".xlsx"):

                    excel_path = os.path.join(
                        circle_path,
                        file
                    )

                    circle_key = circle.upper().strip()

                    to_address = ";".join(
                        circle_mail_map.get(circle_key, [])
                    )
                    cc_mails = ';'.join([
                        # "TES_IN_NH@UST.com",
                                ])

                    if not to_address:
                        print(f"No mail mapping found for {circle}")
                        continue

                    print(f"Sending mail for {circle}")
                    
                    # ================= SUMMARY =================
                    summary_data = get_summary_counts(
                        excel_path
                    )

                    # ================= TEMPLATE =================
                    template_dir = os.path.join(
                        MEDIA_ROOT,
                        "template"
                    )

                    env = Environment(
                        loader=FileSystemLoader(template_dir)
                    )

                    template = env.get_template(
                        "alarm_mailbody.html"
                    )

                    html_body = template.render(
                        # circle=circle,
                        brand="Nokia",
                        circle_name=circle.upper(),
                        generated_time=datetime.now().strftime(
                            "%d-%b-%Y %I:%M %p"
                        ),
                        # ================= TOTAL SITES =================
                        total_4g_sites=summary_data.get(
                            "total_4g_sites", 0
                        ),
                        total_5g_sites=summary_data.get(
                            "total_5g_sites", 0
                        ),

                        # ================= TOTAL CELLS =================
                        Cells_4G=summary_data.get(
                            "Cells_4G", 0
                        ),

                        Cells_5G=summary_data.get(
                            "Cells_5G", 0
                        ),

                        Total_No_of_Cells=summary_data.get(
                            "Total_No_of_Cells", 0
                        ),

                        # ================= NO ALARM =================
                        no_alarm_4g=summary_data.get(
                            "no_alarm_4g", 0
                        ),
                        no_alarm_5g=summary_data.get(
                            "no_alarm_5g", 0
                        ),

                        # ================= SITE DOWN =================
                        site_down_4g=summary_data.get(
                            "site_down_4g", 0
                        ),
                        old_down_4g=summary_data.get(
                            "old_down_4g", 0
                        ),

                        site_down_5g=summary_data.get(
                            "site_down_5g", 0
                        ),
                        old_down_5g=summary_data.get(
                            "old_down_5g", 0
                        ),

                        # ================= SA / NSA =================
                        sa_4g=summary_data.get(
                            "sa_4g", 0
                        ),
                        nsa_4g=summary_data.get(
                            "nsa_4g", 0
                        ),

                        sa_5g=summary_data.get(
                            "sa_5g", 0
                        ),
                        nsa_5g=summary_data.get(
                            "nsa_5g", 0
                        ),

                        # ================= HW / SOFT =================
                        hw_alarm_4g=summary_data.get(
                            "hw_alarm_4g", 0
                        ),
                        soft_alarm_4g=summary_data.get(
                            "soft_alarm_4g", 0
                        ),

                        hw_alarm_5g=summary_data.get(
                            "hw_alarm_5g", 0
                        ),
                        soft_alarm_5g=summary_data.get(
                            "soft_alarm_5g", 0
                        ),
                        # ================= LOCK / UNLOCK =================
                        Both_Locked_Cells=summary_data.get(
                            "Both_Locked_Cells", 0
                        ),

                        Both_Unlocked_Cells=summary_data.get(
                            "Both_Unlocked_Cells", 0
                        ),

                        Both_Locked_Sites=summary_data.get(
                            "Both_Locked_Sites", 0
                        ),

                        Both_Unlocked_Sites=summary_data.get(
                            "Both_Unlocked_Sites", 0
                        ),

                        Total_Locked_Unlocked_Sites=summary_data.get(
                            "Total_Locked_Unlocked_Sites", 0
                        )
                    )

                    # inline css for email
                    html_body = transform(
                        html_body
                    )

                    # ================= SEND EMAIL =================
                    send_email.delay(
                        to_address=to_address,
                        cc_mails=cc_mails,
                        subject=f"{reply_subject} - {circle}",
                        body=html_body,
                        attachment_path=excel_path,
                        is_html=True,
                    )
                    
                    print(f"✅ Mail Sent for Circle => {circle}")
