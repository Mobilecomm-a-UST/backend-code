import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import (
    PatternFill,
    Font,
    Alignment,
    Border,
    Side
)
from openpyxl.utils import get_column_letter
import re


def create_config_report(output_path, data):

    wb = Workbook()
    ws = wb.active
 

    # Header
    header_fill = PatternFill(
        start_color="1F4E78",
        end_color="1F4E78",
        fill_type="solid"
    )

    header_font = Font(
        color="FFFFFF",
        bold=True,
        name="Calibri",
        size=10
    )

    # Alternate rows
    stripe_fill = PatternFill(
        start_color="F3F6F8",
        end_color="F3F6F8",
        fill_type="solid"
    )

    # NA cells
    yellow_fill = PatternFill(
        start_color="FFD966",
        end_color="FFD966",
        fill_type="solid"
    )

    # OK
    ok_fill = PatternFill(
        start_color="00B050",
        end_color="00B050",
        fill_type="solid"
    )

    ok_font = Font(
        color="000000",
        name="Calibri",
        bold=True,
        size=10
    )

    # NOT OK
    notok_fill = PatternFill(
        start_color="E43C3C",
        end_color="E43C3C",
        fill_type="solid"
    )

    notok_font = Font(
        color="000000",
        name="Calibri",
        bold=True,
        size=10
    )

    # Fonts
    normal_font = Font(
        name="Calibri",
        size=10
    )

    first_col_font = Font(
  
        name="Calibri",
        size=10
    )

    center = Alignment(
        horizontal="center",
        vertical="center"
    )


    thin = Side(style="thin", color="D9D9D9")

    border = Border(
        left=thin,
        right=thin,
        top=thin,
        bottom=thin
    )

    num_cols = len(data[0])

   
    for col_idx, header in enumerate(data[0], 1):

        cell = ws.cell(
            row=1,
            column=col_idx,
            value=header
        )

        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center
        cell.border = border

    ws.row_dimensions[1].height = 25

    # Freeze Header
    ws.freeze_panes = "A2"

    for row_idx, row_data in enumerate(data[1:], 2):

        for col_idx, value in enumerate(row_data, 1):

            cell = ws.cell(
                row=row_idx,
                column=col_idx,
                value=value
            )

            cell.alignment = center
            cell.border = border

       
            if row_idx % 2 == 0:
                cell.fill = stripe_fill

            if col_idx == 1:
                cell.font = first_col_font
            else:
                cell.font = normal_font

  
            if col_idx == num_cols:

                status = str(value).strip().upper()

                if status == "OK":
                    cell.fill = ok_fill
                    cell.font = ok_font

                elif status == "NOT OK":
                    cell.fill = notok_fill
                    cell.font = notok_font

                elif status == "NOT FOUND":
                    cell.fill = notok_fill
                    cell.font = notok_font    

            if str(value).strip().upper() == "NA":
                cell.fill = yellow_fill

        ws.row_dimensions[row_idx].height = 20

    for col in ws.columns:

        max_length = 0
        column_letter = get_column_letter(col[0].column)

        for cell in col:
            try:
                if cell.value is not None:
                    max_length = max(
                        max_length,
                        len(str(cell.value))
                    )
            except:
                pass

        ws.column_dimensions[column_letter].width = max_length + 4

    wb.save(output_path)


def normalize_value(v):
    if pd.isna(v):
        return ""

    v = str(v).strip().lower()

    if v in ["true", "1"]:
        return "1"

    if v in ["false", "0"]:
        return "0"

    return v


def check_status(actual, expected):

    if pd.isna(actual):
        actual = ""

    if pd.isna(expected):
        expected = ""

    # -------- Actual values --------
    actual_values = set()

    for val in re.split(r"[;,]", str(actual)):
        val = val.strip().lower()

        if not val:
            continue

        if val in ["true", "1"]:
            actual_values.update(["true", "1"])

        elif val in ["false", "0"]:
            actual_values.update(["false", "0"])

        else:
            actual_values.add(val)

    # -------- Expected values --------
    expected_values = set()

    for item in re.split(r"[,;]", str(expected)):

        item = item.strip()

        if not item:
            continue

        # Remove TDD: / FDD:
        if ":" in item:
            val = item.split(":", 1)[1].strip()
        else:
            val = item

        val = val.lower()

        if val in ["true", "1"]:
            expected_values.update(["true", "1"])

        elif val in ["false", "0"]:
            expected_values.update(["false", "0"])

        else:
            expected_values.add(val)

    # Match if at least one value matches
    if actual_values.intersection(expected_values):
        return "OK"

    return "NOT OK"


