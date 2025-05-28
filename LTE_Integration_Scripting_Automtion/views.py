################################################################################################################################################################################
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime
import os
import json
from LTE_Integration_Scripting_Automtion.circles.KK.KK_INTEGRATION_SCRIPT import (
    kk_GPL_LMS_script,
    kk_GPS_MMS_script,
    kk_TN_script_text,
    NR_CELL_CREATION_AND_SCTP_5G_ENDPOINT_CREATION,
    NR_GPL_LMS,
    KK_GNBCUCPFUNCTION_ELEMENT,
    KK_GNBDUFUNCTION_ELEMENT,
    TREMPOINT_GUTRANCELL_FREQ_RELATION
)
from LTE_Integration_Scripting_Automtion.circles.KK.KK_COMISSIONING_SCRIPT import (
    KK_SITE_BASIC_SCRIPT, KK_SITE_EQUIPMENT_SCRIPT, kk_5G_RRU_creation
)

from LTE_Integration_Scripting_Automtion.universal_SCRIPTS.UNIVERSAL_SCRIPTS import (
    tdd_cell_script, 
    fdd_cell_script, 
    RRU_2219_B0_B1_B3_2X2, 
    RRU_4412_4418_4427_4471_4X4, 
    RRU_6626_6X6, RRU_8863_8X8, 
    RRU_5G_CREATION,
    RBSSummary_script
)
from LTE_Integration_Scripting_Automtion.circles.TN.TN_INTEGRATION_SCRIPT import (
    TN_02_IPV6creationforanchor, 
    TN_03_ENDCanchornode_ROTN, 
    TN_04_FreqRelation, 
    TN_05_5G_LMS_GPL_ROTN, 
    TN_s1_FOR_TN_IDL_B_PORT, 
    TN_s3_LTE_GPL_LMS, 
    NR_TN_RN_Cell_Def,
    TN_GNBCUCPFUNCTION_ELEMENT,
    TN_GNBDUFUNCTION_ELEMENT
)
from mcom_website.settings import MEDIA_ROOT, MEDIA_URL
import pandas as pd
import stat
from django.conf import settings
import zipfile

############################################################## END IMPORT STATEMENTS ############################################################################################

################################################################ MEDIA URL ######################################################################################################
MEDIA_ROOT = settings.MEDIA_ROOT

def ZipFolder(folder_path, ZIP_OUPUT_PATH):
    with zipfile.ZipFile(ZIP_OUPUT_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)


<<<<<<< HEAD
=======



>>>>>>> 56265a0748ce46dced280db17444e8d6ead71b44
def create_script_paths(base_dir, node_name):
    base_node_dir = os.path.join(
        base_dir,
        f"{node_name}_REMOTE_INTEGRATION_SCRIPTS_COMMISSIONING_SCRIPTS",
        f"{node_name}_REMOTE_INTEGRATION_SCRIPTS"
    )

    directories = {
        "lte": os.path.join(base_node_dir, "LTE_4G"),
        "nr": os.path.join(base_node_dir, "NR_5G"),
        "commissioning": os.path.join(
            base_dir,
            f"{node_name}_REMOTE_INTEGRATION_SCRIPTS_COMMISSIONING_SCRIPTS",
            f"{node_name}_Commissioning_Scripts"
        )
    }

    for path in directories.values():
        os.makedirs(path, exist_ok=True)

    return directories


<<<<<<< HEAD
####################################################### --- TN circle code for generating scripts GNBDU and GNBCUCP ----- #############################################################################################################
=======
def generate_lte_cell_def_scripts(lte_df, directories, node_name, current_time):
    ##################################################### Define required columns for FDD and TDD #######################################################################
    columns_to_needed_fdd = [
        "sectorCarrierId", "configuredMaxTxPower", "noOfTxAntennas",
        "noOfRxAntennas", "sectorEquipmentFunctionId", "eUtranCellFDDId",
        "cellId", "crsGain", "dlChannelBandwidth", "earfcndl", "earfcnul",
        "Latitude", "Longitude", "physicalLayerCellIdGroup",
        "physicalLayerSubCellId", "rachRootSequence", "tac",
        "ulChannelBandwidth"
    ]
