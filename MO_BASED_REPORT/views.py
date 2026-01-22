from django.shortcuts import render
from rest_framework.decorators import api_view
from mcom_website.settings import MEDIA_ROOT
from rest_framework.response import Response

from django.core.files.storage import FileSystemStorage
import pandas as pd
import os
from MO_BASED_REPORT.models import *
import datetime
from django.db.models import Sum, Value, IntegerField, Func, F
from django.db.models.functions import Cast
import pandas as pd
from django.db import connection

# Create your views here.
import json
from django.db.models.functions import NullIf

# from .serialzers import *
from MO_BASED_REPORT.serializers import *


@api_view(["POST"])
def Mo_Based_Report_Upload(request):
    try:
        file = request.FILES.get("file")

        if file:
            location = MEDIA_ROOT + r"\MO_TABLE\temporary_files"
            fs = FileSystemStorage(location=location)
            file = fs.save(file.name, file)
            file_path = fs.path(file)

            df = pd.read_excel(file_path, sheet_name="Consolidate MO based signoff ")
            df.columns = df.columns.str.upper().str.strip()
            df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

            objs = []
            for i, d in df.iterrows():
                SREQ_RMO_Date = (
                    None if pd.isnull(d["SREQ/RMO DATE"]) else d["SREQ/RMO DATE"]
                )
                obj = Consolidate_MO_based_Table(
                    Month=str(d["MONTH"]),
                    Circle=str(d["CIRCLE"]),
                    Site_ID=str(d["SITE ID"]),
                    Locator_ID=str(d["LOCATOR ID"]),
                    Project_Name=str(d["PROJECT NAME"]),
                    Module_Name=str(d["MODULE NAME"]),
                    Module_Qty_dispatched_as_per_TO=(
                        d["MODULE QTY DISPATCHED AS PER TO"]
                    ),
                    Module_Qty_received_at_site_as_per_TO=(
                        d["MODULE QTY RECEIVED AT SITE AS PER TO"]
                    ),
                    Gap_Qty_dispatch_vs_received=str(d["GAP QTY DISPATCH VS RECEIVED"]),
                    Site_On_air_date_in_CATS=str(d["SITE ON AIR DATE IN CATS"]),
                    Site_On_air_date_in_DPR=str(d["SITE ON AIR DATE IN DPR"]),
                    Site_On_air_Date_in_CBS=str(d["SITE ON AIR DATE IN CBS"]),
                    Site_visible_in_mobinet_on_of_CATS_on_air_date=str(
                        d["SITE VISIBLE IN MOBINET ON D+7 OF CATS ON AIR DATE"]
                    ),
                    Module_Qty_visible=(d["MODULE QTY VISIBLE"]),
                    Gap_CATS_vs_Mobinet=(d["GAP CATS VS MOBINET"]),
                    RCA_of_Gap=str(d["RCA OF GAP"]),
                    SREQ_RMO_NO=str(d["SREQ/RMO NO"]),
                    SREQ_RMO_Date=SREQ_RMO_Date,
                    WH_inward_status=str(d["WH INWARD STATUS"]),
                    Pivot_summary=str(d["PIVOT SUMMARY"]),
                    CATS_on_air_dump_taken_and_kept_as_repositry_for_the_month=str(
                        d[
                            "CATS ON AIR DUMP TAKEN AND KEPT AS REPOSITRY FOR THE MONTH (26-25 OF MONTH)"
                        ]
                    ),
                    Mobinet_on_air_dump_taken_and_kept_as_repositry_for_the_month=str(
                        d[
                            "MOBINET ON AIR DUMP TAKEN AND KEPT AS REPOSITRY FOR THE MONTH (26-25 OF MONTH)"
                        ]
                    ),
                    Signoff_Airtel_Deployment_Head=str(
                        d["SIGNOFF AIRTEL DEPLOYMENT HEAD"]
                    ),
                    Signoff_OEM_circle_Head=str(d["SIGNOFF OEM CIRCLE HEAD"]),
                    Additional_Remarks=str(d["ADDITIONAL REMARKS"]),
                    Module_type=str(d["MODULE TYPE"]),
                    MO_No=str(d["MO NO"]),
                    Status=str(d["STATUS"]),
                    Signoff_Month=str(d["SIGNOFF MONTH"]),
                    Module_Available_in_OSS=str(d["MODULE AVAILABLE IN OSS"]),
                    SREQ=(d["SREQ"]),
                    RMO=(d["RMO"]),
                    SREQ_RMO=(d["SREQ/RMO"]),
                    SREQ_RMO_WIP=(d["SREQ/RMO WIP"]),
                    Theft=(d["THEFT"]),
                    MOS=(d["MOS"]),
                    Activity_done_by_MSP=(d["ACTIVITY DONE BY MSP"]),
                    Virtual_MO_Regularisation=(d["VIRTUAL MO/REGULARISATION"]),
                    MO_Cancelled=(d["MO CANCELLED"]),
                    Under_check=(d["UNDER CHECK"]),
                )
                objs.append(obj)

            Consolidate_MO_based_Table.objects.bulk_create(objs)

            df = pd.read_excel(file_path, sheet_name="TO vs Shipment Dump")
            df.columns = df.columns.str.strip()
            df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

            objs = []
            for i, d in df.iterrows():
                obj = MO_TO_VS_Shipment_Dump(
                    MONTH=str(d["MONTH"]),
                    COMPLIANCE_RESPONSIBILITY=str(d["COMPLIANCE_RESPONSIBILITY"]),
                    ORCL_OPERATING_UNIT_ID=str(d["ORCL_OPERATING_UNIT_ID"]),
                    ORCL_INV_ORG_ID=str(d["ORCL_INV_ORG_ID"]),
                    REQNUMBER=str(d["REQNUMBER"]),
                    ORCL_FROMLOCATION=str(d["ORCL_FROMLOCATION"]),
                    ORCL_FROMLOCATION_TYPE=str(d["ORCL_FROMLOCATION_TYPE"]),
                    ORCL_TOLOCATION=str(d["ORCL_TOLOCATION"]),
                    ORCL_TOLOCATION_TYPE=str(d["ORCL_TOLOCATION_TYPE"]),
                    REASONFORTRANSFER=str(d["REASONFORTRANSFER"]),
                    MO_OR_SO_NUMBER=str(d["MO_OR_SO_NUMBER"]),
                    MOSO_CREATOR_OLM_ID=str(d["MOSO_CREATOR_OLM_ID"]),
                    MOSO_CREATOR_NAME=str(d["MOSO_CREATOR_NAME"]),
                    MOSO_CREATOR_DEPARTMENT=str(d["MOSO_CREATOR_DEPARTMENT"]),
                    MO_CREATION_DATE=pd.to_datetime(
                        d["MO_CREATION_DATE"], format="%Y-%m-%d %H:%M"
                    ),
                    DC_NUMBER=str(d["DC_NUMBER"]),
                    ORCL_DC_CREATION_DATE=str(d["ORCL_DC_CREATION_DATE"]),
                    ITEMCODE=str(d["ITEMCODE"]),
                    ITEMDESCRIPTION=str(d["ITEMDESCRIPTION"]),
                    ORCL_SOURCE_SUBINVENTORY=str(d["ORCL_SOURCE_SUBINVENTORY"]),
                    SOURCE_LOCATOR=str(d["SOURCE_LOCATOR"]),
                    ORCL_DESTINATION_SUBINVENTORY=str(
                        d["ORCL_DESTINATION_SUBINVENTORY"]
                    ),
                    DESTINATION_LOCATOR=str(d["DESTINATION_LOCATOR"]),
                    ORCL_QTYNEEDED=str(d["ORCL_QTYNEEDED"]),
                    TRANSFERNUMBER=str(d["TRANSFERNUMBER"]),
                    TRANSFERSTATUS=str(d["TRANSFERSTATUS"]),
                    NEEDBYDATE=str(d["NEEDBYDATE"]),
                    LINENUMBER=str(d["LINENUMBER"]),
                    TRANSFERLINESTATUS=str(d["TRANSFERLINESTATUS"]),
                    UNITOFMEASURE=str(d["UNITOFMEASURE"]),
                    QTYORDERED=str(d["QTYORDERED"]),
                    QTYAPPROVED=str(d["QTYAPPROVED"]),
                    QTYAPPROVED_VALUE=str(d["QTYAPPROVED_VALUE"]),
                    QTYALLOCATED=str(d["QTYALLOCATED"]),
                    MO_PICKED=str(d["MO_PICKED"]),
                    QTYPICKED=str(d["QTYPICKED"]),
                    QTYPICKED_PERCENTAGE=str(d["QTYPICKED_PERCENTAGE"]),
                    QTYPICKED_VALUE=str(d["QTYPICKED_VALUE"]),
                    QTYPICKED_VALUE_PERCENTAGE=str(d["QTYPICKED_VALUE_PERCENTAGE"]),
                    QTYSHIPPED=str(d["QTYSHIPPED"]),
                    SHIPPED_DATE=str(d["SHIPPED_DATE"]),
                    QTYSHIPPED_PERCENTAGE=str(d["QTYSHIPPED_PERCENTAGE"]),
                    QTYSHIPPED_VALUE=str(d["QTYSHIPPED_VALUE"]),
                    QTYSHIPPED_VALUE_PERCENTAGE=str(d["QTYSHIPPED_VALUE_PERCENTAGE"]),
                    QTYRECEIVED=str(d["QTYRECEIVED"]),
                    RECEIVED_DATE=str(d["RECEIVED_DATE"]),
                    QTYRECEIVED_PERCENTAGE=str(d["QTYRECEIVED_PERCENTAGE"]),
                    QTYRECEIVED_VALUE=str(d["QTYRECEIVED_VALUE"]),
                    QTYRECEIVED_VALUE_PERCENTAGE=str(d["QTYRECEIVED_VALUE_PERCENTAGE"]),
                    CATS_RECEIVED_LOCATION=str(d["CATS_RECEIVED_LOCATION"]),
                    CATS_RECEIVED_LOCATIONTYPE=str(d["CATS_RECEIVED_LOCATIONTYPE"]),
                    SERIALNUMBER=str(d["SERIALNUMBER"]),
                    ASSETCODE=str(d["ASSETCODE"]),
                    LOTNUMBER=str(d["LOTNUMBER"]),
                    PHY_RECEV_PEND_LESS_3DAYS=str(d["PHY_RECEV_PEND_LESS_3DAYS"]),
                    PHY_RECEV_PEND_LESS_3DAYS_CNT=str(
                        d["PHY_RECEV_PEND_LESS_3DAYS_CNT"]
                    ),
                    PHY_RECEV_PEND_LESS_3DAYS_VAL=str(
                        d["PHY_RECEV_PEND_LESS_3DAYS_VAL"]
                    ),
                    PHY_RECEV_PEND_3_TO_7_DAYS=str(d["PHY_RECEV_PEND_3_TO_7_DAYS"]),
                    PHY_RECEV_PEND_3_TO_7_DAYS_CNT=str(
                        d["PHY_RECEV_PEND_3_TO_7_DAYS_CNT"]
                    ),
                    PHY_RECEV_PEND_3_TO_7_DAYS_VAL=str(
                        d["PHY_RECEV_PEND_3_TO_7_DAYS_VAL"]
                    ),
                    PHY_RECEV_PEND_GR_7DAYS=str(d["PHY_RECEV_PEND_GR_7DAYS"]),
                    PHY_RECEV_PEND_GR_7DAYS_VAL=str(d["PHY_RECEV_PEND_GR_7DAYS_VAL"]),
                    ERRORMESSAGE=str(d["ERRORMESSAGE"]),
                    PROCESSED_MO_SO=str(d["PROCESSED_MO_SO"]),
                    Month=str(d["Month"]),
                    Circle=str(d["Circle"]),
                    Unique=str(d["Unique"]),
                    Module_name=str(d["Module name"]),
                    Signoff_Month=str(d["Signoff Month"]),
                    Status=str(d["Status"]),
                    RCA=str(d["RCA"]),
                )
                objs.append(obj)

            MO_TO_VS_Shipment_Dump.objects.bulk_create(objs)

        else:
            return Response({"Status": False, "message": "Invalid file specified."})

        return Response(
            {"Status": True, "message": "Files uploaded and processed successfully."}
        )

    except Exception as e:
        error = str(e)
        return Response({"Status": False, "message": f"An error occurred: {error}"})


