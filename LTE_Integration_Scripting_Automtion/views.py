from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime
import os
import json
from LTE_Integration_Scripting_Automtion.remote_commision_scripts import (
    RRU_2219_B0_B1_B3_2X2,
    RRU_4412_4418_4427_4471_4X4,
    RRU_6626_6X6,
    RRU_8863_8X8,
    SiteBasic_script,
    site_equipment_script,
    RBSSummary_script,
)
from LTE_Integration_Scripting_Automtion.remote_integration_scripts import *
from mcom_website.settings import MEDIA_ROOT, MEDIA_URL
import pandas as pd
import stat
from django.conf import settings

MEDIA_ROOT = settings.MEDIA_ROOT


####################################################### --- TN ----- ##########################################################


TN_GNBDUFUNCTION_ELEMENT = """ 
crn GNBDUFunction=1,NRSectorCarrier={nRSectorCarrierId}
administrativeState 1
arfcnDL {arfcnDL}
arfcnUL {arfcnUL}
bSChannelBwDL {bSChannelBwDLUL}
bSChannelBwUL {bSChannelBwDLUL}
configuredMaxTxPower {configuredMaxTxPower}
latitude {Latitude}
longitude {Longitude}
sectorEquipmentFunctionRef NodeSupport=1,SectorEquipmentFunction={sectorEquipmentFunctionId}
txDirection 0
txPowerChangeRate 1
txPowerPersistentLock false
txPowerRatio 100
end
#END GNBDUFunction=1,NRSectorCarrier={nRSectorCarrierId} --------------------

crn GNBDUFunction=1,NRCellDU={gUtranCell}
csiRsConfig16P csiRsControl16Ports=0
csiRsConfig2P aRestriction=3F,csiRsControl2Ports=1
csiRsConfig32P csiRsControl32Ports=0
csiRsConfig4P csiRsControl4Ports=1,i11Restriction=FF
csiRsConfig8P csiRsControl8Ports=1,i11Restriction=FFFF
pLMNIdList mcc=404,mnc=94
sibType2 siBroadcastStatus=0,siPeriodicity=64
sibType4 siBroadcastStatus=0,siPeriodicity=64
sibType5 siBroadcastStatus=0,siPeriodicity=64
sibType6 siBroadcastStatus=0,siPeriodicity=16
sibType7 siBroadcastStatus=0,siPeriodicity=64
sibType8 siBroadcastStatus=0,siPeriodicity=64
ailgDlPrbLoadLevel 0
ailgModType 0
ailgPdcchLoadLevel 0
bandListManual 78
cellBarred 1
cellLocalId {cellLocalId}
cellRange 12000
cellReservedForOperator 1
csiReportFormat 0
csiRsPeriodicity 40
dftSOfdmMsg3Enabled false
dftSOfdmPuschEnabled false
dl256QamEnabled true
dlMaxMuMimoLayers 0
dlStartCrb 0
endcUlLegSwitchEnabled true
endcUlNrLowQualThresh -4
endcUlNrQualHyst 6
maxUeSpeed 2
nRPCI {nRPCI}
nRSectorCarrierRef GNBDUFunction=1,NRSectorCarrier={nRSectorCarrierId}
nRTAC {nRTAC}
pdschStartPrbStrategy 3
pMax 23
puschStartPrbStrategy 3
pZeroNomPucch -110
pZeroNomPuschGrant -102
qRxLevMin -128
rachPreambleFormat 0
rachPreambleRecTargetPower -110
rachPreambleTransMax 10
rachRootSequence 733
secondaryCellOnly false
siWindowLength 20
ssbDuration 1
ssbFrequency {ssbFrequency}
ssbOffset 0
ssbPeriodicity 20
ssbSubCarrierSpacing 30
subCarrierSpacing 30
tddSpecialSlotPattern 1
tddUlDlPattern 1
trsPeriodicity 40
trsPowerBoosting 0
ul256QamEnabled true
ulMaxMuMimoLayers 0
ulStartCrb 0
userLabel {gUtranCell}
end
#END GNBDUFunction=1,NRCellDU={gUtranCell} --------------------


crn GNBDUFunction=1,NRSectorCarrier={nRSectorCarrierId},CommonBeamforming=1
cbfMacroTaperType 0
coverageShape 1
digitalTilt 30
end
#END GNBDUFunction=1,NRSectorCarrier={nRSectorCarrierId},CommonBeamforming=1 --------------------
"""


