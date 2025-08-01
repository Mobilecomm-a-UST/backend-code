################################################################################################################################################################################
from email.mime import base
from venv import create
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime
import shutil
import numpy as np
import socket
import os
import json
from mcom_website.settings import MEDIA_ROOT, MEDIA_URL
import pandas as pd
import stat
from django.conf import settings
import zipfile
from LTE_Integration_Scripting_Automtion.circles.KK.KK_INTEGRATION_SCRIPT import (
    kk_GPL_LMS_script,
    kk_GPS_MMS_script,
    kk_TN_script_text,
    NR_CELL_CREATION_AND_SCTP_5G_ENDPOINT_CREATION,
    NR_GPL_LMS,
    KK_GNBCUCPFUNCTION_ELEMENT,
    KK_GNBDUFUNCTION_ELEMENT,
    TREMPOINT_GUTRANCELL_FREQ_RELATION,
)
from LTE_Integration_Scripting_Automtion.circles.KK.KK_COMISSIONING_SCRIPT import (
    KK_SITE_BASIC_SCRIPT,
    KK_SITE_EQUIPMENT_SCRIPT,
    kk_5G_RRU_creation,
)

from LTE_Integration_Scripting_Automtion.universal_SCRIPTS.UNIVERSAL_SCRIPTS import (
    tdd_cell_script,
    fdd_cell_script,
    RRU_2219_B0_B1_B3_2X2,
    RRU_4412_4418_4427_4471_4X4,
    RRU_6626_6X6,
    RRU_8863_8X8,
    RBSSummary_script,
    AIR_5G_GENERATION_SCRIPT,
    SiteEquipment_5216,
    SiteEquipment_6303,
    SiteEquipment_6339,
    SiteEquipment_6353,
    SiteEquipment_6630,
    SiteEquipment_6631,
    SiteEquipment_6651,
    SiteEquipment_6648,
    SiteEquipment_R503,
    ABIS_Site_Basic_script,
)
from LTE_Integration_Scripting_Automtion.circles.TN.TN_INTEGRATION_SCRIPT import (
    TN_Termpoint_GUtranFreqRelation,
    TN_05_5G_LMS_GPL_ROTN,
    TN_s1_FOR_TN_IDL_B_PORT,
    TN_s1_FOR_TN_IDLTN_C_AND_TN_E_PORT,
    TN_s3_LTE_GPL_LMS,
    NR_TN_RN_Cell_Def,
    TN_GNBCUCPFUNCTION_ELEMENT,
    TN_GNBDUFUNCTION_ELEMENT,
)
from LTE_Integration_Scripting_Automtion.circles.TN.TN_COMISSIONING_SCRIPT import (
    TN_SITEBASIC_SCRIPT_BBU6630_BBU6631,
    TN_SITEBASIC_SCRIPT_BBU6651,
    TN_SITEEQUIPMENT_SCRIPT,
)

from LTE_Integration_Scripting_Automtion.circles.RJ.RJ_INTEGRATION_SCRIPT import (
    RJ_Route_4G_GPL_LMS,
    RJ_TN_RN_GPS_MME,
    CISCO_MME_SCRIPT,
    NOKIA_MME_SCRIPT,
    RJ_5G_Cell_creation_Sctp_Endpoint_Creation,
    RJ_5g_CgSwitch_text,
    RJ_GNBCUCPFunction_text,
    RJ_GNBDUFunction_text,
    RJ_Route_5G_GPL_LMS,
    RJ_Termpoint_GUtranFreqRelation
)
from LTE_Integration_Scripting_Automtion.circles.RJ.RJ_COMISSION_SCRIPT import (
    SiteBasic_ipv4_6303,
    SiteBasic_ipv6_6303,
    SiteBasic_ipv4_6339,
    SiteBasic_ipv4_6353,
    SiteBasic_ipv4_6630,
    SiteBasic_ipv4_6631,
    SiteBasic_ipv4_6651,
    SiteBasic_ipv6_6339,
    SiteBasic_ipv6_6630,
    SiteBasic_ipv6_6631,
    SiteBasic_ipv6_6651,
)


from LTE_Integration_Scripting_Automtion.circles.AS.AS_INTEGRATION_SCRIPT import (
    AS_GPL_LMS_DST_SCRIPT,
    AS_TN_RN_GPS_MME_SCRIPT,
    AS_5G_Cell_creation_Sctp_Endpoint_Creation,
    AS_Termpoint_GUtranFreqRelation_script,
    AS_GNBCUCPFunction,
    AS_GNBDUFunction,
    AS_NR_GPL_LMS_SCRIPT,
    AS_CGSWITCH_SCRIPT
)

from LTE_Integration_Scripting_Automtion.circles.AS.AS_COMISSIONING_SCRIPT import (
    AS_SiteBasic_5216_IPV4,
    AS_SiteBasic_5216_IPV6,
    AS_SiteBasic_6630_IPV4,
    AS_SiteBasic_6630_IPV6,
    AS_SiteBasic_6631_IPV4,
    AS_SiteBasic_6631_IPV6,
    AS_SiteBasic_6651_IPV4,
    AS_SiteBasic_6651_IPV6,
)


############################################################## END IMPORT STATEMENTS ############################################################################################

################################################################ MEDIA URL ######################################################################################################
MEDIA_ROOT = settings.MEDIA_ROOT


def zip_folder(folder_path, zip_output_path):
    """
    Compresses the contents of `folder_path` into a ZIP file at `zip_output_path`.
    Maintains the directory structure relative to `folder_path`.
    """
    with zipfile.ZipFile(zip_output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                abs_file_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_file_path, start=folder_path)
                zipf.write(abs_file_path, arcname=rel_path)


def create_script_paths(base_dir, node_name):
    base_node_dir = os.path.join(
        base_dir,
        f"{node_name}_Integration_Sripts",
        f"{node_name}_Remote_Integration_Scripts",
    )

    directories = {
        "lte": os.path.join(base_node_dir, "LTE_4G"),
        "nr": os.path.join(base_node_dir, "NR_5G"),
        "commissioning": os.path.join(
            base_dir,
            f"{node_name}_Integration_Sripts",
            f"{node_name}_Commissioning_Scripts",
        ),
    }

    for path in directories.values():
        os.makedirs(path, exist_ok=True)

    return directories


