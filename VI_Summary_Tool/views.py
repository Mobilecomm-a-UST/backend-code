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
import os
from .utils import format_excel


main_folder = os.path.join(MEDIA_ROOT, "VI_Summary")

@api_view(["GET", "POST", "DELETE"])
def vi_summary_template(request):
    print("Start Process_________")
    folder = os.path.join(main_folder, "template")
    os.makedirs(folder, exist_ok=True)

    if request.method == 'POST':
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file uploaded'}, status=400)

        path = os.path.join(folder, file.name)

        with open(path, 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)

        return Response({'status': True, 'file': file.name})

    if request.method == 'GET':
        return Response({'files': os.listdir(folder)})

    if request.method == 'DELETE':
        for f in os.listdir(folder):
            os.remove(os.path.join(folder, f))
        return Response({'status': True, 'message': 'All files deleted'})
    


@api_view(["POST"])
def vi_4g_summary(request):
    circle = request.POST.get("circle")
    xml_files = request.FILES.getlist("file")
    if not xml_files:
        return Response( {"error": "Please upload XML files"}, status=HTTP_400_BAD_REQUEST)
    

    temp_folder = os.path.join(main_folder, "template")
    if not os.path.isdir(temp_folder):
        return Response({"error": "Template folder not found"}, status=400)
    file_list = [
        file for file in os.listdir(temp_folder)
        if os.path.isfile(os.path.join(temp_folder, file))
    ]

    print(file_list)

    output_folder = os.path.join(main_folder, "Output")
    os.makedirs(output_folder, exist_ok=True)

    dumy_data1 = []
    lnadjgnb_data=[]
    iprtv6_data = []
    nrcell_data=[]
    for file in xml_files:
        file_name = file.name.lower()

        # Read xml/gz file
        if file_name.endswith(".gz"):
            xml_bytes = gzip.decompress(file.read())
        else:
            xml_bytes = file.read()

        root = ET.fromstring(xml_bytes)

        # Namespace handling
        m = re.match(r"\{(.*)\}", root.tag)
        ns_url = m.group(1) if m else root.attrib.get("xmlns", "")
        ns = {"ns": ns_url} if ns_url else {}

        managed_objects = (
            root.findall(".//ns:managedObject", ns)
            if ns else root.findall(".//managedObject")
        )

