import xml.etree.ElementTree as ET


def process(cell_mimo):
    cablink_mo_smod_rmod = """ 
      <managedObject class="com.nokia.srbts.eqm:CABLINK" distName="MRBTS-844360/EQM-1/HWTOP-1/CABLINK-{cablink}" version="EQM23R1_2221_110" operation="create">
        <p name="firstEndpointDN">MRBTS-844360/EQM-1/APEQM-1/CABINET-1/{f_enp_name}</p>
        <p name="firstEndpointLabel">{f_enp_label}</p>
        <p name="firstEndpointPortId">{f_enp_id}</p>
        <p name="secondEndpointDN">MRBTS-844360/EQM-1/APEQM-1/{s_enp_name}</p>
        <p name="secondEndpointLabel">{s_enp_lable}</p>
        <p name="secondEndpointPortId">{s_enp_id}</p>
      </managedObject>

    """
    cablink_mo_smod_fbba = """ 
      <managedObject class="com.nokia.srbts.eqm:CABLINK" distName="MRBTS-844360/EQM-1/HWTOP-1/CABLINK-{cablink}" version="EQM23R1_2221_110" operation="create">
        <p name="firstEndpointDN">MRBTS-844360/EQM-1/APEQM-1/CABINET-1/{f_enp_name}</p>
        <p name="firstEndpointLabel">{f_enp_label}</p>
        <p name="firstEndpointPortId">{f_enp_id}</p>
        <p name="secondEndpointDN">MRBTS-844360/EQM-1/APEQM-1/CABINET-1/{s_enp_name}</p>
        <p name="secondEndpointLabel">{s_enp_lable}</p>
        <p name="secondEndpointPortId">{s_enp_id}</p>
      </managedObject>

    """
    op_str=""" """
    
    cell_no=0
    _2t2r_count=0
    _4t4r_count=0
    for cell,value in cell_mimo.items():
        cell_no = cell_no + len(cell) 
        if value == "2T2R":
            _2t2r_count =_2t2r_count +1
        if value == "4T4R":
            _4t4r_count =_4t4r_count +1
        print(cell)
    
    print(_2t2r_count,_4t4r_count ,cell_no)
    
    op_cablink_mo=""" """

    if cell_no ==3 and _2t2r_count ==3 and _4t4r_count ==0:
        op_cablink_mo = (op_cablink_mo 
                         + cablink_mo_smod_rmod.format(cablink="1",f_enp_name="SMOD-1",f_enp_label="OPT",f_enp_id="1",s_enp_name="RMOD-1",s_enp_lable="OPT",s_enp_id="1")
                         + cablink_mo_smod_rmod.format(cablink="2",f_enp_name="SMOD-1",f_enp_label="OPT",f_enp_id="2",s_enp_name="RMOD-2",s_enp_lable="OPT",s_enp_id="1"))

    elif cell_no ==3 and _2t2r_count ==2 and _4t4r_count ==1:
        op_cablink_mo = ( op_cablink_mo 
                        + cablink_mo_smod_fbba.format(cablink="1",f_enp_name="SMOD-1",f_enp_label="BB_EXT",f_enp_id="1",s_enp_name="BBMOD-1",s_enp_lable="BB_EXT",s_enp_id="1")
                               
                        + cablink_mo_smod_rmod.format(cablink="2",f_enp_name="SMOD-1",f_enp_label="OPT",f_enp_id="1",s_enp_name="RMOD-1",s_enp_lable="OPT",s_enp_id="1")
                        + cablink_mo_smod_rmod.format(cablink="3",f_enp_name="SMOD-1",f_enp_label="OPT",f_enp_id="2",s_enp_name="RMOD-2",s_enp_lable="OPT",s_enp_id="1"))

    elif cell_no ==3 and _2t2r_count ==0 and _4t4r_count ==3:
        op_cablink_mo = ( op_cablink_mo 
                        + cablink_mo_smod_fbba.format(cablink="1",f_enp_name="SMOD-1",f_enp_label="BB_EXT",f_enp_id="1",s_enp_name="BBMOD-1",s_enp_lable="BB_EXT",s_enp_id="1")
                        + cablink_mo_smod_fbba.format(cablink="2",f_enp_name="SMOD-1",f_enp_label="BB_EXT",f_enp_id="2",s_enp_name="BBMOD-2",s_enp_lable="BB_EXT",s_enp_id="1")
                        
                        + cablink_mo_smod_rmod.format(cablink="3",f_enp_name="SMOD-1",f_enp_label="OPT",f_enp_id="1",s_enp_name="RMOD-1",s_enp_lable="OPT",s_enp_id="1")
                        + cablink_mo_smod_rmod.format(cablink="4",f_enp_name="SMOD-1",f_enp_label="OPT",f_enp_id="2",s_enp_name="RMOD-2",s_enp_lable="OPT",s_enp_id="1")
                        + cablink_mo_smod_rmod.format(cablink="5",f_enp_name="SMOD-1",f_enp_label="OPT",f_enp_id="3",s_enp_name="RMOD-3",s_enp_lable="OPT",s_enp_id="1")
                        )





    elif cell_no ==6 and _2t2r_count ==3 and _4t4r_count ==0:
        op_cablink_mo = ( op_cablink_mo 
                        + cablink_mo_smod_fbba.format(cablink="1",f_enp_name="SMOD-1",f_enp_label="BB_EXT",f_enp_id="1",s_enp_name="BBMOD-1",s_enp_lable="BB_EXT",s_enp_id="1")
                        + cablink_mo_smod_fbba.format(cablink="2",f_enp_name="SMOD-1",f_enp_label="BB_EXT",f_enp_id="2",s_enp_name="BBMOD-2",s_enp_lable="BB_EXT",s_enp_id="1")
        
                        + cablink_mo_smod_rmod.format(cablink="3",f_enp_name="SMOD-1",f_enp_label="OPT",f_enp_id="1",s_enp_name="RMOD-1",s_enp_lable="OPT",s_enp_id="1")
                        + cablink_mo_smod_rmod.format(cablink="4",f_enp_name="SMOD-1",f_enp_label="OPT",f_enp_id="2",s_enp_name="RMOD-2",s_enp_lable="OPT",s_enp_id="1"))

    elif cell_no ==6 and _2t2r_count ==2 and _4t4r_count ==1:
        op_cablink_mo = ( op_cablink_mo 
                        + cablink_mo_smod_fbba.format(cablink="1",f_enp_name="SMOD-1",f_enp_label="BB_EXT",f_enp_id="1",s_enp_name="BBMOD-1",s_enp_lable="BB_EXT",s_enp_id="1")
                        + cablink_mo_smod_fbba.format(cablink="2",f_enp_name="SMOD-1",f_enp_label="BB_EXT",f_enp_id="2",s_enp_name="BBMOD-2",s_enp_lable="BB_EXT",s_enp_id="1")
        
                        + cablink_mo_smod_rmod.format(cablink="3",f_enp_name="SMOD-1",f_enp_label="OPT",f_enp_id="1",s_enp_name="RMOD-1",s_enp_lable="OPT",s_enp_id="1")
                        + cablink_mo_smod_rmod.format(cablink="4",f_enp_name="SMOD-1",f_enp_label="OPT",f_enp_id="2",s_enp_name="RMOD-1",s_enp_lable="OPT",s_enp_id="2")
                        + cablink_mo_smod_rmod.format(cablink="5",f_enp_name="SMOD-1",f_enp_label="OPT",f_enp_id="3",s_enp_name="RMOD-2",s_enp_lable="OPT",s_enp_id="1")
                        + cablink_mo_smod_rmod.format(cablink="6",f_enp_name="BBMOD-1",f_enp_label="OPT",f_enp_id="1",s_enp_name="RMOD-2",s_enp_lable="OPT",s_enp_id="2")
                        )
    elif cell_no ==6 and _2t2r_count ==0 and _4t4r_count ==3:
        op_cablink_mo = ( op_cablink_mo 
                        + cablink_mo_smod_fbba.format(cablink="1",f_enp_name="SMOD-1",f_enp_label="BB_EXT",f_enp_id="1",s_enp_name="BBMOD-1",s_enp_lable="BB_EXT",s_enp_id="1")
                        + cablink_mo_smod_fbba.format(cablink="2",f_enp_name="SMOD-1",f_enp_label="BB_EXT",f_enp_id="2",s_enp_name="BBMOD-2",s_enp_lable="BB_EXT",s_enp_id="1")
        
                        + cablink_mo_smod_rmod.format(cablink="3",f_enp_name="SMOD-1",f_enp_label="OPT",f_enp_id="1",s_enp_name="RMOD-1",s_enp_lable="OPT",s_enp_id="1")
                        + cablink_mo_smod_rmod.format(cablink="4",f_enp_name="SMOD-1",f_enp_label="OPT",f_enp_id="2",s_enp_name="RMOD-1",s_enp_lable="OPT",s_enp_id="2")
                        + cablink_mo_smod_rmod.format(cablink="5",f_enp_name="SMOD-1",f_enp_label="OPT",f_enp_id="3",s_enp_name="RMOD-2",s_enp_lable="OPT",s_enp_id="1")
                        + cablink_mo_smod_rmod.format(cablink="6",f_enp_name="BBMOD-1",f_enp_label="OPT",f_enp_id="1",s_enp_name="RMOD-2",s_enp_lable="OPT",s_enp_id="2")
                        + cablink_mo_smod_rmod.format(cablink="7",f_enp_name="BBMOD-2",f_enp_label="OPT",f_enp_id="1",s_enp_name="RMOD-3",s_enp_lable="OPT",s_enp_id="1")
                        + cablink_mo_smod_rmod.format(cablink="8",f_enp_name="BBMOD-2",f_enp_label="OPT",f_enp_id="2",s_enp_name="RMOD-3",s_enp_lable="OPT",s_enp_id="2")
                        )
    
    else :
        # op_cablink_mo = ( op_cablink_mo 
        #                 + cablink_mo_smod_fbba.format(cablink="1",f_enp_name="SMOD-1",f_enp_label="BB_EXT",f_enp_id="1",s_enp_name="BBMOD-1",s_enp_lable="BB_EXT",s_enp_id="1")
        #                 + cablink_mo_smod_fbba.format(cablink="2",f_enp_name="SMOD-1",f_enp_label="BB_EXT",f_enp_id="2",s_enp_name="BBMOD-2",s_enp_lable="BB_EXT",s_enp_id="1")
                        
        #                 + cablink_mo_smod_rmod.format(cablink="3",f_enp_name="SMOD-1",f_enp_label="OPT",f_enp_id="1",s_enp_name="RMOD-1",s_enp_lable="OPT",s_enp_id="1")
        #                 + cablink_mo_smod_rmod.format(cablink="4",f_enp_name="SMOD-1",f_enp_label="OPT",f_enp_id="2",s_enp_name="RMOD-2",s_enp_lable="OPT",s_enp_id="1")
        #                 + cablink_mo_smod_rmod.format(cablink="5",f_enp_name="SMOD-1",f_enp_label="OPT",f_enp_id="3",s_enp_name="RMOD-3",s_enp_lable="OPT",s_enp_id="1")
        #                 )
         pass


    op_cablink_mo= "<root>" +op_cablink_mo +"</root>"
    root = ET.fromstring(op_cablink_mo)
    # print(op_cablink_mo)
    return root

if __name__ == "__main__":
        cell_mimo={(11,21):"4T4R",(12,22):"2T2R",(13,23):"2T2R"}
    # cell_mimo={(11,):"2T2R",(12,):"2T2R",(13,):"2T2R"}
        root=process(cell_mimo)
