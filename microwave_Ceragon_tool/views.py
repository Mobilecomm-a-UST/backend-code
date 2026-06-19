# # from django.shortcuts import render
# # import pandas as pd
# # from rest_framework.decorators import api_view
# # from rest_framework.response import Response
# # from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST 
# # from mcom_website.settings import MEDIA_ROOT, MEDIA_URL
# # from rest_framework import status
# # import re
# # import gzip
# # import os


# # @api_view(['POST'])
# # def upload_cergon_dump(request):
# #     dump_file = request.FILES.get("dump_file")

# #     if not dump_file:
# #         return Response({"message": "dump_file not provided"}, status=400)
    

# #     file_content = dump_file.read().decode("utf-8")
# #     lines = file_content.splitlines()
 
# #     parameter_patterns = {
# #         "sw_version": (r'-sw version\s*:\s*(.+)', "Software Version IDU"),
# #         "unit_name": (r'unit-name=(.*)', "Site Name/System name/Unit Name"),
# #         "ip_address":(r'-ip address\s*:\s*(.+)', "NETWORK IP"),

# #     }

# #     result = []

# #     for key, (pattern, display_name) in parameter_patterns.items():
# #         value = ""
# #         for line in lines:
# #             match = re.search(pattern, line, re.IGNORECASE)
# #             if match:
# #                 value = match.group(1).strip()
# #                 break

# #         result.append({
# #             "parameter": display_name,
# #             "value in dump": value
# #         })

# #     df = pd.DataFrame(result)
# #     print(df)

# #     return Response({
# #         "message": True,
# #         "total_lines": len(lines),
# #     })



# import re
# import pandas as pd
# from rest_framework.decorators import api_view
# from rest_framework.response import Response


# @api_view(['POST'])
# def upload_cergon_dump(request):
#     dump_file = request.FILES.get("dump_file")
#     if not dump_file:
#         return Response({"message": "dump_file not provided"}, status=400)
    
#     lb_file = request.FILES.get("lb_file")
#     if not lb_file:
#         return Response({"message": "lb_file not provided"}, status=400)

#     file_name = lb_file.name.lower()
#     if file_name.endswith(".csv"):
#         df_lb = pd.read_csv(lb_file)
#     elif file_name.endswith((".xlsx", ".xls")):
#         df_lb = pd.read_excel(lb_file)
#     else:
#         return Response(
#             {"message": "Only csv/xlsx/xls files are supported"},
#             status=400
#         )
    


#     lines = dump_file.read().decode("utf-8").splitlines()

#     result = []
#     # Simple parameters------------ 1

#     patterns = {
#         "Software Version IDU": r'-sw version\s*:\s*(.+)',
#         "Site Name/System name/Unit Name": r'unit-name=(.*)',
#         "Current RSL": r'sys-rf/hw-patch-rsl-threshold=(.*)',
#         "SNMP Version": r'snmp-s-version=(.*)',
#         "License Key": r'-license key\s*:\s*(.+)',
#         "Network IP": r'-ip address\s*:\s*(.+)',
#         "System Type": r'-system type\s*:\s*(.+)',
#         "System ID": r'-system id\s*:\s*(.+)',
#         "MTU Value ": r'sw-ap-l2-if-global-mru=(.*)',
#         "TX Mute": r'rf-config-table\.0\.mute-tx=(.*)',
#         "Server Location": r'unit-location=(.*)',
#         "Node LAT LONG": r'unit-longitude=(.*)',
#         "MULTICAREER": r'sys-UNIT-MGR/workaround_manager_config\.0\.interface\(1\)=(.*)',
#         "HTTP S": r'http-s-admin=(.*)',
#         "SNMP":r'snmp-s-admin=(.*)',
#         "Password":r'security-config-log-upload-configuration-table\.0\.Password=(.*)',
#         "MRMC Script ID":r'mrmc-script-config-table\.0\.mrmc-config-active-script-id=(.*)',
#         "MRMC Profile": r'mrmc-script-config-table\.0\.mrmc-config-max-profile=(.*)',
#         "Ethernet port speed":r'radio-ethernet-config-table\.\d+\.threshold-capacity=(.*)',
#         "Modulation": r'mrmc-script-config-table\.\d+\.mrmc-config-script-operational-mode=(.*)',
#         "Frequency Tx (MHz)": r'rf-config-table\.\d+\.tx-frequency=(.*)',
#         "Frequency Rx (MHz)": r'rf-config-table\.\d+\.rx-frequency=(.*)',
#         "Tx Power (dBm)": r'rf-config-table\.\d+\.tx-level-config=(.*)',
     
      





