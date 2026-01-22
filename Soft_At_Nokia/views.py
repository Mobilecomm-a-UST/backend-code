
import os
from .models import MOData  # Adjust the path if the model is in a different app
import pandas as pd
from .models import ExpectedParameter, SummaryData
import xml.etree.ElementTree as ET
from django.conf import settings
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from mcom_website.settings import MEDIA_ROOT, MEDIA_URL
from rest_framework.response import Response
from rest_framework import status
# from rest_framework import status
from .models import ExpectedParameter ,SummaryData , UserCounter
from  mcom_website.settings import MEDIA_ROOT
from .serializers import ExpectedParameterSerializer,SummaryDataSerializer ,UserCounterSerializer
import json



#---------------------------project Type #--------------------

from .models import ExpectedParameter ,SummaryData,AlarmMapping
from  mcom_website.settings import MEDIA_ROOT
from .serializers import ExpectedParameterSerializer,SummaryDataSerializer
import json
import os
import pandas as pd
import xml.etree.ElementTree as ET
from django.conf import settings
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import ExpectedParameter
from .serializers import ExpectedParameterSerializer
from mcom_website.settings import MEDIA_ROOT


# -------------------- Utility Functions --------------------

def extract_site_id(dist_name):

    """Extract site id from distName attribute."""

    try:
        parts = dist_name.split('/')
        for part in parts:
            if part.startswith("MRBTS-"):
                return part.split('-')[1]
    except Exception:
        return None
    return None


def normalize_path(path):

    """Normalize MO path to lowercase and remove 'managedobject=' prefix if present."""

    if isinstance(path, str):
        path = path.strip().lower()
        if path.startswith("managedObject ="):
            path = path[len("managedObject ="):]
        return path
    return ''


def get_default_namespace(element):

    """Extract the default namespace URI from the root element tag."""
    if element.tag.startswith("{"):
        return element.tag[1:].split("}")[0]
    return ''


def format_excel_sheet(writer, sheet_name, df, startrow=0, startcol=0):
        """Apply formatting to an Excel sheet with adjustable start positions."""
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]

        header_format = workbook.add_format(
                {
                    "bold": True,
                    "bg_color": "#000957",
                    "border": 2,
                    "font_color": "#ffffff",
                    "align": "center",
                    "valign": "vcenter",
                }
                )
        center_format = workbook.add_format(
                {
                    "align": "center",
                    "valign": "center",
                    "border": 1,
                    "border_color": "#000000",
                    "bold": True,
                }
                )
        ok_format = workbook.add_format(
                {
                    "bg_color": "#90EE90",
                    "font_color": "#000000",
                    "align": "center",
                    "valign": "center",
                }
                )
        not_ok_format = workbook.add_format(
                {
                    "bg_color": "#FF0000",
                    "font_color": "#FFFFFF",
                    "align": "center",
                    "valign": "center",
                }
                )

        worksheet.set_row(startrow, 23)

        for col_num, col_name in enumerate(df.columns):
                worksheet.write(startrow, startcol + col_num, str(col_name), header_format)

                column_series = df[col_name]
                if isinstance(column_series, pd.DataFrame):
                    column_series = column_series.iloc[:, 0]

                max_length = max(
                column_series.fillna("").astype(str).str.len().max(skipna=True) or 0,
                len(str(col_name)),
                )
                max_length = min(max_length, 255)
                worksheet.set_column(startcol + col_num, startcol + col_num, max_length + 5)

        for row_num in range(len(df)):
                worksheet.set_row(startrow + row_num + 1, 15)

                for col_num in range(len(df.columns)):
                    cell_value = str(df.iloc[row_num, col_num])
                    format_style = center_format
                    if cell_value == "OK":
                            format_style = ok_format
                    elif cell_value == "NOT OK" or cell_value == "NOK":
                            format_style = not_ok_format
                    elif cell_value == "Missing" or cell_value == "Missing in Post":
                            format_style = workbook.add_format(
                                {
                                "bg_color": "#FF6347",
                                "font_color": "#FFFFFF",
                                "align": "center",
                                "valign": "center",
                                "bold": True,
                                "border": 1,
                                }
                            )
                    elif cell_value == "NA":
                            format_style = workbook.add_format(
                                {
                                        "bg_color": "#FCF259",
                                        "font_color": "#222831",
                                        "align": "center",
                                        "valign": "center",
                                        "bold": True,
                                        "border": 1,
                                }
                    )
                    elif "|" in cell_value:
                            format_style = workbook.add_format(
                                {
                                        "font_color": "#FF0000",
                                        "align": "center",
                                        "valign": "center",
                                        "bold": True,
                                        "border": 1,
                                        "border_color": "#000000",
                                }
                    )

                    worksheet.write(
                            startrow + row_num + 1, startcol + col_num, cell_value, format_style
                    )

                    # workbook.__save()

# --- ADDED: match_value() for flexible comparison ---
def match_value(actual, expected):
    actual = actual.strip().lower()
    expected = expected.strip().lower()
    if ';' in expected:
        options = [opt.split('(')[0].strip().lower() for opt in expected.split(';')]
        return any(actual == opt for opt in options)
    if "should be" in expected or "if" in expected:
        return expected.split()[0] in actual
    return actual == expected


# --- ADDED: matches_path() for hierarchical class path matching ---


