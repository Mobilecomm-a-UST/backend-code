import re
import time

import pandas as pd
def process_log(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as f:
        content = f.read()
    


# ===============================
# Split log into NE sections
# ===============================
    ne_dict = {}

    matches = re.finditer(
        r'([^\s>]+)>\s*(.*?)(?=[^\s>]+>\s*|\Z)',
        content,
        re.DOTALL
    )

    for m in matches:
        ne = m.group(1).strip()

        ne_dict.setdefault(ne, "")
        ne_dict[ne] += "\n" + m.group(2)

    ne_sections = list(ne_dict.items())

        # ===============================
    # Cell extraction Block
    # ===============================
    cells = []

    for ne_name, ne_content in ne_sections:

        cell_pattern = re.findall(
            r'(\d+)\s+'
            r'(\d+)\s+\(([^)]+)\)\s+'
            r'(\d+)\s+\(([^)]+)\)\s+'
            r'GNBDUFunction=\d+,NRCellDU=([^\n]+)',
            ne_content,
            re.IGNORECASE
        )

        for proxy, adm_num, admin, opr_num, oper, cell_name in cell_pattern:

            cells.append([
                ne_name,
                cell_name.strip(),
                admin.strip(),
                oper.strip()
            ])

    cell_df = pd.DataFrame(
        cells,
        columns=[
            "NE Name",
            "Cell",
            "AdminState",
            "OperState"
        ]
    ).drop_duplicates()

    # ===============================
    # Extract RIM Parameters
    # ===============================
    rim_rows = []

    for ne_name, ne_content in ne_sections:

        current_cell = None

        rim_location = {}
        rim_pdsch = {}

        for line in ne_content.splitlines():

            line = line.strip()

            m = re.search(
                r'NRCellDU=([^,\s]+)',
                line,
                re.I
            )

            if m:
                current_cell = m.group(1)

            m = re.search(
                r'rimLocationEnabled\s+(\S+)',
                line,
                re.I
            )

            if m and current_cell:
                rim_location[current_cell] = (
                    m.group(1).lower()
                )

            m = re.search(
                r'rimPdschSlotBlankMode\s+(\S+)',
                line,
                re.I
            )

            if m and current_cell:
                rim_pdsch[current_cell] = (
                    m.group(1)
                )

        all_cells = (
            set(rim_location)
            |
            set(rim_pdsch)
        )

        for cell in all_cells:

            rim_rows.append([
                ne_name,
                cell,
                rim_pdsch.get(cell, ""),
                rim_location.get(cell, "")
            ])

    rim_df = pd.DataFrame(
        rim_rows,
        columns=[
            "NE Name",
            "Cell",
            "rimPdschSlotBlankMode",
            "rimLocationEnabled"
        ]
    ).drop_duplicates()

    print("\n===== RIM RAW VALUES =====")

    for ne in rim_df["NE Name"].unique():

        temp = rim_df[rim_df["NE Name"] == ne]

        print(f"\nNE : {ne}")

        print(temp[
            [
                "Cell",
                "rimPdschSlotBlankMode",
                "rimLocationEnabled"
            ]
        ].to_string(index=False))

    # ===============================
    # Extract AMF Status from "st amf"
    # ===============================
    amf_list = []

    amf_sections = list(
        re.finditer(
            r'([^\s>]+)>\s*st\s+amf(.*?)(?=[^\s>]+>\s*(?:st|alt)|\Z)',
            content,
            re.DOTALL | re.IGNORECASE
        )
    )

    for section in amf_sections:

        ne_name = section.group(1).strip()
        amf_content = section.group(2)

        print(f"\n===== DEBUG AMF BLOCK : {ne_name} =====")
        print(amf_content[:500])     # Remove later after validation

        amf_pattern = re.findall(
            r'(\d+)\s+'                      # Proxy
            r'(\d+)\s+\(([^)]+)\)\s+'        # Admin State
            r'(\d+)\s+\(([^)]+)\)\s+'        # Oper State
            r'GNBCUCPFunction=\d+,TermPointToAmf=([^\n]+)',
            amf_content,
            re.IGNORECASE
        )

        for proxy, adm_num, admin, opr_num, oper, amf_id in amf_pattern:

            amf_list.append([
                ne_name,
                amf_id.strip(),
                admin.strip(),
                oper.strip()
            ])

    amf_df = pd.DataFrame(
        amf_list,
        columns=[
            "NE Name",
            "AMF",
            "AdminState",
            "OperState"
        ]
    ).drop_duplicates()



    # ===============================
    # Extract Features
    # ===============================
    # ===============================
    # Extract Features with KeyId
    # ===============================

    # ===============================
    # Extract Features with NE Name
    # ===============================
    features = []

    for ne_name, ne_content in ne_sections:

        feature_pattern = re.findall(
            r'description\s+([^\n]+).*?'
            r'featureState\s+(\d+\s+\([^)]+\)).*?'
            r'featureStateId\s+([^\n]+).*?'
            r'keyId\s+([^\n]+).*?'
            r'licenseState\s+(\d+\s+\([^)]+\)).*?'
            r'serviceState\s+(\d+\s+\([^)]+\))',
            ne_content,
            re.DOTALL
        )

        for (
            feature_name,
            feature_state,
            feature_state_id,
            key_id,
            license_state,
            service_state
        ) in feature_pattern:

            features.append([
                ne_name,
                feature_name.strip(),
                feature_state.strip(),
                feature_state_id.strip(),
                key_id.strip(),
                license_state.strip(),
                service_state.strip()
            ])

    feature_df = pd.DataFrame(
        features,
        columns=[
            "NE Name",
            "Feature",
            "FeatureState",
            "FeatureStateId",
            "KeyId",
            "LicenseState",
            "ServiceState"
        ]
    ).drop_duplicates()


    # Extract SD count per MO Class
    # ===============================

    sd_summary = []

    mo_classes = ["NRCellDU", "NRCellCU", "GNBCUUPFunction"]

    for mo_class in mo_classes:

        # Extract the block corresponding to each MO
        pattern = (
            rf'{mo_class}=[^\n]+.*?sNSSAIList.*?'
            rf'(?=(?:NRCellDU=|NRCellCU=|GNBCUUPFunction=|^[^\s].*>|$))'
        )

        mo_blocks = re.findall(
            pattern,
            content,
            re.DOTALL | re.MULTILINE
        )

        sd_values = []

        for block in mo_blocks:
            # Capture SD values inside the block
            sd_values.extend(
                re.findall(
                    r'\bsd\s*=?\s*(\d+)',
                    block,
                    re.IGNORECASE
                )
            )

    

    # ===============================
    # Extract Site ID
    # ===============================

    print("\n===== NEs FOUND =====")

    for ne_name, _ in ne_sections:
        print(ne_name)

    # ===============================
    # Extract Network Slicing per NE
    # ===============================

    sd_summary = []

    mo_classes = ["NRCellDU", "NRCellCU", "GNBCUUPFunction"]

    for ne_name, ne_content in ne_sections:

        for mo_class in mo_classes:

            sd_values = []

            # Capture MO blocks
            mo_blocks = re.findall(
                rf'({mo_class}=[^\n]+.*?)(?='
                rf'NRCellDU=|'
                rf'NRCellCU=|'
                rf'GNBCUUPFunction=|'
                rf'[^\s>]+>\s*(?:st|alt)|'
                rf'\Z)',
                ne_content,
                re.DOTALL | re.IGNORECASE
            )

            for block in mo_blocks:

                # Locate sNSSAIList within the MO block
                snssai_match = re.search(
                    r'sNSSAIList.*?(?=\n\S|\Z)',
                    block,
                    re.DOTALL | re.IGNORECASE
                )

                if snssai_match:

                    sd_values.extend(
                        re.findall(
                            r'\bsd\s*=?\s*(\d+)',
                            snssai_match.group(),
                            re.IGNORECASE
                        )
                    )

            # Remove duplicate SD values
            unique_sd = sorted(set(sd_values), key=int)

            # Skip entries having No_of_SD = 0
            if len(unique_sd) > 0:
                sd_summary.append([
                    ne_name,
                    mo_class,
                    len(unique_sd),
                    ", ".join(unique_sd)
                ])

    # Create DataFrame
    sd_df = pd.DataFrame(
        sd_summary,
        columns=[
            "NE Name",
            "MO Class",
            "No_of_SD",
            "SD_Values"
        ]
    )

    print("\n===== NETWORK SLICING =====")
    print(sd_df.to_string(index=False))

    # ===============================
    # Extract Alarms with NE Name
    # ===============================
    severity_map = {
        "C": "Critical",
        "M": "Major",
        "m": "Minor",
        "w": "Warning"
    }

    alarms = []

    alt_sections = re.findall(
        r'([^\s>]+)>\s*alt(.*?)(?=(?:[^\s>]+>\s*alt|$))',
        content,
        re.DOTALL
    )

    for ne_name, alt_content in alt_sections:

        alarm_pattern = re.findall(
            r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+'
            r'([CMwm])\s+'
            r'(.+?)\s{2,}'
            r'(.+?)(?:\(|$)',
            alt_content
        )

        for date, severity, alarm, mo in alarm_pattern:

            alarms.append([
                ne_name.strip(),
                date.strip(),
                severity_map.get(severity, severity),
                alarm.strip(),
                mo.strip()
            ])

    alarm_df = pd.DataFrame(
        alarms,
        columns=[
            "NE Name",
            "Date",
            "Severity",
            "Alarm",
            "MO"
        ]
    ).drop_duplicates()

    # ===============================
    # Extract License Key Fault Alarm from altk
    # ===============================
    altk_alarms = []

    altk_sections = re.findall(
        r'([^\s>]+)>\s*altk(.*?)(?=(?:[^\s>]+>\s*altk|[^\s>]+>\s*(?:st|alt)|$))',
        content,
        re.DOTALL | re.IGNORECASE
    )

    for ne_name, altk_content in altk_sections:

        if re.search(
            r'license\s+key\s+file\s+fault',
            altk_content,
            re.IGNORECASE
        ):
            altk_alarms.append(ne_name.strip())

    # Unique NEs having License Key File Fault
    license_fault_nes = set(altk_alarms)

    print("\n===== LICENSE KEY FILE FAULT =====")

    if license_fault_nes:
        for ne in license_fault_nes:
            print(f"{ne} : License Key File Fault Found")
    else:
        print("No License Key File Fault Found")

    # ===============================
    # Summary
    # ===============================
    print("\n===== SITE SUMMARY =====")
    print(f"Total Cells      : {len(cell_df)}")
    print(f"Total AMFs       : {len(amf_df)}")
    print(f"Active Features  : {len(feature_df)}")
    print(f"Active Alarms    : {len(alarm_df)}")

    print("\n===== CELL STATUS =====")
    print(cell_df)

    print("\n===== AMF STATUS =====")
    print(amf_df)

    print("\n===== ACTIVE ALARMS =====")
    print(alarm_df)

    print("\n===== RIM DEBUG =====")

    for ne_name, ne_content in ne_sections:

        print("\nNE =", ne_name)

        print(
            "rimLocationEnabled found:",
            "rimLocationEnabled" in ne_content
        )

        print(
            "rimPdschSlotBlankMode found:",
            "rimPdschSlotBlankMode" in ne_content
        )

    print("\nRIM DF:")
    print(rim_df.to_string(index=False))


    # ===============================
    # Export Excel
    # ===============================
    output_file = f"media/reports/report_{int(time.time())}.xlsx"

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:

        cell_df.to_excel(
            writer,
            sheet_name="Cells",
            index=False
        )

        rim_df.to_excel(
            writer,
            sheet_name="RIM",
            index=False
        )

        amf_df.to_excel(
            writer,
            sheet_name="AMF",
            index=False
        )

        feature_df.to_excel(
            writer,
            sheet_name="Features",
            index=False
        )

        alarm_df.to_excel(
            writer,
            sheet_name="Alarms",
            index=False
        )

        sd_df.to_excel(
            writer,
            sheet_name="Network_Slicing",
            index=False
        )

    print(f"\nReport Generated: {output_file}")

    summary_data = []

    # Get unique NE Names
    unique_ne_names = sorted(
        set(cell_df["NE Name"])
        | set(amf_df["NE Name"])
        | set(feature_df["NE Name"])
        | set(sd_df["NE Name"])  
        | set(rim_df["NE Name"]) 
    ) 

    for ne_name in unique_ne_names:
        # --------------------------------
        # Cells Status
        # --------------------------------
        ne_cells = cell_df[cell_df["NE Name"] == ne_name]

        if len(ne_cells) > 0:
            cell_status = (
                "OK"
                if ne_cells["OperState"]
                .astype(str)
                .str.upper()
                .eq("ENABLED")
                .all()
                else "Not OK"
            )
        else:
            cell_status = "Not OK"

        summary_data.append([
            ne_name,
            "Cells",
            cell_status
        ])

    # --------------------------------
        # RIM Status
        # --------------------------------
        ne_rim = rim_df[
            rim_df["NE Name"] == ne_name
        ]

        if not ne_rim.empty:

            rim_status = (
                "OK"
                if (
                    ne_rim["rimPdschSlotBlankMode"]
                    .astype(str)
                    .str.strip()
                    .eq("4")
                    .all()
                    and
                    ne_rim["rimLocationEnabled"]
                    .astype(str)
                    .str.strip()
                    .str.lower()
                    .eq("true")
                    .all()
                )
                else "Not OK"
            )

        else:
            rim_status = "Not OK"

        summary_data.append([
            ne_name,
            "RIM",
            rim_status
        ])



        # --------------------------------
        # AMF Status
        # --------------------------------
        ne_amf = amf_df[amf_df["NE Name"] == ne_name]

        if len(ne_amf) > 0:
            amf_status = (
                "OK"
                if ne_amf["OperState"]
                .astype(str)
                .str.upper()
                .eq("ENABLED")
                .all()
                else "Not OK"
            )
        else:
            amf_status = "Not OK"

        summary_data.append([
            ne_name,
            "AMF",
            amf_status
        ])

        # --------------------------------
        # Features Status
        # --------------------------------
        ne_feature = feature_df[
            feature_df["NE Name"] == ne_name
        ]

        if len(ne_feature) > 0:

            feature_ok = (
                ne_feature["FeatureState"]
                .astype(str)
                .str.startswith("1")
                .all()
            )

            license_ok = (
                ne_feature["LicenseState"]
                .astype(str)
                .str.startswith("1")
                .all()
            )

            feature_status = (
                "OK"
                if feature_ok and license_ok
                else "Not OK"
            )

        else:
            feature_status = "Not OK"

        summary_data.append([
            ne_name,
            "Features",
            feature_status
        ])

        # --------------------------------
        # Network Slicing Status
        # --------------------------------
        ne_sd = sd_df[
            sd_df["NE Name"] == ne_name
        ]

        required_mos = [
            "NRCellDU",
            "NRCellCU",
            "GNBCUUPFunction"
        ]

        network_ok = True

        for mo in required_mos:

            mo_df = ne_sd[
                ne_sd["MO Class"] == mo
            ]

            if mo_df.empty:
                network_ok = False
                break

            if not mo_df["No_of_SD"].eq(4).all():
                network_ok = False
                break

        summary_data.append([
            ne_name,
            "Network_Slicing",
            "OK" if network_ok else "Not OK"
        ])

    # --------------------------------
        # License Key Alarm Status
        # --------------------------------
        alarm_status = (
            "Not OK"
            if ne_name in license_fault_nes
            else "OK"
        )

        summary_data.append([
            ne_name,
            "Alarm",
            alarm_status
        ])

    # --------------------------------
    # Create Summary DataFrame
    # --------------------------------
    summary_df = pd.DataFrame(
        summary_data,
        columns=[
            "NE Name",
            "Check",
            "Status"
        ]
    )

    # ===============================
    # Final Status per NE
    # ===============================
    final_status = []

    for ne_name in sorted(summary_df["NE Name"].unique()):

        ne_summary = summary_df[
            summary_df["NE Name"] == ne_name
        ]

        status = (
            "OK"
            if ne_summary["Status"].eq("OK").all()
            else "Not OK"
        )

        final_status.append([
            ne_name,
            status
        ])

    final_status_df = pd.DataFrame(
        final_status,
        columns=[
            "NE Name",
            "Final Status"
        ]
    )




    # ===============================
    # Export Excel
    # ===============================
    output_file = f"media/reports/report_{int(time.time())}.xlsx"

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:

        cell_df.to_excel(
            writer,
            sheet_name="Cells",
            index=False
        )

        rim_df.to_excel(
            writer,
            sheet_name="RIM",
            index=False
        )

        amf_df.to_excel(
            writer,
            sheet_name="AMF",
            index=False
        )

        feature_df.to_excel(
            writer,
            sheet_name="Features",
            index=False
        )

        alarm_df.to_excel(
            writer,
            sheet_name="Alarms",
            index=False
        )

        sd_df.to_excel(
            writer,
            sheet_name="Network_Slicing",
            index=False
        )

        summary_df.to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )

        # ===============================
        # Final Status Sheet
        # ===============================
        final_status_df.to_excel(
            writer,
            sheet_name="Status",
            index=False
        )

    print("\n===== SUMMARY STATUS =====")
    print(summary_df.to_string(index=False))

    print("\n===== FINAL STATUS =====")
    print(final_status_df.to_string(index=False))

    print(f"\nReport Generated: {output_file}")
    return output_file