#--------------------------
        mrbts_id = ""
        nrbts_id=""
        lnbts_id=""
        bts_name = ""
        version = ""
        ip = ""
        enode=""
        lncel_id=""
        mme_ip_0 = ""
        mme_ip_4 = ""
        mme_ip_1=""
        sgw_ips = [""] * 11   # SGW1 to SGW11
        ntp_ip1=""
        ntp_ip2=""
        

      
    
        


    
        for mo in managed_objects:
            mo_class = mo.attrib.get("class", "")
            if mo_class == "com.nokia.srbts:MRBTS":
                dist_name = mo.attrib.get("distName", "")
                version = mo.attrib.get("version", "")

                mrbts_id = dist_name.split("-")[-1]
                p_tags = (
                    mo.findall("ns:p", ns)
                    if ns else mo.findall("p"))
                for p in p_tags:
                    if p.attrib.get("name") == "btsName":
                        bts_name = p.text
                        break

            elif mo_class == "com.nokia.srbts.tnl:IPADDRESSV4":
                p_tags = (
                    mo.findall("ns:p", ns)
                    if ns else mo.findall("p")
                )
                for p in p_tags:
                    if p.attrib.get("name") == "localIpAddr":
                        ip = p.text
                        break
            
            elif mo_class =="NOKLTE:LNBTS":
                dist_name = mo.attrib.get("distName", "")
                lnbts_id = dist_name.split("/")[-1].split("-")[-1]
                p_tags = (
                    mo.findall("ns:p", ns)
                    if ns else mo.findall("p")
                )
                for p in p_tags:
                    if p.attrib.get("name") == "enbName":
                        enode = p.text
                        break

            elif mo_class == "NOKLTE:LNCEL":    
                dist_name = mo.attrib.get("distName", "")
                lncel_id = dist_name.split("/")[-1].split("-")[-1]   

            elif mo_class == "com.nokia.srbts.nrbts:NRBTS":
                dist_name = mo.attrib.get("distName", "")
                nrbts_id = dist_name.split("/")[-1].split("-")[-1]  


            elif mo_class == "NOKLTE:LNMME": 
                dist_name = mo.attrib.get("distName", "")
                lnmme_id = dist_name.split("/")[-1].split("-")[-1]
                p_tags = mo.findall("ns:p", ns) if ns else mo.findall("p")
                for p in p_tags:
                    if p.attrib.get("name") == "ipAddrPrim":
                        ip = p.text
                        break

                if lnmme_id == "0":
                    mme_ip_0 = ip
                elif lnmme_id=="1":
                    mme_ip_1 = ip    
                elif lnmme_id == "4":
                    mme_ip_4 = ip

            elif mo_class == "NOKLTE:GTPU":
                items = mo.findall(".//ns:list[@name='sgwIpAddressList']/ns:item", ns) \
                    if ns else mo.findall(".//list[@name='sgwIpAddressList']/item")
                for idx, item in enumerate(items[:11]):
                    p_tags = item.findall("ns:p", ns) if ns else item.findall("p")
                    for p in p_tags:
                        if p.attrib.get("name") == "sgwIpAddress":
                            sgw_ips[idx] = p.text
                            break      

            elif mo_class=="com.nokia.srbts.mnl:NTP":
                ntp_list = (
                    mo.find("ns:list[@name='ntpServerIpAddrOrFqdnList']", ns)
                    if ns else
                    mo.find("list[@name='ntpServerIpAddrOrFqdnList']")
                )
                if ntp_list is not None:
                    p_list = (
                        ntp_list.findall("ns:p", ns)
                        if ns else
                        ntp_list.findall("p")
                    )
                    if len(p_list) > 0:
                        ntp_ip1 = p_list[0].text
                    if len(p_list) > 1:
                        ntp_ip2 = p_list[1].text   

            elif mo_class == "NOKLTE:LNADJGNB":
                dist_name = mo.attrib.get("distName", "")
                mrbts_id = dist_name.split("/")[0].split("-")[-1]
                lnbts_id = dist_name.split("/")[1].split("-")[-1]
                lnadjgnb_id = dist_name.split("/")[2].split("-")[-1]

                row = {
                    "MRBTS": mrbts_id,
                    "LNBTS": lnbts_id,
                    "LNADJGNB": lnadjgnb_id
                }

                p_tags = (
                    mo.findall("ns:p", ns)
                    if ns else mo.findall("p")
                )

                for p in p_tags:
                    name = p.attrib.get("name")

                    if name == "adjGnbId":
                        row["adjGnbId"] = p.text

                    elif name == "adjGnbIdLength":
                        row["adjGnbIdLength"] = p.text

                    elif name == "administrativeState":
                        row["administrativeState"] = p.text

                    elif name == "cPlaneIpAddr":
                        row["cPlaneIpAddr"] = p.text

                lnadjgnb_data.append(row) 

            elif mo_class == "com.nokia.srbts.tnl:IPRTV6":
                dist_name = mo.attrib.get("distName", "")
                mrbts = dist_name.split("/")[0].split("-")[-1]
                iprtv6 = dist_name.split("/")[-1].split("-")[-1]
                row = {
                    "MRBTS": mrbts,
                    "IPRTV6": iprtv6
                }
                # userLabel
                p_tags = mo.findall("ns:p", ns) if ns else mo.findall("p")
                for p in p_tags:
                    if p.attrib.get("name") == "userLabel":
                        row["userLabel"] = p.text

                # gatewayIpv6Addr
                items = (
                    mo.findall(".//ns:list[@name='staticIpv6Routes']/ns:item", ns)
                    if ns else
                    mo.findall(".//list[@name='staticIpv6Routes']/item")
                )

                for item in items:
                    p_tags = item.findall("ns:p", ns) if ns else item.findall("p")
                    for p in p_tags:
                        if p.attrib.get("name") == "gatewayIpv6Addr":
                            row["gatewayIpv6Addr"] = p.text
                            break

                iprtv6_data.append(row)     

            
            elif mo_class == "com.nokia.srbts.nrbts:NRCELL":
                dist_name = mo.attrib.get("distName", "")

                mrbts_id = dist_name.split("/")[0].split("-")[-1]
                nrbts_id = dist_name.split("/")[1].split("-")[-1]
                nrcell_id = dist_name.split("/")[-1].split("-")[-1]

                row = {
                    "MRBTS": mrbts_id,
                    "NRBTS": nrbts_id,
                    "NRCELL": nrcell_id
                }

                p_tags = (
                    mo.findall("ns:p", ns)
                    if ns else mo.findall("p")
                )

                for p in p_tags:
                    name = p.attrib.get("name")

                    if name in ["pMax", "chBw", "nrarfcn"]:
                        row[name] = p.text

                nrcell_data.append(row)
            
        row = {
            "MRBTS_ID": mrbts_id,
            "BTS_Name": bts_name,
            "Version": version,
            "IP": ip,
            "eNode": enode,
            "LNBTS_ID": lnbts_id,
            "LNCel_ID": lncel_id,
            "mme_ip_0": mme_ip_0,
            "mme_ip_4": mme_ip_4,
            "mme_ip_1": mme_ip_1,
            "nrbts_id": nrbts_id.strip() if nrbts_id and nrbts_id.strip() else mrbts_id,
            "ntp_ip1": ntp_ip1,
            "ntp_ip2": ntp_ip2,
            "nrcell_id":nrcell_id,
            "circle":circle 
          
        

        }

        for i in range(11):
            row[f"sgw_ip_{i+1}"] = sgw_ips[i]

        dumy_data1.append(row)

    dumy = pd.DataFrame(dumy_data1)  
    if lnadjgnb_data:
        lnadjgnb_df = pd.DataFrame(lnadjgnb_data)
    else:
        lnadjgnb_df = pd.DataFrame(columns=[
             "MRBTS",
             "LNBTS",
            "LNADJGNB",
            "adjGnbId",
            "adjGnbIdLength",
            "administrativeState",
            "cPlaneIpAddr"
        ])

    if iprtv6_data:
        iprtv6_df = pd.DataFrame(iprtv6_data)
    else:
        iprtv6_df = pd.DataFrame(columns=[
            "MRBTS",
            "IPRTV6",
            "userLabel",
            "gatewayIpv6Addr"
        ])
    if nrcell_data:
        nr_df = pd.DataFrame(nrcell_data)
    else:
        nr_df = pd.DataFrame(columns=[
            "MRBTS",
            "NRBTS",
            "NRCELL",
            "pMax",
            "chBw",
            "nrarfcn"
            
        ])    
