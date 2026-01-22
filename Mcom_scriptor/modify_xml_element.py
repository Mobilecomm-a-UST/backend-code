import os 
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import datetime
import pandas as pd
import xml.etree.ElementTree as ET
from mcom_website.settings import MEDIA_ROOT
# _____________________________________ MRBTS/LNBTS CHANGE ________________________________

# Iterate through each managedObject and update the DistName
def MRBTS_LNBTS_change(root,LMBTS,MRBTS,cell_list,input1_dict):
        managed_objects = root.findall(".//managedObject")
        for managed_object in managed_objects:
            dist_name = managed_object.get("distName", "")
            parts = dist_name.split("/")
            
            if len(parts) >= 1 and parts[0] =="MRBTS-844360" :
                # Modify the first part of the DistName (assuming it's the MRBTS part)
                parts[0] = MRBTS  # Replace "MRBTS" with your desired new value
            if len(parts) >= 2 and parts[1] =="LNBTS-844360" :
                # Modify the first part of the DistName (assuming it's the MRBTS part)
                parts[1] = LMBTS
                # Join the parts back together and set the updated DistName
            try:
                    for cell in cell_list:
                        if len(parts)>=3 and parts[2]==F"LNCEL-{cell}":
                            parts[2]=f"LNCEL-{input1_dict[cell-1]['Cell ID']}"
            except:
                pass
                    
            updated_dist_name = "/".join(parts)
            managed_object.set("distName", updated_dist_name)

        def iterate_over_elements(element):
            if element.text:
                # print("Text:", element.text)
                if  element.text !='nan':
                    if isinstance(element.text, str) and "MRBTS-844360" in element.text:
                    # if "MRBTS-844360" in element.text:
                        element.text = element.text.replace("MRBTS-844360", MRBTS)
            for child in element:
                iterate_over_elements(child)

        iterate_over_elements(root)
        return root
# Print the modified XML


# _______________________________********************************________________________