@api_view(["POST"])
def cats_tracker_dashboard(request):
    data = request.data
    circles = data.get("circle", [])
    print(circles)

    status = data.get("status", [])
    print(status)
    if not circles:
        objs = Consolidate_MO_based_Table.objects.all()
        unique_circle = objs.values_list("Circle", flat=True).distinct()
        circles = list(unique_circle)

    if not status:
        objs = Consolidate_MO_based_Table.objects.all()
        unique_status = objs.values_list("Status", flat=True).distinct()
        status = list(unique_status)

    objs = Consolidate_MO_based_Table.objects.all()
    objs_data = objs.filter(Circle__in=circles, Status__in=status)

    obj_val = objs_data.values(
        "Module_Name",
        "Module_Qty_dispatched_as_per_TO",
        "Module_Qty_received_at_site_as_per_TO",
        "Module_Qty_visible",
        "Gap_CATS_vs_Mobinet",
        "Module_Available_in_OSS",
        "SREQ",
        "RMO",
        "SREQ_RMO",
        "SREQ_RMO_WIP",
        "Theft",
        "MOS",
        "Virtual_MO_Regularisation",
        "MO_Cancelled",
        "Under_check",
    )
    df = pd.DataFrame(obj_val)

    for i in df.columns[1:]:
        df[i] = pd.to_numeric(df[i], errors="coerce").fillna(0).astype(int)

    grouped_df = df.groupby("Module_Name").sum()
    grouped_df.loc["total"] = grouped_df.sum()
    json_data = grouped_df.reset_index().to_json(orient="records", lines=False)

    print(grouped_df)

    new_json = json.loads(json_data)

    return Response(
        {
            "status": True,
            "data": new_json,
        }
    )