#for Commercial Radiation sheet-----
    cr_df = pd.read_excel(os.path.join(temp_folder, "Reference_Data_4g.xlsx"), sheet_name="Commercial Radiation")
    cr_df.columns = cr_df.columns.str.strip()
    cr_df = pd.concat([cr_df] * len(dumy), ignore_index=True)
    parts = dumy["BTS_Name"].str.split("_")

    cr_df["Site Name"] = parts.apply(
        lambda x: x[-2] if x[-1].upper() == "SRAN" else x[-1]
    )
    cr_df["Circle Name"]=dumy["circle"]
    cr_df["MRBTS ID (As per OSS Snap)"] = dumy["MRBTS_ID"]
    cr_df["MRBTS Name"] = dumy["BTS_Name"]
    cr_df["MRBTS IP"] = dumy["IP"]
    cr_df["Current SW Version"] =dumy["Version"]
    cr_df["TSP Site ID"] = dumy["eNode"].str[6:]
    
    mrbts_df=pd.read_excel(os.path.join(temp_folder, "Reference_Data_4g.xlsx"), sheet_name="MRBTS")
    mrbts_df.columns = mrbts_df.columns.str.strip()
    mrbts_df = pd.concat([mrbts_df] * len(dumy), ignore_index=True)
    mrbts_df["MRBTS ID"] =  dumy["MRBTS_ID"]
    mrbts_df["name"] = dumy["BTS_Name"]
    mrbts_df["btsName"] = dumy["BTS_Name"]
    mrbts_df["siteTemplateDescription"] = dumy["eNode"].str[6:]

    lnbts_df=pd.read_excel(os.path.join(temp_folder, "Reference_Data_4g.xlsx"), sheet_name="LNBTS")
    lnbts_df.columns = lnbts_df.columns.str.strip()
    lnbts_df = pd.concat([lnbts_df] * len(dumy), ignore_index=True)
    lnbts_df["MRBTS ID"] =  dumy["MRBTS_ID"]
    lnbts_df["LNBTS ID"] = dumy["LNBTS_ID"]
    lnbts_df["name (User label)"] = dumy["BTS_Name"]
    lnbts_df["enbName"] = dumy["eNode"].str[2:]


    nrcell_df=pd.read_excel(os.path.join(temp_folder, "Reference_Data_4g.xlsx"), sheet_name="NRCELL")
    nrcell_df.columns = nrcell_df.columns.str.strip()
    if nrcell_df.empty:
        nrcell_df = pd.concat([nrcell_df] * len(nr_df),ignore_index=True)
        nrcell_df["MRBTS"] = nr_df["MRBTS"].values
        nrcell_df["NRBTS"] = nr_df["NRBTS"].values
        nrcell_df["NRCELL"] = nr_df["NRCELL"].values
        # nrcell_df["name"] = nr_df["adjGnbId"].values
        nrcell_df["pMax"] =nr_df["pMax"].values
        nrcell_df["nrarfcn"] = nr_df["nrarfcn"].values
        nrcell_df["chBw"] = nr_df["chBw"].values

        name_map = (
            dumy[["MRBTS_ID", "eNode"]]
            .drop_duplicates(subset="MRBTS_ID", keep="first")
            .set_index("MRBTS_ID")["eNode"]
        )

        nrcell_df["name"] = nrcell_df["MRBTS"].map(name_map)

    


    else:     
         nrcell_df =  nrcell_df.iloc[0:0].copy()
    
    lncel_df=pd.read_excel(os.path.join(temp_folder, "Reference_Data_4g.xlsx"), sheet_name="LNCEL")
    lncel_df.columns = lncel_df.columns.str.strip()
    lncel_df = pd.concat([lncel_df] * len(dumy), ignore_index=True)
    lncel_df["MRBTS ID"] =  dumy["MRBTS_ID"]
    lncel_df["LNBTS ID"] =  dumy["LNBTS_ID"]
    lncel_df["LNCEL"] = dumy["LNCel_ID"]
    lncel_df["name"] = dumy["eNode"]
    lncel_df["cellName"] = dumy["eNode"]

    mmeip_df=pd.read_excel(os.path.join(temp_folder, "Reference_Data_4g.xlsx"), sheet_name="MME IP")
    mmeip_df.columns = mmeip_df.columns.str.strip()
    mmeip_df = pd.concat([mmeip_df] * len(dumy), ignore_index=True)
    mmeip_df["MRBTS"] =  dumy["MRBTS_ID"]
    mmeip_df["MME0"] =  dumy["mme_ip_0"]
    mmeip_df["MME1"] =  dumy["mme_ip_1"]
    mmeip_df["MME4"] =  dumy["mme_ip_4"]

    sgw_df=pd.read_excel(os.path.join(temp_folder, "Reference_Data_4g.xlsx"), sheet_name="SGW IP")
    sgw_df.columns = sgw_df.columns.str.strip()
    sgw_df = pd.concat([sgw_df] * len(dumy), ignore_index=True)
    sgw_df["MRBTS"] =  dumy["MRBTS_ID"]
    sgw_df["SGW1"] = dumy["sgw_ip_1"]
    sgw_df["SGW2"] = dumy["sgw_ip_2"]
    sgw_df["SGW3"] = dumy["sgw_ip_3"]
    sgw_df["SGW4"] = dumy["sgw_ip_4"]
    sgw_df["SGW5"] = dumy["sgw_ip_5"]
    sgw_df["SGW6"] = dumy["sgw_ip_6"]
    sgw_df["SGW7"] = dumy["sgw_ip_7"]
    sgw_df["SGW8"] = dumy["sgw_ip_8"]
    sgw_df["SGW9"] = dumy["sgw_ip_9"]
    sgw_df["SGW10"] = dumy["sgw_ip_10"]
    sgw_df["SGW11"] = dumy["sgw_ip_11"]
   
   
    ntp_df=pd.read_excel(os.path.join(temp_folder, "Reference_Data_4g.xlsx"), sheet_name="NTP IP")
    ntp_df.columns = ntp_df.columns.str.strip()
    ntp_df = pd.concat([ntp_df] * len(dumy), ignore_index=True)
    ntp_df["MRBTS"] =  dumy["MRBTS_ID"]
    ntp_df["NTP IP1"] =  dumy["ntp_ip1"]
    ntp_df["NTP IP2"] =  dumy["ntp_ip2"]

    LNADJGNB_df=pd.read_excel(os.path.join(temp_folder, "Reference_Data_4g.xlsx"), sheet_name="LNADJGNB")
    LNADJGNB_df.columns = LNADJGNB_df.columns.str.strip()
    
    if not lnadjgnb_df.empty:
        LNADJGNB_df = pd.concat([LNADJGNB_df] * len(lnadjgnb_df),ignore_index=True)

        LNADJGNB_df["MRBTS"] = lnadjgnb_df["MRBTS"].values
        LNADJGNB_df["LNBTS"] = lnadjgnb_df["LNBTS"].values
        LNADJGNB_df["LNADJGNB"] = lnadjgnb_df["LNADJGNB"].values
        LNADJGNB_df["adjGnbId"] = lnadjgnb_df["adjGnbId"].values
        LNADJGNB_df["adjGnbIdLength"] = lnadjgnb_df["adjGnbIdLength"].values
        LNADJGNB_df["administrativeState"] = lnadjgnb_df["administrativeState"].values
        LNADJGNB_df["cPlaneIpAddr"] = lnadjgnb_df["cPlaneIpAddr"].values

    else:     
        LNADJGNB_df = LNADJGNB_df.iloc[0:0].copy()


    LTEENB_df=pd.read_excel(os.path.join(temp_folder, "Reference_Data_4g.xlsx"), sheet_name="LTEENB")
    LTEENB_df.columns = LTEENB_df.columns.str.strip()
    LTEENB_df = pd.concat([LTEENB_df] * len(dumy), ignore_index=True)
    LTEENB_df["MRBTS"] =  dumy["MRBTS_ID"]
    LTEENB_df["NRBTS"] =  dumy["nrbts_id"]
  


    IPRTV6_df=pd.read_excel(os.path.join(temp_folder, "Reference_Data_4g.xlsx"), sheet_name="IPRTV6")
    IPRTV6_df.columns = IPRTV6_df.columns.str.strip()

    if not iprtv6_df.empty:
        IPRTV6_df = pd.concat([IPRTV6_df] * len(iprtv6_df),ignore_index=True)

        IPRTV6_df["MRBTS"] =  iprtv6_df[ "MRBTS"].values
        IPRTV6_df["IPRTV6"] =  iprtv6_df["IPRTV6"].values
        IPRTV6_df["Item-staticIpv6Routes-gatewayIpv6Addr"]=iprtv6_df["gatewayIpv6Addr"].values
        IPRTV6_df["userLabel"]=iprtv6_df["userLabel"].values
    else:     
        IPRTV6_df = IPRTV6_df.iloc[0:0].copy()     

    
    QOS_df=pd.read_excel(os.path.join(temp_folder, "Reference_Data_4g.xlsx"), sheet_name="QOS Parameter")
    QOS_df.columns = QOS_df.columns.str.strip()
    
    Golden_para_df=pd.read_excel(os.path.join(temp_folder, "Reference_Data_4g.xlsx"), sheet_name="Golden Parameter")
    Golden_para_df.columns = Golden_para_df.columns.str.strip()

  
    inventory_df = pd.read_excel(os.path.join(temp_folder, "INVENTORY_SHEET_4g.xlsx"))
    inventory_df.columns=inventory_df.columns.str.strip()
    inventory_df = pd.concat([inventory_df] * len(dumy), ignore_index=True)
    inventory_df["SR. No."]= range(1, len(inventory_df) + 1)
    inventory_df["Circle"]=dumy["circle"]
    inventory_df["Location"] =  dumy["MRBTS_ID"]
    inventory_df["Nodename"]= dumy["BTS_Name"]
    inventory_df["Node_IP"]=dumy["IP"]
    inventory_df["NSS ID"] = dumy["eNode"].str[6:]
    

    ran_uim_df= pd.read_excel(os.path.join(temp_folder, "RAN_UIM_BTS_4g.xlsx"))
    ran_uim_df.columns=ran_uim_df.columns.str.strip()
    ran_uim_df = pd.concat([ran_uim_df] * len(dumy), ignore_index=True)
    ran_uim_df["SR. No."]= range(1, len(ran_uim_df) + 1)
    ran_uim_df["Circle"]=dumy["circle"]
    ran_uim_df["Node id"] = dumy["MRBTS_ID"]
    ran_uim_df["Nodename"] = dumy["BTS_Name"]
    ran_uim_df["Location"] = dumy["BTS_Name"].str.split("_").str[0].str[3:]   
    ran_uim_df["NSS ID"] = dumy["eNode"].str[6:]
    parts = dumy["BTS_Name"].str.split("_")
    ran_uim_df["SRAN Name"]= parts.apply(
        lambda x: x[-2] if x[-1].upper() == "SRAN" else x[-1]
)
    

    output_file1 = os.path.join(output_folder, f"Reference_Data_{circle}_4G.xlsx")

    with pd.ExcelWriter(output_file1, engine="openpyxl") as writer:
        cr_df.to_excel(writer,sheet_name="Commercial Radiation",index=False)
        mrbts_df.to_excel(writer,sheet_name="MRBTS",index=False)
        lnbts_df.to_excel(writer,sheet_name="LNBTS",index=False)
        nrcell_df.to_excel(writer,sheet_name="NRCELL",index=False)
        lncel_df.to_excel(writer,sheet_name="LNCEL",index=False)
        mmeip_df.to_excel(writer,sheet_name="MME IP",index=False)
        sgw_df.to_excel(writer,sheet_name="SGW IP",index=False)
        ntp_df.to_excel(writer,sheet_name="NTP IP",index=False)
        # LNADJGNB_df.to_excel(writer,sheet_name="LNADJGNB",index=False)
        # LTEENB_df.to_excel(writer,sheet_name="LTEENB",index=False)
        # IPRTV6_df.to_excel(writer,sheet_name="IPRTV6",index=False)
        QOS_df.to_excel(writer,sheet_name="QOS Parameter",index=False)
        Golden_para_df.to_excel(writer,sheet_name="Golden Parameter",index=False)

    format_excel(output_file1)

    output_file2= os.path.join(output_folder, f"INVENTORY_Data_{circle}_4G.xlsx")
    with pd.ExcelWriter(output_file2, engine="openpyxl") as writer:
        inventory_df.to_excel(writer,sheet_name="INVENTORY",index=False)
    format_excel(output_file2)

    output_file3= os.path.join(output_folder, f"RAN_UIM_BTS_Data_{circle}_4G.xlsx")
    with pd.ExcelWriter(output_file3, engine="openpyxl") as writer:
        ran_uim_df.to_excel(writer,sheet_name="RAN_UIM_BTS",index=False)
    format_excel(output_file3)



    relative_path1 = os.path.relpath(output_file1, MEDIA_ROOT)
    download_url1 = request.build_absolute_uri(
        os.path.join(MEDIA_URL, relative_path1).replace("\\", "/")
    )

    relative_path2 = os.path.relpath(output_file2, MEDIA_ROOT)
    download_url2 = request.build_absolute_uri(
        os.path.join(MEDIA_URL, relative_path2).replace("\\", "/")
    )

    relative_path3 = os.path.relpath(output_file3, MEDIA_ROOT)
    download_url3 = request.build_absolute_uri(
        os.path.join(MEDIA_URL, relative_path3).replace("\\", "/")
    )

    return Response({
        "status": True,
        "message": "Files generated successfully",
        "download_url1": download_url1,
        "download_url2": download_url2,
        "download_url3": download_url3,
    })



