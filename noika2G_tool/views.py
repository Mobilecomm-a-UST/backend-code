from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from pathlib import Path
from mcom_website.settings import MEDIA_ROOT, MEDIA_URL
import os
import pandas as pd

from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

base_media_url = os.path.join(MEDIA_ROOT, "Nokia2G_Script")
output_path = os.path.join(base_media_url, "Output")
os.makedirs(output_path, exist_ok=True)


def excel_formate(file_path):
    wb = load_workbook(file_path)

    header_fill = PatternFill(start_color="215967", end_color="215967", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)

    strip_fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")

 
    command_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    command_font = Font(color="333333", bold=True)

    thin_border = Side(border_style="thin", color="808080")
    full_border = Border(left=thin_border, right=thin_border, top=thin_border, bottom=thin_border)

    MAX_WIDTH = 60

    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]

     
        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border = full_border
            cell.font=Font(size=9,bold=True,color="FFFFFF")

        ws.row_dimensions[1].height =35

        col_letter = None
        col_index = None
        for col in ws.iter_cols(1, ws.max_column):
            if col[0].value == "Command":
                col_letter = col[0].column_letter
                col_index = col[0].column 
                break

    
        for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
            for cell in row:
             
                if col_index and cell.column == col_index:
                    cell.fill = command_fill
                    cell.font = command_font

                
                elif cell.row % 2 == 0:
                    cell.fill = strip_fill

                cell.alignment = Alignment(vertical="center", wrap_text=True)
                cell.border = full_border

       
        for column_cells in ws.columns:
            column = column_cells[0].column_letter

            if column == col_letter:
                ws.column_dimensions[column].width = 170
                continue

            max_length = 0
            for cell in column_cells:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))

            ws.column_dimensions[column].width = max_length + 2

     
       

    wb.save(file_path)

