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
    nrx2link_data=[]
    ipaddressv6_data=[]
    lncel_ids = []
    lncel_data = []
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
        nrcell_id=""
        mme_ip_0 = ""
        mme_ip_4 = ""
        mme_ip_1=""
        sgw_ips = [""] * 11   # SGW1 to SGW11
        ntp_ip1=""
        ntp_ip2=""
        ip4=""
        
        

      
    
        


    
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
                        # Sirf pehli baar IP set karo
                        if not ip4:
                            ip4 = p.text
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

                mrbts = dist_name.split("/")[0].split("-")[-1]
                lnbts = dist_name.split("/")[1].split("-")[-1]
                lncel = dist_name.split("/")[-1].split("-")[-1]

                lncel_data.append({
                    "MRBTS ID": mrbts,
                    "LNBTS ID": lnbts,
                    "LNCEL": lncel,
                    "name": enode,
                    "cellName": enode
                })

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

            elif mo_class == "com.nokia.srbts.mnl:NTP":
                if ns:
                    ntp_list = mo.find("ns:list[@name='ntpServerIpAddrOrFqdnList']", ns)
                    if ntp_list is None:
                        ntp_list = mo.find("ns:list[@name='ntpServerIpAddrList']", ns)
                else:
                    ntp_list = mo.find("list[@name='ntpServerIpAddrOrFqdnList']")
                    if ntp_list is None:
                        ntp_list = mo.find("list[@name='ntpServerIpAddrList']")

                if ntp_list is not None:
                    p_list = (
                        ntp_list.findall("ns:p", ns)
                        if ns else
                        ntp_list.findall("p")
                    )

                    if len(p_list) > 0:
                        ntp_ip1 = p_list[0].text or ""

                    if len(p_list) > 1:
                        ntp_ip2 = p_list[1].text or ""   

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
                    "IPRTV6": iprtv6,
                    "gatewayIpv6Addr": "",
                    "userLabel": ""
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
            

            elif mo_class == "com.nokia.srbts.nrbts:NRX2LINK_TRUST":
                dist_name = mo.attrib.get("distName", "")
                mrbts = dist_name.split("/")[0].split("-")[-1]
                nrbts = dist_name.split("/")[1].split("-")[-1]
                nrx2_id = dist_name.split("/")[-1].split("-")[-1]

                row = {
                    "MRBTS": mrbts,
                    "NRBTS": nrbts,
                    "NRX2LINK_TRUST": nrx2_id,
                    "ipV6Addr": "",
                    "x2LinkTrustCtrl": ""
                }

                p_tags = mo.findall("ns:p", ns) if ns else mo.findall("p")

                for p in p_tags:
                    name = p.attrib.get("name")
                    if name == "ipV6Addr":
                        row["ipV6Addr"] = p.text
                    elif name == "x2LinkTrustCtrl":
                        row["x2LinkTrustCtrl"] = p.text

                nrx2link_data.append(row)

            elif mo_class == "com.nokia.srbts.tnl:IPADDRESSV6":
                dist_name = mo.attrib.get("distName", "")

                mrbts = dist_name.split("/")[0].split("-")[-1]
                ipaddressv6 = dist_name.split("/")[-1].split("-")[-1]

                row = {
                    "MRBTS": mrbts,
                    "IPADDRESSV6": ipaddressv6
                }

                p_tags = mo.findall("ns:p", ns) if ns else mo.findall("p")

                for p in p_tags:
                    if p.attrib.get("name") == "localIpAddr":
                        row["localIpAddr"] = p.text
                    elif p.attrib.get("name") == "localIpPrefixLength":
                        row["localIpPrefixLength"] = p.text
                    elif p.attrib.get("name") == "ipAddressAllocationMethod":
                        row["ipAddressAllocationMethod"] = p.text

                ipaddressv6_data.append(row)    
            

        row = {
            "MRBTS_ID": mrbts_id,
            "BTS_Name": bts_name,
            "Version": version,
            "ip4":ip4,
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
            "circle":circle ,
            "LNCel_ID": ",".join(lncel_ids),
          
        

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

    if nrx2link_data:
        nrx2_df = pd.DataFrame(nrx2link_data)
    else:
        nrx2_df = pd.DataFrame(columns=[
            "MRBTS",
            "NRBTS",
            "NRX2LINK_TRUST",
            "ipV6Addr",
            "x2LinkTrustCtrl"
        ])
    if ipaddressv6_data:
        ipaddressv6_df = pd.DataFrame(ipaddressv6_data)
    else:
        ipaddressv6_df = pd.DataFrame(columns=[
            "MRBTS",
            "localIpAddr",
            "localIpPrefixLength",

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
    cr_df["MRBTS IP"] = dumy["ip4"]
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


    nrcell_df = pd.read_excel(
    os.path.join(temp_folder, "Reference_Data_4g.xlsx"),
    sheet_name="NRCELL"
    )
    nrcell_df.columns = nrcell_df.columns.str.strip()

    if not nr_df.empty:
        # Create empty dataframe with same columns and required rows
        nrcell_df = pd.DataFrame(
            index=range(len(nr_df)),
            columns=nrcell_df.columns
        )

        nrcell_df["MRBTS"] = nr_df["MRBTS"].values
        nrcell_df["NRBTS"] = nr_df["NRBTS"].values
        nrcell_df["NRCELL"] = nr_df["NRCELL"].values
        nrcell_df["pMax"] = nr_df["pMax"].values
        nrcell_df["nrarfcn"] = nr_df["nrarfcn"].values
        nrcell_df["chBw"] = nr_df["chBw"].values

        # Map eNode name
        name_map = (
            dumy[["MRBTS_ID", "eNode"]]
            .drop_duplicates(subset="MRBTS_ID", keep="first")
            .set_index("MRBTS_ID")["eNode"]
        )

        nrcell_df["name"] = nrcell_df["MRBTS"].map(name_map)

    else:
        # Empty dataframe with same columns
        nrcell_df = nrcell_df.iloc[0:0].copy()

    


    
    template_lncel = pd.read_excel(os.path.join(temp_folder, "Reference_Data_4g.xlsx"),sheet_name="LNCEL")
    template_lncel.columns = template_lncel.columns.str.strip()
    if lncel_data:
        lncel_df = pd.DataFrame(lncel_data)

        for col in template_lncel.columns:
            if col not in lncel_df.columns:
                lncel_df[col] = ""

        lncel_df = lncel_df[template_lncel.columns]
    else:
        lncel_df = template_lncel.iloc[0:0].copy()


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


    LTEENB_df = pd.read_excel(
        os.path.join(temp_folder, "Reference_Data_4g.xlsx"),
        sheet_name="LTEENB"
    )
    LTEENB_df.columns = LTEENB_df.columns.str.strip()

    if not nrx2_df.empty:

        if len(LTEENB_df) > 0:
            template = LTEENB_df.iloc[[0]].copy()
            LTEENB_df = pd.concat([template] * len(nrx2_df), ignore_index=True)
        else:
            LTEENB_df = pd.DataFrame(
                index=range(len(nrx2_df)),
                columns=LTEENB_df.columns
            )

        LTEENB_df["MRBTS"] = nrx2_df["MRBTS"].values
        LTEENB_df["NRBTS"] = nrx2_df["NRBTS"].values
        LTEENB_df["LTEENB"] = nrx2_df["NRX2LINK_TRUST"].values
        LTEENB_df["localCuIpAddr"] = nrx2_df["ipV6Addr"].values
        ip_map = (
            iprtv6_df
            .drop_duplicates(subset="MRBTS", keep="first")
            .set_index("MRBTS")["gatewayIpv6Addr"]
        )

        LTEENB_df["ipAddr"] = LTEENB_df["MRBTS"].map(ip_map)

        LTEENB_df["ipAddr"] = LTEENB_df["MRBTS"].map(ip_map)
        LTEENB_df["x2LinkLock"]=0
        LTEENB_df["x2LinkStatus"]=1
        LTEENB_df["x2_LinkLock"]="unlocked"
        LTEENB_df["x2_LinkStatus"]="available"
       

    else:
        LTEENB_df = LTEENB_df.iloc[0:0].copy()
    


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
    inventory_df["Node_IP"]=dumy["ip4"]
    inventory_df["NSS ID"] = dumy["eNode"].str[6:]
    

    ran_uim_df= pd.read_excel(os.path.join(temp_folder, "RAN_UIM_BTS_4g.xlsx"))
    ran_uim_df.columns=ran_uim_df.columns.str.strip()
    ran_uim_df = pd.concat([ran_uim_df] * len(dumy), ignore_index=True)
    ran_uim_df["SR. No."]= range(1, len(ran_uim_df) + 1)
    ran_uim_df["Circle"]=dumy["circle"]
    ran_uim_df["Node id"] = dumy["MRBTS_ID"]
    ran_uim_df["Nodename"] = dumy["BTS_Name"]
    ran_uim_df["Location"] = (
        dumy["BTS_Name"]
        .str.split("_").str[0]
        .apply(lambda x: x[2:] if x.startswith("ZR") else x)
    )
    ran_uim_df["NSS ID"] = dumy["eNode"].str[6:]
    parts = dumy["BTS_Name"].str.split("_")
    ran_uim_df["SRAN Name"]= parts.apply(
        lambda x: x[-2] if x[-1].upper() == "SRAN" else x[-1]
)
    

    output_file1 = os.path.join(output_folder, f"Reference_Data_{circle}_4G_5G.xlsx")

    with pd.ExcelWriter(output_file1, engine="openpyxl") as writer:
        cr_df.to_excel(writer,sheet_name="Commercial Radiation",index=False)
        mrbts_df.to_excel(writer,sheet_name="MRBTS",index=False)
        lnbts_df.to_excel(writer,sheet_name="LNBTS",index=False)
        nrcell_df.to_excel(writer,sheet_name="NRCELL",index=False)
        lncel_df.to_excel(writer,sheet_name="LNCEL",index=False)
        mmeip_df.to_excel(writer,sheet_name="MME IP",index=False)
        sgw_df.to_excel(writer,sheet_name="SGW IP",index=False)
        ntp_df.to_excel(writer,sheet_name="NTP IP",index=False)
        LNADJGNB_df.to_excel(writer,sheet_name="LNADJGNB",index=False)
        LTEENB_df.to_excel(writer,sheet_name="LTEENB",index=False)
        IPRTV6_df.to_excel(writer,sheet_name="IPRTV6",index=False)
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
        "message":"4G Summary generated successfully",
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
                    "IPRTV6": iprtv6,
                    "userLabel": "",
                    "gatewayIpv6Addr": ""
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
    required_cols = [
        "MRBTS",
        "IPRTV6",
        "userLabel",
        "gatewayIpv6Addr"
    ]

    for col in required_cols:
        if col not in iprtv6_df.columns:
            iprtv6_df[col] = ""    
   
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
        "message":"5G Summary generated successfully",
        "download_url": download_url,
    
    })



@api_view(["POST"])
def vi_2g_summary(request):
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
        bcf_data = []
        for mo in managed_objects:
            mo_class = mo.attrib.get("class", "")
            if mo_class == "BCF":
                dist_name = mo.attrib.get("distName", "")
                version = mo.attrib.get("version", "")

                bsc_id = dist_name.split("/")[1].split("-")[-1]
                bcf_id = dist_name.split("/")[2].split("-")[-1]

                row = {
                    "BSC_ID": bsc_id,
                    "BCF_ID": bcf_id,
                    "Version": version,
                }

                p_tags = mo.findall("ns:p", ns) if ns else mo.findall("p")

                for p in p_tags:
                    name = p.attrib.get("name")

                    if name == "name":
                        row["BTS_Name"] = p.text

                    elif name == "siteTemplateDescription":
                        row["Site_Template"] = p.text

                    elif name == "SBTSId":
                        row["SBTS_ID"] = p.text

                    elif name=="btsMPlaneIpAddress":
                        row["IP"] = p.text  

                    

                bcf_data.append(row)

    bcf_df = pd.DataFrame(bcf_data)
    print(bcf_df)

    rf_df = pd.read_excel(os.path.join(temp_folder, "Reference_2g.xlsx"))
    rf_df.columns = rf_df.columns.str.strip()

    rf_df = pd.concat([rf_df] * len(bcf_df), ignore_index=True)

    # Fill columns
    rf_df["Circle"] = circle
    rf_df["Location"] = bcf_df["BTS_Name"].str.extract(r'([A-Z]{4}\d{4})', expand=False)
    rf_df["Nodename"] = bcf_df["BTS_Name"]
    rf_df["Node_IP"] = bcf_df["IP"]
    rf_df["2G Site ID"]= bcf_df["BTS_Name"].str.extract(r'([A-Z]{4}\d{4})', expand=False)
    rf_df["NSSID"]=bcf_df["Site_Template"]
    rf_df["BSC Name"]=""


    # Save
    output_file = os.path.join(output_folder, f"Reference_Data_{circle}_2G.xlsx")

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        rf_df.to_excel(writer, index=False)

    format_excel(output_file)

    relative_path = os.path.relpath(output_file, MEDIA_ROOT)
    download_url = request.build_absolute_uri(
        os.path.join(MEDIA_URL, relative_path).replace("\\", "/")
    )

    return Response({
        "status": True,
        "message": "2G Summary generated successfully",
        "download_url": download_url,
    })
