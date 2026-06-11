from django.shortcuts import render
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST 
from mcom_website.settings import MEDIA_ROOT, MEDIA_URL
from rest_framework import status
import xml.etree.ElementTree as ET
import re
import gzip
from .utils import *
import os


main_folder = os.path.join(MEDIA_ROOT, "VI_CheckPoint")

@api_view(["POST"])
def vi_tracker_dump(request):
    xml_files = request.FILES.getlist("file")

    if not xml_files:
        return Response({"error": "Please upload XML files"}, status=HTTP_400_BAD_REQUEST)
    
    output_folder = os.path.join(main_folder, "Output")
    os.makedirs(output_folder, exist_ok=True)



    required_parameters= {
    # NOKLTE:LNBTS------  
    "actCoMp",
    "actDLCAggr",
    "actFlexScellSelect",
    "actLBPowerSaving",
    "rrcGuardTimer",

    #"NOKLTE:LNCEL":-----------
    "actTtiBundling",
    "actUlpcMethod",
    "actVoipCovBoostEnh",
    "dlCaMinPcellCqiQci1",
    "harqMaxTrUlTtiBundling",
    "ttibOperMode",
    "ulsSchedMethod",
    "mdtxPdcchSymb",
    "actMicroDtx",
    "allowTrafficConcentration",
    "mdtxAggressiveness",
    "mdtxPdcchSymb",
    "ttibSinrThresholdIn",
    "scellFastSchedulingSelect",





    #"NOKLTE:LNHOG"------------
    "b2Threshold2RssiGERANQci1",

    #"NOKLTE:SIB"------------
    "qrxlevmin",

    # "NOKLTE:LNCEL_FDD"-------
    "dlRsBoost",
    "actDlMuMimo",
    "actFastMimoSwitch",
    "actMMimo",
    "actAutoPucchAlloc",
   


    

    #"NOKLTE:PSGRP"----
    "lbpsLastCellMinLoad",
    "lbpsLastCellRTXMinLoad",
    "lbpsLastCellSOEnabled",
    "lbpsMaxLoad",
    "lbpsMinLoad",
    "lbpsPdcchLoadOffset",
    "lbpsRTXCellCapOffset",
    "lbpsRTXMaxLoad",
    "lbpsRTXMinLoad",

    #"com.nokia.srbts.mnl:FMCADM"-----
    "actRadioFanFailureEarlyNotif",
    
    #com.nokia.srbts.eqm:RMOD--
    "alVoltHighThreshold",
    "alVoltLowThreshold",
    "alVoltUnstableThreshold",


}   
    wb = Workbook()
    wb.remove(wb.active)

    for file in xml_files:
        dumy_data = []
        file_name = file.name.lower()
       
        if file_name.endswith(".gz"):
            xml_bytes = gzip.decompress(file.read())
        else:
            xml_bytes = file.read()
        root = ET.fromstring(xml_bytes)

        # Namespace handling
        m = re.match(r'\{(.*)\}', root.tag)
        ns_url = m.group(1) if m else root.attrib.get("xmlns", "")
        ns = {"ns": ns_url} if ns_url else {}

        print(f"Namespace: {ns_url}")

        # Find managedObjects
        managed_objects = (root.findall(".//ns:managedObject", ns)
            if ns else
            root.findall(".//managedObject")
        )
        

        for mo in managed_objects:
            mo_class = mo.attrib.get("class", "")
            dist_name = mo.attrib.get("distName", "")

            if mo_class == "NOKLTE:LNBTS":
                params_lnbts = {}
                p_tags = (
                    mo.findall("ns:p", ns) if ns else mo.findall("p"))

                for p in p_tags:
                    name = p.attrib.get("name")
                    if name in required_parameters:
                        value = p.text
                        params_lnbts[name] = value
                        dumy_data.append({
                            "MO":"NOKLTE:LNBTS",
                            "DistName": dist_name,
                            "Parameter": name,
                            "Value": value
                        })

            elif mo_class == "NOKLTE:LNCEL":
                params_lncel = {}
                p_tags = (
                    mo.findall("ns:p", ns) if ns else mo.findall("p"))
                for p in p_tags:
                    name = p.attrib.get("name")

                    if name in required_parameters:
                        value = (p.text or "").strip()
                        params_lncel.setdefault(name, []).append(value)
                for name, values in params_lncel.items():
                    dumy_data.append({
                        "MO": "NOKLTE:LNCEL",
                        "DistName": dist_name,
                        "Parameter": name,
                        "Value": ";".join(values)
                    })



            elif mo_class =="NOKLTE:LNHOG":
                params_lnhog={}
                p_tags=(mo.findall("ns:p", ns)if ns else mo.findall("p")
                )
                for p in p_tags:
                    name = p.attrib.get("name")
                    if name in required_parameters:
                        value = p.text
                        params_lnhog[name] = value
                        dumy_data.append({

                            "MO":"NOKLTE:LNHOG",
                            "DistName": dist_name,
                            "Parameter": name,
                            "Value": value
                        })

            elif mo_class=="NOKLTE:SIB":
                params_sbi={}
                p_tags=(mo.findall("ns:p", ns)if ns else mo.findall("p")
                )
                for p in p_tags:
                    name = p.attrib.get("name")
                    if name in required_parameters:
                        value = p.text
                        params_sbi[name] = value
                        dumy_data.append({
                            "MO":"NOKLTE:SIB",
                            "DistName": dist_name,
                            "Parameter": name,
                            "Value": value
                        })
                

            elif mo_class == "NOKLTE:LNCEL_FDD":
                print("FDD FOUND:", dist_name)
                params_lncel_fdd = {}
                p_tags = mo.findall("ns:p", ns) if ns else mo.findall("p")
                for p in p_tags:
                    name = p.attrib.get("name", "").strip()

                    if name in required_parameters:

                        value = (p.text or "").strip()

                        params_lncel_fdd[name] = value

                        dumy_data.append({
                            "MO": "NOKLTE:LNCEL_FDD",
                            "DistName": dist_name,
                            "Parameter": name,
                            "Value": value
                        })

            elif mo_class == "NOKLTE:LNCEL_TDD":
                 print("TDD FOUND:", dist_name)
                 p_tags = mo.findall("ns:p", ns) if ns else mo.findall("p")
  
                 for p in p_tags:
                    name = p.attrib.get("name", "").strip()

                    if name in required_parameters:
                        dumy_data.append({
                            "MO": "NOKLTE:LNCEL_TDD",
                            "DistName": dist_name,
                            "Parameter": name,
                            "Value": p.text
                        })           
    
            
            elif mo_class == "NOKLTE:PSGRP":
                params_psgrp = {}
                p_tags = mo.findall(".//ns:p", ns) if ns else mo.findall(".//p")
                lbpsDayOfWeek = []
                lbpsDuration = []
                lbpsStartTimeHour = []
                lbpsStartTimeMinute = []
                lbpsSuspended = []

                for p in p_tags:
                    name = p.attrib.get("name")
                    value = p.text
                    if name == "lbpsDayOfWeek":
                        lbpsDayOfWeek.append(value)
                    elif name == "lbpsDuration":
                        lbpsDuration.append(value)
                    elif name == "lbpsStartTimeHour":
                        lbpsStartTimeHour.append(value)
                    elif name == "lbpsStartTimeMinute":
                        lbpsStartTimeMinute.append(value)
                    elif name == "lbpsSuspended":
                        lbpsSuspended.append(value)
                    if name in required_parameters:
                        params_psgrp[name] = value

                        dumy_data.append({
                            "MO": "NOKLTE:PSGRP",
                            "DistName": dist_name,
                            "Parameter": name,
                            "Value": value
                        })

                # Period List values-------
                dumy_data.append({
                    "MO": "NOKLTE:PSGRP",
                    "DistName": dist_name,
                    "Parameter": "lbpsDayOfWeek",
                    "Value": ";".join(lbpsDayOfWeek)
                })

                dumy_data.append({
                    "MO": "NOKLTE:PSGRP",
                    "DistName": dist_name,
                    "Parameter": "lbpsDuration",
                    "Value": ";".join(lbpsDuration)
                })

                dumy_data.append({
                    "MO": "NOKLTE:PSGRP",
                    "DistName": dist_name,
                    "Parameter": "lbpsStartTimeHour",
                    "Value": ";".join(lbpsStartTimeHour)
                })

                dumy_data.append({
                    "MO": "NOKLTE:PSGRP",
                    "DistName": dist_name,
                    "Parameter": "lbpsStartTimeMinute",
                    "Value": ";".join(lbpsStartTimeMinute)
                })

                dumy_data.append({
                    "MO": "NOKLTE:PSGRP",
                    "DistName": dist_name,
                    "Parameter": "lbpsSuspended",
                    "Value": ";".join(lbpsSuspended)
                })
            


            elif mo_class == "com.nokia.srbts.mnl:FMCADM":
                p_tags = mo.findall("ns:p", ns) if ns else mo.findall("p")

                for p in p_tags:
                    name = p.attrib.get("name")
                
                    if name == "actRadioFanFailureEarlyNotif":
                        value = p.text
                        dumy_data.append({
                            "MO": "com.nokia.srbts.mnl:FMCADM",
                            "DistName": dist_name,
                            "Parameter": name,
                            "Value": value
                        })

            elif mo_class == "com.nokia.srbts.eqm:RMOD":
                p_tags = mo.findall("ns:p", ns) if ns else mo.findall("p")

                for p in p_tags:
                    name = p.attrib.get("name")
                
                    if name in required_parameters:
                        value = p.text
                        dumy_data.append({
                            "MO": "com.nokia.srbts.eqm:RMOD",
                            "DistName": dist_name,
                            "Parameter": name,
                            "Value": value
                        })   

   
            elif mo_class == "com.nokia.srbts.tnl:IPIF":
                ipif_id = dist_name.split("/")[-1]      # IPIF-1, IPIF-2 ...
                p_tags = (
                    mo.findall("ns:p", ns)
                    if ns else
                    mo.findall("p")
                )

                for p in p_tags:

                    name = p.attrib.get("name", "").strip()

                    if name == "userLabel":

                        value = (p.text or "").strip()

                        dumy_data.append({
                            "Parameter": f"userLabel-{ipif_id}",
                            "Value": value
                        })

            elif mo_class in ["com.nokia.srbts.tnl:IPRT", "com.nokia.srbts.tnl:IPRTV6"]:
                iprt_id = dist_name.split("/")[-1]   # IPRT-3, IPRT-5, IPRTV6-1 ...
                p_tags = mo.findall("ns:p", ns) if ns else mo.findall("p")
                for p in p_tags:
                    name = p.attrib.get("name", "").strip()
                    if name == "userLabel":
                        value = (p.text or "").strip()
                        dumy_data.append({
                            "Parameter": f"userLabel(SR)-{iprt_id}",
                            "Value": value
                        })


            elif mo_class == "com.nokia.srbts:MRBTS":
                params_lnbts = {}
                p_tags = (
                    mo.findall("ns:p", ns) if ns else mo.findall("p"))

                for p in p_tags:
                    name = p.attrib.get("name")
                    if name == "btsName":
                        value = p.text
                        params_lnbts[name] = value
                        bts_name=value
        
        print(bts_name)
                
                         
        vi_df = pd.DataFrame(dumy_data)
        # vi_df.to_excel("dumy_vi.xlsx",index=False)

        vi_df = (
        vi_df.groupby(["Parameter"], as_index=False)
            .agg({
                "Value": lambda x: ";".join(sorted(set(map(str, x))))
            })
    )    
    
        found_params = set(vi_df["Parameter"])
        missing_rows = []

        for param in master_parameters:
            if param not in found_params:
                missing_rows.append({
                    "Parameter": param,
                    "Value": "Not Found In SCF"
                })

        if missing_rows:
            vi_df = pd.concat(
                [vi_df, pd.DataFrame(missing_rows)],
                ignore_index=True
            )
            
        vi_df.drop_duplicates(subset=["Parameter"], inplace=True)
        vi_df["Expected Value"] = vi_df["Parameter"].map(parameter_map)


        vi_df.loc[
        vi_df["Parameter"] == "ttibSinrThresholdIn",
        "Value"
    ] = (
        pd.to_numeric(
            vi_df.loc[
                vi_df["Parameter"] == "ttibSinrThresholdIn",
                "Value"
            ],
            errors="coerce"
        ) / 4
    ).astype(int).astype(str)

        # Existing code
        vi_df["Status"] = vi_df.apply(
            lambda row:
                "NOT FOUND"
                if row["Value"] == "Not Found In SCF"
                else check_status(
                    row["Value"],
                    row["Expected Value"]
                ),
            axis=1
        )


        
        vi_df.rename(
        columns={"Value": "Actual Value"},
        inplace=True
        )

        report_data = [vi_df.columns.tolist()] + vi_df.values.tolist()
        ws = wb.create_sheet(title=str(bts_name)[:31])

        create_config_report(ws, report_data)

        output_file = os.path.join(output_folder, "VI_Config_Report.xlsx")

        wb.save(output_file)


  
    relative_path = os.path.relpath(output_file, MEDIA_ROOT)

    download_url = request.build_absolute_uri(
        os.path.join(MEDIA_URL, relative_path).replace("\\", "/")
    )

    return Response({
        "status": True,
        "message":f"{len(xml_files)} SCF files parsed successfully.",
        "download_url": download_url
    }, status=HTTP_200_OK)

   