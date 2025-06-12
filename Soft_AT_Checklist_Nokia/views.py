
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
from .models import ExpectedParameter ,SummaryData
from  mcom_website.settings import MEDIA_ROOT
from .serializers import ExpectedParameterSerializer,SummaryDataSerializer
import json



#---------------------------project Type #--------------------

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
def matches_path(expected_path, dist_name):
    expected_parts = [p.split('-')[0].lower() for p in expected_path.split('/')]
    dist_parts = [p.split('-')[0].lower() for p in dist_name.split('/')]
    idx = 0
    for part in dist_parts:
        if idx < len(expected_parts) and part == expected_parts[idx]:
            idx += 1
    return idx == len(expected_parts)

# ------------------- Main API VieW ####################################################

@api_view(['GET', 'PUT', 'POST'])
def upload_and_compare_xml(request):
    if request.method == 'GET':
        expected_parameters = ExpectedParameter.objects.all()
        serializer = ExpectedParameterSerializer(expected_parameters, many=True)
        print(serializer.data)
        return Response(serializer.data)
    
    elif request.method == 'POST':
            serializer= ExpectedParameterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT':
        data = request.data
        serializer = ExpectedParameterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Upload Excel one-time and save expected values to DB
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_excel(request):
    excel_file = request.FILES.get('excel_file')
    if not excel_file:
        return Response({"error": "Excel file is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        df = pd.read_excel(excel_file)
        df = df.dropna(subset=['MO Class', 'Parameter', 'Value'])

        ExpectedParameter.objects.all().delete()  # Optional: clean slate
        errors = []

        for _, row in df.iterrows():
            data = {
                "path": str(row['MO Class']).strip(),
                "parameter_name": str(row['Parameter']).strip(),
                "expected_value": str(row['Value']).strip(),
            }
            serializer = ExpectedParameterSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                errors.append(serializer.errors)

        if errors:
            return Response({"error": "Some rows failed validation", "details": errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Excel uploaded and saved successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"Failed to process Excel file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


# Upload XMLs and compare with database values
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_and_compare_xml_files(request):
    xml_files = request.FILES.getlist('xml_files')
    circle_name = request.data.get('circle_name', 'default_circle').strip()
    project_type = request.data.get('project_type', 'project_type').strip()


    if not xml_files:
        return Response({"error": "At least one XML file is required"}, status=status.HTTP_400_BAD_REQUEST)

    expected_params = ExpectedParameter.objects.all()
    serializer = ExpectedParameterSerializer(expected_params, many=True)
    expected_params_json = serializer.data
 
    expected_values = {}
    print("expected_params", expected_params_json)
    for param in expected_params_json:
        norm_path = normalize_path(param['path'])  # Access via dictionary keys
        if norm_path not in expected_values:
            expected_values[norm_path] = {}
        expected_values[norm_path][param['parameter_name'].lower()] = param['expected_value']

   

    # process_xml_files(xml_files, project_type, expected_values)
    results = []
    


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

        for mo in mo_elements:
            dist_name = mo.attrib.get('distName', '')

            for path, param_dict in expected_values.items():
                if not matches_path(path, dist_name):
                    continue

                for param_name, expected_value in param_dict.items():
                    actual_value = ''
                    p_tag = f"{{{ns_uri}}}p" if ns_uri else 'p'
                    for p in mo.findall(p_tag):
                        if p.attrib.get('name', '').strip().lower() == param_name.strip().lower():
                            actual_value = (p.text or '').strip()
                            break

             
                    results.append({
                        "file": xml_file.name,
                        "site_id": extract_site_id(dist_name),
                        "mo_path": path,
                        "parameter": param_name,
                        "actual_value": actual_value,
                        "expected_value": expected_value,
                        "status": "OK" if match_value(actual_value, expected_value) else "NOT OK"
                    })

   
    # Save result
    report_folder = os.path.join(MEDIA_ROOT, 'reports')
    os.makedirs(report_folder, exist_ok=True)

    filename = f"report_{circle_name}.xlsx"
    filepath = os.path.join(report_folder, filename)

    df_results = pd.DataFrame(results)
    df_results.drop_duplicates(
        subset=['file', 'site_id', 'mo_path', 'parameter', 'actual_value', 'expected_value'],
        keep='first', inplace=True
    )

    with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
        df_results.to_excel(writer, index=False, sheet_name='Sheet1')
        format_excel_sheet(writer,"Sheet1" ,df_results )

    download_link = request.build_absolute_uri(settings.MEDIA_URL + 'reports/' + filename)

    return Response({
        "message": f"Report generated successfully for circle: {circle_name}",
        "download_link": download_link,
        "status": True
    }, status=status.HTTP_200_OK)



#####################################################abhinav##############################
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_Summary_excel(request):
    excel_file = request.FILES.get('excel_file')
    if not excel_file:
        return Response({"error": "Excel file is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        df = pd.read_excel(excel_file)
        df = df.dropna(subset=['MO Class', 'Parameter'])

        SummaryData.objects.all()
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

        return Response({"message": "Excel uploaded and saved successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"Failed to process Excel file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    


    
@api_view(['GET','POST','PUT'])
def get_summary_data(request):
    if request.method == 'GET':
        summary_data = SummaryData.objects.all()
        serializer = SummaryDataSerializer(summary_data, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = SummaryDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
####################################### work for summary report##########################################################################

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_summary_xml_files(request):
    xml_files = request.FILES.getlist('xml_files')
    circle_name = request.data.get('circle_name', 'default_circle').strip()

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
    
    
    all_dataframes = []
    def extract_data_from_xml(xml_file):
        data = {}
        tree = ET.parse(xml_file)
        root = tree.getroot()
        ns = {'ns': root.tag.split('}')[0].strip('{')} if '}' in root.tag else {}

        def findall(path):
            return root.findall(path, namespaces=ns)

        def find(path):
            return root.find(path, namespaces=ns)
        ################################mmmmmmmmmmm
        all_sites = []

        for mrbts in findall(".//ns:managedObject[@class='MRBTS']"):
            data = {}
            p_dict = {
                p.attrib.get("name"): p.text.strip()
                for p in mrbts.findall("ns:p", namespaces=ns)
                if p.text
            }

            dist_name = mrbts.attrib.get("distName", "")
            mrbts_id = dist_name.split("MRBTS-")[-1] if "MRBTS-" in dist_name else ""

            data["MRBTS_ID"] = mrbts_id
            data["MRBTS_Name"] = p_dict.get("btsName", "")
            data["latitude"] = p_dict.get("latitude", "")
            data["longitude"] = p_dict.get("longitude", "")

            # BCF (from matching GNBCF with same MRBTS?)
            bcfid = ""
            for gnbcf in findall(".//ns:managedObject[@class='GNBCF']"):
                if "distName" in gnbcf.attrib and mrbts_id in gnbcf.attrib["distName"]:
                    for p in gnbcf.findall("ns:p", namespaces=ns):
                        if p.attrib.get("name") == "bcfId":
                            bcfid = p.text.strip() if p.text else ""
                            break
            data["bcfid"] = bcfid

            # swVersion
            swVersion = ""
            for hw in findall(".//ns:managedObject[@class='HW']"):
                if "distName" in hw.attrib and mrbts_id in hw.attrib["distName"]:
                    for p in hw.findall("ns:p", namespaces=ns):
                        if p.attrib.get("name") == "swVersion":
                            swVersion = p.text.strip() if p.text else ""
                            break
            data["swVersion"] = swVersion

            # NRCELLGRP
            data["cells"] = []
            for cell in findall(".//ns:managedObject[@class='NRCELLGRP']"):
                if mrbts_id in cell.attrib.get("distName", ""):
                    for p in cell.findall("ns:p", namespaces=ns):
                        if p.attrib.get("name") == "nrCellList":
                            data["cells"].append({"LNCEL_ID": p.text.strip()})

            # RET Count
            data["RET Count"] = len([
                r for r in findall(".//ns:managedObject[@class='RET']")
                if mrbts_id in r.attrib.get("distName", "")
            ])

            # TAC
            tracking = find(".//ns:managedObject[@class='TRACKINGAREA']")
            if tracking:
                for p in tracking.findall("ns:p", namespaces=ns):
                    if p.attrib.get("name") == "fiveGsTac":
                        data["TAC"] = p.text.strip() if p.text else ""
                        break

            # LAC
            lnbts = find(".//ns:managedObject[@class='LNBTS']")
            if lnbts:
                for p in lnbts.findall("ns:p", namespaces=ns):
                    if p.attrib.get("name") == "lac":
                        data["LAC"] = p.text.strip() if p.text else ""
                        break
            sync_status = "Not Available"

            for clock in root.findall(".//ns:managedObject[@class='CLOCK']", namespaces=ns):
                if mrbts_id in clock.attrib.get("distName", ""):
                    for sync_list in clock.findall("ns:list[@name='syncInputList']", namespaces=ns):
                        for item in sync_list.findall("ns:item", namespaces=ns):
                            for p in item.findall("ns:p", namespaces=ns):
                                if p.attrib.get("name") == "syncInputType":
                                    print("Sync Input Type:", p.text)
                                    if p.text and "GNSS" in p.text:
                                        sync_status = "GPS"
                                        break
            all_sites.append(data)

        return all_sites

    # Process each file
    for xml_file in xml_files:
        sites_data = extract_data_from_xml(xml_file)

        for data in sites_data:
            template_df = pd.read_excel(template_path, engine='openpyxl', sheet_name='Sheet1')
            template_df.loc[0, 'OEM'] = 'Nokia'

            template_df.loc[0, 'MRBTS_ID'] = data.get('MRBTS_ID', '')
            template_df.loc[0, 'MRBTS_Name'] = data.get('MRBTS_Name', '')
            template_df.loc[0, 'BCF'] = data.get('bcfid', '')
            template_df.loc[0, 'Latitude (N)'] = data.get('latitude', '')
            template_df.loc[0, 'Longitude (E)'] = data.get('longitude', '')
            template_df.loc[0, 'Profile'] = data.get('swVersion', '')
            template_df.loc[0, 'TAC'] = data.get('TAC', '')
            template_df.loc[0, 'LAC'] = data.get('LAC', '')
            template_df.loc[0, 'RET Count'] = data.get('RET Count', '')
            template_df.loc[0, 'Sync Status'] = data.get('Sync Status', '')
            template_df.loc[0, 'LNCEL_ID'] = data['cells'][0]['LNCEL_ID'] if data.get("cells") else ''

            all_dataframes.append(template_df)

    # Combine all
    final_df = pd.concat(all_dataframes, ignore_index=True)

    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        final_df.to_excel(writer, index=False, sheet_name='Sheet1')
        format_excel_sheet(writer, 'Sheet1', final_df)

    # Build download link
    relative_output_path = os.path.relpath(output_path, MEDIA_ROOT)
    download_link = request.build_absolute_uri(os.path.join(MEDIA_URL, relative_output_path).replace('\\', '/'))

    return Response({
        "message": f"Report generated successfully for circle: {circle_name}",
        "download_link": download_link,
        "status": True
    }, status=status.HTTP_200_OK)
        