@api_view(["POST"])
def vi_5g_summary(request):
    circle = request.POST.get("circle")
    xml_files = request.FILES.getlist("file")
    if not xml_files:
        return Response( {"error": "Please upload XML files"}, status=HTTP_400_BAD_REQUEST)
    

    temp_folder = os.path.join(main_folder, "template")
    if not os.path.isdir(temp_folder):
        return Response({"error": "Template folder not found"}, status=400)
    file_list = [
        file for file in os.listdir(temp_folder)
        if os.path.isfile(os.path.join(temp_folder, file))
    ]

    print(file_list)

    output_folder = os.path.join(main_folder, "Output")
    os.makedirs(output_folder, exist_ok=True)

    lnadjgnb_data=[]
    iprtv6_data = []
  
    for file in xml_files:
        file_name = file.name.lower()

        # Read xml/gz file
        if file_name.endswith(".gz"):
            xml_bytes = gzip.decompress(file.read())
        else:
            xml_bytes = file.read()

        root = ET.fromstring(xml_bytes)

        # Namespace handling
        m = re.match(r"\{(.*)\}", root.tag)
        ns_url = m.group(1) if m else root.attrib.get("xmlns", "")
        ns = {"ns": ns_url} if ns_url else {}

        managed_objects = (
            root.findall(".//ns:managedObject", ns)
            if ns else root.findall(".//managedObject")
        )

