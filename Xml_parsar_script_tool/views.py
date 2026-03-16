import pandas as pd
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from mcom_website.settings import MEDIA_ROOT, MEDIA_URL
import xml.etree.ElementTree as ET
import re
import math
import gzip


def convert_int(val):
    s = str(val).strip()
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    else:
        return val


def in_excel(df, writer, sheet_name):
    """
    Save DataFrame to Excel with chunking if rows exceed Excel limit.
    """
    max_rows = 1_048_000
    total_rows = len(df)
    num_sheets = math.ceil(total_rows / max_rows)

    start = 0
    for i in range(num_sheets):
        end = start + max_rows
        chunk_df = df.iloc[start:end]

        if num_sheets == 1:
            chunk_df.to_excel(writer, sheet_name=sheet_name, index=False)
        else:
            chunk_df.to_excel(writer, sheet_name=f"{sheet_name}_{i+1}", index=False)

        start = end


@api_view(["POST"])
def xml_bulk_to_excel(request):
    try:

        xml_files = request.FILES.getlist("xml_files")

        if not xml_files:
            return Response({"error": "Please upload XML files"}, status=HTTP_400_BAD_REQUEST)

        main_folder = os.path.join(MEDIA_ROOT, "Xml_parsar_script")
        output_folder = os.path.join(main_folder, "Parsed_Output")
        os.makedirs(output_folder, exist_ok=True)

        parse_data = []
        xnlink_data = []

        for file in xml_files:

            try:

                file_name = file.name.lower()

                if file_name.endswith(".gz"):
                    xml_bytes = gzip.decompress(file.read())
                else:
                    xml_bytes = file.read()

                root = ET.fromstring(xml_bytes)

                m = re.match(r"\{(.*)\}", root.tag)
                ns_url = m.group(1) if m else root.attrib.get("xmlns", "")
                ns = {"ns": ns_url} if ns_url else {}

                managed_objects = root.findall(".//ns:managedObject", ns) if ns else []

                if not managed_objects:
                    managed_objects = root.findall(".//managedObject")

                for mo in managed_objects:

                    record = {
                        "File_Name": file.name,
                        "SW_Version": mo.get("version"),
                        "distName": mo.get("distName", ""),
                        "id": mo.get("id", "")
                    }

                    mo_class = mo.get("class", "")
                    distname = mo.get("distName", "")

                    p_tags = mo.findall("ns:p", ns) if ns else []

                    if not p_tags:
                        p_tags = mo.findall("p")

                    for p in p_tags:
                        key = p.get("name")
                        value = (p.text or "").strip()
                        record[key] = value

                    # ---- XNLINK condition ----
                    if mo_class == "XNLINK" or "XNLINK-" in distname:
                        xnlink_data.append(record)
                    else:
                        parse_data.append(record)

            except Exception as e:

                parse_data.append({
                    "File_Name": file.name,
                    "Error": f"Error parsing XML: {str(e)}"
                })

        # ---------------- LNADJGNB DATA ---------------- #

        dump_df = pd.DataFrame(parse_data)

        if not dump_df.empty:

            dump_df[["MRBTS", "LNBTS", "LNADJGNB"]] = dump_df["distName"].str.extract(
                r"MRBTS-*(\d+).*LNBTS-*(\d+).*LNADJGNB-*(\d+)", expand=True
            )

            priority_cols = ["MRBTS", "LNBTS", "LNADJGNB", "id"]
            remaining_cols = [c for c in dump_df.columns if c not in priority_cols]

            dump_df = dump_df[priority_cols + remaining_cols]

        # ---------------- XNLINK DATA ---------------- #

        xnlink_df = pd.DataFrame(xnlink_data)

        if not xnlink_df.empty:

            xnlink_df[["MRBTS", "NRBTS", "XNLINK"]] = xnlink_df["distName"].str.extract(
                r"MRBTS-(\d+).*NRBTS-(\d+).*XNLINK-(\d+)", expand=True
            )

            priority_cols = ["MRBTS", "NRBTS", "XNLINK", "id"]
            remaining_cols = [c for c in xnlink_df.columns if c not in priority_cols]

            xnlink_df = xnlink_df[priority_cols + remaining_cols]

        output_path = os.path.join(output_folder, "Dump_Parsed_Output.xlsx")

        with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:

            if not dump_df.empty:
                in_excel(dump_df, writer, "LNADJGNB")

            if not xnlink_df.empty:
                in_excel(xnlink_df, writer, "XNLINK")

      

        relative_path = os.path.relpath(output_path, MEDIA_ROOT)

        download_url = request.build_absolute_uri(
            os.path.join(MEDIA_URL, relative_path).replace("\\", "/")
        )

        return Response({
            "status": True,
            "message": "All XML files successfully parsed",
            "download_url": download_url
        }, status=HTTP_200_OK)

    except Exception as e:

        return Response({
            "find an error": str(e)
        }, status=HTTP_400_BAD_REQUEST)