@api_view(["GET"])
def unique_circle_status_month(request):
    objs = Consolidate_MO_based_Table.objects.all()
    unique_circle = objs.values_list("Circle", flat=True).distinct()
    unique_status = objs.values_list("Status", flat=True).distinct()
    unique_month = objs.values_list("Month", flat=True).distinct()

    return Response(
        {
            "status": True,
            "unique_circle": list(unique_circle),
            "unique_status": list(unique_status),
            "unique_month": list(unique_month),
        }
    )


@api_view(["POST"])
def shipment_dump(request):
    data = request.data
    circles = data.get("circle", [])
    status = data.get("status", [])

    if not circles:
        circles = list(
            MO_TO_VS_Shipment_Dump.objects.values_list("Circle", flat=True).distinct()
        )

    if not status:
        status = list(
            MO_TO_VS_Shipment_Dump.objects.values_list("Status", flat=True).distinct()
        )

    objs_data = MO_TO_VS_Shipment_Dump.objects.filter(
        Circle__in=circles, Status__in=status
    )

    obj_val = objs_data.values("Module_name", "QTYSHIPPED", "QTYRECEIVED")
    df = pd.DataFrame(obj_val)

    for i in df.columns[1:]:
        df[i] = pd.to_numeric(df[i], errors="coerce").fillna(0).astype(int)
    grouped_df = df.groupby("Module_name").sum()
    grouped_df.loc["total"] = grouped_df.sum()
    json_data = grouped_df.reset_index().to_json(orient="records", lines=False)

    new_json = json.loads(json_data)

    return Response({"status": True, "data": new_json})