TN_GNBCUCPFUNCTION_ELEMENT = """ 
crn GNBCUCPFunction=1,NRCellCU={gUtranCell}
cellLocalId {cellLocalId}
qHyst 4
sNonIntraSearchP 0
threshServingLowP 0
transmitSib2 false
transmitSib4 false
transmitSib5 false
userLabel {gUtranCell}
end
#END GNBCUCPFunction=1,NRCellCU={gUtranCell} --------------------

crn GNBCUCPFunction=1,NRNetwork=1
end
#END GNBCUCPFunction=1,NRNetwork=1 --------------------

crn GNBCUCPFunction=1,NRNetwork=1,NRFrequency=629952-30
arfcnValueNRDl 629952
bandListManual 78
smtcDuration 1
smtcOffset 0
smtcPeriodicity 20
smtcScs 30
end
#END GNBCUCPFunction=1,NRNetwork=1,NRFrequency=629952-30 --------------------

crn GNBCUCPFunction=1,NRCellCU={gUtranCell},NRFreqRelation=629952
anrMeasOn true
cellReselectionPriority 7
nRFrequencyRef GNBCUCPFunction=1,NRNetwork=1,NRFrequency=629952-30
end
#END GNBCUCPFunction=1,NRCellCU={gUtranCell},NRFreqRelation=629952 --------------------
"""


KK_GNBDUFUNCTION_ELEMENT = """
##########################################GNBDUFunction=1,NRSectorCarrier={nRSectorCarrierId}##########################################################################


crn GNBDUFunction=1,NRSectorCarrier={nRSectorCarrierId}
administrativeState 1
arfcnDL {arfcnDL}                                          
arfcnUL {arfcnUL}                                           
bSChannelBwDL {bSChannelBwDLUL}                                        
bSChannelBwUL {bSChannelBwDLUL}                                        
configuredMaxTxPower {configuredMaxTxPower}
latitude {Latitude}                                         
longitude {Longitude}                                        
sectorEquipmentFunctionRef NodeSupport=1,SectorEquipmentFunction={sectorEquipmentFunctionId}
txDirection 0
txPowerChangeRate 1
txPowerPersistentLock false
txPowerRatio 100
end
#END GNBDUFunction=1,NRSectorCarrier={nRSectorCarrierId} --------------------

##########################################GNBDUFunction=1,{gUtranCell}##########################################################################


crn GNBDUFunction=1,NRCellDU={gUtranCell}                  
csiRsConfig16P csiRsControl16Ports=0
csiRsConfig2P aRestriction=3F,csiRsControl2Ports=1
csiRsConfig32P csiRsControl32Ports=0
csiRsConfig4P csiRsControl4Ports=1,i11Restriction=FF
csiRsConfig8P csiRsControl8Ports=1,i11Restriction=FFFF
pLMNIdList mcc=404,mnc=45
sibType2 siBroadcastStatus=0,siPeriodicity=64
sibType4 siBroadcastStatus=0,siPeriodicity=64
sibType5 siBroadcastStatus=0,siPeriodicity=64
sibType6 siBroadcastStatus=0,siPeriodicity=16
sibType7 siBroadcastStatus=0,siPeriodicity=64
sibType8 siBroadcastStatus=0,siPeriodicity=64
administrativeState 1
ailgDlPrbLoadLevel 0
ailgModType 0
ailgPdcchLoadLevel 0
bandListManual 78
bfrEnabled true
cellBarred 1
cellLocalId {cellLocalId}                                                          
cellRange 15000
cellReservedForOperator 1
csiReportFormat 0
csiRsPeriodicity 40
dftSOfdmMsg3Enabled false
dftSOfdmPuschEnabled false
dl256QamEnabled true
dlMaxMuMimoLayers 0
dlStartCrb 0
drxEnable false
drxInactivityTimer 15
drxLongCycle 10
drxOnDurationTimer 39
endcDlNrLowQualThresh 3
endcDlNrQualHyst 5
endcUlLegSwitchEnabled true
endcUlNrLowQualThresh -4
endcUlNrQualHyst 6
maxUeSpeed 2
nRPCI {nRPCI}                                                                     
nRSectorCarrierRef GNBDUFunction=1,NRSectorCarrier={nRSectorCarrierId}
nRTAC {nRTAC}                                                                   
pdschStartPrbStrategy 3
pMax 23
puschStartPrbStrategy 3
pZeroNomPucch -110
pZeroNomPuschGrant -102
qRxLevMin -128
rachPreambleFormat 0
rachPreambleRecTargetPower -110
rachPreambleTransMax 10
rachRootSequence 273
secondaryCellOnly false
siWindowLength 20
ssbDuration 1
ssbFrequency 627936
ssbOffset 0
ssbPeriodicity 20
ssbSubCarrierSpacing 30
subCarrierSpacing 30
tddSpecialSlotPattern 3
tddUlDlPattern 1
trsPeriodicity 40
trsPowerBoosting 0
ul256QamEnabled true
ulMaxMuMimoLayers 0
ulStartCrb 0
userLabel {gUtranCell}
end
#END GNBDUFunction=1,NRCellDU={gUtranCell} --------------------



crn GNBDUFunction=1,NRSectorCarrier={nRSectorCarrierId},CommonBeamforming=1
cbfMacroTaperType 0
coverageShape 1
digitalTilt 30
end
#END GNBDUFunction=1,NRSectorCarrier={nRSectorCarrierId},CommonBeamforming=1 --------------------

crn GNBDUFunction=1,NRSectorCarrier={nRSectorCarrierId},CommonBeamforming=1
cbfMacroTaperType 0
coverageShape 1
digitalTilt 30
end
#END GNBDUFunction=1,NRSectorCarrier={nRSectorCarrierId},CommonBeamforming=1 --------------------

crn GNBDUFunction=1,TermPointToGNBCUCP=1
administrativeState 1
ipv4Address 10.0.0.1
ipv6Address ::
end
#END GNBDUFunction=1,TermPointToGNBCUCP=1 --------------------

ld GNBDUFunction=1
lset GNBDUFunction=1$ endpointResourceRef GNBDUFunction=1,EndpointResource=1
"""