#     }

#     for display_name, pattern in patterns.items():
#         value = ""
#         for line in lines:
#             match = re.search(pattern, line, re.IGNORECASE)
#             if match:
#                 value = match.group(1).strip()
#                 break

#         result.append({
#             "parameter": display_name,
#             "value in dump": value
#         })
#     result.append({
#     "parameter": "ACM Enabled/Modulation mode",
#     "value in dump": "adaptive"
#     })


#     result.append({
#         "parameter": "ATPC",
#         "value in dump": "disable"
#     })    


#     header = None
#     values = None

# # Voltage table parameters------ 4

#     for i, line in enumerate(lines):
#         if line.strip() == "unit-mgr-voltage-config-table":
#             for j in range(i + 1, len(lines)):
#                 if lines[j].startswith("row|"):
#                     header = [x.strip() for x in lines[j].split("|")]
#                 elif lines[j].startswith("0|"):
#                     values = [x.strip() for x in lines[j].split("|")]
#                     break
#             break


#     if header and values:
#         required_columns = [
#             "Undervoltage clear threshold (V)",
#             "Undervoltage raise threshold (V)",
#         ]

#         for col in required_columns:
#             if col in header:
#                 result.append({
#                     "parameter": col,
#                     "value in dump": values[header.index(col)]
#                 })

#     creation_date = ""
#     timer = ""

#     for line in lines:

#         if line.startswith("unit-info-creation-date="):
#             creation_date = line.split("=",1)[1].strip()

#         elif line.startswith("software-mgt-s-timer="):
#             timer = line.split("=",1)[1].strip() 

#     result.append({
#         "parameter": "Date and Time",
#         "value in dump": f"{creation_date} {timer}".strip()
#     })  

#     df = pd.DataFrame(result)
#     dump_df = df.set_index("parameter").T
#     print(dump_df)
#     dump_df.to_excel("dump.xlsx",index=False)

#     df_lb= df_lb[[   
#         "Circle",
#         "Plan Id",
#         "Polarization",
#         "Equipment Make",
#         "Site ID-A",
#         "BER10e6 Tx Power (dBm)",
#         "Tx Frequency (MHz)",
#         "BER10e6 Rx Level (dBm)",
#         "Site ID -B",
#         "Rx Frequency (MHz)",
#         "Tx Radio",
#         "Bandwidth (MHz)",
#         "ACM Min QAM",
#         "ACM Max QAM",
#         "MRMC Script ID",
#         "Hop Type",
#         "Fiber POP Id"
#     ]]
#     print(df_lb)

#     df_lb["Site ID-A"] = df_lb["Site ID-A"].astype(str).str.strip()
#     df_lb["Site ID -B"] = df_lb["Site ID -B"].astype(str).str.strip()

#     df_lb["MRMC Script ID"] = pd.to_numeric(
#     df_lb["MRMC Script ID"], errors="coerce"
#     )

#     df_lb["Tx Frequency (MHz)"] = pd.to_numeric(
#     df_lb["Tx Frequency (MHz)"], errors="coerce"
#     )

#     df_lb["Rx Frequency (MHz)"] = pd.to_numeric(
#     df_lb["Rx Frequency (MHz)"], errors="coerce"
#     )


#     unit_name = next(
#         (x["value in dump"] for x in result
#         if x["parameter"] == "Site Name/System name/Unit Name"),
#         ""
#     )

#     mrmc_script_id = pd.to_numeric(
#         next(
#             (x["value in dump"] for x in result
#             if x["parameter"] == "MRMC Script ID"),
#             None
#         ),
#         errors="coerce"
#     )

#     matched_df = df_lb[
#     (
#         (df_lb["Site ID-A"] == unit_name)
#         |
#         (df_lb["Site ID -B"] == unit_name)
#     )
#     &
#     (df_lb["MRMC Script ID"] == mrmc_script_id)
# ]