@api_view(["POST"])
def monthly_signoff_cats_vs_mobinet(request):
    data = request.data
    circle = data.get("circle")
    project = data.get("project")
    month = data.get("month")
    ms1_done_sites = data.get("ms1_done_sites")
    module_qty_dispatch_d_as_per_to_a = data.get(
        "module_qty_dispatch_d_as_per_to_a"
    )
    module_qty_recived_as_site_as_per_tO = data.get(
        "module_qty_recived_as_site_as_per_tO"
    )
    no_of_sites_gap = data.get("no_of_sites_gap")
    gap_qty_dispatch_vs_recived_c = data.get("gap_qty_dispatch_vs_recived_c")
    module_qty_visible_enm = data.get("module_qty_visible_enm")
    gap_cats_vs_emn_module_e = data.get("gap_cats_vs_emn_module_e")
    rmo_srn_qty = data.get("rmo_srn_qty")
    cam_qty = data.get("cam_qty")
    againts_faulty_qty = data.get("againts_faulty_qty")
    locator_issue_qty = data.get("locator_issue_qty")
    theft_qty = data.get("theft_qty")
    mos_pri_qty = data.get("mos_pri_qty")
    m1sc = data.get("mos_pri_qty")
    gaps_remarks = data.get("gaps_remarks")
    
    print(circle)
    print(project)
    print(month)
    print(ms1_done_sites)
    

    try:
        objects_to_create = [
            Monthly_Signoff_CATS_VS_Mobinet(
                Circle=circle,
                Project=project,
                month=month,
                MS1_Done_Sites=ms1_done_sites,
                Module_Qty_dispatch_d_as_per_to_A=module_qty_dispatch_d_as_per_to_a,
                Module_Qty_recived_as_site_as_per_TO=module_qty_recived_as_site_as_per_tO,
                No_of_Sites_Gap=no_of_sites_gap,
                Gap_Qty_Dispatch_vs_recived_c=gap_qty_dispatch_vs_recived_c,
                Module_qty_visible_ENM=module_qty_visible_enm,
                Gap_CATS_vs_ENM_Module_E=gap_cats_vs_emn_module_e,
                RMO_SRN_QTY=rmo_srn_qty,
                CAM_QTY=cam_qty,
                Againts_Faulty_QTY=againts_faulty_qty,
                Locator_Issue_QTY=locator_issue_qty,
                Theft_QTY=theft_qty,
                MOS_PRI_QTY=mos_pri_qty,
                Mlsc=m1sc,
                Gaps_Remarks=gaps_remarks,
            )
        ]

        # Bulk create instances of Monthly_Signoff_CATS_VS_Mobinet
        Monthly_Signoff_CATS_VS_Mobinet.objects.bulk_create(objects_to_create)

        return Response(
            {
                "Status": True,
                "message": "Data uploaded and processed successfully.",
            }
        )
    except Exception as e:
        return Response(
            {
                "Status": False,
                "message": e,
            }
        )