def process(input1_dict,input2_dict,cell_list,root,irfim_dict,lnhoif_dict):
    #______________________________ STATIC CHANGES __________________________
    namespace_dic = {'raml': 'raml21.xsd'}
    # tree = ET.parse(xml_file_path)
    # root = tree.getroot()

    module_location= input2_dict["Site Name/module location"][0]
    target_element=root.find(".//managedObject[@class='com.nokia.srbts.eqm:SMOD'][@distName='MRBTS-844360/EQM-1/APEQM-1/CABINET-1/SMOD-1']/p[@name='moduleLocation']")
    # print(target_element)
    target_element.text=module_location

    LNBTS_Name_enodename = input2_dict["LNBTS Name/enodename"][0]
    target_element=root.find(".//managedObject[@class='NOKLTE:LNBTS'][@distName='MRBTS-844360/LNBTS-844360']/p[@name='enbName']")
    # print(target_element)
    target_element.text=LNBTS_Name_enodename


    MRBTS_Name= input2_dict['MRBTS Name'][0]
    target_element=root.find(".//managedObject[@class='com.nokia.srbts:MRBTS'][@distName='MRBTS-844360']/p[@name='btsName']")
    # print(target_element)
    target_element.text=MRBTS_Name

    U_Plane_VLAN = input2_dict["UP 'VLAN /VLANIF1"][0]
    target_element=root.find(".//managedObject[@class='com.nokia.srbts.tnl:VLANIF'][@distName='MRBTS-844360/TNLSVC-1/TNL-1/ETHSVC-1/ETHIF-1/VLANIF-1']/p[@name='vlanId']")
    # print(target_element)
    target_element.text=U_Plane_VLAN

    C_Plane_VLAN = input2_dict["CP 'VLAN/VLANIF2"][0]
    target_element=root.find(".//managedObject[@class='com.nokia.srbts.tnl:VLANIF'][@distName='MRBTS-844360/TNLSVC-1/TNL-1/ETHSVC-1/ETHIF-1/VLANIF-2']/p[@name='vlanId']")
    # print(target_element)
    target_element.text=C_Plane_VLAN

    M_Plane_VLAN =input2_dict["OM 'VLAN/VLANIF3"][0]
    target_element=root.find(".//managedObject[@class='com.nokia.srbts.tnl:VLANIF'][@distName='MRBTS-844360/TNLSVC-1/TNL-1/ETHSVC-1/ETHIF-1/VLANIF-3']/p[@name='vlanId']")
    # print(target_element)
    target_element.text=M_Plane_VLAN




    #--------------------------------------------------------------UP_eNB_InterfaceIP_IF1,CP_eNB_InterfaceIP_IF2,OM_eNB_InterfaceIP_IF3 ______
    UP_eNB_InterfaceIP_IF1= input2_dict["UP 'eNB InterfaceIP/IF1"][0]
    #for 1st place

    target_element=root.find(".//managedObject[@class='com.nokia.srbts.tnl:IPADDRESSV4'][@distName='MRBTS-844360/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-1']/p[@name='localIpAddr']")
    # print(target_element)
    target_element.text=UP_eNB_InterfaceIP_IF1

    #for 2nd place 
    # target_element=root.find(".//managedObject[@class='com.nokia.srbts.tnl:RTPOL'][@distName='MRBTS-844360/TNLSVC-1/TNL-1/IPNO-1/RTPOL-1']/list[@name='routingPolicies']/item/p[@name='srcIpAddress']")
    # # print(target_element)
    # target_element.text=UP_eNB_InterfaceIP_IF1

    #----------------------------------------------------------------
    CP_eNB_InterfaceIP_IF2=input2_dict["CP 'eNB InterfaceIP/IF2"][0]
    # 1st place
    target_element=root.find(".//managedObject[@class='com.nokia.srbts.tnl:IPADDRESSV4'][@distName='MRBTS-844360/TNLSVC-1/TNL-1/IPNO-1/IPIF-2/IPADDRESSV4-1']/p[@name='localIpAddr']")
    # print(target_element)
    target_element.text=CP_eNB_InterfaceIP_IF2

    #for 2nd place 
    # target_element=root.find(".//managedObject[@class='com.nokia.srbts.tnl:RTPOL'][@distName='MRBTS-844360/TNLSVC-1/TNL-1/IPNO-1/RTPOL-1']/list/item[p[@name='orderNumber' and text()='1']]/p[@name='srcIpAddress']")
    # # print(target_element)
    # target_element.text=UP_eNB_InterfaceIP_IF1

    #----------------------------------------------------------------

    OM_eNB_InterfaceIP_IF3= input2_dict["OM 'eNB InterfaceIP/IF3"][0]
    # 1st place
    target_element=root.find(".//managedObject[@class='com.nokia.srbts.tnl:IPADDRESSV4'][@distName='MRBTS-844360/TNLSVC-1/TNL-1/IPNO-1/IPIF-3/IPADDRESSV4-1']/p[@name='localIpAddr']")
    # print(target_element)
    target_element.text=OM_eNB_InterfaceIP_IF3

    #for 2nd place 
    # target_element=root.find(".//managedObject[@class='com.nokia.srbts.tnl:RTPOL'][@distName='MRBTS-844360/TNLSVC-1/TNL-1/IPNO-1/RTPOL-1']/list/item[p[@name='orderNumber' and text()='1']]/p[@name='srcIpAddress']")
    # # print(target_element)
    # target_element.text=UP_eNB_InterfaceIP_IF1

    #_______________________________---------------------------________________________________

    UP_Default_Gateway_IP_IPRT1=input2_dict["UP 'Default Gateway IP/IPRT1"][0]
    target_element=root.find(".//managedObject[@class='com.nokia.srbts.tnl:IPRT'][@distName='MRBTS-844360/TNLSVC-1/TNL-1/IPNO-1/IPRT-1']/list/item/p[@name='gateway']")
    # print(target_element)
    target_element.text= UP_Default_Gateway_IP_IPRT1

    CP_Default_Gateway_IP_IPRT2=input2_dict["CP 'Default Gateway IP/IPRT2"][0]
    target_element=root.find(".//managedObject[@class='com.nokia.srbts.tnl:IPRT'][@distName='MRBTS-844360/TNLSVC-1/TNL-1/IPNO-1/IPRT-2']/list/item/p[@name='gateway']")
    # print(target_element)
    target_element.text=CP_Default_Gateway_IP_IPRT2

    OM_Default_Gateway_IP_IPRT3=input2_dict["OM 'Default Gateway IP/IPRT3"][0]
    target_element=root.find(".//managedObject[@class='com.nokia.srbts.tnl:IPRT'][@distName='MRBTS-844360/TNLSVC-1/TNL-1/IPNO-1/IPRT-3']/list/item/p[@name='gateway']")
    # print(target_element)
    target_element.text=OM_Default_Gateway_IP_IPRT3

    #____________________________________Anchor_IP_eNB_IPv6_ENDC___________________________________
    Anchor_IP_eNB_IPv6_ENDC = input2_dict["Anchor IP (eNB - IPv6 ENDC)"][0]

    # 1st place
    target_element=root.find(".//managedObject[@class='com.nokia.srbts.tnl:IPADDRESSV6'][@distName='MRBTS-844360/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV6-1']/p[@name='localIpAddr']")
    # print(target_element)
    target_element.text=Anchor_IP_eNB_IPv6_ENDC

    # for 2nd place
    # target_element=root.find(".//managedObject[@class='com.nokia.srbts.tnl:RTPOL'][@distName='MRBTS-844360/TNLSVC-1/TNL-1/IPNO-1/RTPOL-1']//list/item[p[@name='orderNumber' and text()='1']]/p[@name='srcIpAddress']")
    # # print(target_element)
    # target_element.text=Anchor_IP_eNB_IPv6_ENDC
    #________________________________________--------------------________________________________

    #________________________________________Anchor IP (IPv6 Gateway)________________________________________
    Anchor_IP_IPv6_Gateway= input2_dict["Anchor IP (IPv6 Gateway)"][0]
    target_element=root.find(".//managedObject[@class='com.nokia.srbts.tnl:IPRTV6'][@distName='MRBTS-844360/TNLSVC-1/TNL-1/IPNO-1/IPRTV6-4']/list/item/p[@name='gatewayIpv6Addr']")
    # print(target_element)
    target_element.text=Anchor_IP_IPv6_Gateway

    #_____________________________________-------------------------________________________________

    #_____________________________________Megaplexer IP________________________________

    Megaplexer_IP= input2_dict["Megaplexer IP"][0]
    # 1st Place
    target_element=root.find(".//managedObject[@class='NOKLTE:CTRLTS'][@distName='MRBTS-844360/LNBTS-844360/CTRLTS-1']/list/item/p[@name='loggedTCEIP']")
    #print(target_element)
    target_element.text = Megaplexer_IP

    # 2nd place
    target_element=root.find(".//managedObject[@class='NOKLTE:MTRACE'][@distName='MRBTS-844360/LNBTS-844360/CTRLTS-1/MTRACE-1']/p[@name='tceIpAddress']")
    #print(target_element)
    target_element.text = Megaplexer_IP

    #_____________________________________-------------------------________________________________

    #________________________________NTP IP________________________
    NTP_IP=input2_dict["NTP IP"][0]
    target_element=root.find(".//managedObject[@class='com.nokia.srbts.mnl:NTP'][@distName='MRBTS-844360/MNL-1/MNLENT-1/SYNC-1/CLOCK-1/NTP-1']/list[@name='ntpServerIpAddrList']/p")
    #print(target_element)
    target_element.text = NTP_IP

    #_____________________________________-------------------------________________________________

    #_____________________________________mnc_______________________________
    MNC=input2_dict["MNC"][0]
    target_element=root.find(".//managedObject[@class='NOKLTE:LNBTS'][@distName='MRBTS-844360/LNBTS-844360']/p[@name='mnc']")
    #print(target_element)
    target_element.text = MNC
    #________________________________----------------------------------________________________________

    #_____________________________________mcc_______________________________
    MCC=input2_dict["MCC"][0]
    target_element=root.find(".//managedObject[@class='NOKLTE:LNBTS'][@distName='MRBTS-844360/LNBTS-844360']/p[@name='mcc']")
    #print(target_element)
    target_element.text = MCC
    #________________________________----------------------------------________________________________

    #________________________________External Alarm (EAC)_____________________________________
    # 1st place
    External_Alarm_EAC_1=input2_dict['External Alarm Configuration (EAC)'][0]
    target_element=root.find(".//managedObject[@class='com.nokia.srbts.eqm:EAC_IN'][@distName='MRBTS-844360/EQM-1/APEQM-1/CABINET-1/SMOD-1/EAC_IN-1']/p[@name='descr']")
    #print(target_element)
    target_element.text = External_Alarm_EAC_1

    # 2st place
    External_Alarm_EAC_2=input2_dict['External Alarm Configuration (EAC)'][1]
    target_element=root.find(".//managedObject[@class='com.nokia.srbts.eqm:EAC_IN'][@distName='MRBTS-844360/EQM-1/APEQM-1/CABINET-1/SMOD-1/EAC_IN-2']/p[@name='descr']")
    #print(target_element)
    target_element.text = External_Alarm_EAC_2

    # 3rd place
    External_Alarm_EAC_3=input2_dict['External Alarm Configuration (EAC)'][2]
    target_element=root.find(".//managedObject[@class='com.nokia.srbts.eqm:EAC_IN'][@distName='MRBTS-844360/EQM-1/APEQM-1/CABINET-1/SMOD-1/EAC_IN-3']/p[@name='descr']")
    #print(target_element)
    target_element.text = External_Alarm_EAC_3

    # 4th place
    External_Alarm_EAC_4=input2_dict['External Alarm Configuration (EAC)'][3]
    target_element=root.find(".//managedObject[@class='com.nokia.srbts.eqm:EAC_IN'][@distName='MRBTS-844360/EQM-1/APEQM-1/CABINET-1/SMOD-1/EAC_IN-4']/p[@name='descr']")
    #print(target_element)
    target_element.text = External_Alarm_EAC_4

    #_____________________________________---------------------------__________________________

    #_____________________________________MME________________________________________________________________
    # 1st place
    # MME_0=input2_dict["MME IP"][0]
    # target_element=root.find(".//managedObject[@class='NOKLTE:LNMME'][@distName='MRBTS-844360/LNBTS-844360/LNMME-0']/p[@name='ipAddrPrim']")
    # #print(target_element)
    # target_element.text = MME_0
    
    # # 2nd place
    # MME_1=input2_dict["MME IP"][1]
    # target_element=root.find(".//managedObject[@class='NOKLTE:LNMME'][@distName='MRBTS-844360/LNBTS-844360/LNMME-1']/p[@name='ipAddrPrim']")
    # #print(target_element)
    # target_element.text = MME_1
    
    # # 3rd place
    # MME_2=input2_dict["MME IP"][2]
    # target_element=root.find(".//managedObject[@class='NOKLTE:LNMME'][@distName='MRBTS-844360/LNBTS-844360/LNMME-2']/p[@name='ipAddrPrim']")
    # #print(target_element)
    # target_element.text = MME_2
    
    # # 4th place
    # MME_3=input2_dict["MME IP"][3]
    # target_element=root.find(".//managedObject[@class='NOKLTE:LNMME'][@distName='MRBTS-844360/LNBTS-844360/LNMME-3']/p[@name='ipAddrPrim']")
    # #print(target_element)
    # target_element.text = MME_3
    
    #_____________________________________SGW IPs________________________________
    # sgw_ip=input2_dict['S-GW']
    # if len(sgw_ip)<=23:
    #     target_element=root.find(".//managedObject[@class='NOKLTE:GTPU'][@distName='MRBTS-844360/LNBTS-844360/GTPU-1']/list[@name='sgwIpAddressList']")
    #     all_items=target_element.findall(".//item/p[@name='sgwIpAddress']")
    #     print(len(all_items))
    #     for i,ip in enumerate(sgw_ip):
    #         # p=item.find(".//p[@name='sgwIpAddress']")
    #         all_items[i].text=ip
    #________________________________--------------------------------__________________________________
    ip=[UP_eNB_InterfaceIP_IF1,CP_eNB_InterfaceIP_IF2,OM_eNB_InterfaceIP_IF3,Anchor_IP_eNB_IPv6_ENDC]
    all_item_element=root.findall(".//managedObject[@class='com.nokia.srbts.tnl:RTPOL'][@distName='MRBTS-844360/TNLSVC-1/TNL-1/IPNO-1/RTPOL-1']/list/item")
    for i,item in enumerate(all_item_element):
        it=item.find(".//p[@name='srcIpAddress']")
        it.text=ip[i]    
    
    #__________________________________________  MTRACE ________________________________________________
    MTRACE_element=root.find(".//managedObject[@class='NOKLTE:MTRACE'][@distName='MRBTS-844360/LNBTS-844360/CTRLTS-1/MTRACE-1']/list[@name='eutranTraceId']/item/p[@name='traceId']")
    MTRACE_element.text= str(input2_dict['MRBTS ID'][0])
    #________________________________ ---------------------------------- ________________________________
    
    cell_list=cell_list
    for i,cell in enumerate(cell_list):
        print("cell:",cell)
        MO_element=root.find(f".//managedObject[@class='NOKLTE:LNCEL'][@distName='MRBTS-844360/LNBTS-844360/LNCEL-{str(cell)}']")
        
        cellTechnology_element=MO_element.find(".//p[@name='cellTechnology']")
        cellTechnology_element.text = input1_dict[i]['Tech']

        lcrId_element=MO_element.find(".//p[@name='lcrId']")
        lcrId_element.text = input1_dict[i]['Cell ID']

        cellName_element=MO_element.find(".//p[@name='cellName']")
        cellName_element.text = input1_dict[i]['LTE CellName']

        phyCellId_element=MO_element.find(".//p[@name='phyCellId']")
        phyCellId_element.text = input1_dict[i]['PCI']

        tac_element=MO_element.find(".//p[@name='tac']")
        tac_element.text = input1_dict[i]['TAC']

        pMax_element=MO_element.find(".//p[@name='pMax']")
        pMax_element.text = str(int(input1_dict[i]['Max. Output Power (Pmax)'])*10)
        
        redBwMaxRbUL_element= MO_element.find(".//list[@name='redBwRbUlConfig']/item/p[@name='redBwMaxRbUl']")
        redBwMaxRbUL_element.text=str(int(input1_dict[i]['Bandwidth'].strip())*5)

    #------------------------------------------------------------------------------------------
        mimo_dict={'2T2R':'Closed Loop Mimo','4T4R':'Closed Loop MIMO (4x4)'}
        
        MO_element_TDD_0=root.find(f".//managedObject[@class='NOKLTE:LNCEL_TDD'][@distName='MRBTS-844360/LNBTS-844360/LNCEL-{str(cell)}/LNCEL_TDD-0']")
        
        rootSeqIndex_element=MO_element_TDD_0.find(".//p[@name='rootSeqIndex']")
        rootSeqIndex_element.text = input1_dict[i]['RSI']

        dlMimoMode_element=MO_element_TDD_0.find(".//p[@name='dlMimoMode']")
        dlMimoMode_element.text = mimo_dict[input1_dict[i]['MIMO']]

        earfcn_element=MO_element_TDD_0.find(".//p[@name='earfcn']")
        earfcn_element.text = input1_dict[i]['EARFCN']
        try :
            bandwidth_element=MO_element_TDD_0.find(".//p[@name='chBw']")
            bandwidth_element.text = input1_dict[i]['Bandwidth'].strip() +" MHz"
        except:
            pass
       #---------------------------------------------- REDRT -------------------------------------
        REDRT_element_TDD_0=root.find(f".//managedObject[@class='NOKLTE:REDRT'][@distName='MRBTS-844360/LNBTS-844360/LNCEL-{str(cell)}/REDRT-0']")
        redirFreqEutra_element=REDRT_element_TDD_0.find(".//p[@name='redirFreqEutra']")
        redirFreqEutra_element.text = input1_dict[i]["EARFCN"]
    # #----------------------------------------------------------------------------------------------
        print("lnhoif:")
        for lnhoif_id,value in lnhoif_dict[cell].items():
            print(lnhoif_id,":",value) 
            MO_element_LNHOIF_1=root.find(f".//managedObject[@class='NOKLTE:LNHOIF'][@distName='MRBTS-844360/LNBTS-844360/LNCEL-{str(cell)}/LNHOIF-{str(lnhoif_id)}']/p[@name='eutraCarrierInfo']")
            MO_element_LNHOIF_1.text = value


    # #-----------------------------------------------------------------------------------------------------------------------------------------------------------
        print("irfim:")
        for irfim_id,value in irfim_dict[cell].items(): 
            print(irfim_id,":",value)
            MO_element_IRFIM_1=root.find(f".//managedObject[@class='NOKLTE:IRFIM'][@distName='MRBTS-844360/LNBTS-844360/LNCEL-{str(cell)}/IRFIM-{str(irfim_id)}']/p[@name='dlCarFrqEut']")
            MO_element_IRFIM_1.text = value
    
        

    MRBTS= "MRBTS" + "-" +str(input2_dict['MRBTS ID'][0])
    LNBTS="LNBTS" + "-" +str(input2_dict['LNBTS ID'][0])
    root=MRBTS_LNBTS_change(root,LNBTS,MRBTS,cell_list,input1_dict)
    namespace = "raml21.xsd"
    prefix = ""