#--------------------------
    
        for mo in managed_objects:
            mo_class = mo.attrib.get("class", "")
            if mo_class == "NOKLTE:LNADJGNB":
                dist_name = mo.attrib.get("distName", "")
                mrbts_id = dist_name.split("/")[0].split("-")[-1]
                lnbts_id = dist_name.split("/")[1].split("-")[-1]
                lnadjgnb_id = dist_name.split("/")[2].split("-")[-1]

                row = {
                    "MRBTS": mrbts_id,
                    "LNBTS": lnbts_id,
                    "LNADJGNB": lnadjgnb_id
                }

                p_tags = (
                    mo.findall("ns:p", ns)
                    if ns else mo.findall("p")
                )

                for p in p_tags:
                    name = p.attrib.get("name")

                    if name == "adjGnbId":
                        row["adjGnbId"] = p.text

                    elif name == "adjGnbIdLength":
                        row["adjGnbIdLength"] = p.text

                    elif name == "administrativeState":
                        row["administrativeState"] = p.text

                    elif name == "cPlaneIpAddr":
                        row["cPlaneIpAddr"] = p.text

                lnadjgnb_data.append(row) 

            elif mo_class == "com.nokia.srbts.tnl:IPRTV6":
                dist_name = mo.attrib.get("distName", "")
                mrbts = dist_name.split("/")[0].split("-")[-1]
                iprtv6 = dist_name.split("/")[-1].split("-")[-1]
                row = {
                    "MRBTS": mrbts,
                    "IPRTV6": iprtv6
                }
                # userLabel
                p_tags = mo.findall("ns:p", ns) if ns else mo.findall("p")
                for p in p_tags:
                    if p.attrib.get("name") == "userLabel":
                        row["userLabel"] = p.text

                # gatewayIpv6Addr
                items = (
                    mo.findall(".//ns:list[@name='staticIpv6Routes']/ns:item", ns)
                    if ns else
                    mo.findall(".//list[@name='staticIpv6Routes']/item")
                )

                for item in items:
                    p_tags = item.findall("ns:p", ns) if ns else item.findall("p")
                    for p in p_tags:
                        if p.attrib.get("name") == "gatewayIpv6Addr":
                            row["gatewayIpv6Addr"] = p.text
                            break

                iprtv6_data.append(row)     

            
        

     
    if lnadjgnb_data:
        lnadjgnb_df = pd.DataFrame(lnadjgnb_data)
    else:
        lnadjgnb_df = pd.DataFrame(columns=[
             "MRBTS",
             "LNBTS",
            "LNADJGNB",
            "adjGnbId",
            "adjGnbIdLength",
            "administrativeState",
            "cPlaneIpAddr"
        ])

    if iprtv6_data:
        iprtv6_df = pd.DataFrame(iprtv6_data)
    else:
        iprtv6_df = pd.DataFrame(columns=[
            "MRBTS",
            "IPRTV6",
            "userLabel",
            "gatewayIpv6Addr"
        ])
   
