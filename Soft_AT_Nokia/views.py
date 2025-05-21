
import os
import pandas as pd
import xml.etree.ElementTree as ET
from django.conf import settings
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
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


########################################## soft at summary ##########################

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