>>>>>>> 56265a0748ce46dced280db17444e8d6ead71b44

    columns_to_needed_tdd = [
        "sectorCarrierId", "configuredMaxTxPower", "noOfTxAntennas",
        "noOfRxAntennas", "sectorEquipmentFunctionId", "eUtranCellFDDId",
        "cellId", "crsGain", "dlChannelBandwidth", "earfcndl",
        "Latitude", "Longitude", "physicalLayerCellIdGroup",
        "physicalLayerSubCellId", "rachRootSequence", "tac",
        "ulChannelBandwidth"
    ]

    node_rows = lte_df[lte_df["eNodeBName"] == node_name]
    output_file_path = os.path.join(
        directories["lte"], f"3_Cell_Def_script_{node_name}_{current_time}.txt"
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
        lte_df["earfcnul"] = lte_df["earfcnul"].astype("Int64")
        unique_nodes = lte_df["eNodeBName"].dropna().unique()

        for node_name in unique_nodes:
<<<<<<< HEAD
            current_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            node_dir = os.path.join(
                base_path_url, f"{node_name}_REMOTE_INTEGRATION_SCRIPTS_COMMISSIONING_SCRIPTS",f"{node_name}_REMOTE_INTEGRATION_SCRIPTS", "LTE_4G"
            )

            node_dir_5g = os.path.join(
                base_path_url, f"{node_name}_REMOTE_INTEGRATION_SCRIPTS_COMMISSIONING_SCRIPTS",f"{node_name}_REMOTE_INTEGRATION_SCRIPTS", "NR_5G"
            )
            os.makedirs(node_dir, exist_ok=True)
            os.makedirs(node_dir_5g, exist_ok=True)
            node_rows = lte_df[lte_df["eNodeBName"] == node_name]
            output_file_path = os.path.join(
                node_dir, f"3 Cell_Def_script_{node_name}_{current_time}.txt"
            )
            #os.makedirs(output_file_path, exist_ok=True)
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
=======
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            directories = create_script_paths(base_path_url, node_name)        
            generate_lte_cell_def_scripts(lte_df=lte_df, directories=directories, node_name=node_name, current_time=current_time)
>>>>>>> 56265a0748ce46dced280db17444e8d6ead71b44

        ##################################################################### Map Node -> Cell IDs ############################################################################
        unique_nodes = lte_df["eNodeBName"].unique()
        cell_mapped_node = {
            node: lte_df[lte_df["eNodeBName"] == node]["eUtranCellFDDId"].to_list()
            for node in unique_nodes
        }
        ############################################################## KK Circle-specific Script Generation ####################################################################
        if circle == "KK":
            current_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            
            for idx, row in site_basic_df.iterrows():
                print(site_basic_df)
                node_name = row.get("eNodeBName", "UnknownNode")
                
                node_dir = create_script_paths(base_path_url, node_name)['lte']
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
                script_path = os.path.join(create_script_paths(base_path_url, node)['lte'], gps_mme_path)
                with open(script_path,"a") as file:
                    file.write(kk_GPS_MMS_script + "\n")

            ########################################################################## GPL/LMS Script ###########################################################################
            gpl_lms_path = f"4 GPL_LMS_script_{node_name}_{current_time}.txt"
            for node in unique_nodes:
                script_path = os.path.join(create_script_paths(base_path_url, node)['lte'], gpl_lms_path)
                with open(script_path,"a") as file:
                    file.write(kk_GPL_LMS_script + "\n")

            ############################################################################### 5G Cell Scripts ##########################################################################
            #---------------------------------------------------------------------------------------------------
            if not nr_cell_df.empty:
                for node in nr_cell_df["gNodeBName"].unique():
                    nr_cell_df: pd.DataFrame = nr_cell_df[
                        nr_cell_df["gNodeBName"] == node
                    ]
                    nr_cell_df.rename(
                        columns={"bSChannelBwDL/UL": "bSChannelBwDL-UL"}, inplace=True
                    )
                    nr_cell_df_path = os.path.join(
                        create_script_paths(base_path_url, node)['nr'], f"1_{node}_5G Cell creation_Sctp Endpoint Creation_{current_time}.txt"
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
                            bSChannelBwDL_UL=row["bSChannelBwDL-UL"],
                            configuredMaxTxPower=row["configuredMaxTxPower"],
                            Latitude=row["Latitude"],
                            Longitude=row["Longitude"],
                            sectorEquipmentFunctionId=row["sectorEquipmentFunctionId"],
                            gUtranCell=row["gUtranCell"],
                            cellLocalId=row["cellLocalId"],
                            nRPCI=row["nRPCI"],
                            nRTAC=row["nRTAC"],
<<<<<<< HEAD
                            rachRootSequence = row["rachRootSequence"],  ############################################################################ Added rachRootSequence
=======
                            rachRootSequence = row["rachRootSequence"],  # Added rachRootSequence
                            ssbFrequency = row['ssbFrequency']
>>>>>>> 56265a0748ce46dced280db17444e8d6ead71b44

                        )

                        gnbcucp_fuction_element += KK_GNBCUCPFUNCTION_ELEMENT.format(
                            gUtranCell=row["gUtranCell"],
                            cellLocalId=row["cellLocalId"],
                        )
                    with open(nr_cell_df_path, "a") as file:
                        file.write(
                            NR_CELL_CREATION_AND_SCTP_5G_ENDPOINT_CREATION.format(
                                gNBId=gnbid,
                                GNBDUFUNCTION_SCRIPT_ELEMENT=gnbdu_fuction_element,
                                GNBCUCPFUNCTION_SCRIPT_ELEMENT=gnbcucp_fuction_element,
                            )
                        )
                        file.close()
                

                    NR_GPL_LMS_path = os.path.join(create_script_paths(base_path_url, node)['nr'], f"2_{node}_NR_GPL_LMS_{current_time}.txt")
                    with open(NR_GPL_LMS_path, "a") as file:
                        file.write(NR_GPL_LMS + "\n")

                    Termpoint_GUtranFreqRelation_path = os.path.join(
                        create_script_paths(base_path_url, node_name)['nr'], f"3_{node_name}_Termpoint_GUtranFreqRelation_{current_time}.txt"
                    )
                    with open(Termpoint_GUtranFreqRelation_path, "a") as file:
                        file.write(TREMPOINT_GUTRANCELL_FREQ_RELATION + "\n")
                # .......................................................................... NRCELL CONFIGRATION FOR CELL CREATION IN 5G ................................................

            ############################################################### creating the SiteBasic script for 4G and 5G ###############################################################
            for node in site_basic_df["eNodeBName"].unique():
                commision_scripts_dir = create_script_paths(base_path_url, node)['commissioning']
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                os.makedirs(commision_scripts_dir, exist_ok=True)
                sitebasic_df: pd.DataFrame = site_basic_df[
                    site_basic_df["eNodeBName"] == node
                ]
                sitebasic_df_path = os.path.join(
                    commision_scripts_dir, f"01_SiteBasic_{node}_{current_time}.xml"
                )
                siteBasicFilePath = os.path.relpath(
                    sitebasic_df_path,
                    os.path.join(base_path_url, f"{node}_REMOTE_INTEGRATION_SCRIPTS_COMMISSIONING_SCRIPTS")
                ).replace("\\", "/")
                relative_path = os.path.relpath(
                    sitebasic_df_path,
                    os.path.join(base_path_url, f"{node_name}_REMOTE_INTEGRATION_SCRIPTS_COMMISSIONING_SCRIPTS")
                )
                siteBasicFilePath = relative_path.replace("\\", "/")


                for idx, row in sitebasic_df.iterrows():
                    with open(sitebasic_df_path, "a") as file:
                        file.write(
                            KK_SITE_BASIC_SCRIPT.format(
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
                commissioning_scripts_dir = create_script_paths(base_path_url, node)['commissioning']
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                os.makedirs(commissioning_scripts_dir, exist_ok=True)

                site_specific_rru_df = rru_hw_df[rru_hw_df["eNodeBName"] == node]
                rru_hw_path = os.path.join(
                    commissioning_scripts_dir,
                    f"02_SiteEquipment_{node}_{current_time}.xml",
                )
                site_equipment_text = ""
<<<<<<< HEAD
                relative_path = os.path.relpath(
                    rru_hw_path,
                    os.path.join(base_path_url, f"{node_name}_REMOTE_INTEGRATION_SCRIPTS_COMMISSIONING_SCRIPTS")
                )
                siteEquipmentFilePath = relative_path.replace("\\", "/")

=======
                siteEquipmentFilePath = os.path.relpath(
                    rru_hw_path,
                    os.path.join(base_path_url, f"{node}_REMOTE_INTEGRATION_SCRIPTS_COMMISSIONING_SCRIPTS")
                ).replace("\\", "/")
>>>>>>> 56265a0748ce46dced280db17444e8d6ead71b44


                print("site_equipment_path", siteEquipmentFilePath)
                site_basic_df_N = site_basic_df[site_basic_df["eNodeBName"] == node]
                if site_basic_df_N.empty:
                    print(f"Warning: No basic site data found for {node}")
                    continue

                site_basic_df_N.rename(
                    columns={"Phy SiteID/Userlabel": "Phy_SiteID_Userlabel"},
                    inplace=True,
                )

                site_equipment_script_text = KK_SITE_EQUIPMENT_SCRIPT.format(
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
                node_dir = create_script_paths(base_path_url, node_name)['lte']
                node_dir_5g = create_script_paths(base_path_url, node_name)['nr']
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
        ########################################################## MAKING THE ZIP FILE #############################################################
        
        ZIP_OUTPUT_PATH = ...
        
        ############################################################################################################################################
        return Response(
            {"status": "OK", "message": "Integration scripts generated successfully."},
            status=status.HTTP_200_OK,
        )