def format_excel_sheet(writer, sheet_name, df, startrow=0, startcol=0):
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    header_format = workbook.add_format({
        "bold": True, "bg_color": "#000957", "border": 2,
        "font_color": "#ffffff", "align": "center", "valign": "vcenter"
    })

    center_format = workbook.add_format({
        "align": "center", "valign": "center", "border": 1, "bold": True
    })

    ok_format = workbook.add_format({
        "bg_color": "#90EE90", "font_color": "#000000",
        "align": "center", "valign": "center"
    })

    not_ok_format = workbook.add_format({
        "bg_color": "#FF0000", "font_color": "#FFFFFF",
        "align": "center", "valign": "center"
    })

    worksheet.set_row(startrow, 23)

    for col_num, col_name in enumerate(df.columns):
        worksheet.write(startrow, startcol + col_num, str(col_name), header_format)

        column_series = df[col_name]
        if isinstance(column_series, pd.DataFrame):
            column_series = column_series.iloc[:, 0]

        max_length = max(
            column_series.fillna("").astype(str).str.len().max(skipna=True) or 0,
            len(str(col_name)),
        )
        max_length = min(max_length, 255)
        worksheet.set_column(startcol + col_num, startcol + col_num, max_length + 5)

    for row_num in range(len(df)):
        worksheet.set_row(startrow + row_num + 1, 15)
        for col_num in range(len(df.columns)):
            cell_value = str(df.iloc[row_num, col_num])
            format_style = center_format
            if cell_value == "OK":
                format_style = ok_format
            elif cell_value in ["NOT OK", "NOK"]:
                format_style = not_ok_format
            elif cell_value in ["Missing", "Missing in Post"]:
                format_style = workbook.add_format({
                    "bg_color": "#FF6347", "font_color": "#FFFFFF",
                    "align": "center", "valign": "center", "bold": True, "border": 1
                })
            elif cell_value == "NA":
                format_style = workbook.add_format({
                    "bg_color": "#FCF259", "font_color": "#222831",
                    "align": "center", "valign": "center", "bold": True, "border": 1
                })
            elif "|" in cell_value:
                format_style = workbook.add_format({
                    "font_color": "#FF0000", "align": "center",
                    "valign": "center", "bold": True, "border": 1
                })

            worksheet.write(startrow + row_num + 1, startcol + col_num, cell_value, format_style)
import re
import re

def normalize_value(val):
    """Clean value: uppercase, strip spaces, remove special chars"""
    if not val:
        return ''
    
    val = val.strip().upper()
    digits = re.sub(r'\D', '', val)

    # For values like '30m' — return only digits if present
    if digits and val.lower().endswith('m'):
        return digits
    
    return re.sub(r'\W+', '', val)




def match_value(actual, expected):
    """Check if normalized actual is in any normalized expected values"""
    actual_norm = normalize_value(actual)
    expected_values = [normalize_value(val) for val in expected.split("or")]
    return actual_norm in expected_values

def matches_path(expected_path, dist_name):
    expected_parts = [p.split('-')[0].lower() for p in expected_path.split('/')]
    dist_parts = [p.split('-')[0].lower() for p in dist_name.split('/')]
    idx = 0
    for part in dist_parts:
        if idx < len(expected_parts) and part == expected_parts[idx]:
            idx += 1
    return idx == len(expected_parts)


# ------------------- Main API VieW ####################################################
def deduplicate_alarms(alarms):
    seen = set()
    unique_alarms = []
    for alarm in alarms:
        key = (alarm['file'], alarm['site_id'], alarm['mo_path'], alarm['parameter'])
        if key not in seen:
            seen.add(key)
            unique_alarms.append(alarm)
    return unique_alarms


def api_usage_all(userId, api):
    print(userId)
    qs = UserCounter.objects.filter(user_name=userId, api_name=api).first()

    if qs:
        qs.count += 1
        qs.save()
    
    else:
        qs = UserCounter.objects.create(user_name=userId, api_name=api, count=1)


@api_view(['GET', 'POST'])
def user_count(request):
    if request.method == 'GET':
        qs = UserCounter.objects.all()
        serializer = UserCounterSerializer(qs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserCounterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'POST'])