# Add the namespace to the root element
    ET.register_namespace(prefix, namespace)
    # file_path=r"C:\Users\Lenovo\Desktop\Django..., Projects\Mobile_com_web_app\mcom_website\media\Mcom_scriptor\singe_module_testing\main_op.xml"
    # tree.write(file_path,encoding="utf-8",xml_declaration=True)
    formatted_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name=str(input1_dict[0]['Siteid'])+"_"+ str(formatted_datetime) +".xml"
    save_path=os.path.join(MEDIA_ROOT,"Mcom_scriptor","output",file_name)
    ET.ElementTree(root).write(save_path, encoding="utf-8", xml_declaration=True)
    return file_name



if __name__=="__main__":
    input_df2=pd.read_excel(r"E:\Mcom_Projects_files\Mcom_Scriptor_project\ULS_Input Sheet_modified_6_cells.xlsx", sheet_name="Sheet2",dtype=str)
    # input_df2=input_df2.dropna().astype(str)
    input2_dict=input_df2.to_dict(orient='list')
    # print(input2_dict)
    for key,value in input2_dict.items():
        print(key,":",value)
        # print(value)

    input_df1=pd.read_excel(r"E:\Mcom_Projects_files\Mcom_Scriptor_project\ULS_Input Sheet_modified_6_cells.xlsx", sheet_name="CellWise",dtype=str)
    input_df1.dropna(subset=['Cell ID'], inplace=True)
    print(input_df1)
    input1_dict=input_df1.to_dict(orient='record')
    # print(input1_dict)
    for x in input1_dict:
        print(x)

    # xml_main_teml = r"E:\Mcom_Projects_files\Mcom_Scriptor_project\FSMF_TDD.xml"
    xml_main_temp = r"C:\Users\Lenovo\Desktop\Django..., Projects\Mobile_com_web_app\mcom_website\media\Mcom_scriptor\singe_module_testing\main_temp.xml"
   
    cell_list= input_df1["Cell ID"].tolist()
    print("cell_list.....................",cell_list)


    irfim_dict={'11':{1:'34',2:'23',3:'234',4:'895',5:'903',6:'903'},
                '12':{1:'34',2:'23',3:'234',4:'895',5:'903',6:'903'},
                '13':{1:'34',2:'23',3:'234',4:'895',5:'903',6:'903'},
                '21':{1:'69',2:'23',3:'234',4:'895',5:'903',6:'903'},
                '22':{1:'69',2:'23',3:'234',4:'895',5:'903',6:'903'},
                '23':{1:'69',2:'23',3:'234',4:'895',5:'903',6:'903'},
                }
    lnhoif_dict={'11':{1:'34',2:'23',3:'234',4:'895',5:'903',6:'903'},
            '12':{1:'34',2:'23',3:'234',4:'895',5:'903',6:'903'},
            '13':{1:'34',2:'23',3:'234',4:'895',5:'903',6:'903'},
            '21':{1:'69',2:'23',3:'234',4:'895',5:'903',6:'903'},
            '22':{1:'69',2:'23',3:'234',4:'895',5:'903',6:'903'},
            '23':{1:'69',2:'23',3:'234',4:'895',5:'903',6:'903'},
            }
    
   
    

    tree=process(input1_dict,input2_dict,cell_list,xml_main_temp,irfim_dict,lnhoif_dict)
    
    # Specify the namespace and prefix
   
    print("successfully")