#for Commercial Radiation sheet-----
    
    LNADJGNB_df=pd.read_excel(os.path.join(temp_folder, "Reference_Data_4g.xlsx"), sheet_name="LNADJGNB")
    LNADJGNB_df.columns = LNADJGNB_df.columns.str.strip()
    
    if not lnadjgnb_df.empty:
        LNADJGNB_df = pd.concat([LNADJGNB_df] * len(lnadjgnb_df),ignore_index=True)

        LNADJGNB_df["MRBTS"] = lnadjgnb_df["MRBTS"].values
        LNADJGNB_df["LNBTS"] = lnadjgnb_df["LNBTS"].values
        LNADJGNB_df["LNADJGNB"] = lnadjgnb_df["LNADJGNB"].values
        LNADJGNB_df["adjGnbId"] = lnadjgnb_df["adjGnbId"].values
        LNADJGNB_df["adjGnbIdLength"] = lnadjgnb_df["adjGnbIdLength"].values
        LNADJGNB_df["administrativeState"] = lnadjgnb_df["administrativeState"].values
        LNADJGNB_df["cPlaneIpAddr"] = lnadjgnb_df["cPlaneIpAddr"].values

    else:     
        LNADJGNB_df = LNADJGNB_df.iloc[0:0].copy()


    IPRTV6_df=pd.read_excel(os.path.join(temp_folder, "Reference_Data_4g.xlsx"), sheet_name="IPRTV6")
    IPRTV6_df.columns = IPRTV6_df.columns.str.strip()

    if not iprtv6_df.empty:
        IPRTV6_df = pd.concat([IPRTV6_df] * len(iprtv6_df),ignore_index=True)

        IPRTV6_df["MRBTS"] =  iprtv6_df[ "MRBTS"].values
        IPRTV6_df["IPRTV6"] =  iprtv6_df["IPRTV6"].values
        IPRTV6_df["Item-staticIpv6Routes-gatewayIpv6Addr"]=iprtv6_df["gatewayIpv6Addr"].values
        IPRTV6_df["userLabel"]=iprtv6_df["userLabel"].values
    else:     
        IPRTV6_df = IPRTV6_df.iloc[0:0].copy()     



    output_file = os.path.join(output_folder, f"Reference_Data_{circle}_5G.xlsx")

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
 
        LNADJGNB_df.to_excel(writer,sheet_name="LNADJGNB",index=False)
        IPRTV6_df.to_excel(writer,sheet_name="IPRTV6",index=False)
    
    format_excel(output_file)

    relative_path = os.path.relpath(output_file, MEDIA_ROOT)
    download_url = request.build_absolute_uri(
        os.path.join(MEDIA_URL, relative_path).replace("\\", "/")
    )
    return Response({
        "status": True,
        "message": "Files generated successfully",
        "download_url": download_url,
    
    })