parameter_map = {
    "actCoMp": "fixedULCoMp",
    "actDLCAggr": "TRUE",
    "actFlexScellSelect": "TRUE",
    "actTtiBundling": "TDD:0, FDD:1",
    "actDlMuMimo": "1",
    "actFastMimoSwitch": "1",
    "actMMimo": "1",
    "actUlMuMimo": "1",
    "actUlpcMethod": "TDD:PuschCLSrsPucchCL, FDD:PuschIAwPucchCL",
    "actVoipCovBoostEnh": "TDD:off, FDD:on_ttib_entry_PHR_based",
    "dlCaMinPcellCqiQci1": "0",
    "harqMaxTrUlTtiBundling": "20",
    "ttibOperMode": "sinrBasedNotWithMeasGap",
    "ulsSchedMethod": "TDD:channelaware, FDD:interference aware",
    "b2Threshold2RssiGERANQci1": "15",
    "qrxlevmin": "-124",
    "dlRsBoost": "0dB",
    "actLBPowerSaving": "1",
    "lbpsLastCellMinLoad": "40",
    "lbpsLastCellRTXMinLoad": "40",
    "lbpsLastCellSOEnabled": "0",
    "lbpsMaxLoad": "60",
    "lbpsMinLoad": "40",
    "lbpsPdcchLoadOffset": "20",
    "lbpsRTXCellCapOffset": "50",
    "lbpsRTXMaxLoad": "60",
    "lbpsRTXMinLoad": "40",
    "mdtxPdcchSymb": "1",
    "lbpsDayOfWeek": "Sun;Mon;Tue;Wed;Thu;Fri;Sat",
    "lbpsDuration": "360;360;360;360;360;360;360",
    "lbpsStartTimeHour": "0;0;0;0;0;0;0",
    "lbpsStartTimeMinute": "0;0;0;0;0;0;0",
    "lbpsSuspended": "notSuspended",
    "actRadioFanFailureEarlyNotif": "true",
    "rrcGuardTimer":"60",
    "validate_ntp": "The NTP IP should be present inside the reference sheet and it should match with the XML data.",
    "ntpStatus": "Available",
    "mdtxAggressiveness":"8",
    "actAutoPucchAllo":"1",
    "actMicroDtx":"1",
    "actAutoPucchAlloc":"FDD:1,TDD:0",
    "allowTrafficConcentration":"1"
}

master_parameters = [
    "actAutoPucchAlloc",
    "actCoMp",
    "actDLCAggr",
    "actDlMuMimo",
    "actFastMimoSwitch",
    "actFlexScellSelect",
    "actLBPowerSaving",
    "actMMimo",
    "actMicroDtx",
    "actRadioFanFailureEarlyNotif",
    "actTtiBundling",
    "actUlpcMethod",
    "actVoipCovBoostEnh",
    "allowTrafficConcentration",
    "b2Threshold2RssiGERANQci1",
    "dlCaMinPcellCqiQci1",
    "dlRsBoost",
    "harqMaxTrUlTtiBundling",
    "lbpsDayOfWeek",
    "lbpsDuration",
    "lbpsLastCellMinLoad",
    "lbpsLastCellRTXMinLoad",
    "lbpsLastCellSOEnabled",
    "lbpsMaxLoad",
    "lbpsMinLoad",
    "lbpsPdcchLoadOffset",
    "lbpsRTXCellCapOffset",
    "lbpsRTXMaxLoad",
    "lbpsRTXMinLoad",
    "lbpsStartTimeHour",
    "lbpsStartTimeMinute",
    "lbpsSuspended",
    "mdtxAggressiveness",
    "mdtxPdcchSymb",
    "qrxlevmin",
    "rrcGuardTimer",
    "ttibOperMode",
    "ulsSchedMethod",
]