def upload_and_compare_xml(request):
    userId = request.data.get('userId')
    api = "Checkpoints Data"
    if request.method == 'GET':
        expected_parameters = ExpectedParameter.objects.all()
        serializer = ExpectedParameterSerializer(expected_parameters, many=True)
        print(serializer.data)
        # api_usage_all(userId, api)
        return Response(serializer.data)
    
    elif request.method == 'POST':
            serializer= ExpectedParameterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                api_usage_all(userId, api)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT':
        data = request.data
        serializer = ExpectedParameterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # api_usage_all(userId, api)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# -------------------------expeted parameter------------

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_excel(request):
    userId = request.data.get('userId')
    api = "checkpoints Upload"
    excel_file = request.FILES.get('excel_file')
    if not excel_file:
        return Response({"error": "Excel file is required"}, status=status.HTTP_400_BAD_REQUEST)
 
    try:
        df = pd.read_excel(excel_file)
        # df = df.dropna(subset=['MO Class', 'Parameter', 'Value'])
 
 
        ExpectedParameter.objects.all().delete()  
 

        errors = []

        for _, row in df.iterrows():
            data = {
            "path": str(row["path"]).strip(),
            "parameter_name": str(row["parameter_name"]).strip(),
            "expected_value": str(row["expected_value"]).strip(),
                            }
            serializer = ExpectedParameterSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                errors.append(serializer.errors)
 
        if errors:
            return Response({"error": "Some rows failed validation", "details": errors}, status=status.HTTP_400_BAD_REQUEST)
        api_usage_all(userId, api)
        return Response({"status": True,"message": "Excel uploaded and saved successfully"},status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"Failed to process Excel file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

# Upload XMLs and compare with database values

FIXED_PARAMETERS = [
    {"parameter": "actLBpowersaving", "mo_class": "MRBTS/LNBTS"},
    {"parameter": "gnssAntennaLatitude", "mo_class": "MRBTS/EQM_R-1/APEQM_R-1/CABINET_R-1/SMOD_R-1/GNSSE_R"},
    {"parameter": "gnssAntennaLongitude", "mo_class": "MRBTS/EQM_R-1/APEQM_R-1/CABINET_R-1/SMOD_R-1/GNSSE_R"},
    {"parameter": "activeSWReleaseVersion", "mo_class": "MNL_R"},
    {"parameter": "speedAndDuplex", "mo_class": "MRBTS/TNLSVC-1/TNL-1/ETHSVC-1/ETHLK-1"},
    {"parameter": "detectedSpeedAndDuplex", "mo_class": "MRBTS/TNLSVC-1/TNL-1/ETHSVC-1/ETHLK-1/ETHLK_R-1"},
    {"parameter": "holdOverModeUsed", "mo_class": "MRBTS/MNL/MNLENT/SYNC-1/CLOCK-1"},
    {"parameter": "syncInputType", "mo_class": "MRBTS/MNL/MNLENT/SYNC-1/CLOCK-1"},
    {"parameter": "transmissionrate", "mo_class": "MRBTS/EQM_R-1/APEQM_R-1/RMOD_R-1/SFP_R"},
    {"parameter": "autoDetectTotalDelayFromSHM", "mo_class": "MRBTS/MNL-1/MNLENT-1/SYNC-1/CLOCK_R-1"},
    {"parameter": "productName", "mo_class": "CABINET_R"}

]


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_and_compare_xml_files(request):
    userId = request.data.get('userId')
    api = "checkpoints Report Downloaded"
    xml_files = request.FILES.getlist('xml_files')
    circle_name = request.data.get('circle_name', 'default_circle').strip()
    project_type = request.data.get('project_type', 'project_type').strip()

    if not xml_files:
        return Response({"error": "At least one XML file is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Load ExpectedParameter DB
    expected_params = ExpectedParameter.objects.all()
    serializer = ExpectedParameterSerializer(expected_params, many=True)
    expected_params_json = serializer.data

    # Normalize expected values
    expected_values = {}
    for param in expected_params_json:
        norm_path = normalize_path(param['path'])
        if norm_path not in expected_values:
            expected_values[norm_path] = {}
        expected_values[norm_path][param['parameter_name'].lower()] = param['expected_value']

    # Containers
    results = []
    all_alarms = []
    summary_rows = []
    ipmtu_rows = []

    # ------------------------
    # Helper function
    # ------------------------
    def get_param_value(mo, param_name, ns_uri):
        p_tag = f"{{{ns_uri}}}p" if ns_uri else "p"
        list_tag = f"{{{ns_uri}}}list" if ns_uri else "list"
        item_tag = f"{{{ns_uri}}}item" if ns_uri else "item"

        # Search direct <p>
        for p in mo.findall(p_tag):
            if p.attrib.get("name", "").lower() == param_name:
                return (p.text or "").strip()

        # Search inside list/item/p
        for lst in mo.findall(list_tag):
            for item in lst.findall(item_tag):
                for p in item.findall(p_tag):
                    if p.attrib.get("name", "").lower() == param_name:
                        return (p.text or "").strip()

        return ""

    # ------------------------
    # MAIN XML LOOP
    # ------------------------
    for xml_file in xml_files:
        xml_file.seek(0)
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
        except ET.ParseError:
            results.append({
                "file": xml_file.name,
                "site_id": '',
                "mo_path": '',
                "parameter": '',
                "actual_value": '',
                "expected_value": '',
                "status": "Failed to parse XML"
            })
            continue

        ns_uri = get_default_namespace(root)
        ns = {'ns': ns_uri} if ns_uri else {}

        mo_elements = root.findall('.//ns:managedObject', ns) if ns else root.findall('.//managedObject')

        # 1. IPMTU VALIDATION
        REQUIRED_IPIF_DISTNAMES = [
            "MRBTS/TNLSVC-1/TNL-1/IPNO-1/IPIF-1",
            "MRBTS/TNLSVC-1/TNL-1/IPNO-1/IPIF-2",
            "MRBTS/TNLSVC-1/TNL-1/IPNO-1/IPIF-3",
        ]

        for mo in mo_elements:
            if mo.attrib.get("class", "") != "IPIF":
                continue

            dist_name = mo.attrib.get("distName", "")
            site_id = extract_site_id(dist_name)

            ipmtu_val = get_param_value(mo, "ipmtu", ns_uri)
            status_ip = "OK" if any(matches_path(req, dist_name) for req in REQUIRED_IPIF_DISTNAMES) else "Extra"

            ipmtu_rows.append({
                "file": xml_file.name,
                "site_id": site_id,
                "dist_name": dist_name,
                "ipMtu": ipmtu_val,
                "status": status_ip
            })

        # 2. FIXED PARAMETERS SECTION
        
        summary_rows = []

        # First, get all unique site IDs from your XML
        site_ids = set()
        for mo in mo_elements:
            dist_name = mo.attrib.get("distName", "")
            site_id = extract_site_id(dist_name)
            if site_id:
                site_ids.add(site_id)

        # Now, for each site, iterate over each parameter rule
        for site_id in site_ids:
            for rule in FIXED_PARAMETERS:
                param = rule["parameter"].lower().strip()
                mo_class = rule["mo_class"]

                # Find the MO that matches both site_id and mo_class
                value_found = "Missing"
                for mo in mo_elements:
                    dist_name = mo.attrib.get("distName", "")
                    if extract_site_id(dist_name) == site_id and matches_path(mo_class, dist_name):
                        value_found = get_param_value(mo, param, ns_uri)
                        break  # Take first match

                summary_rows.append({
                    "file": xml_file.name,
                    "site_id": site_id,
                    "mo_class": mo_class,
                    "parameter": param,
                    "value": value_found
                })

# ALARM SHEET DATA
# -------- Fixed Alarm Definitions --------

        # LIST_1 = {
        #     "MAINS FAIL": "Normally_open",
        #     "RECTIFIER FAIL": "Normally_open",
        #     "SITE ON BATTERY": "Normally_open",
        #     "AC FAIL or CANOPY FAN FAIL": "Normally_open",
        #     "FIRE AND SMOKE": "Normally_open",
        #     "DG ON LOAD": "Normally_open",
        #     "DG FAILED TO START": "Normally_open",
        #     "DG FAILED TO STOP": "Normally_open",
        #     "HIGH TEMPERATURE": "Normally_open",
        #     "DOOR OPEN": "Normally_open",
        #     "LOW BATTERY VOLTAGE": "Normally_open",
        #     "DG FUEL LEVEL LOW": "Normally_open",
        # }

        # LIST_2 = {
        #     "ACOC DOOR OPEN": "Normally_closed",
        #     "ACOC EXT FAN FAIL": "Normally_closed",
        #     "ACOC INT FAN FAIL": "Normally_closed",
        #     "ACOC OVER TEMPERATURE": "Normally_open",
        #     "MAINS FAIL": "Normally_open",
        #     "SITE ON BATTERY": "Normally_open",
        #     "LOW BATTERY VOLTAGE": "Normally_open",
        #     "DG ON LOAD": "Normally_open",
        #     "DG FUEL LEVEL LOW": "Normally_open",
        #     "DG FAILED TO START": "Normally_open",
        #     "HIGH TEMPERATURE": "Normally_open",
        #     "FIRE AND SMOKE": "Normally_open",
        # }


        # LIST_1_ORDER = {name: idx for idx, name in enumerate(LIST_1.keys())}
        # LIST_2_ORDER = {name: idx for idx, name in enumerate(LIST_2.keys())}



        # def valid_alarm_pair(descr, polarity):
        #     if descr in LIST_1 and LIST_1[descr] == polarity:
        #         return True
        #     if descr in LIST_2 and LIST_2[descr] == polarity:
        #         return True
        #     return False



        alarms = []
        if project_type == 'uls':
            max_alarms_per_site = 4
        elif project_type == 'nt relocation':
            max_alarms_per_site = 12
        else:
            max_alarms_per_site = None

        site_alarm_counts = {}

        for mo in mo_elements:
            dist_name = mo.attrib.get('distName', '')
            site_id = extract_site_id(dist_name)

            port_id = get_param_value(mo, "portid", ns_uri)
            descr = get_param_value(mo, "descr", ns_uri)
            polarity = get_param_value(mo, "polarity", ns_uri)

            if not (port_id and descr and polarity):
                continue

            if site_id not in site_alarm_counts:
                site_alarm_counts[site_id] = 0

            if max_alarms_per_site is None or site_alarm_counts[site_id] + 2 <= max_alarms_per_site:
                alarms.append({
                    "file": xml_file.name,
                    "site_id": site_id,
                    "mo_path": dist_name,
                    "parameter": "descr",
                    "Status": descr
                })
                alarms.append({
                    "file": xml_file.name,
                    "site_id": site_id,
                    "mo_path": dist_name,
                    "parameter": "polarity",
                    "Status": polarity
                })
                site_alarm_counts[site_id] += 2

        all_alarms.extend(alarms)

        # ---------------------------------------
        # 4. EXPECTED PARAMETER COMPARISON
        # ---------------------------------------
        for mo in mo_elements:
            dist_name = mo.attrib.get("distName", "")
            site_id = extract_site_id(dist_name)

            for path, params in expected_values.items():
                if not matches_path(path, dist_name):
                    continue

                for param_name, expected_value in params.items():
                    param_name = param_name.lower().strip()

                    # Get all values for this parameter in the current MO
                    def get_all_param_values(mo, param_name, ns_uri):
                        values = []
                        p_tag = f"{{{ns_uri}}}p" if ns_uri else "p"
                        for p in mo.findall(p_tag):
                            if p.attrib.get("name", "").lower() == param_name:
                                values.append(p.text.strip() if p.text else "")
                        return values

                    actual_values = get_all_param_values(mo, param_name, ns_uri)

                    # Skip if parameter does not exist in MO
                    if not actual_values:
                        continue

                    # Pick the value that matches DB (expected_value), if any
                    matching_value = next((v for v in actual_values if match_value(v, expected_value)), None)

                    if matching_value:
                        results.append({
                            "file": xml_file.name,
                            "site_id": site_id,
                            "mo_path": path,
                            "parameter": param_name,
                            "actual_value": matching_value,
                            "expected_value": expected_value,
                            "status": "OK"
                        })
                    # else:
                    #     # If none match DB, still log first actual value as NOT OK
                    #     results.append({
                    #         "file": xml_file.name,
                    #         "site_id": site_id,
                    #         "mo_path": path,
                    #         "parameter": param_name,
                    #         "actual_value": actual_values[0],
                    #         "expected_value": expected_value,
                    #         "status": "NOT OK"
                    #     })

        # ---------------------------------------
        # Deduplicate final outputs
        # ---------------------------------------
        all_alarms = deduplicate_alarms(all_alarms)

        df_results = pd.DataFrame(results).drop_duplicates(
            subset=["file", "site_id", "mo_path", "parameter", "actual_value", "expected_value"],
            keep="first"
        )

        df_alarms = pd.DataFrame(all_alarms).drop_duplicates(
            subset=["file", "site_id", "mo_path", "parameter", "Status"],
            keep="first"
        )

        df_summary = pd.DataFrame(summary_rows).drop_duplicates()

        df_ipmtu = pd.DataFrame(ipmtu_rows).drop_duplicates(
            subset=["file", "site_id", "dist_name", "ipMtu", "status"],
            keep="first"
        )
        # ---------------------------------------
        # SAVE EXCEL REPORT
        # ---------------------------------------
        report_folder = os.path.join(settings.MEDIA_ROOT, "reports")
        os.makedirs(report_folder, exist_ok=True)

        filename = f"report_{circle_name}.xlsx"
        filepath = os.path.join(report_folder, filename)

        with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
            df_results.to_excel(writer, index=False, sheet_name="Comparison")
            format_excel_sheet(writer, "Comparison", df_results)

            if not df_alarms.empty:
                df_alarms["sort_key"] = df_alarms["mo_path"].str.extract(r"EAC_IN-(\d+)$").astype(int)
                df_alarms["param_order"] = df_alarms["parameter"].map({"descr": 1, "polarity": 2})

                df_alarms = df_alarms.sort_values(
                    by=["site_id", "sort_key", "param_order"],
                    ascending=[True, True, True]
                ).drop(columns=["sort_key", "param_order"])


                # ---- Flattened Lists ----
                list1 = [
                    'MAINS FAIL', 'Normally_open',
                    'RECTIFIER FAIL', 'Normally_open',
                    'SITE ON BATTERY', 'Normally_open',
                    'AC FAIL or CANOPY FAN FAIL', 'Normally_open',
                    'FIRE AND SMOKE', 'Normally_open',
                    'DG ON LOAD', 'Normally_open',
                    'DG FAILED TO START', 'Normally_open',
                    'DG FAILED TO STOP', 'Normally_open',
                    'HIGH TEMPERATURE', 'Normally_open',
                    'DOOR OPEN', 'Normally_open',
                    'LOW BATTERY VOLTAGE', 'Normally_open',
                    'DG FUEL LEVEL LOW', 'Normally_open'
                ]

                list2 = [
                    'ACOC DOOR OPEN', 'Normally_closed',
                    'ACOC EXT FAN FAIL', 'Normally_closed',
                    'ACOC INT FAN FAIL', 'Normally_closed',
                    'ACOC OVER TEMPERATURE', 'Normally_open',
                    'MAINS FAIL', 'Normally_open',
                    'SITE ON BATTERY', 'Normally_open',
                    'LOW BATTERY VOLTAGE', 'Normally_open',
                    'DG ON LOAD', 'Normally_open',
                    'DG FUEL LEVEL LOW', 'Normally_open',
                    'DG FAILED TO START', 'Normally_open',
                    'HIGH TEMPERATURE', 'Normally_open',
                    'FIRE AND SMOKE', 'Normally_open'
                ]

                valid_orders = {
                    "list1": list1,
                    "list2": list2,
                    "list1_list2": list1 + list2,
                    "list2_list1": list2 + list1,
                }

                # ---- Detect order ----
                def detect_order(status_values, valid_orders):
                    scores = {}
                    for name, order in valid_orders.items():
                        score = 0
                        for s, o in zip(status_values, order):
                            if s == o:
                                score += 1
                            else:
                                break
                        scores[name] = score
                    return max(scores, key=scores.get)

                status_list = df_alarms["Status"].astype(str).tolist()
                detected_order = detect_order(status_list, valid_orders)
                expected_sequence = valid_orders[detected_order]

                # ---- Validation flag ----
                # df_alarms["Status_OK"] = [
                #     actual == expected
                #     for actual, expected in zip(status_list, expected_sequence)
                # ]

                status_ok = []

                for idx, actual in enumerate(status_list):
                    if idx < len(expected_sequence):
                        status_ok.append(actual == expected_sequence[idx])
                    else:
                        # extra rows beyond expected sequence = WRONG
                        status_ok.append(False)

                df_alarms["Status_OK"] = status_ok

                # ---- Write alarms sheet ----
                sheet_name = "Alarms"
                df_alarms.to_excel(writer, index=False, sheet_name=sheet_name)
                format_excel_sheet(writer, sheet_name, df_alarms)

                workbook = writer.book
                worksheet = writer.sheets[sheet_name]

                green_fmt = workbook.add_format({
                    "bg_color": "#4DC765",
                    "border": 1
                })
                red_fmt = workbook.add_format({
                    "bg_color": "#DB6976",
                    "border": 1
                })

                status_col_idx = df_alarms.columns.get_loc("Status")
                ok_col_idx = df_alarms.columns.get_loc("Status_OK")

                # ---- Apply coloring ----
                for row_idx in range(len(df_alarms)):
                    fmt = green_fmt if df_alarms.iloc[row_idx, ok_col_idx] else red_fmt
                    worksheet.write(
                        row_idx + 1,
                        status_col_idx,
                        df_alarms.iloc[row_idx, status_col_idx],
                        fmt
                    )

                # ---- Hide helper column ----
                worksheet.set_column(ok_col_idx, ok_col_idx, None, None, {"hidden": True})

            # df_alarms.to_excel(writer, index=False, sheet_name="Alarms")
            # format_excel_sheet(writer, "Alarms", df_alarms)

            # workbook  = writer.book
            # worksheet = writer.sheets["Alarms"]

            # red_fmt = workbook.add_format({"bg_color": "#F65353", "bold": True})
            # green_fmt = workbook.add_format({"bg_color": "#50CB50", "bold": True})

            # status_col = df_alarms.columns.get_loc("Status")

            # last_index_1 = -1
            # last_index_2 = -1

            # for i in range(0, len(df_alarms), 2):
            #     if i + 1 >= len(df_alarms):
            #         break

            #     descr = df_alarms.iloc[i]["Status"].strip()
            #     polarity = df_alarms.iloc[i + 1]["Status"].strip()

            #     # ---------- polarity check ----------
            #     if descr in LIST_1:
            #         expected_polarity = LIST_1[descr]
            #         list_type = 1
            #     elif descr in LIST_2:
            #         expected_polarity = LIST_2[descr]
            #         list_type = 2
            #     else:
            #         expected_polarity = None
            #         list_type = None

            #     polarity_ok = expected_polarity == polarity

            #     # ---------- order check ----------
            #     order_ok = True

            #     if list_type == 1:
            #         current_idx = LIST_1_ORDER[descr]
            #         if current_idx < last_index_1:
            #             order_ok = False
            #         last_index_1 = max(last_index_1, current_idx)

            #     elif list_type == 2:
            #         current_idx = LIST_2_ORDER[descr]
            #         if current_idx < last_index_2:
            #             order_ok = False
            #         last_index_2 = max(last_index_2, current_idx)

            #     # ---------- coloring ----------
            #     if not polarity_ok:
            #         descr_fmt = red_fmt
            #         polarity_fmt = red_fmt
            #     elif not order_ok:
            #         descr_fmt = red_fmt        # ❗ sirf descr red
            #         polarity_fmt = green_fmt
            #     else:
            #         descr_fmt = green_fmt
            #         polarity_fmt = green_fmt

            #     worksheet.write(i + 1, status_col, descr, descr_fmt)
            #     worksheet.write(i + 2, status_col, polarity, polarity_fmt)

            if not df_summary.empty:
                df_summary.to_excel(writer, index=False, sheet_name="FixedParameters")
                format_excel_sheet(writer, "FixedParameters", df_summary)

            if not df_ipmtu.empty:
                df_ipmtu.to_excel(writer, index=False, sheet_name="ipMtu Status")
                format_excel_sheet(writer, "ipMtu Status", df_ipmtu)
        api_usage_all(userId, api)
        return Response({
            "message": f"Report generated successfully for circle: {circle_name}",
            "download_link": request.build_absolute_uri(settings.MEDIA_URL + 'reports/' + filename),
            "status": True
        })


##################################################### summary ##############################
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_Summary_excel(request):
    userId = request.data.get('userId')
    api = "Summary Upload"

    excel_file = request.FILES.get('excel_file')
    if not excel_file:
        return Response({"error": "Excel file is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        df = pd.read_excel(excel_file)
        df = df.dropna(subset=['MO Class', 'Parameter'])
        
        SummaryData.objects.all().delete()
        errors = []

        for _, row in df.iterrows():
            data = {
                "MO_Class": str(row['MO Class']).strip(),
                "Parameter": str(row['Parameter']).strip(),
            
            }
            serializer = SummaryDataSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                errors.append(serializer.errors)

        if errors:
            return Response({"error": "Some rows failed validation", "details": errors}, status=status.HTTP_400_BAD_REQUEST)
        api_usage_all(userId, api)
        return Response({"status": True,"message": "Excel uploaded and saved successfully"},status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"Failed to process Excel file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    


    
@api_view(['GET','POST','PUT'])
def get_summary_data(request):
    userId = request.data.get('userId')
    api = "Summary Data"
    if request.method == 'GET':
        summary_data = SummaryData.objects.all()
        serializer = SummaryDataSerializer(summary_data, many=True)
        # api_usage_all(userId, api)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = SummaryDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            api_usage_all(userId, api)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT':
        try:
            param_id = request.data.get('id')
            if not param_id:
                return Response({'error': 'ID is required for update.'}, status=status.HTTP_400_BAD_REQUEST)

            summary_data = SummaryData.objects.get(id=param_id)
        except SummaryData.DoesNotExist:
            return Response({'error': 'SummaryData not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SummaryDataSerializer(summary_data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # api_usage_all(userId, api)
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    
####################################### summary report##########################################################################
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_summary_xml_files(request):
    userId = request.data.get('userId')
    api = "Summary Report Downloaded"
    xml_files = request.FILES.getlist('xml_files')
    circle_name = request.data.get('circle_name', 'default_circle').strip()
    project_type = request.data.get('project_type', 'project_type').strip()

    if not xml_files:
        return Response({"error": "At least one XML file is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Paths
    base_media_url = os.path.join(MEDIA_ROOT, "Soft_AT_Nokia")
    template_file_path = os.path.join(base_media_url, "template_file")
    output_dir = os.path.join(base_media_url, 'output_files')

    os.makedirs(template_file_path, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    template_path = os.path.join(template_file_path, "Sample Site_Soft AT.xlsx")
    output_path = os.path.join(output_dir, "AT_Summary_Filled.xlsx")

    # Load template ONCE (important)
    base_template_df = pd.read_excel(template_path, engine='openpyxl', sheet_name='Sheet1')

    all_dataframes = []

    # -----------------------------
    #       XML Extractor
    # -----------------------------
    def extract_data_from_xml(xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Namespace
        ns = {}
        if '}' in root.tag:
            ns = {'ns': root.tag.split('}')[0].strip('{')}

        def find(path): return root.find(path, ns)
        def findall(path): return root.findall(path, ns)

        all_sites = []

        for mrbts in findall(".//ns:managedObject[@class='MRBTS']"):
            data = {}

            # Dictionary for MRBTS
            p_dict = {
                p.attrib.get("name"): (p.text.strip() if p.text else "")
                for p in mrbts.findall("ns:p", ns)
            }

            dist_name = mrbts.attrib.get("distName", "")
            mrbts_id = dist_name.split("MRBTS-")[-1] if "MRBTS-" in dist_name else ""

            data["MRBTS_ID"] = mrbts_id
            data["MRBTS_Name"] = p_dict.get("btsName", "")

            # Site ID from name
            site_name = p_dict.get("btsName", "")
            data["Site_ID"] = site_name.split('_')[-1] if site_name else ""

            data["latitude"] = p_dict.get("latitude", "")
            data["longitude"] = p_dict.get("longitude", "")

            # ----------------- Latitude & Longitude -----------------
            # data["latitude"] = ""
            # for latitude in findall(".//ns:managedObject[@class='GNSSE_R']"):
            #     if mrbts_id in latitude.attrib.get("distName", ""):
            #         for p in latitude.findall("ns:p", ns):
            #             if p.attrib.get("name") == "gnssAntennaLatitude":
            #                 data["latitude"] = p.text.strip()
            #                 break
                    

            # data["longitude"] = ""
            # for longitude in findall(".//ns:managedObject[@class='GNSSE_R']"):
            #     if mrbts_id in longitude.attrib.get("distName", ""):
            #         for p in longitude.findall("ns:p", ns):
            #             if p.attrib.get("name") == "gnssAntennaLongitude":
            #                 data["longitude"] = p.text.strip()
            #                 break


            # ----------------- BCF -----------------
            bcfid = ""
            for gnbcf in findall(".//ns:managedObject[@class='GNBCF']"):
                if "distName" in gnbcf.attrib and mrbts_id in gnbcf.attrib["distName"]:
                    for p in gnbcf.findall("ns:p", namespaces=ns):
                        if p.attrib.get("name") == "bcfId":
                            bcfid = p.text.strip() if p.text else ""
                            break
            data["bcfid"] = bcfid

            # ----------------- SW Version -----------------
            data["swVersion"] = ""
            for hw in findall(".//ns:managedObject[@class='MNL_R']"):
                if mrbts_id in hw.attrib.get("distName", ""):
                    for p in hw.findall("ns:p", ns):
                        if p.attrib.get("name") == "activeSWReleaseVersion":
                            data["swVersion"] = p.text.strip()
                            break

            # ----------------- MPlane IP -----------------
            data["Mplane"] = ""

            for ip in root.findall(".//ns:managedObject", ns):
                dist = ip.attrib.get("distName", "")

                # Check for correct class AND IPIF-3 in distName
                if "IPIF-3" in dist and mrbts_id in dist:
                    for p in ip.findall("ns:p", ns):
                        if p.attrib.get("name") == "localIpAddrAllocated":
                            data["Mplane"] = p.text.strip()
                            break


            # ----------------- Cells -----------------
            # data["cells"] = []
            # for cell in findall(".//ns:managedObject[@class='NRCELLGRP']"):
            #     if mrbts_id in cell.attrib.get("distName", ""):
            #         # find the nrCellList list
            #         nr_list = cell.find("ns:list[@name='nrCellList']", ns)
            #         if nr_list is not None:
            #             # each entry is a <p> element containing the cell ID
            #             for item in nr_list.findall("ns:p", ns):
            #                 data["cells"].append({"LNCEL_ID": item.text.strip()})

            # ----------------- RET Count -----------------
            data["RET Count"] = len([
                r for r in findall(".//ns:managedObject[@class='RET']")
                if mrbts_id in r.attrib.get("distName", "")
            ])

            # ----------------- TAC -----------------
            data["TAC"] = ""
            for tracking in findall(".//ns:managedObject[@class='LNCEL']"):
                if mrbts_id in tracking.attrib.get("distName", ""):
                    for p in tracking.findall("ns:p", ns):
                        if p.attrib.get("name") == "tac":
                            data["TAC"] = p.text.strip()
                            break
            # tracking = find(".//ns:managedObject[@class='LNCEL']")
            # if tracking:
            #     for p in tracking.findall("ns:p", ns):
            #         if p.attrib.get("name") == "tac":
            #             data["TAC"] = p.text.strip()
            #             break

            # ----------------- LAC -----------------
            # data["LAC"] = ""
            # lnbts = find(".//ns:managedObject[@class='LNRELG']")
            # if lnbts:
            #     for p in lnbts.findall("ns:p", ns):
            #         if p.attrib.get("name") == "lac":
            #             data["LAC"] = p.text.strip()
            #             break

            # ----------------- Sync Status -----------------
            data["Sync Status"] = "Not Available"
            for clock in findall(".//ns:managedObject[@class='CLOCK']"):
                if mrbts_id in clock.attrib.get("distName", ""):
                    sync_list = clock.find("ns:list[@name='syncInputList']", ns)
                    if sync_list is not None:
                        for item in sync_list.findall("ns:item", ns):
                            for p in item.findall("ns:p", ns):
                                # We only need syncInputType
                                if p.attrib.get("name") == "syncInputType" and p.text:
                                    value = p.text.strip()
                                    if "GNSS" in value:
                                        data["Sync Status"] = "GPS"
                                    elif "Sync Hub Master" in value:
                                        data["Sync Status"] = "HUB"
                                    else:
                                        data["Sync Status"] = value
                                    break

            # ----------------- DPR Cell Name -----------------
            data["DPR_Cell_Name"] = ""
            for lncel in findall(".//ns:managedObject[@class='LNCEL']"):
                dist = lncel.attrib.get("distName", "")
                if mrbts_id in dist:
                    for p in lncel.findall("ns:p", ns):
                        if p.attrib.get("name") == "name":
                            data["DPR_Cell_Name"] = p.text.strip()
                            break

            # ----------------- Bands -----------------
            band_mapping = {
                "T1":"L2300",
                "T2": "L2300",
                "F1": "L2100",
                "F3": "L1800",
                "F8": "L900",
                "G1": "G900",
                "G3": "G1800"
            }

            band_set = set()
            for lncel in findall(".//ns:managedObject[@class='LNCEL']"):
                if mrbts_id in lncel.attrib.get("distName", ""):
                    for p in lncel.findall("ns:p", ns):
                        if p.attrib.get("name") == "name" and p.text:
                            cell_name = p.text.strip()
                            for code, band in band_mapping.items():
                                if code in cell_name:
                                    band_set.add(band)

            data["Band"] = "_".join(sorted(band_set)) if band_set else ""

            # ----------------- LCR_ID (LNCEL IDs) -----------------
            lncel_ids = []
            for lncel in findall(".//ns:managedObject[@class='LNCEL']"):
                dist = lncel.attrib.get("distName", "")
                if mrbts_id in dist:
                    match = re.search(r"LNCEL-(\d+)", dist)
                    if match:
                        lncel_ids.append(match.group(1))

            data["LCR_ID"] = "&".join(lncel_ids)

            # ----------Determine Activity Type based on project_type---------------------------------
            Activity_Type = []
            if project_type.lower() == 'uls':
                Activity_Type.append('NEW_TOWER_ULS')
            elif project_type.lower() == 'nt':
                Activity_Type.append('NEW_TOWER')
            elif project_type.lower() == 'relocation':
                Activity_Type.append('NT_Relocation')
            elif project_type.lower() == 'upgrade':
                Activity_Type.append('L2100_UPGRADE')

            data["Activity_Type"] = ",".join(Activity_Type) if Activity_Type else ""


            # Add to site list
            all_sites.append(data)

        return all_sites

    # -----------------------------
    #       Process each XML
    # -----------------------------
    for xml_file in xml_files:
        sites_data = extract_data_from_xml(xml_file)

        for data in sites_data:
            template_df = base_template_df.copy()

            # Static fields
            template_df.loc[0, 'OEM'] = 'Nokia'
            template_df.loc[0, 'AoP'] = '2025-26'
            template_df.loc[0, 'AT_Type'] = 'Soft_AT'
            template_df.loc[0, 'TSP'] = 'Mobilecomm'
            template_df.loc[0, 'Offer/Reoffer'] = 'OFFER'
            template_df.loc[0, 'Project Remarks'] = '4G GPL parameters are as per the guidelines is OK.'
            template_df.loc[0, 'SMP_ID'] = 'NA'
            template_df.loc[0, 'Media '] = 'Microwave'
            template_df.loc[0, 'Processed_By'] = 'Mobilecomm'
            template_df.loc[0, 'Tech_info'] = 'NT'
            template_df.loc[0, 'Tech'] = 'NT'
            template_df.loc[0, 'Activity Type'] = data.get("Activity_Type", '')
            template_df.loc[0, 'MRBTS_Name'] = data.get('MRBTS_Name', '')
            template_df.loc[0, 'Site_ID'] = data.get('Site_ID', '')
            template_df.loc[0, 'BCF'] = data.get('bcfid', '')
            template_df.loc[0, 'Latitude (N)'] = data.get('latitude', '')
            template_df.loc[0, 'Longitude (E)'] = data.get('longitude', '')
            template_df.loc[0, 'Profile'] = data.get("swVersion",'')
            template_df.loc[0, 'TAC'] = data.get('TAC', '')
            # template_df.loc[0, 'LAC'] = data.get('LAC', '')
            template_df.loc[0, 'RET Count'] = data.get('RET Count', '')
            template_df.loc[0, 'Sync Status'] = data.get('Sync Status', '')
            # template_df.loc[0, 'LNCEL_ID'] = data['cells'][0]['LNCEL_ID'] if data.get("cells") else ''
            template_df.loc[0, 'DPR_Cell_Name'] = data.get('DPR_Cell_Name', '')
            template_df.loc[0, 'Band'] = data.get('Band', '')
 
            

            # Dynamic (from XML)
            for key, value in data.items():
                if key in template_df.columns:
                    template_df.loc[0, key] = value

            template_df.loc[0, 'Circle'] = circle_name

            all_dataframes.append(template_df)

    # -----------------------------
    # Final Excel Output
    # -----------------------------
    final_df = pd.concat(all_dataframes, ignore_index=True)
    final_df.drop_duplicates(inplace=True)
    final_df = final_df.fillna("")

    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        final_df.to_excel(writer, index=False, sheet_name='Sheet1')
        format_excel_sheet(writer, 'Sheet1', final_df)

    relative_output_path = os.path.relpath(output_path, MEDIA_ROOT)
    download_link = request.build_absolute_uri(os.path.join(MEDIA_URL, relative_output_path).replace('\\', '/'))
    api_usage_all(userId, api)
    return Response({
        "message": f"Report generated successfully for circle: {circle_name}",
        "download_link": download_link,
        "status": True
    }, status=status.HTTP_200_OK)