KK_GNBCUCPFUNCTION_ELEMENT = """
##########################################GNBCUCPFunction=1,{gUtranCell}##########################################################################


crn GNBCUCPFunction=1,NRCellCU={gUtranCell}
cellLocalId {cellLocalId}
qHyst 4
sNonIntraSearchP 0
threshServingLowP 0
transmitSib2 false
transmitSib4 false
transmitSib5 false
userLabel {gUtranCell}
end
#END GNBCUCPFunction=1,NRCellCU={gUtranCell} --------------------

crn GNBCUCPFunction=1,NRNetwork=1
end
#END GNBCUCPFunction=1,NRNetwork=1 --------------------


crn GNBCUCPFunction=1,NRNetwork=1,NRFrequency=627936-30
arfcnValueNRDl 627936
smtcScs 30
end
#END GNBCUCPFunction=1,NRNetwork=1,NRFrequency=627936-30 --------------------

crn GNBCUCPFunction=1,NRCellCU={gUtranCell},NRFreqRelation=627936
anrMeasOn true
cellReselectionPriority 7
nRFrequencyRef GNBCUCPFunction=1,NRNetwork=1,NRFrequency=627936-30
end
#END GNBCUCPFunction=1,NRCellCU={gUtranCell},NRFreqRelation=627936 --------------------
"""