#     print(matched_df)

#     if not matched_df.empty:
#         final_row = matched_df.iloc[0].to_dict()

#         for item in result:
#             final_row[item["parameter"]] = item["value in dump"]

#         final_df = pd.DataFrame([final_row])

#     else:
#         final_df = pd.DataFrame(result)


#     print()    

#     output_file = "final_parameters.xlsx"
#     final_df.to_excel(output_file, index=False)

#     return Response({
#         "message": True,
#         "rows": len(df),
#         "data": result
#     })


import re
import pandas as pd
import numpy as np
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from microwave_Ceragon_tool.models import Microwavepara
from microwave_Ceragon_tool.serializers import MicrowaveparaSerializer
from microwave_Ceragon_tool.utils import *
from openpyxl import Workbook
import os
from pathlib import Path
from mcom_website.settings import MEDIA_ROOT, MEDIA_URL
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.shortcuts import get_object_or_404



main_folder = os.path.join(MEDIA_ROOT, 'MicroWave_Ceragone_Tool')
os.makedirs(main_folder, exist_ok=True)
final_folder=os.path.join(main_folder, 'MW_Final_Output')
os.makedirs(final_folder, exist_ok=True)


@api_view(['POST', 'GET' , 'DELETE'])
def upload_link_budget(request):
    try:
        Link_budget_path = os.path.join(main_folder, 'Link_budget_file')
        os.makedirs(Link_budget_path, exist_ok=True)
 
        if request.method == 'POST':
            files = request.FILES.getlist('link_buget_file')
            if not files:
                return Response({'error': 'link_buget_file files uploaded'}, status=status.HTTP_400_BAD_REQUEST)
 
            for f in files:
                file_path = os.path.join(Link_budget_path, f.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
 
            return Response({'status': True, 'message': 'Files uploaded and saved successfully'}, status=status.HTTP_200_OK)
 
        elif request.method == 'GET':
            if not os.path.exists(Link_budget_path):
                return Response({'files': []}, status=status.HTTP_200_OK)
 
            files = os.listdir(Link_budget_path)
            return Response({
                'status': True,
                'message': f'{len(files)} Files found in Link_budget_file folder',
                'files': files,
                }, status=status.HTTP_200_OK)
           
        elif request.method == 'DELETE':
            if not os.path.exists(Link_budget_path):
                return Response({'error': 'Folder does not exist'}, status=status.HTTP_404_NOT_FOUND)
 
            deleted_files = []
            for filename in os.listdir(Link_budget_path):
                file_path = os.path.join(Link_budget_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    deleted_files.append(filename)
 
            return Response({
                'status': True,
                'message': f'{len(deleted_files)} Files deleted successfully',
                'deleted_files': deleted_files
            }, status=status.HTTP_200_OK)
           
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def microwave_para(request, pk=None):
    if request.method == "GET":
        idu = request.data.get('idu', '')
        queryset = Microwavepara.objects.all()
        if idu:
            queryset = queryset.filter(idu_model__iexact=idu)
        serializer = MicrowaveparaSerializer(queryset, many=True)

        return Response(serializer.data)

    elif request.method == "POST":
        data = request.data
          # Bulk upload
        if isinstance(data, list):
            serializer = MicrowaveparaSerializer(data=data, many=True)
        else:
            serializer = MicrowaveparaSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": True,
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "PUT":

        obj = get_object_or_404(Microwavepara, pk=pk)

        serializer = MicrowaveparaSerializer(
            obj,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "status": True,
                    "data": serializer.data
                }
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":

        obj = get_object_or_404(Microwavepara, pk=pk)
        obj.delete()

        return Response(
            {
                "status": True,
                "message": "Deleted successfully"
            }
        )


@api_view(['POST'])
def search_plan_id(request):
    search_text = request.data.get('plan_id', '').strip()
    if not search_text:
        return Response([])

    link_budget_folder = os.path.join(main_folder, "Link_budget_file")
    files = os.listdir(link_budget_folder)
    if not files:
        return Response([])

    file_path = os.path.join(link_budget_folder, files[0])
    if file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
    else:
        df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()

    if "Plan Id" not in df.columns:
        return Response([])
    
    result = (
        df["Plan Id"].astype(str).str.strip().loc[lambda x: x.str.contains(search_text, case=False, na=False)]
        .drop_duplicates()
        .head(15)
        .tolist()
    )

    return Response(result)


@api_view(['POST'])
def upload_cergon_dump(request):
    plan_id = request.data.get("plan_id")
    if not plan_id:
        return Response({"message": "plan_id not provided"}, status=400)

    dump_file1 = request.FILES.get("dump_file1")
    if not dump_file1:
        return Response({"message": "dump_file1 not provided"}, status=400)
    
    dump_file2 = request.FILES.get("dump_file2")
    if not dump_file2:
        return Response({"message": "dump_file2 not provided"}, status=400)

    link_budget_file = os.path.join(main_folder, 'Link_budget_file')
    if not os.path.exists(link_budget_file):
        return Response({"error": "Link_budget_file folder not found"}, status=400)

    link_budget_file_list = []
    for filename in os.listdir(link_budget_file):
        file_path = os.path.join(link_budget_file, filename)
        if filename.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        elif filename.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            return Response(
                {"status": "ERROR", "message": f"Unsupported file type: {filename}"},
                status=HTTP_400_BAD_REQUEST
            )
        df.columns = df.columns.str.strip()
        link_budget_file_list.append(df)

    if link_budget_file_list:
        link_budget_df = pd.concat(link_budget_file_list, ignore_index=True)
    else:
        return Response(
            {"status": "ERROR", "message": "No valid files found"},
            status=HTTP_400_BAD_REQUEST
        )
    # print(link_budget_df.columns.tolist())
    


#read dump file1 -----------
    dump_files = [
        ("Report1", dump_file1),
        ("Report2", dump_file2)
    ]
    report_dfs = []
    Atcp_df = pd.DataFrame(columns=[
        "SL NO",
        "MW Plan Id",
        "Link ID (Site ID A - Site ID B and Site ID B - Site ID A)",
        "Site ID",
        "Site Name/System name/Unit Name",
        "Server/RDP -IP",
        "Type of Equipment",
        "ODU/IDU (New/Existing)",
        "MRMC Script ID/Bandw",
        "MRMC Profile/Bandw",
        "Link configuration ( 1+0 / 1+1 / 2+0/ XPIC/1G)",
        "IDU Model (Modular IDU-IP20N, IP-20G , High capacity packet radio IP20C/IP20S, IP-20GX, IP-20F)",
        "Link-Slot Number",
        "Link-Port Number",
        "Frequency Tx",
        "Frequency Rx",
        "Tx Power  (dBm)",
        "RSL(dBM) Main [<=3 dB Deviation permitted]",
        "Modulation",
        "ATPC (enabled/disable)",
        "ACM Enabled/Modulation mode (Fixed/adaptive)",
        "ODU IP Address",
        "IDU IP Address/Remarks",
        "ODU IP Ethernet slot port detail  /Other remarks"
    ])

    for sheet_name, dump_file in dump_files:
        if not dump_file:
            continue
        lines = dump_file.read().decode("utf-8").splitlines()
        result = []
        # ---- Simple parameters ----
        patterns = {
            "Software Version IDU": r'-sw version\s*:\s*(.+)',
            "Site Name/System name/Unit Name": r'unit-name=(.*)',
            "Current RSL": r'sys-rf/hw-patch-rsl-threshold=(.*)',
            "SNMP Version": r'snmp-s-version=(.*)',
            "License Key": r'-license key\s*:\s*(.+)',
            "Network IP": r'-ip address\s*:\s*(.+)',
            "IDU Model": r'-system type\s*:\s*(.+)',
            "Type of Equipment": r'-system id\s*:\s*(.+)',
            "MTU Value": r'sw-ap-l2-if-global-mru=(.*)',
            "Tx Mute": r'rf-config-table\.0\.mute-tx=(.*)',
            "Server Location": r'unit-location=(.*)',
            "NodeLONG": r'unit-longitude=(.*)',
            "NodeLAT" :r'unit-latitude=(.*)',
            "Multicarrier ABC": r'.*workaround_manager_config\.0\.interface\(1\)\s*=\s*(.*)',
            "HTTPS": r'http-s-admin=(.*)',
            "SNMP": r'snmp-s-admin=(.*)',
            "Password": r'security-config-log-upload-configuration-table\.0\.Password=(.*)',
            "MRMC Script ID/Bandw": r'mrmc-script-config-table\.0\.mrmc-config-active-script-id=(.*)',
            "MRMC Profile/Bandw": r'mrmc-script-config-table\.0\.mrmc-config-max-profile=(.*)',
            "Ethernet Port Speed": r'radio-ethernet-config-table\.\d+\.threshold-capacity=(.*)',
            "Modulation": r'mrmc-script-config-table\.\d+\.mrmc-config-script-operational-mode=(.*)',
            "Frequency Tx (MHz)": r'rf-config-table\.\d+\.tx-frequency=(.*)',
            "Frequency Rx (MHz)": r'rf-config-table\.\d+\.rx-frequency=(.*)',
            "Tx Power (dBm)": r'rf-config-table\.\d+\.tx-level-config=(.*)',
        }

        for display_name, pattern in patterns.items():
            value = "NA"        # default value
            for line in lines:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    value = match.group(1).strip()

                    if value == "":
                        value = "NA"

                    break

            result.append({
                "parameter": display_name,
                "value in dump": value
            })

        result.append({"parameter": "ACM Enabled/Modulation mode", "value in dump": "adaptive"})
        result.append({"parameter": "ATPC", "value in dump": "disable"})

        # ---- Voltage table parameters ----
        header = None
        values = None
        for i, line in enumerate(lines):
            if line.strip() == "unit-mgr-voltage-config-table":
                for j in range(i + 1, len(lines)):
                    if lines[j].startswith("row|"):
                        header = [x.strip() for x in lines[j].split("|")]
                    elif lines[j].startswith("0|"):
                        values = [x.strip() for x in lines[j].split("|")]
                        break
                break

        if header and values:
            required_columns = [
                "Undervoltage clear threshold (V)",
                "Undervoltage raise threshold (V)",
            ]
            for col in required_columns:
                if col in header:
                    result.append({"parameter": col, "value in dump": values[header.index(col)]})

        # ---- Date and Time ----
        creation_date = ""
        timer = ""
        for line in lines:
            if line.startswith("unit-info-creation-date="):
                creation_date = line.split("=", 1)[1].strip()
            elif line.startswith("software-mgt-s-timer="):
                timer = line.split("=", 1)[1].strip()


        dscp_cos_list = []
        inside_table = False

        for line in lines:
            line = line.strip()
            if line == "sw-ap-global-ingress-mapping-dscp-to-cos-table":
                inside_table = True
                continue
            if inside_table:
                # next section start ho gaya
                if line.startswith("%%%"):
                    break
                # data rows
                if re.match(r'^\d+\|', line):
                    cols = line.split("|")
                    dscp = cols[1]
                    cos = cols[4]
                    dscp_cos_list.append({
                        "DSCP": dscp,
                        "CoS": cos
                    })

        # print(dscp_cos_list)  

        expected_set = {(x["DSCP"], x["CoS"]) for x in dscp_cos_mapping}
        actual_set = {(x["DSCP"], x["CoS"]) for x in dscp_cos_list}

        qos_status = "all cos value match" if expected_set == actual_set else "NOT match cos"       

        result.append({"parameter": "Date and Time", "value in dump": f"{creation_date} {timer}".strip()})
        result.append({
                "parameter": "QoS configured (Y/N)",
                "value in dump": qos_status
            })

        # convert dump result list -> dict for easy lookup
        dump_values = {item["parameter"]: item["value in dump"] for item in result}
        print(dump_values)

        dump_values["Type of Equipment/IDU Model"] = (
            str(dump_values.get("Type of Equipment", "")).strip()
            + " | "
            + str(dump_values.get("IDU Model", "")).strip()
        )

        idu_model = (
            dump_values.get("Type of Equipment/IDU Model", "")
            .split("|")[-1]
            .strip()
            .upper()
        )

        queryset = Microwavepara.objects.filter(
            idu_model__iexact=idu_model
        ).values("parameter", "value")

        db_values = {
            row["parameter"].strip().lower(): str(row["value"]).strip()
            for row in queryset
        }

    
        site_id = dump_values.get("Site Name/System name/Unit Name", "").strip()

        mask_a = link_budget_df["Site ID-A"].astype(str).str.strip() == site_id
        mask_b = link_budget_df["Site ID -B"].astype(str).str.strip() == site_id

        row = None
        mapping = {}

        common_mapping = {
            "Link ID (Site ID A - Site ID B and Site ID B - Site ID A)":"Link ID",
            "Tx Power (dBm)": "BER10e6 Tx Power (dBm)",
            "MRMC Script ID/Bandw": "MRMC Script ID",
            "MRMC Profile/Bandw": "Tx Radio",
            "Modulation": "ACM Max QAM",
            "ACM Enabled/Modulation mode": "ACM Status",
            "ATPC": "ATPC Status",
            "Current RSL": "RSL",
            "Plan Id":"Plan Id",
            "Hop Type":"Hop Type",
        
            
        }

        site_a_mapping = {
            "Site Name/System name/Unit Name": "Site ID-A",
            "NodeLAT": "Site A Lat",
            "NodeLONG": "Site A Long",
            "Type of Equipment/IDU Model": "(MODEM(IF Card)/Ethernet Port) Site-A",
            "Frequency Tx (MHz)": "Tx Frequency (MHz)",
            "Frequency Rx (MHz)": "Rx Frequency (MHz)",

        }

        site_b_mapping = {
            "Site Name/System name/Unit Name": "Site ID -B",
            "NodeLAT": "Site B Lat",
            "NodeLONG": "Site B Long",
            "Type of Equipment/IDU Model": "(MODEM(IF Card)/Ethernet Port) Site-B",
            "Frequency Tx (MHz)": "Rx Frequency (MHz)",
            "Frequency Rx (MHz)": "Tx Frequency (MHz)"
        }

        if mask_a.any():
            row = link_budget_df.loc[mask_a].iloc[0]
            mapping = {**common_mapping, **site_a_mapping}

        elif mask_b.any():
            row = link_budget_df.loc[mask_b].iloc[0]
            mapping = {**common_mapping, **site_b_mapping}

        # ---------------- LB Values ----------------
        lb_values = {}

        if row is not None:
            for k, v in mapping.items():
                if v in row.index:
                    lb_values[k] = row[v]

        lb_values["band"] = "D band" if "IP-50" in str(lb_values.get("Type of Equipment/IDU Model", "")).upper() else "C band"

        # clean NA
        for k in lb_values:
            if pd.isna(lb_values[k]) or str(lb_values[k]).strip() == "":
                lb_values[k] = "NA"
            else:
                lb_values[k] = str(lb_values[k]).strip()

        print(lb_values)
        report = []
        plan_status = (
            "OK"
            if str(plan_id).strip() == str(row.get("Plan Id", "")).strip()
            else "NOT OK"
        )

        report.append([
            "Plan-ID",
            plan_id,                  # Request se aaya hua
            row.get("Plan Id", "NA"), # LB file ka Plan Id
            plan_status
        ])

        for param in master_parameters:
            param_key = param.strip().lower()
            if param == "Link ID (Site ID A - Site ID B and Site ID B - Site ID A)":
                dump_value = lb_values.get(
                    "Link ID (Site ID A - Site ID B and Site ID B - Site ID A)",
                    "NA"
                )

                expected_value = dump_value

                status = "OK" if dump_value not in ["NA", ""] else "NOT OK"

            else:
                dump_value = dump_values.get(param, "NA")
                if param == "High Low Violation (Y/N)":

                    dump_value = dump_values.get("Frequency Tx (MHz)", "NA")
                    expected_value = lb_values.get("Frequency Tx (MHz)", "NA")

                    status = check_status(
                        "Frequency Tx (MHz)",dump_value,expected_value,dump_values)

                    report.append([param, dump_value, expected_value, status])
                    continue

                # ---------------- LB Parameters ----------------
                if param in check_lb_params:

                    if param == "Current RSL":
                        idu = str(dump_values.get("IDU Model", "")).upper()
                        expected_value = "+/-4" if "IP-50" in idu else "+/-3"

                    else:
                        expected_value = lb_values.get(param, "NA")

                elif param_key in db_values:
                    expected_value = db_values[param_key]

                elif param in fix_values:
                    expected_value = fix_values[param]

                elif param in check_in_manual:
                    expected_value = "MANUAL"

                else:
                    expected_value = "NA"

                status = check_status( param,dump_value,expected_value,dump_values)

            report.append([
                    param,
                    dump_value,
                    expected_value,
                    status
                ])

        report_df = pd.DataFrame( report,
                columns=[
                "Parameter",
                "Dump Value",
                "Expected Value",
                "Remark"
            ]
        )

        report_df = report_df[~report_df["Parameter"].isin([
            "MSTP",
            "Server Location",
            "NodeLONG",
            "NodeLAT",
            "Management Service",
            "Password"
        ])]
        report_dfs.append((sheet_name, report_df))
  
        row_data = {
            "SL NO":"1",
            "MW Plan Id": row.get("Plan Id", "NA"),
            "Link ID (Site ID A - Site ID B and Site ID B - Site ID A)": row.get("Link ID", "NA"),
            "Site ID":dump_values.get("Site Name/System name/Unit Name", "NA"),
            "Site Name/System name/Unit Name":dump_values.get("Site Name/System name/Unit Name", "NA"),
            "Server/RDP -IP":db_values.get("software version idu", "NA"),
            "Type of Equipment":"Ceragone",
            "ODU/IDU (New/Existing)":"New",
            "MRMC Script ID/Bandw":dump_values.get("MRMC Script ID/Bandw", "NA"),
            "MRMC Profile/Bandw":dump_values.get("MRMC Profile/Bandw", "NA"),
            "Link configuration ( 1+0 / 1+1 / 2+0/ XPIC/1G)":row.get("Hop Type","NA"),
            "IDU Model (Modular IDU-IP20N, IP-20G , High capacity packet radio IP20C/IP20S, IP-20GX, IP-20F)":dump_values.get("Type of Equipment/IDU Model", "NA"),
            "Link-Slot Number":dump_values.get("Multicarrier ABC", "NA"),
            "Link-Port Number":dump_values.get("Multicarrier ABC", "NA"),
            "Frequency Tx":dump_values.get("Frequency Tx (MHz)", "NA"),
            "Frequency Rx":dump_values.get("Frequency Rx (MHz)", "NA"),
            "Tx Power  (dBm)":row.get("BER10e6 Tx Power (dBm)", "NA"),
            "RSL(dBM) Main [<=3 dB Deviation permitted]":dump_values.get("Current RSL", "NA"),
            "Modulation":row.get("ACM Max QAM", "NA"),
            "ATPC (enabled/disable)":row.get("ATPC Status", "NA"),
            "ACM Enabled/Modulation mode (Fixed/adaptive)":row.get("ACM Status", "NA"),
            "ODU IP Address":dump_values.get("Network IP", "NA"),
            "IDU IP Address/Remarks":"",
            "ODU IP Ethernet slot port detail  /Other remarks":""

        }

        Atcp_df = pd.concat(
            [Atcp_df, pd.DataFrame([row_data])],
            ignore_index=True
        )
    wb = Workbook()
    wb.remove(wb.active)

    # Report1, Report2 create karna
    for sheet_name, df in report_dfs:
        ws = wb.create_sheet(sheet_name)

        data = [df.columns.tolist()] + df.values.tolist()

        create_config_report(ws, data)

    # ATP Sheet
    if not Atcp_df.empty:
        ws_atp = wb.create_sheet("ATP")

        data_atp = [Atcp_df.columns.tolist()] + Atcp_df.values.tolist()

        create_config_report(ws_atp, data_atp)

    output_file = os.path.join(final_folder, "MW_Ceragone_Report.xlsx")
    wb.save(output_file)

    relative_path = os.path.relpath(output_file, MEDIA_ROOT).replace("\\", "/")
    download_url = request.build_absolute_uri(MEDIA_URL + relative_path)

    return Response({
        "status": True,
        "message": "Report generated successfully",
        "download_url": download_url
    })
    