@api_view(['POST'])
def nokia_2g(request):
    ref_file = request.FILES.get("ref_file")
    if not ref_file:
        return Response({"status": False, "message": "ref_file not uploaded"}, status=400)
    
    # work for STCP TRX 2 for two command-------
    ref_sctp_df=pd.read_excel(ref_file, sheet_name="STCP TRX 2")
    ref_sctp_df.columns = ref_sctp_df.columns.str.strip()


    ref_sctp_df["Command"] = ref_sctp_df.apply(
        lambda row: (
            f"ZOYX:{row['SCTP association name']}:{row['SCTP user']}:{row['role']}:"
            f"{row['unit']},{row['index(BCSU)']}:AFAST{row['SCTP parameter set']}:;\n"
            
            f"ZOYP:{row['SCTP user']}:{row['SCTP association name']}:"
            f"\"{row['SOURCE ADDRESS']}\",,{row['SOURCE PORT']}:"
            f"\"{row['DESTINATION ADDRESS']}\",{row['Net Mask Length']},,,{row['DESTINATION PORT']}:;\n"
            
            # f"ZOYS:{row['SCTP user']}:{row['SCTP association name']}:ACT;"
        ),
        axis=1
    )

    #work for LAPD------------------
    lapd_df=pd.read_excel(ref_file,sheet_name="LAPD")
    lapd_df["Command"]=lapd_df.apply(
        lambda raw :(
            f"ZDWP:{raw['LAPD_ID']}:{raw['unit']},{raw['index(BCSU)']}:0,{raw['SCTP parameter set']}:{raw['SCTP association name']}"
        ),axis=1
    )

    # work for BCF for command-------

    bcf_df=pd.read_excel(ref_file,sheet_name="BCF")
    bcf_df.columns = bcf_df.columns.str.strip()
    bcf_df["Command"]= bcf_df.apply(
        lambda row:( 
        f"ZEFC:{row['BCF_ID']},{row['BTS_TYPE']}:{row['DNAME']},REF={row['REF BCF'] if pd.notna(row['REF BCF']) else ''}"
        f",::VLANID={row['VLAN ID']},"
        f"BCUIP={row['BCUIP']},SMCUP={row['SMCUP']},"
        f"BMIP={row['BMIP']},SMMP={row['SMMP']},"
        f"ETPGID={row['Used ETME ID']},::;\n"

        f"ZEFM:{row['BCF_ID']}::::PACC={row['PACC']},PL1={row['PL1']},PL2={row['PL2']},DLCIR={row['DLCIR']},"
        f"ULTS={row['ULTS']},ULCIR={row['ULCIR']},ULCBS={row['ULCBS']},MBMWT={row['MBMWT']},MEMWT={row['MEMWT']},MMPS={row['MMPS']},;\n"

        f"ZEXA:LMUA={row['LMUA']}:TRE={row['TRE']},BCF={row['BCF_ID']},:"
        f"FNO={row['FNO']},LTO={row['LTO']},FMU={row['FMU']},LTD={row['LTD']},:;\n"

        f"ZEFM:{row['BCF_ID']}:CS={row['CS']},SENA={row['SENA']};\n"

        f"ZEFM:{row['BCF_ID']}::BU1={row['BU1']},BU2={row['BU2']};\n"

        f"ZEFM:{row['BCF_ID']}:CS={row['CS']};\n"

        f"ZEEI:BCF={row['BCF_ID']}:;"

        ),axis=1
    )
   
    # work for BTS for command-------
    bts_df=pd.read_excel(ref_file,sheet_name="BTS")
    bts_df.columns = bts_df.columns.str.strip()
    bts_df["Command"] = bts_df.apply(
    lambda row: "\n".join([
        f"ZEQC:BCF={row['BCF']},BTS={row['BTS_ID']},SEG={row['SEG_ID']},REF={row['MR ID']},NAME={row['NW_NAME']},SEGNAME={row['SEG_NAME']}:CI={row['CI']},BAND={row['BAND']}:NCC={row['NCC']},BCC={row['BCC']}:MCC={row['MCC']},MNC={row['MNC']},LAC={row['LAC']}::GENA={row['GENA']},RAC={row['RAC']};",

        f"ZEQA:BTS={row['BTS_ID']}:MAL={row['MAL']},MO={row['MO']},MS={row['MS']};",

        f"ZEQE:BTS={row['BTS_ID']}:HOP={row['HOP']},HSN1={row['HSN1']};",

        f"ZEUC:SEG={row['SEG_ID']},RSEG={row['MR ID']};",
        f"ZEHC:SEG={row['SEG_ID']},RSEG={row['MR ID']};",
        f"ZEHC:SEG={row['SEG_ID']},RSEG={row['MR ID']};",

        f"ZEQV:SEG={row['SEG_ID']}:GENA={row['GENA']},:PCU={row['PCU']};",
        f"ZEQV:BTS={row['BTS_ID']}:EGENA={row['EGENA']};",
        f"ZEQV:BTS={row['BTS_ID']}:CDED={row['CDED']},CDEF={row['CDEF']};",

        f"ZEFM:{row['BCF']}::T200S={row['T200S']},T200F={row['T200F']};",

        f"ZEQM:BTS={row['BTS_ID']}:RDIV={row['RXDIV']};",
        f"ZEQV:SEG={row['SEG_ID']}:BFG={row['BFG']};",

        f"ZEQM:SEG={row['SEG_ID']}:PMAX1={row['PMAX1']},PMAX2={row['PMAX2']},FRL={row['FRL']},FRU={row['FRU']},AFRL={row['AFRL']},AFRU={row['AFRU']},BMA={row['BMA']};",

        f"ZEQF:SEG={row['SEG_ID']}:PLMN={row['PLMN']},;",
        f"ZEQY:SEG={row['SEG_ID']}:AHRLT={row['AHRLT']},ARLT={row['ARLT']},;",
        f"ZEQG:SEG={row['SEG_ID']}:RLT={row['RLT']};",

        f"ZEQM:SEG={row['SEG_ID']}::::QSRI={row['QSRI']},QSRP={row['QSRP']},:::::;",
        f"ZEQM:BTS={row['BTS_ID']}:RDIV={row['RXDIV']},;",
        f"ZEQM:SEG={row['SEG_ID']}::::FDD={row['FDD']},FDM={row['FDM']},;",

        f"ZEQF:SEG={row['SEG_ID']}:FRLTE={row['FRLTE']};",
        f"ZEQM:SEG={row['SEG_ID']}:SLO={row['SLO']},CB={row['CB']},BLT={row['BLT']},NECI={row['NECI']},CABE={row['CABE']};",
        f"ZEQB:SEG={row['SEG_ID']}:IDLE={row['BAL']},ACT={row['ACT']},;",

        f"ZEQF:SEG={row['SEG_ID']}:RE={row['RE']},;",
        f"ZEQM:SEG={row['SEG_ID']}:TRP={row['TRP']};",
        f"ZEQE:BTS={row['BTS_ID']}:AHOP={row['AHOP']};",
        f"ZEQF:SEG={row['SEG_ID']}:DR={row['DR']};",
        f"ZEQJ:SEG={row['SEG_ID']}:PER={row['PER']};",
        f"ZEQV:SEG={row['SEG_ID']}:GENA={row['GENA']};"
    ]),
    axis=1
)
   
    
    trx_df=pd.read_excel(ref_file,sheet_name="TRX")
    trx_df.columns = trx_df.columns.str.strip()
    trx_df["Command"] = trx_df.apply(
    lambda row: (
        f"ZDWP:{row['LAPD_NAME']}:"
        f"{'BCSU' if 'BCSU' in row and pd.notna(row['BCSU']) else 'BCXU'},"
        f"{row['BCSU'] if 'BCSU' in row and pd.notna(row['BCSU']) else row['BCXU']}"
        f":0,1:{row['SCTP Name']},:;\n"

        f"ZERC:BTS={row['BTS_ID']},TRX={row['TRX_ID']}:"
        f"PREF={row['PREF']},GTRX={row['GTRX']},:"
        f"FREQ={row['FREQ']},TSC={row['TSC']}:"
        f"DNAME={row['LAPD_NAME']}:"
        f"CH0={row['CH_0']},CH1={row['CH_1']},CH2={row['CH_2']},CH3={row['CH_3']},"
        f"CH4={row['CH_4']},CH5={row['CH_5']},CH6={row['CH_6']},CH7={row['CH_7']},:;\n"
    ),
    axis=1
)
    
    lbs_df=pd.read_excel(ref_file,sheet_name="LBS Data")
    lbs_df.columns = lbs_df.columns.str.strip()
    lbs_df["Command"]=lbs_df.apply(
    lambda row:(
        f"ZEXC:LAC={row['LAC']},CI={row['CI']}:"
        f"FREQ={row['FREQ']},NCC={row['NCC']},BCC={row['BCC']}:"
        f"LADS={row['LADS']},LAD={row['LAD']},LAM={row['LAM']},LAS={row['LAS']},LAF={row['LAF']},"
        f"LODS={row['LODS']},LOD={row['LOD']},LOM={row['LOM']},LOS={row['LOS']},LOF={row['LOF']},AL={row['AL']}:"
        f"ABE={row['ABE']},CIT={row['CIT']},AHE={row['AHE']},AHB={row['AHB']},MRP={row['MRP']},"
        f"FSR={row['FSR']},BSR={row['BSR']};"
    ),
    axis=1
    )

    adce_df=pd.read_excel(ref_file,sheet_name="ADCE")
    adce_df.columns = adce_df.columns.str.strip()
    adce_df["Command"]=adce_df.apply(
    lambda row:(
    f"ZEAC:SEG={row['S_BTS_ID']}::"
    f"MCC={row['MCC']},MNC={row['MNC']},LAC={row['A_LAC']},CI={row['A_CI']}:"
    f"NCC={row['A_NCC']},BCC={row['A_BCC']},FREQ={row['A_FREQ']}:"
    f"SYNC={row['SYNC']},DRT={row['DRT']},SL={row['SL']},"
    f"PMRG={row['PMRG']},LMRG={row['LMRG']},QMRG={row['QMRG']},RAC={row['RAC']};"

    ),axis=1   
    )
    
    # ref_sctp_df2=pd.read_excel(ref_file, sheet_name="STCP TRX 2")
    # ref_sctp_df2.columns = ref_sctp_df2.columns.str.strip()
    # ref_sctp_df2["Command"] = ref_sctp_df2.apply(
    #     lambda row: (
    #         f"ZOYS:{row['SCTP user']}:{row['SCTP association name']}:ACT;"
    #     ),
    #     axis=1
    # )
    

    # trx_df2=pd.read_excel(ref_file,sheet_name="TRX")
    # trx_df2.columns = trx_df2.columns.str.strip()
    # trx_df2["Command"] = trx_df2.apply(
    # lambda row: (
    #     f"ZERS:BTS={row['BTS_ID']},TRX={row['TRX_ID']}:U;\n"
    #     f"ZEQS:BTS={row['BTS_ID']}:U;"

    # ),
    # axis=1
    # )


    
    all_commands = []
    all_commands += [("STCP TRX 2", cmd) for cmd in ref_sctp_df["Command"].dropna()]
    all_commands += [("LAPD", cmd) for cmd in lapd_df["Command"].dropna()]
    all_commands += [("BCF", cmd) for cmd in bcf_df["Command"].dropna()]
    all_commands += [("BTS", cmd) for cmd in bts_df["Command"].dropna()]
    all_commands += [("TRX", cmd) for cmd in trx_df["Command"].dropna()]
    all_commands += [("LBS Data", cmd) for cmd in lbs_df["Command"].dropna()]
    all_commands += [("ADCE", cmd) for cmd in adce_df["Command"].dropna()]
    # all_commands += [("STCP TRX 2", cmd) for cmd in ref_sctp_df2["Command"].dropna()]
    # all_commands += [("TRX", cmd) for cmd in trx_df2["Command"].dropna()]
    final_df = pd.DataFrame(all_commands, columns=["Sheet Name","Command"])
    final_df["Command"] = final_df["Command"].str.replace(r"=(nan|None)\b", "=", regex=True)
    

    file_name = "2G_Script.xlsx"
    final_output_path = os.path.join(output_path, file_name)

    with pd.ExcelWriter(final_output_path, engine='openpyxl') as writer:
        # ref_sctp_df.to_excel(writer, sheet_name="STCP TRX 2", index=False)
        # lapd_df.to_excel(writer,sheet_name="LAPD",index=False)
        # bcf_df.to_excel(writer, sheet_name="BCF", index=False)
        # bts_df.to_excel(writer,sheet_name="BTS", index=False)
        # trx_df.to_excel(writer,sheet_name="TRX",index=False)
        # lbs_df.to_excel(writer,sheet_name="LBS Data",index=False)
        # adce_df.to_excel(writer,sheet_name="ADCE",index=False)
        final_df.to_excel(writer, sheet_name="Command", index=False)
    excel_formate(final_output_path)

    relative_path = os.path.relpath(final_output_path, MEDIA_ROOT).replace("\\", "/")
    download_url = request.build_absolute_uri(f"{MEDIA_URL}{relative_path}")

    return Response({
        "status": True,
        "message": "2G Script Generated Successfully",
        "download_url": download_url
    })
 
   