@api_view(["GET", "POST"])
def generate_integration_script(request):
    if request.method == "POST":
        integration_input_file = request.FILES.get("integration_input_file")
        circle = request.POST.get(
            "Circle"
        )  ########################## circle for different frequency and configreation as per circle:- ['AP','KK', 'DEL',...]

        if circle is None:
            return Response(
                {"status": "ERROR", "message": "circle not provided or invalid."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not integration_input_file:
            return Response(
                {
                    "status": "ERROR",
                    "message": "integration_input_file not provided or invalid.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            integration_file = pd.ExcelFile(integration_input_file)
            lte_df = integration_file.parse("LTE-CELL")
            rru_hw_df = integration_file.parse("Radio_HW")
            site_basic_df = integration_file.parse("Site_Basic")
            nr_cell_df = integration_file.parse("NR-CELL")
        except Exception as e:
            return Response(
                {"status": "ERROR", "message": f"Failed to parse Excel file: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        base_path_url = os.path.join(MEDIA_ROOT, "LTE_INTEGRATION_CONFIG_FILES")
        os.makedirs(base_path_url, exist_ok=True)
        siteBasicFilePath = ""
        siteEquipmentFilePath = ""
        ################################################ Define required columns for fdd and tdd also ###############################################################
        columns_to_needed_fdd = list(
            dict.fromkeys(
                [
                    "sectorCarrierId",
                    "configuredMaxTxPower",
                    "noOfTxAntennas",
                    "noOfRxAntennas",
                    "sectorEquipmentFunctionId",
                    "eUtranCellFDDId",
                    "cellId",
                    "crsGain",
                    "dlChannelBandwidth",
                    "earfcndl",
                    "earfcnul",
                    "Latitude",
                    "Longitude",
                    "physicalLayerCellIdGroup",
                    "physicalLayerSubCellId",
                    "rachRootSequence",
                    "tac",
                    "ulChannelBandwidth",
                ]
            )
        )

        columns_to_needed_tdd = list(
            dict.fromkeys(
                [
                    "sectorCarrierId",
                    "configuredMaxTxPower",
                    "noOfTxAntennas",
                    "noOfRxAntennas",
                    "sectorEquipmentFunctionId",
                    "eUtranCellFDDId",
                    "cellId",
                    "crsGain",
                    "dlChannelBandwidth",
                    "earfcndl",
                    "Latitude",
                    "Longitude",
                    "physicalLayerCellIdGroup",
                    "physicalLayerSubCellId",
                    "rachRootSequence",
                    "tac",
                    "ulChannelBandwidth",
                ]
            )
        )

        ############################################################# Generate FDD/TDD Cell Scripts ####################################################################
        lte_df["earfcnul"] = lte_df["earfcnul"].astype("Int64")
        unique_nodes = lte_df["eNodeBName"].dropna().unique()

        for node_name in unique_nodes:
            current_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            node_dir = os.path.join(
                base_path_url, f"{node_name}_REMOTE_INTEGRATION_SCRIPTS", "LTE_4G"
            )
            node_dir_5g = os.path.join(
                base_path_url, f"{node_name}_REMOTE_INTEGRATION_SCRIPTS", "NR_5G"
            )
            os.makedirs(node_dir, exist_ok=True)
            os.makedirs(node_dir_5g, exist_ok=True)
            node_rows = lte_df[lte_df["eNodeBName"] == node_name]
            output_file_path = os.path.join(
                node_dir, f"3 Cell_Def_script_{node_name}_{current_time}.txt"
            )
            script_lines = []
            for _, row in node_rows.iterrows():
                cell_id = row.get("eUtranCellFDDId", "")

                if any(f in cell_id for f in ["_F1_", "_F3_", "_F8_"]):
                    formatted = fdd_cell_script.format(
                        **{key: row.get(key, "") for key in columns_to_needed_fdd}
                    )
                    script_lines.append(formatted)
                elif any(t in cell_id for t in ["_T1_", "_T2_"]):
                    formatted = tdd_cell_script.format(
                        **{key: row.get(key, "") for key in columns_to_needed_tdd}
                    )
                    script_lines.append(formatted)
            if script_lines:
                with open(output_file_path, "w") as file:
                    file.write("\n".join(script_lines) + "\n")

        ##################################################################### Map Node -> Cell IDs ############################################################################
        unique_nodes = lte_df["eNodeBName"].unique()
        cell_mapped_node = {
            node: lte_df[lte_df["eNodeBName"] == node]["eUtranCellFDDId"].to_list()
            for node in unique_nodes
        }

        ############################################################## KK Circle-specific Script Generation ####################################################################
        if circle == "KK":
            for idx, row in site_basic_df.iterrows():
                node_name = row.get("eNodeBName", "UnknownNode")
                current_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                node_dir = os.path.join(
                    base_path_url, f"{node_name}_REMOTE_INTEGRATION_SCRIPTS", "LTE_4G"
                )
                os.makedirs(node_dir, exist_ok=True)

                if node_name in cell_mapped_node:
                    cell_ids = cell_mapped_node[node_name]

                    if any(
                        tech in "".join(cell_ids) for tech in ["_F1_", "_F2_", "_F3_"]
                    ):
                        formatted_text = kk_TN_script_text.format(
                            eNodeBName=row["eNodeBName"], eNBId=row["eNBId"]
                        )
                        script_path = os.path.join(
                            node_dir, f"1 TN_Script_{node_name}_{current_time}.txt"
                        )
                        with open(script_path, "a") as file:
                            file.write(formatted_text + "\n")

                    elif any(tech in "".join(cell_ids) for tech in ["_T1_", "_T2_"]):
                        formatted_text = kk_TN_script_text.format(
                            eNodeBName=row["eNodeBName"], eNBId=row["eNBId"]
                        )
                        script_path = os.path.join(
                            node_dir, f"1 TN_Script_{node_name}_{current_time}.txt"
                        )
                        with open(script_path, "a") as file:
                            file.write(formatted_text + "\n")

            ######################################################################### GPS/MME Script #######################################################################
            gps_mme_path = f"2 GPS_MME_script_{node_name}_{current_time}.txt"
            for node in unique_nodes:
                with open(
                    os.path.join(
                        base_path_url,
                        f"{node}_REMOTE_INTEGRATION_SCRIPTS",
                        "LTE_4G",
                        gps_mme_path,
                    ),
                    "a",
                ) as file:
                    file.write(kk_GPS_MMS_script + "\n")

            ########################################################################## GPL/LMS Script ###########################################################################
            gpl_lms_path = f"4 GPL_LMS_script_{node_name}_{current_time}.txt"
            for node in unique_nodes:
                with open(
                    os.path.join(
                        base_path_url,
                        f"{node}_REMOTE_INTEGRATION_SCRIPTS",
                        "LTE_4G",
                        gpl_lms_path,
                    ),
                    "a",
                ) as file:
                    file.write(kk_GPL_LMS_script + "\n")

            ############################################################################### 5G Cell Scripts ##########################################################################
            rru_5G_creation = rru_5G_creation_xml
            os.makedirs(node_dir_5g, exist_ok=True)
            if not nr_cell_df.empty:
                rru_5g_creation_path = os.path.join(
                    node_dir_5g, f"1_5G RRU creation.xml"
                )
                with open(rru_5g_creation_path, "a") as file:
                    file.write(rru_5G_creation + "\n")

                sctp_5g_endpoint_path = os.path.join(
                    node_dir_5g, f"3_5G Sctp Endpoint Creation.txt"
                )
                with open(sctp_5g_endpoint_path, "a") as file:
                    file.write(sctp_5g_endpoint_creation + "\n")

                Standalone_LTE_TERM_Enter_NR_IP_path = os.path.join(
                    node_dir_5g, f"4_Standalone_LTE_TERM_Enter NR IP.mos"
                )
                with open(Standalone_LTE_TERM_Enter_NR_IP_path, "a") as file:
                    file.write(Standalone_LTE_TERM_Enter_NR_IP + "\n")

                NR_GPL_LMS_path = os.path.join(node_dir_5g, f"5_NR_GPL_LMS.txt")
                with open(NR_GPL_LMS_path, "a") as file:
                    file.write(nr_gpl_lms_script + "\n")

                OR_LTE_Relation_LTE_ONLY_site_Enter_Gnb_ID_path = os.path.join(
                    node_dir_5g, f"6_OR_LTE-Relation-LTE-ONLY-site_Enter Gnb ID.txt"
                )
                with open(OR_LTE_Relation_LTE_ONLY_site_Enter_Gnb_ID_path, "a") as file:
                    file.write(OR_LTE_Relation_LTE_ONLY_site_Enter_Gnb_ID + "\n")
                # .......................................................................... NRCELL CONFIGRATION FOR CELL CREATION IN 5G ................................................
                for node in nr_cell_df["gNodeBName"].unique():
                    nr_cell_df: pd.DataFrame = nr_cell_df[
                        nr_cell_df["gNodeBName"] == node
                    ]
                    nr_cell_df.rename(
                        columns={"bSChannelBwDL/UL": "bSChannelBwDL-UL"}, inplace=True
                    )
                    nr_cell_df_path = os.path.join(
                        node_dir_5g, f"2_5G Cell creation.txt"
                    )
                    gnbid = nr_cell_df["gNBId"].unique()[0]
                    print(nr_cell_df)

                    gnbdu_fuction_element = ""
                    gnbcucp_fuction_element = ""

                    for idx, row in nr_cell_df.iterrows():
                        gnbdu_fuction_element += KK_GNBDUFUNCTION_ELEMENT.format(
                            nRSectorCarrierId=row["nRSectorCarrierId"],
                            arfcnDL=row["arfcnDL"],
                            arfcnUL=row["arfcnUL"],
                            bSChannelBwDLUL=row["bSChannelBwDL-UL"],
                            configuredMaxTxPower=row["configuredMaxTxPower"],
                            Latitude=row["Latitude"],
                            Longitude=row["Longitude"],
                            sectorEquipmentFunctionId=row["sectorEquipmentFunctionId"],
                            gUtranCell=row["gUtranCell"],
                            cellLocalId=row["cellLocalId"],
                            nRPCI=row["nRPCI"],
                            nRTAC=row["nRTAC"],
                        )

                        gnbcucp_fuction_element += KK_GNBCUCPFUNCTION_ELEMENT.format(
                            gUtranCell=row["gUtranCell"],
                            cellLocalId=row["cellLocalId"],
                        )
                    with open(nr_cell_df_path, "a") as file:
                        file.write(
                            cell_creation_5g_script.format(
                                gNBId=gnbid,
                                GNBDUFUNCTION_SCRIPT_ELEMENT=gnbdu_fuction_element,
                                GNBCUCPFUNCTION_SCRIPT_ELEMENT=gnbcucp_fuction_element,
                            )
                        )
                        file.close()
            ############################################################### creating the SiteBasic script for 4G and 5G ###############################################################
            for node in site_basic_df["eNodeBName"].unique():
                commision_scripts_dir = os.path.join(
                    base_path_url, f"{node}_Commissioning_Scripts"
                )
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                os.makedirs(commision_scripts_dir, exist_ok=True)
                sitebasic_df: pd.DataFrame = site_basic_df[
                    site_basic_df["eNodeBName"] == node
                ]
                sitebasic_df_path = os.path.join(
                    commision_scripts_dir, f"01_SiteBasic_{node}_{current_time}.xml"
                )
                siteBasicFilePath = sitebasic_df_path.replace(
                    base_path_url + os.sep, ""
                ).replace("\\", "/")

                for idx, row in sitebasic_df.iterrows():
                    with open(sitebasic_df_path, "a") as file:
                        file.write(
                            SiteBasic_script.format(
                                eNodeBName=row["eNodeBName"],
                                fieldReplaceableUnitId=row["fieldReplaceableUnitId"],
                                tnPortId=row["tnPortId"],
                                OAM_vlan=row["OAM_vlan"],
                                OAM_IP=row["OAM_IP"],
                                LTE_UP_IP=row["LTE_UP_IP"],
                                NR_ENDC_IP=row["NR_ENDC_IP"],
                                LTE_UP_GW=row["LTE_UP_GW"],
                                OAM_GW=row["OAM_GW"],
                            )
                        )
                        file.close()

            for node in rru_hw_df["eNodeBName"].unique():
                commissioning_scripts_dir = os.path.join(
                    base_path_url, f"{node}_Commissioning_Scripts"
                )
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                os.makedirs(commissioning_scripts_dir, exist_ok=True)

                site_specific_rru_df = rru_hw_df[rru_hw_df["eNodeBName"] == node]
                rru_hw_path = os.path.join(
                    commissioning_scripts_dir,
                    f"02_SiteEquipment_{node}_{current_time}.xml",
                )
                site_equipment_text = ""
                siteEquipmentFilePath = rru_hw_path.replace(
                    base_path_url + os.sep, ""
                ).replace("\\", "/")

                print("site_equipment_path", siteEquipmentFilePath)
                site_basic_df_N = site_basic_df[site_basic_df["eNodeBName"] == node]
                if site_basic_df_N.empty:
                    print(f"Warning: No basic site data found for {node}")
                    continue

                site_basic_df_N.rename(
                    columns={"Phy SiteID/Userlabel": "Phy_SiteID_Userlabel"},
                    inplace=True,
                )

                site_equipment_script_text = site_equipment_script.format(
                    fieldReplaceableUnitId=site_basic_df_N[
                        "fieldReplaceableUnitId"
                    ].values[0],
                    Phy_SiteID_Userlabel=site_basic_df_N["Phy_SiteID_Userlabel"].values[
                        0
                    ],
                )

                for idx, row in site_specific_rru_df.iterrows():
                    radio_type = row["Radio_Type"]

                    if radio_type.startswith("RRU22"):
                        site_equipment_text += RRU_2219_B0_B1_B3_2X2.format(
                            eNodeBName=row["eNodeBName"],
                            Radio_UnitId=row["Radio_UnitId"],
                            fieldReplaceableUnitId=site_basic_df_N[
                                "fieldReplaceableUnitId"
                            ].values[0],
                            RiPort_BB=row["RiPort_BB"],
                            RiPort_Radio=row["RiPort_Radio"],
                            sectorEquipmentFunctionId=row["sectorEquipmentFunctionId"],
                        )
                    elif radio_type.startswith("RRU44"):
                        site_equipment_text += RRU_4412_4418_4427_4471_4X4.format(
                            eNodeBName=row["eNodeBName"],
                            Radio_UnitId=row["Radio_UnitId"],
                            fieldReplaceableUnitId=site_basic_df_N[
                                "fieldReplaceableUnitId"
                            ].values[0],
                            RiPort_BB=row["RiPort_BB"],
                            RiPort_Radio=row["RiPort_Radio"],
                            sectorEquipmentFunctionId=row["sectorEquipmentFunctionId"],
                        )
                    elif radio_type.startswith("RRU66"):
                        site_equipment_text += RRU_6626_6X6.format(
                            eNodeBName=row["eNodeBName"],
                            Radio_UnitId=row["Radio_UnitId"],
                            fieldReplaceableUnitId=site_basic_df_N[
                                "fieldReplaceableUnitId"
                            ].values[0],
                            RiPort_BB=row["RiPort_BB"],
                            RiPort_Radio=row["RiPort_Radio"],
                            sectorEquipmentFunctionId=row["sectorEquipmentFunctionId"],
                        )
                    elif radio_type.startswith("RRU88"):
                        site_equipment_text += RRU_8863_8X8.format(
                            eNodeBName=row["eNodeBName"],
                            Radio_UnitId=row["Radio_UnitId"],
                            fieldReplaceableUnitId=site_basic_df_N[
                                "fieldReplaceableUnitId"
                            ].values[0],
                            RiPort_BB=row["RiPort_BB"],
                            RiPort_Radio=row["RiPort_Radio"],
                            sectorEquipmentFunctionId=row["sectorEquipmentFunctionId"],
                        )

                with open(rru_hw_path, "a") as file:
                    file.write(
                        site_equipment_script_text + "\n" + site_equipment_text + "\n"
                    )

                site_equipment_script_path = os.path.join(
                    commissioning_scripts_dir, f"RBSSummary_{node}_{current_time}.xml"
                )
                with open(site_equipment_script_path, "a") as file:
                    file.write(
                        RBSSummary_script.format(
                            siteEquipmentFilePath=siteEquipmentFilePath,
                            siteBasicFilePath=siteBasicFilePath,
                        )
                    )

        ###############################################################################################################################################################################################################
        elif circle == "TN":
            # ..................................................... TN 4G Script ....................................................#
            for _, row in lte_df.iterrows():
                node_name = row.get("eNodeBName", "UnknownNode")
                current_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                node_dir = os.path.join(
                    base_path_url, f"{node_name}_REMOTE_INTEGRATION_SCRIPTS", "LTE_4G"
                )
                node_dir_5g = os.path.join(
                    base_path_url, f"{node_name}_REMOTE_INTEGRATION_SCRIPTS", "NR_5G"
                )
                os.makedirs(node_dir, exist_ok=True)
                formatted_text = TN_s1_FOR_TN_IDL_B_PORT.format(eNBId=row["enbId"])
                script_path = os.path.join(
                    node_dir, f"01_TN_FOR_TN_IDL_B_PORT_{node_name}_{current_time}.txt"
                )
                with open(script_path, "a") as file:
                    file.write(formatted_text + "\n")
                    file.close()

                TN_GPL_script_path = os.path.join(
                    node_dir, f"02_TN_LTE_GPL_LMS_{node_name}_{current_time}.txt"
                )
                formatted_text = TN_s3_LTE_GPL_LMS
                with open(TN_GPL_script_path, "a", encoding="utf-8") as file:
                    file.write(formatted_text + "\n")
                    file.close()
            # -------------------------------------------------------------------------- 5g ______________________________________________
            nr_cell_df = integration_file.parse("NR-CELL")
            for node in nr_cell_df["gNodeBName"].unique():
                nr_cell_df: pd.DataFrame = nr_cell_df[nr_cell_df["gNodeBName"] == node]
                nr_cell_df.rename(
                    columns={"bSChannelBwDL/UL": "bSChannelBwDL-UL"}, inplace=True
                )
                nr_cell_df_path = os.path.join(
                    node_dir_5g,
                    f"01_NR_TN_RN_Cell_Def_{node_name}_{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.txt",
                )
                os.makedirs(node_dir_5g, exist_ok=True)
                gnbid = nr_cell_df["gNBId"].unique()[0]
                print(nr_cell_df)
                gnbdu_fuction_element = ""
                gnbcucp_fuction_element = ""

                for idx, row in nr_cell_df.iterrows():
                    gnbdu_fuction_element += TN_GNBDUFUNCTION_ELEMENT.format(
                        nRSectorCarrierId=row["nRSectorCarrierId"],
                        arfcnDL=row["arfcnDL"],
                        arfcnUL=row["arfcnUL"],
                        bSChannelBwDLUL=row["bSChannelBwDL-UL"],
                        configuredMaxTxPower=row["configuredMaxTxPower"],
                        Latitude=row["Latitude"],
                        Longitude=row["Longitude"],
                        sectorEquipmentFunctionId=row["sectorEquipmentFunctionId"],
                        gUtranCell=row["gUtranCell"],
                        cellLocalId=row["cellLocalId"],
                        nRPCI=row["nRPCI"],
                        nRTAC=row["nRTAC"],
                        ssbFrequency=row["ssbFrequency"],
                    )

                    gnbcucp_fuction_element += TN_GNBCUCPFUNCTION_ELEMENT.format(
                        gUtranCell=row["gUtranCell"],
                        cellLocalId=row["cellLocalId"],
                    )

                with open(nr_cell_df_path, "a") as file:
                    file.write(
                        NR_TN_RN_Cell_Def.format(
                            gNBId=gnbid,
                            TN_GNPDUFUNCTION_ELEMENT=gnbdu_fuction_element,
                            TN_GNBCUCPFUNCTION_ELEMENT=gnbcucp_fuction_element,
                        )
                        + "\n"
                    )

                TN_02_IPV6creationforanchor_text = TN_02_IPV6creationforanchor
                os.makedirs(node_dir_5g, exist_ok=True)

                TN_02_IPV6creationforanchor_path = os.path.join(
                    node_dir_5g, f"02_IPV6creationforanchor.txt"
                )
                with open(TN_02_IPV6creationforanchor_path, "a") as file:
                    file.write(TN_02_IPV6creationforanchor_text + "\n")

                TN_03_ENDCanchornode_ROTN_path = os.path.join(
                    node_dir_5g, f"03_ENDCanchornode_ROTN.txt"
                )
                with open(TN_03_ENDCanchornode_ROTN_path, "a") as file:
                    file.write(TN_03_ENDCanchornode_ROTN + "\n")

                TN_04_FreqRelation_path = os.path.join(
                    node_dir_5g, f"04_FreqRelation.txt"
                )
                with open(TN_04_FreqRelation_path, "a") as file:
                    file.write(TN_04_FreqRelation + "\n")

                TN_05_5G_LMS_GPL_ROTN_path = os.path.join(
                    node_dir_5g, f"05_5G_LMS_GPL ROTN.txt"
                )
                with open(TN_05_5G_LMS_GPL_ROTN_path, "a") as file:
                    file.write(TN_05_5G_LMS_GPL_ROTN + "\n")

        return Response(
            {"status": "OK", "message": "Integration scripts generated successfully."},
            status=status.HTTP_200_OK,
        )