####################################################### --- TN circle code for generating scripts GNBDU and GNBCUCP ----- #############################################################################################################
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def generate_lte_cell_def_scripts(lte_df, directories, node_name, current_time):
    ##################################################### Define required columns for FDD and TDD #######################################################################
    columns_to_needed_fdd = [
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

    columns_to_needed_tdd = [
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

    node_rows = lte_df[lte_df["eNodeBName"] == node_name]
    output_file_path = os.path.join(
        directories["lte"], f"02_{node_name}_Cell_Def_script_{current_time}.txt"
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

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

####################################################################### MAKING THE COLUMNS VALIDATER #####################################################


def column_validater(
    Integration_rf_data: pd.ExcelFile, template_df: pd.ExcelFile
) -> None:
    """
    Validates that each sheet in Integration_rf_data contains all columns from the corresponding sheet in template_df.
    Shows only missing columns in the error message (columns expected but not found).
    Raises ValueError if any expected column is missing.
    """
    integration_sheet_names = Integration_rf_data.sheet_names
    template_sheet_names = template_df.sheet_names

    ############################################# Check for missing sheets ######################################################
    # missing_sheets = set(integration_sheet_names) - set(template_sheet_names)
    # if missing_sheets:
    #     raise ValueError(f"Invalid template sheet name(s): {', '.join(missing_sheets)}")
    ##############################################################################################################################

    def normalize_columns(columns):
        return [str(col).strip().lower() for col in columns]

    columns_status = {}
    for sheet in integration_sheet_names:
        expected_cols = normalize_columns(template_df.parse(sheet).columns)
        integration_cols = normalize_columns(Integration_rf_data.parse(sheet).columns)

        ##################################################### Identify missing columns ######################################################
        missing_columns = list(set(expected_cols) - set(integration_cols))
        found_columns = list(set(integration_cols) - set(expected_cols))

        if missing_columns:
            columns_status[sheet] = {"missing": missing_columns, "found": found_columns}

    if columns_status:
        error_messages = []
        for sheet, status in columns_status.items():
            error_messages.append(
                {
                    "sheet": sheet,
                    "missing_columns": status["missing"],
                    "found_columns": status["found"],  # shows all expected columns
                }
            )
        raise ValueError(error_messages)


@api_view(["GET", "POST"])
def generate_integration_script(request):
    if request.method == "POST":
        integration_input_file = request.FILES.get("integration_input_file")
        circle = request.POST.get(
            "Circle"
        )  ########################## circle for different frequency and configreation as per circle:- ['AP','KK', 'DEL',...]

        if circle is None:
            return Response(
                {"status": False, "error": "circle not provided or invalid."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not integration_input_file:
            return Response(
                {
                    "status": False,
                    "error": "integration_input_file not provided or invalid.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            integration_file = pd.ExcelFile(integration_input_file)
            lte_df = integration_file.parse("LTE-CELL")
            rru_hw_df = integration_file.parse("Radio_HW")
            site_basic_df = integration_file.parse("Site_Basic")
            nr_cell_df = integration_file.parse("NR-CELL")

            template_file = pd.ExcelFile(
                os.path.join(
                    MEDIA_ROOT,
                    "project_templates",
                    "LTE_Integration_file_tmplate",
                    "LTE_Integration_scriptV1.0_file.xlsx",
                )
            )
            column_validater(integration_file, template_file)

        except Exception as e:
            return Response(
                {"status": False, "error": f"{str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except ValueError as ve:
            return Response(
                {"status": False, "error": str(ve)}, status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------------------------------------------------------------------------------------------------------------------------------
        # -        -                    -          - ----------------------- defining the output path -------------------- -           -                 -
        base_path_url = os.path.join(MEDIA_ROOT, "LTE_INTEGRATION_CONFIG_FILES")
        if os.path.exists(base_path_url):
            os.chmod(base_path_url, stat.S_IWRITE)
            shutil.rmtree(base_path_url)
        os.makedirs(base_path_url, exist_ok=True)
        # ___________________________________________________________________________________________________________________________________________________________

        siteBasicFilePath = ""
        siteEquipmentFilePath = ""
        ################################################ Define required columns for fdd and tdd also ###############################################################
        unique_nodes = lte_df["eNodeBName"].dropna().unique()
        lte_df["earfcnul"] = lte_df["earfcnul"].astype("Int64")
        
        lte_df["Latitude"] = lte_df["Latitude"].apply(
            lambda x: str(x).replace(".", "") if "." in str(x) else x
        )

        lte_df["Longitude"] = lte_df["Longitude"].apply(
            lambda x: str(x).replace(".", "") if "." in str(x) else x
        )

        nr_cell_df["Latitude"] = nr_cell_df["Latitude"].apply(
            lambda x: str(x).replace(".", "") if "." in str(x) else x
        )

        nr_cell_df["Longitude"] = nr_cell_df["Longitude"].apply(
            lambda x: str(x).replace(".", "") if "." in str(x) else x
        )

        site_id_name = (
            lte_df["eUtranCellFDDId"].apply(lambda x: x.split("_")[4][:-1]).unique()[0]
        )

        for node_name in unique_nodes:
            current_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            node_dir = create_script_paths(base_path_url, node_name)["lte"]

            node_dir_5g = create_script_paths(base_path_url, node_name)["nr"]
            os.makedirs(node_dir, exist_ok=True)
            os.makedirs(node_dir_5g, exist_ok=True)

            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            directories = create_script_paths(base_path_url, node_name)
            generate_lte_cell_def_scripts(lte_df=lte_df,directories=directories,node_name=node_name,current_time=current_time)

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

                node_dir = create_script_paths(base_path_url, node_name)["lte"]
                os.makedirs(node_dir, exist_ok=True)
                
                Phy_SiteID_Userlabel = site_basic_df['Phy SiteID/Userlabel'].unique()[0]
                
                if node_name in cell_mapped_node:
                    cell_ids = cell_mapped_node[node_name]
                    
                    if any(
                        tech in "".join(cell_ids) for tech in ["_F1_", "_F8_", "_F3_"]
                    ):
                        formatted_text = kk_TN_script_text.format(
                            eNodeBName=row["eNodeBName"], eNBId=row["eNBId"],
                        )
                        script_path = os.path.join(
                            node_dir, f"01_{node_name}_TN_RN_GPS_MME_{current_time}.txt"
                        )
                        with open(script_path, "a") as file:
                            file.write(formatted_text + "\n" + kk_GPS_MMS_script.format(Phy_SiteID_Userlabel = Phy_SiteID_Userlabel))

                    elif any(tech in "".join(cell_ids) for tech in ["_T1_", "_T2_"]):
                        formatted_text = kk_TN_script_text.format(
                            eNodeBName=row["eNodeBName"], eNBId=row["eNBId"],
                        )
                        script_path = os.path.join(
                            node_dir, f"01_{node_name}_TN_RN_GPS_MME_{current_time}.txt"
                        )
                        with open(script_path, "a") as file:
                            file.write(formatted_text + "\n" + kk_GPS_MMS_script.format(Phy_SiteID_Userlabel = Phy_SiteID_Userlabel))

            ######################################################################### GPS/MME Script #######################################################################
            # gps_mme_path = f"01 GPS_MME_script_{node_name}_{current_time}.txt"
            # for node in unique_nodes:
            #    script_path = os.path.join(create_script_paths(base_path_url, node)['lte'], gps_mme_path)
            #    with open(script_path,"a") as file:
            #        file.write(kk_GPS_MMS_script + "\n")
            ########################################################################## GPL/LMS Script ###########################################################################
            gpl_lms_path = f"03_{node_name}_GPL_LMS_script_{current_time}.txt"

            
            for node in unique_nodes:
                script_path = os.path.join(
                    create_script_paths(base_path_url, node)["lte"], gpl_lms_path
                )
                with open(script_path, "a") as file:
                    file.write(kk_GPL_LMS_script + "\n")

            ############################################################################### 5G Cell Scripts ##########################################################################
            # ---------------------------------------------------------------------------------------------------
            if not nr_cell_df.empty:
                for node in nr_cell_df["gNodeBName"].unique():
                    nr_cell_df: pd.DataFrame = nr_cell_df[nr_cell_df["gNodeBName"] == node].copy()
                    
                    nr_cell_df.rename(columns={"bSChannelBwDL/UL": "bSChannelBwDL-UL"}, inplace=True)
                    
                    nr_cell_df_path = os.path.join(create_script_paths(base_path_url, node)["nr"], f"1_{node}_5G Cell creation_Sctp Endpoint Creation_{current_time}.txt")
                    
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
                            rachRootSequence=int(
                                row["rachRootSequence"]
                            ),  ############################################################################ Added rachRootSequence
                            ssbFrequency=row["ssbFrequency"],
                        )

                        gnbcucp_fuction_element += KK_GNBCUCPFUNCTION_ELEMENT.format(gUtranCell=row["gUtranCell"],cellLocalId=row["cellLocalId"])
                        
                    with open(nr_cell_df_path, "a") as file:
                        file.write(
                            NR_CELL_CREATION_AND_SCTP_5G_ENDPOINT_CREATION.format(
                                gNBId=gnbid,
                                GNBDUFUNCTION_SCRIPT_ELEMENT=gnbdu_fuction_element,
                                GNBCUCPFUNCTION_SCRIPT_ELEMENT=gnbcucp_fuction_element,
                            )
                        )

                    NR_GPL_LMS_path = os.path.join(create_script_paths(base_path_url, node)["nr"], f"2_{node}_NR_GPL_LMS_{current_time}.txt")
                    
                    with open(NR_GPL_LMS_path, "a") as file:
                        file.write(NR_GPL_LMS + "\n")

                    Termpoint_GUtranFreqRelation_path = os.path.join(create_script_paths(base_path_url, node_name)["nr"],f"3_{node_name}_Termpoint_GUtranFreqRelation_{current_time}.txt")
                    
                    with open(Termpoint_GUtranFreqRelation_path, "a") as file:
                        file.write(TREMPOINT_GUTRANCELL_FREQ_RELATION + "\n")
                # .......................................................................... NRCELL CONFIGRATION FOR CELL CREATION IN 5G ................................................

            ############################################################### creating the SiteBasic script for 4G and 5G ###############################################################
            unique_nodes = site_basic_df["eNodeBName"].dropna().unique()
            for node in unique_nodes:
                commision_scripts_dir = create_script_paths(base_path_url, node)["commissioning"]
                
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                
                os.makedirs(commision_scripts_dir, exist_ok=True)
                
                sitebasic_df: pd.DataFrame = site_basic_df[site_basic_df["eNodeBName"] == node].copy()
                
                sitebasic_df_path = os.path.join(commision_scripts_dir, f"01_{node}_SiteBasic_{current_time}.xml")
                
                relative_path = os.path.relpath(sitebasic_df_path,os.path.join(base_path_url, f"{node_name}_Integration_Sripts"))
                
                siteBasicFilePath = relative_path.replace("\\", "/")

                siteBasicFilePath = os.path.relpath(sitebasic_df_path, os.path.join(base_path_url, f"{node}_Integration_Sripts")).replace("\\", "/")

                for idx, row in sitebasic_df.iterrows():
                    with open(sitebasic_df_path, "a", encoding="utf-8") as file:
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
            # -----------------------------------------------------------------------------------------------------------------------------------------------#
            radio_templates = {
                "2219": RRU_2219_B0_B1_B3_2X2,
                "2279": RRU_2219_B0_B1_B3_2X2,
                "4412": RRU_4412_4418_4427_4471_4X4,
                "4418": RRU_4412_4418_4427_4471_4X4,
                "4427": RRU_4412_4418_4427_4471_4X4,
                "4471": RRU_4412_4418_4427_4471_4X4,
                "6626": RRU_6626_6X6,
                "8863": RRU_8863_8X8,
                "AIR": AIR_5G_GENERATION_SCRIPT,
            }

            for node in rru_hw_df["eNodeBName"].unique():
                
                commissioning_scripts_dir = create_script_paths(base_path_url, node)["commissioning"]
                
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                
                os.makedirs(commissioning_scripts_dir, exist_ok=True)

                site_specific_rru_df = rru_hw_df[rru_hw_df["eNodeBName"] == node].copy()
                
                rru_hw_path = os.path.join(commissioning_scripts_dir, f"02_{node}_SiteEquipment_{current_time}.xml")

                site_equipment_text = ""
                
                relative_path = os.path.relpath(rru_hw_path, os.path.join(base_path_url, f"{node_name}_Integration_Sripts"))
                
                siteEquipmentFilePath = relative_path.replace("\\", "/")

                siteEquipmentFilePath = os.path.relpath(rru_hw_path, os.path.join(base_path_url, f"{node}_Integration_Sripts")).replace("\\", "/")

                print("site_equipment_path", siteEquipmentFilePath)
                
                site_basic_df_N = site_basic_df[site_basic_df["eNodeBName"] == node].copy()
                
                if site_basic_df_N.empty:
                    print(f"Warning: No basic site data found for {node}")
                    continue

                site_basic_df_N.rename(
                    columns={"Phy SiteID/Userlabel": "Phy_SiteID_Userlabel"},
                    inplace=True,
                )

                site_equipment_script_text = KK_SITE_EQUIPMENT_SCRIPT.format(
                    fieldReplaceableUnitId=site_basic_df_N["fieldReplaceableUnitId"].values[0],
                    Phy_SiteID_Userlabel=site_basic_df_N["Phy_SiteID_Userlabel"].values[0],
                )

                for idx, row in site_specific_rru_df.iterrows():
                    radio_type = row.get("Radio_Type", "")

                    for prefix, template in radio_templates.items():
                        if prefix in radio_type:
                            site_equipment_text += template.format(
                                eNodeBName=row.get("eNodeBName", ""),
                                Radio_UnitId=row.get("Radio_UnitId", ""),
                                fieldReplaceableUnitId=site_basic_df_N["fieldReplaceableUnitId"].values[0],
                                RiPort_BB=row.get("RiPort_BB", ""),
                                RiPort_Radio=row.get("RiPort_Radio", ""),
                                sectorEquipmentFunctionId=row.get("sectorEquipmentFunctionId", ""),
                                riLinkId=row.get("riLinkId", ""),  # optional
                            )

                with open(rru_hw_path, "a", encoding="utf-8") as file:
                    file.write(
                        site_equipment_script_text + "\n" + site_equipment_text
                    )

                site_equipment_script_path = os.path.join(
                    commissioning_scripts_dir, f"RBSSummary_{node}_{current_time}.xml"
                )
                with open(site_equipment_script_path, "a", encoding="utf-8") as file:
                    file.write(
                        RBSSummary_script.format(
                            siteEquipmentFilePath=siteEquipmentFilePath,
                            siteBasicFilePath=siteBasicFilePath,
                        )
                    )

        ###############################################################################################################################################################################################################
        elif circle == "TN":
            # ..................................................... TN 4G Script ....................................................#
            for node_name in lte_df["eNodeBName"].unique():
                
                for _, row in lte_df.iterrows():
                    node_name = row.get("eNodeBName", "UnknownNode")
                    current_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                    node_dir = create_script_paths(base_path_url, node_name)["lte"]
                    node_dir_5g = create_script_paths(base_path_url, node_name)["nr"]
                    sitebasic_df_N: pd.DataFrame = site_basic_df[
                        site_basic_df["eNodeBName"] == node_name
                    ].copy()
                    os.makedirs(node_dir, exist_ok=True)
                    formatted_text = (
                        TN_s1_FOR_TN_IDL_B_PORT.format(eNBId=row["enbId"])
                        if "_B" in str(sitebasic_df_N["tnPortId"])
                        else TN_s1_FOR_TN_IDLTN_C_AND_TN_E_PORT.format(
                            eNBId=row["enbId"]
                        )
                    )
                    #########################################################################
                    script_path = os.path.join(
                        node_dir, f"01_{node_name}_TN_RN_GPS_MME_{current_time}.txt"
                    )
                    with open(script_path, "a") as file:
                        file.write(formatted_text + "\n")


                    TN_GPL_script_path = os.path.join(
                        node_dir, f"03_TN_LTE_GPL_LMS_{node_name}_{current_time}.txt"
                    )
                    formatted_text = TN_s3_LTE_GPL_LMS
                    with open(TN_GPL_script_path, "a", encoding="utf-8") as file:
                        file.write(formatted_text + "\n")

            # -------------------------------------------------------------------------- 5g ______________________________________________
            for node in nr_cell_df["gNodeBName"].unique():
                nr_cell_df: pd.DataFrame = nr_cell_df[nr_cell_df["gNodeBName"] == node]
                nr_cell_df.rename(
                    columns={"bSChannelBwDL/UL": "bSChannelBwDL-UL"}, inplace=True
                )
                commision_scripts_dir = create_script_paths(base_path_url, node)[
                    "commissioning"
                ]
                current_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                nr_cell_df_path = os.path.join(
                    node_dir_5g,
                    f"01_{node_name}_NR_TN_RN_Cell_Def_{current_time}.txt",
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
                        rachRootSequence=row[
                            "rachRootSequence"
                        ],  ############################################################################ Added rachRootSequence ################################################
                    )

                    gnbcucp_fuction_element += TN_GNBCUCPFUNCTION_ELEMENT.format(
                        gUtranCell=row["gUtranCell"],
                        cellLocalId=row["cellLocalId"],
                    )

                with open(nr_cell_df_path, "a") as file:
                    file.write(
                        NR_TN_RN_Cell_Def.format(gNBId=gnbid,TN_GNPDUFUNCTION_ELEMENT=gnbdu_fuction_element,TN_GNBCUCPFUNCTION_ELEMENT=gnbcucp_fuction_element) + "\n")

                TN_04_FreqRelation_path = os.path.join(node_dir_5g,f"03_{node}_Termpoint_GUtranFreqRelation_{current_time}.txt")
                
                with open(TN_04_FreqRelation_path, "a") as file:
                    file.write(TN_Termpoint_GUtranFreqRelation + "\n")
                #
                TN_05_5G_LMS_GPL_ROTN_path = os.path.join(node_dir_5g, f"02_{node}_NR_GPL_LMS_{current_time}.txt")
                
                with open(TN_05_5G_LMS_GPL_ROTN_path, "a", encoding="utf-8") as file:
                    file.write(TN_05_5G_LMS_GPL_ROTN + "\n")
            # -------------------------------------------------------------------------------------------- TN Commissioning Scripts Generation Logic ------------------------------------------------------------------#
            for node in site_basic_df["eNodeBName"].unique():
                
                commision_scripts_dir = create_script_paths(base_path_url, node)["commissioning"]
                
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                
                os.makedirs(commision_scripts_dir, exist_ok=True)
                
                sitebasic_df: pd.DataFrame = site_basic_df[site_basic_df["eNodeBName"] == node].copy()

                sitebasic_df_path = os.path.join(commision_scripts_dir, f"01_{node}_SiteBasic_{current_time}.xml")
                
                siteBasicFilePath = os.path.relpath(sitebasic_df_path,os.path.join(base_path_url, f"{node}_Integration_Sripts")).replace("\\", "/")
                
                relative_path = os.path.relpath(sitebasic_df_path,os.path.join(base_path_url, f"{node}_Integration_Sripts"))
                
                siteBasicFilePath = relative_path.replace("\\", "/")
                
                for idx, row in sitebasic_df.iterrows():
                    bbu_type = row.get("BB_Type", "UnknownType")

                    bbu_script_mapping_ipv4_ipv6 = {
                        "6651": TN_SITEBASIC_SCRIPT_BBU6651,
                        "6630": TN_SITEBASIC_SCRIPT_BBU6630_BBU6631,
                        "6631": TN_SITEBASIC_SCRIPT_BBU6630_BBU6631,
                    }
                    bbu_script_mapping = bbu_script_mapping_ipv4_ipv6

                    for bbu_prefix, template in bbu_script_mapping.items():
                        if bbu_type in bbu_prefix:
                            print("inside bbu type tracker.....")
                            formatted_text = template.format(
                                eNodeBName=row["eNodeBName"],
                                fieldReplaceableUnitId=row["fieldReplaceableUnitId"],
                                tnPortId=row["tnPortId"],
                                OAM_vlan=row["OAM_vlan"],
                                OAM_IP=row["OAM_IP"],
                                OAM_GW=row["OAM_GW"],
                                LTE_S1_vlan=row["LTE_S1_vlan"],
                                LTE_S1_IP=row["LTE_S1_IP"],
                                LTE_S1_GW=row["LTE_S1_GW"],
                                LTE_UP_vlan=row["LTE_UP_vlan"],
                                LTE_UP_IP=row["LTE_UP_IP"],
                                LTE_UP_GW=row["LTE_UP_GW"],
                                NR_ENDC_IP=row["NR_ENDC_IP"],
                            )
                            with open(sitebasic_df_path, "a") as file:
                                file.write(formatted_text + "\n")

                commissioning_scripts_dir = create_script_paths(base_path_url, node)["commissioning"]
                
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                
                os.makedirs(commissioning_scripts_dir, exist_ok=True)
                
                rru_hw_path = os.path.join(commissioning_scripts_dir,f"02_{node}_SiteEquipment_{current_time}.xml")

                site_equipment_text = ""
                
                relative_path = os.path.relpath(rru_hw_path,os.path.join(base_path_url, f"{node_name}_Integration_Sripts"))
                
                siteEquipmentFilePath = relative_path.replace("\\", "/")

                siteEquipmentFilePath = os.path.relpath(rru_hw_path,os.path.join(base_path_url, f"{node}_Integration_Sripts")).replace("\\", "/")

                if sitebasic_df.empty:
                    print(f"Warning: No basic site data found for {node}")
                    continue

                sitebasic_df.rename(columns={"Phy SiteID/Userlabel": "Phy_SiteID_Userlabel"},inplace=True)

                site_equipment_script_text = TN_SITEEQUIPMENT_SCRIPT.format(
                    fieldReplaceableUnitId=site_basic_df_N["fieldReplaceableUnitId"].values[0],
                    Phy_SiteID_Userlabel=site_basic_df_N["Phy_SiteID_Userlabel"].values[0],
                )

                rru_type = {
                    "2219": RRU_2219_B0_B1_B3_2X2,
                    "2279": RRU_2219_B0_B1_B3_2X2,
                    "4412": RRU_4412_4418_4427_4471_4X4,
                    "6626": RRU_6626_6X6,
                    "8863": RRU_8863_8X8,
                    "4418": RRU_4412_4418_4427_4471_4X4,
                    "4427": RRU_4412_4418_4427_4471_4X4,
                    "4471": RRU_4412_4418_4427_4471_4X4,
                }

                for idx, row in site_specific_rru_df.iterrows():
                    for rru, rru_template in rru_type.items():
                        if rru in str(row["Radio_Type"]):
                            site_equipment_text += rru_template.format(
                                eNodeBName=row["eNodeBName"],
                                Radio_UnitId=row["Radio_UnitId"],
                                fieldReplaceableUnitId=site_basic_df_N["fieldReplaceableUnitId"].values[0],
                                RiPort_BB=row["RiPort_BB"],
                                RiPort_Radio=row["RiPort_Radio"],
                                sectorEquipmentFunctionId=row["sectorEquipmentFunctionId"],
                            )
                            break

                with open(rru_hw_path, "a") as file:
                    file.write(site_equipment_script_text + "\n" + site_equipment_text + "\n")

                site_equipment_script_path = os.path.join(commissioning_scripts_dir, f"RBSSummary_{node}_{current_time}.xml")
                
                with open(site_equipment_script_path, "a", encoding="utf-8") as file:
                    file.write(RBSSummary_script.format(siteEquipmentFilePath=siteEquipmentFilePath,siteBasicFilePath=siteBasicFilePath))

        # --------------------------------------------------------------- RJ Circle-specific Script Generation ---------------------------------------------------------------------
        elif circle == "RJ":
            
            unique_nodes = lte_df["eNodeBName"].dropna().unique()
            
            for node_name in unique_nodes:
                
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                
                directories = create_script_paths(base_path_url, node_name)
                
                generate_lte_cell_def_scripts(lte_df=lte_df,directories=directories,node_name=node_name,current_time=current_time)
                
                # ---------------------------------------------------------- RJ Circle-specific Script Generation ---------------------------------------------------------------------
                RJ_Route_4G_GPL_LMS_path = os.path.join(create_script_paths(base_path_url, node_name)["lte"],f"03_{node_name}_Route_GPL_LMS_{current_time}.txt")
                
                with open(RJ_Route_4G_GPL_LMS_path, "a", encoding="utf-8") as file:
                    file.write(RJ_Route_4G_GPL_LMS + "\n")

                temp_lte_df = lte_df[lte_df["eNodeBName"] == node_name].copy()

                enodebname = (temp_lte_df["eNodeBName"].values[0] if not temp_lte_df.empty else "UnknownNode")
                
                enbid = (temp_lte_df["enbId"].values[0] if not temp_lte_df.empty else "UnknownENBId")

                RJ_TN_RN_GPS_MME_path = os.path.join(create_script_paths(base_path_url, node_name)["lte"], f"01_{node_name}_TN_RN_GPS_MME_{current_time}.txt")

                site_basic = site_basic_df[site_basic_df["eNodeBName"] == node_name].copy()
                
                tnPortId = site_basic["tnPortId"].values[0]
                
                mme_type = (NOKIA_MME_SCRIPT if (str(temp_lte_df["MME"].unique()[0]).upper()).startswith("NOKIA") else CISCO_MME_SCRIPT)
                
                Phy_SiteID_Userlabel = site_basic_df['Phy SiteID/Userlabel'].unique()[0]
                with open(RJ_TN_RN_GPS_MME_path, "a", encoding="utf-8") as file:
                    file.write(RJ_TN_RN_GPS_MME.format(eNodeBName=enodebname, tnPortId=tnPortId, eNBId=enbid, Phy_SiteID_Userlabel=Phy_SiteID_Userlabel) + mme_type + "\n")

            # --------------------------------------------------------------------------------------- 5G Cell Scripts ----------------------------------------------------------------#
            # Implemented RJ Circle-specific 5G Script Generation Logic
            if not nr_cell_df.empty:
                
                for node in nr_cell_df["gNodeBName"].unique():
                    
                    nr_cell_df: pd.DataFrame = nr_cell_df[nr_cell_df["gNodeBName"] == node].copy()
                    
                    nr_cell_df.rename(columns={"bSChannelBwDL/UL": "bSChannelBwDL-UL"}, inplace=True)
                    
                    site_basic_data_df = site_basic_df[site_basic_df["eNodeBName"] == node].copy()
                    
                    NR_IP = site_basic_data_df['NR_IP'].unique()[0]
                    
                    NR_ENDC_IP = site_basic_data_df['NR_ENDC_IP'].unique()[0]
                    
                    NR_GW = site_basic_data_df['NR_GW'].unique()[0]
                    
                    tnPortId = site_basic_data_df['tnPortId'].unique()[0]
                    
                    nr_cell_df_path = os.path.join(create_script_paths(base_path_url, node)["nr"],f"1_{node}_5G Cell creation_Sctp Endpoint Creation_{current_time}.txt")
                    
                    gnbid = nr_cell_df["gNBId"].unique()[0]

                    gnbdu_fuction_element = ""
                    
                    gnbcucp_fuction_element = ""
                    
                    gnb_cgswitch_element = ""
                    for idx, row in nr_cell_df.iterrows():
                        gnbdu_fuction_element += RJ_GNBDUFunction_text.format(
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
                            rachRootSequence=int(
                                row["rachRootSequence"]
                            )
                            ############################################################################ Added rachRootSequence
                        )
                        
                        gnb_cgswitch_element += RJ_5g_CgSwitch_text.format(gUtranCell = row['gUtranCell'])
                        

                        gnbcucp_fuction_element += RJ_GNBCUCPFunction_text.format(
                            gUtranCell=row["gUtranCell"],
                            cellLocalId = row['cellLocalId']
                        )
                    with open(nr_cell_df_path, "a") as file:
                        file.write(
                            RJ_5G_Cell_creation_Sctp_Endpoint_Creation.format(
                                gUtranCell=row["gUtranCell"],
                                NR_IP = NR_IP,
                                NR_ENDC_IP = NR_ENDC_IP,
                                NR_GW = NR_GW,
                                gNodeBName = node,
                                gNBId = gnbid,
                                RJ_5g_CgSwitch_text = gnb_cgswitch_element,
                                RJ_GNBDUFunction_text=gnbdu_fuction_element,
                                RJ_GNBCUCPFunction_text=gnbcucp_fuction_element,
                            )
                        )

                    NR_GPL_LMS_path = os.path.join(create_script_paths(base_path_url, node)["nr"],f"2_{node}_NR_GPL_LMS_{current_time}.txt")
                    
                    with open(NR_GPL_LMS_path, "a") as file:
                        file.write(RJ_Route_5G_GPL_LMS + "\n")

                    Termpoint_GUtranFreqRelation_path = os.path.join(create_script_paths(base_path_url, node_name)["nr"],f"3_{node_name}_Termpoint_GUtranFreqRelation_{current_time}.txt")
                    
                    with open(Termpoint_GUtranFreqRelation_path, "a") as file:
                        file.write(RJ_Termpoint_GUtranFreqRelation + "\n")
            # ________________________________________________________________________________________________________________________________________________________________________#

            ########################################## RJ Commissioning Scripts Generation Logic ###############################################################
            #
            for node in site_basic_df["eNodeBName"].unique():
                
                commision_scripts_dir = create_script_paths(base_path_url, node)["commissioning"]
                
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                
                os.makedirs(commision_scripts_dir, exist_ok=True)
                
                sitebasic_df: pd.DataFrame = site_basic_df[site_basic_df["eNodeBName"] == node].copy()
                
                print(f"node_name:- {node}\n",sitebasic_df)
                sitebasic_df_path = os.path.join(commision_scripts_dir, f"01_{node}_SiteBasic_{current_time}.xml")
                
                relative_path = os.path.relpath(sitebasic_df_path, os.path.join(base_path_url, f"{node_name}_Integration_Sripts"))
                
                siteBasicFilePath = relative_path.replace("\\", "/")

                siteBasicFilePath = os.path.relpath(sitebasic_df_path,os.path.join(base_path_url, f"{node}_Integration_Sripts"),).replace("\\", "/")

                def ip_type(ip_address):
                    try:
                        socket.inet_pton(socket.AF_INET, ip_address)
                        return "IPv4"
                    except socket.error:
                        try:
                            socket.inet_pton(socket.AF_INET6, ip_address)
                            return "IPv6"
                        except socket.error:
                            return "Unknown"

                # sitebasic_df.replace('NA', '',inplace=True)
                for idx, row in sitebasic_df.iterrows():
                    bbu_type = row.get("BB_Type", "UnknownType")
                    oam_ip, subnet = (row.get("OAM_IP", "UnknownOAMID").split("/")[0],row.get("OAM_IP", "UnknownOAMID").split("/")[1])
                    abis_ip = row.get("ABIS_IP", "NA")
                    print(abis_ip)
                    ip_type = ip_type(oam_ip)

                    ############################################################ if ip_type in ["IPv4", "IPv6"]:git #####################################################################
                    bbu_script_mapping_ipv4 = {
                        "BB6651": SiteBasic_ipv4_6651,
                        "BB6631": SiteBasic_ipv4_6631,
                        "BB6630": SiteBasic_ipv4_6630,
                        "BB6353": SiteBasic_ipv4_6353,
                        "BB6339": SiteBasic_ipv4_6339,
                        "BB6303": SiteBasic_ipv4_6303,
                    }

                    bbu_script_mapping_ipv6 = {
                        "BB6651": SiteBasic_ipv6_6651,
                        "BB6631": SiteBasic_ipv6_6631,
                        "BB6630": SiteBasic_ipv6_6630,
                        "BB6339": SiteBasic_ipv6_6339,
                        "BB6303": SiteBasic_ipv6_6303,
                    }
                    bbu_script_mapping = (bbu_script_mapping_ipv4 if ip_type == "IPv4" else bbu_script_mapping_ipv6)

                    for bbu_prefix, template in bbu_script_mapping.items():
                        if bbu_type in bbu_prefix:
                            formatted_text = template.format(
                                eNodeBName=row["eNodeBName"],
                                fieldReplaceableUnitId=row["fieldReplaceableUnitId"],
                                tnPortId=row["tnPortId"],
                                OAM_vlan=row["OAM_vlan"],
                                OAM_IP=row["OAM_IP"],
                                OAM_GW=row["OAM_GW"],
                                LTE_S1_vlan=row["LTE_S1_vlan"],
                                LTE_S1_IP=row["LTE_S1_IP"],
                                LTE_S1_GW=row["LTE_S1_GW"],
                                LTE_UP_vlan=row["LTE_UP_vlan"],
                                LTE_UP_IP=row["LTE_UP_IP"],
                                LTE_UP_GW=row["LTE_UP_GW"],
                            )
                            if not (pd.isna(abis_ip) or abis_ip in ['NA', 'nan']):
                                print(f"abis generated for {node}")
                                abis_site_basic_text = ABIS_Site_Basic_script.format(
                                    tnPortId=row["tnPortId"],
                                    ABIS_vlan = int(row['ABIS_vlan']),
                                    ABIS_IP = row['ABIS_IP'],
                                    ABIS_GW = row['ABIS_GW']
                                )
                                formatted_text += '\n' + abis_site_basic_text
                                
                            with open(sitebasic_df_path, "a", encoding="utf-8") as file:
                                file.write(formatted_text + "\n")


                commissioning_scripts_dir = create_script_paths(base_path_url, node)["commissioning"]
                
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                
                os.makedirs(commissioning_scripts_dir, exist_ok=True)

                site_specific_rru_df = rru_hw_df[rru_hw_df["eNodeBName"] == node]
                
                rru_hw_path = os.path.join(commissioning_scripts_dir, f"02_{node}_SiteEquipment_{current_time}.xml",)

                site_equipment_text = ""
                
                relative_path = os.path.relpath(rru_hw_path, os.path.join(base_path_url, f"{node_name}_Integration_Sripts"))
                
                siteEquipmentFilePath = relative_path.replace("\\", "/")

                siteEquipmentFilePath = os.path.relpath(rru_hw_path,os.path.join(base_path_url, f"{node}_Integration_Sripts")).replace("\\", "/")

                print("site_equipment_path", siteEquipmentFilePath)
                
                if sitebasic_df.empty:
                    print(f"Warning: No basic site data found for {node}")
                    continue

                sitebasic_df.rename(
                    columns={"Phy SiteID/Userlabel": "Phy_SiteID_Userlabel"},
                    inplace=True,
                )

                bbu_mapped_script = {
                    "6630": SiteEquipment_6630,
                    "6631": SiteEquipment_6631,
                    "6651": SiteEquipment_6651,
                    "6303": SiteEquipment_6303,
                    "6353": SiteEquipment_6353,
                    "6339": SiteEquipment_6339,
                    "5216": SiteEquipment_5216,
                    "6648": SiteEquipment_6648,
                    "R503": SiteEquipment_R503,
                    
                }
                site_equipment_script_text = ""
                for _, row in sitebasic_df.iterrows():
                    for bbu_prefix, template in bbu_mapped_script.items():
                        if bbu_prefix in str(row["BB_Type"]):
                            site_equipment_script_text += template.format(
                                fieldReplaceableUnitId=row["fieldReplaceableUnitId"],
                                Phy_SiteID_Userlabel=row["Phy_SiteID_Userlabel"],
                            )
                            break
                        
                        
                rru_type = {
                    "2219": RRU_2219_B0_B1_B3_2X2,
                    "2279": RRU_2219_B0_B1_B3_2X2,
                    "4412": RRU_4412_4418_4427_4471_4X4,
                    "6626": RRU_6626_6X6,
                    "8863": RRU_8863_8X8,
                    "4418": RRU_4412_4418_4427_4471_4X4,
                    "4427": RRU_4412_4418_4427_4471_4X4,
                    "4471": RRU_4412_4418_4427_4471_4X4,
                    "AIR" : AIR_5G_GENERATION_SCRIPT,
                }
                print(site_specific_rru_df)

                for idx, row in site_specific_rru_df.iterrows():
                    print(row['Radio_Type'])
                    for rru, rru_template in rru_type.items():
                        if rru in str(row["Radio_Type"]):
                            print(rru)
                            site_equipment_text += rru_template.format(
                                eNodeBName=row["eNodeBName"],
                                Radio_UnitId=row["Radio_UnitId"],
                                fieldReplaceableUnitId=sitebasic_df["fieldReplaceableUnitId"].values[0],
                                RiPort_BB=row["RiPort_BB"],
                                RiPort_Radio=row["RiPort_Radio"],
                                sectorEquipmentFunctionId=row["sectorEquipmentFunctionId"],
                                riLinkId=row.get("riLinkId", ""),
                            )
                            break

                with open(rru_hw_path, "a", encoding="utf-8") as file:
                    file.write(
                        site_equipment_script_text + "\n" + site_equipment_text + "\n"
                    )

                site_equipment_script_path = os.path.join(
                    commissioning_scripts_dir, f"RBSSummary_{node}_{current_time}.xml"
                )
                with open(site_equipment_script_path, "a", encoding="utf-8") as file:
                    file.write(
                        RBSSummary_script.format(
                            siteEquipmentFilePath=siteEquipmentFilePath,
                            siteBasicFilePath=siteBasicFilePath,
                        )
                    )

        # ---------------------------------------------------------------- AS(Asaam) Circle-specific Script Generation ---------------------------------------------------------------------
        elif circle == "AS":
            current_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            for idx, row in site_basic_df.iterrows():
                print(site_basic_df)
                node_name = row.get("eNodeBName", "UnknownNode")

                node_dir = create_script_paths(base_path_url, node_name)["lte"]
                os.makedirs(node_dir, exist_ok=True)

                if node_name in cell_mapped_node:
                    cell_ids = cell_mapped_node[node_name]

                    if any(
                        tech in "".join(cell_ids) for tech in ["_F1_", "_F8_", "_F3_"]
                    ):
                        formatted_text = AS_TN_RN_GPS_MME_SCRIPT.format(
                            LTE_UP_GW=row["LTE_UP_GW"],
                            eNBId=row["eNBId"],
                            tnPortId=row["tnPortId"],
                            Phy_SiteID_Userlabel=row["Phy SiteID/Userlabel"],
                        )
                        script_path = os.path.join(
                            node_dir, f"01_{node_name}_TN_RN_GPS_MME_{current_time}.txt"
                        )
                        with open(script_path, "a") as file:
                            file.write(formatted_text + "\n")

                    elif any(tech in "".join(cell_ids) for tech in ["_T1_", "_T2_"]):
                        formatted_text = AS_TN_RN_GPS_MME_SCRIPT.format(
                            LTE_UP_GW=row["LTE_UP_GW"],
                            eNBId=row["eNBId"],
                            tnPortId=row["tnPortId"],
                            Phy_SiteID_Userlabel=row["Phy SiteID/Userlabel"],
                        )
                        script_path = os.path.join(
                            node_dir, f"01_{node_name}_TN_RN_GPS_MME_{current_time}.txt"
                        )
                        with open(script_path, "a") as file:
                            file.write(formatted_text + "\n")

            ######################################################################### GPS/MME Script #######################################################################
            # gps_mme_path = f"01 GPS_MME_script_{node_name}_{current_time}.txt"
            # for node in unique_nodes:
            #    script_path = os.path.join(create_script_paths(base_path_url, node)['lte'], gps_mme_path)
            #    with open(script_path,"a") as file:
            #        file.write(kk_GPS_MMS_script + "\n")
            ########################################################################## GPL/LMS Script ###########################################################################
            
            gpl_lms_path = f"03 GPL_LMS_script_{node_name}_{current_time}.txt"
            #### physical siteID is unique for all node in any circle ######################################################
            Phy_SiteID_Userlabel = site_basic_df['Phy SiteID/Userlabel'].unique()[0]
            for node in unique_nodes:
                script_path = os.path.join(create_script_paths(base_path_url, node)["lte"], gpl_lms_path)
                with open(script_path, "a") as file:
                    file.write(AS_GPL_LMS_DST_SCRIPT + "\n")

            ############################################################################### 5G Cell Scripts ##########################################################################
            # ---------------------------------------------------------------------------------------------------
            print(nr_cell_df)
            if not nr_cell_df.empty:
                for node in nr_cell_df["gNodeBName"].unique():
                    nr_cell_df: pd.DataFrame = nr_cell_df[
                        nr_cell_df["gNodeBName"] == node
                    ]
                    nr_cell_df.rename(
                        columns={"bSChannelBwDL/UL": "bSChannelBwDL-UL"}, inplace=True
                    )
                    site_basic_data_df = site_basic_df[site_basic_df["eNodeBName"] == node].copy()
                    NR_IP = site_basic_data_df['NR_IP'].unique()[0]
                    NR_ENDC_IP = site_basic_data_df['NR_ENDC_IP'].unique()[0]
                    NR_GW = site_basic_data_df['NR_GW'].unique()[0]
                    tnPortId = site_basic_data_df['tnPortId'].unique()[0]
                    nr_cell_df_path = os.path.join(
                        create_script_paths(base_path_url, node)["nr"],
                        f"1_{node}_5G Cell creation_Sctp Endpoint Creation_{current_time}.txt",
                    )
                    gnbid = nr_cell_df["gNBId"].unique()[0]
                    print(nr_cell_df)

                    gnbdu_fuction_element = ""
                    gnbcucp_fuction_element = ""
                    gnb_cgswitch_element = ""
                    for idx, row in nr_cell_df.iterrows():
                        gnbdu_fuction_element += AS_GNBDUFunction.format(
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
                            rachRootSequence=int(
                                row["rachRootSequence"]
                            )
                            ############################################################################ Added rachRootSequence
                        )
                        
                        gnb_cgswitch_element += AS_CGSWITCH_SCRIPT.format(
                            gUtranCell = row['gUtranCell'],
                        )
                        

                        gnbcucp_fuction_element += AS_GNBCUCPFunction.format(
                            gUtranCell=row["gUtranCell"],
                            cellLocalId = row['cellLocalId']
                        )
                    with open(nr_cell_df_path, "a") as file:
                        file.write(
                            AS_5G_Cell_creation_Sctp_Endpoint_Creation.format(
                                gUtranCell=row["gUtranCell"],
                                NR_IP = NR_IP,
                                NR_ENDC_IP = NR_ENDC_IP,
                                NR_GW = NR_GW,
                                tnPortId = tnPortId,
                                gNBId = gnbid,
                                AS_CGSWITCH_SCRIPT = gnb_cgswitch_element,
                                AS_GNBDUFunction=gnbdu_fuction_element,
                                AS_GNBCUCPFunction=gnbcucp_fuction_element,
                            )
                        )

                    NR_GPL_LMS_path = os.path.join(
                        create_script_paths(base_path_url, node)["nr"],
                        f"2_{node}_NR_GPL_LMS_{current_time}.txt",
                    )
                    with open(NR_GPL_LMS_path, "a") as file:
                        file.write(AS_NR_GPL_LMS_SCRIPT + "\n")

                    Termpoint_GUtranFreqRelation_path = os.path.join(
                        create_script_paths(base_path_url, node_name)["nr"],
                        f"3_{node_name}_Termpoint_GUtranFreqRelation_{current_time}.txt",
                    )
                    with open(Termpoint_GUtranFreqRelation_path, "a") as file:
                        file.write(AS_Termpoint_GUtranFreqRelation_script + "\n")
            # .......................................................................... NRCELL CONFIGRATION FOR CELL CREATION IN 5G ................................................
            ########################################## AS Commissioning Scripts Generation Logic ###############################################################
            for node in site_basic_df["eNodeBName"].unique():
                
                commision_scripts_dir = create_script_paths(base_path_url, node)["commissioning"]
                
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                
                os.makedirs(commision_scripts_dir, exist_ok=True)
                
                sitebasic_df: pd.DataFrame = site_basic_df[site_basic_df["eNodeBName"] == node].copy()
                
                sitebasic_df_path = os.path.join(commision_scripts_dir, f"01_{node}_SiteBasic_{current_time}.xml")

                relative_path = os.path.relpath(sitebasic_df_path, os.path.join(base_path_url, f"{node_name}_Integration_Sripts"))
                
                siteBasicFilePath = relative_path.replace("\\", "/")

                siteBasicFilePath = os.path.relpath(sitebasic_df_path,os.path.join(base_path_url, f"{node}_Integration_Sripts")).replace("\\", "/")

                def ip_type(ip_address):
                    try:
                        socket.inet_pton(socket.AF_INET, ip_address)
                        return "IPv4"
                    except socket.error:
                        try:
                            socket.inet_pton(socket.AF_INET6, ip_address)
                            return "IPv6"
                        except socket.error:
                            return "Unknown"

                for idx, row in sitebasic_df.iterrows():
                    bbu_type = row.get("BB_Type", "UnknownType")
                    
                    oam_ip, subnet = row.get("OAM_IP", "UnknownOAMID").split("/")[0],row.get("OAM_IP", "UnknownOAMID").split("/")[1]
                    
                    abis_ip = row.get('ABIS_IP', 'NA')
                    
                    ip_type = ip_type(oam_ip)

                    ############################################################ if ip_type in ["IPv4", "IPv6"]:git #####################################################################
                    bbu_script_mapping_ipv4 = {
                        "6651": AS_SiteBasic_6651_IPV4,
                        "6631": AS_SiteBasic_6631_IPV4,
                        "6630": AS_SiteBasic_6630_IPV4,
                        "5216": AS_SiteBasic_5216_IPV4,
                    }

                    bbu_script_mapping_ipv6 = {
                        "6651": AS_SiteBasic_6651_IPV6,
                        "6631": AS_SiteBasic_6631_IPV6,
                        "6630": AS_SiteBasic_6630_IPV6,
                        "5216": AS_SiteBasic_5216_IPV6,
                    }
                    bbu_script_mapping = (bbu_script_mapping_ipv4 if ip_type == "IPv4" else bbu_script_mapping_ipv6)

                    for bbu_prefix, template in bbu_script_mapping.items():
                        if bbu_prefix in bbu_type:
                            formatted_text = template.format(
                                eNodeBName=row["eNodeBName"],
                                fieldReplaceableUnitId=row["fieldReplaceableUnitId"],
                                tnPortId=row["tnPortId"],
                                OAM_vlan=row["OAM_vlan"],
                                OAM_IP=row["OAM_IP"],
                                OAM_GW=row["OAM_GW"],
                                LTE_S1_vlan=row["LTE_S1_vlan"],
                                LTE_S1_IP=row["LTE_S1_IP"],
                                LTE_S1_GW=row["LTE_S1_GW"],
                                LTE_UP_vlan=row["LTE_UP_vlan"],
                                LTE_UP_IP=row["LTE_UP_IP"],
                                LTE_UP_GW=row["LTE_UP_GW"],
                            )

                            if not (pd.isna(abis_ip) or abis_ip in ['NA', 'nan']):
                                abis_site_basic_text = ABIS_Site_Basic_script.format(
                                    tnPortId=row["tnPortId"],
                                    ABIS_vlan = int(row['ABIS_vlan']),
                                    ABIS_IP = row['ABIS_IP'],
                                    ABIS_GW = row['ABIS_GW']
                                )
                                formatted_text += '\n' + abis_site_basic_text
                            
                            with open(sitebasic_df_path, "a", encoding="utf-8") as file:
                                file.write(formatted_text + "\n")

                commissioning_scripts_dir = create_script_paths(base_path_url, node)["commissioning"]
                
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                
                os.makedirs(commissioning_scripts_dir, exist_ok=True)

                site_specific_rru_df = rru_hw_df[rru_hw_df["eNodeBName"] == node]
                
                rru_hw_path = os.path.join(commissioning_scripts_dir, f"02_{node}_SiteEquipment_{current_time}.xml")

                site_equipment_text = ""
                
                relative_path = os.path.relpath(rru_hw_path, os.path.join(base_path_url, f"{node_name}_Integration_Sripts"))
                
                siteEquipmentFilePath = relative_path.replace("\\", "/")

                siteEquipmentFilePath = os.path.relpath(rru_hw_path, os.path.join(base_path_url, f"{node}_Integration_Sripts")).replace("\\", "/")

                print("site_equipment_path", siteEquipmentFilePath)
                
                if sitebasic_df.empty:
                    print(f"Warning: No basic site data found for {node}")
                    continue

                sitebasic_df.rename(columns={"Phy SiteID/Userlabel": "Phy_SiteID_Userlabel"},inplace=True)

                bbu_mapped_script = {
                    "6630": SiteEquipment_6630,
                    "6631": SiteEquipment_6631,
                    "6651": SiteEquipment_6651,
                    "6303": SiteEquipment_6303,
                    "6353": SiteEquipment_6353,
                    "6339": SiteEquipment_6339,
                    "5216": SiteEquipment_5216,
                    "6648": SiteEquipment_6648,
                    "R503": SiteEquipment_R503,
                }

                rru_type = {
                    "2219": RRU_2219_B0_B1_B3_2X2,
                    "2279": RRU_2219_B0_B1_B3_2X2,
                    "4412": RRU_4412_4418_4427_4471_4X4,
                    "6626": RRU_6626_6X6,
                    "8863": RRU_8863_8X8,
                    "4418": RRU_4412_4418_4427_4471_4X4,
                    "4427": RRU_4412_4418_4427_4471_4X4,
                    "4471": RRU_4412_4418_4427_4471_4X4,
                    "AIR": AIR_5G_GENERATION_SCRIPT,
                }

        
                site_equipment_script_text = ""
                for _, row in sitebasic_df.iterrows():
                    for bbu_prefix, template in bbu_mapped_script.items():
                        if bbu_prefix in str(row["BB_Type"]):
                            site_equipment_script_text += template.format(
                                fieldReplaceableUnitId=row["fieldReplaceableUnitId"],
                                Phy_SiteID_Userlabel=row["Phy_SiteID_Userlabel"],
                            )
                            break

                for idx, row in site_specific_rru_df.iterrows():
                    for rru, rru_template in rru_type.items():
                        if rru in str(row["Radio_Type"]):
                            site_equipment_text += rru_template.format(
                                eNodeBName=row["eNodeBName"],
                                Radio_UnitId=row["Radio_UnitId"],
                                fieldReplaceableUnitId=sitebasic_df["fieldReplaceableUnitId"].values[0],
                                RiPort_BB=row["RiPort_BB"],
                                RiPort_Radio=row["RiPort_Radio"],
                                sectorEquipmentFunctionId=row["sectorEquipmentFunctionId"],
                                riLinkId=row.get("riLinkId", "")
                            )
                            break

                with open(rru_hw_path, "a", encoding="utf-8") as file:
                    file.write(site_equipment_script_text + "\n" + site_equipment_text + "\n")

                site_equipment_script_path = os.path.join(commissioning_scripts_dir, f"RBSSummary_{node}_{current_time}.xml")
                
                with open(site_equipment_script_path, "a", encoding="utf-8") as file:
                    file.write(RBSSummary_script.format(siteEquipmentFilePath=siteEquipmentFilePath,siteBasicFilePath=siteBasicFilePath))

        #####################################################################################################################################################
        # Add CIRCLES specific script generation logic here if needed
        ########################################################## MAKING THE ZIP FILE #############################################################
        folder_path = os.path.join(MEDIA_ROOT, "LTE_INTEGRATION_CONFIG_FILES")

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        zip_filename = f"{site_id_name}_LTE_Integration_Scripts_{timestamp}.zip"
        zip_output_path = os.path.join(MEDIA_ROOT, zip_filename)

        ################################################ Clean up old zips (optional) ######################################################################
        #        for file in os.listdir(MEDIA_ROOT):
        #            if file.endswith(".zip"):
        #               os.remove(os.path.join(MEDIA_ROOT, file))

        ##################################################################### Create ZIP archive #############################################################
        zip_folder(folder_path, zip_output_path)

        ##################################################### Create download link relative to MEDIA_URL ####################################################
        download_link = os.path.join(MEDIA_URL, zip_filename).replace("\\", "/")

        ############################################################################################################################################
        return Response(
            {
                "status": True,
                "message": "Integration scripts generated successfully.",
                "download_link": download_link,
            },
            status=status.HTTP_200_OK,

        )
      

