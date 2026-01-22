import xml.etree.ElementTree as ET
def dynamic_Rmod_cellmapping(cell_mimo):
        # Custom importance mapping
        importance_mapping = {'4T4R': 1, '2T2R': 2}

        # Define a function to get the importance of a value
        def get_importance(item):
            return importance_mapping.get(item[1], 0)  # Default to 0 if importance not defined

        # Sort the dictionary based on importance
        cell_mimo_sorted= dict(sorted(cell_mimo.items(), key=get_importance))

        # Print the sorted dictionary
        print(cell_mimo_sorted)
        AnC=1
        Rmod=1
        temp1=""" 
            <managedObject class="com.nokia.srbts.mnl:LCELL" distName="MRBTS-844360/MNL-1/MNLENT-1/CELLMAPPING-1/LCELL-{cell}" version="MNL23R1_2221_110" operation="create">
            <p name="actAsiDistMimo">false</p>
            <p name="actDynamicSharedSpectrum">false</p>
            <p name="actWcdmaLteSharedSpectrum">false</p>
            </managedObject>
            <managedObject class="com.nokia.srbts.mnl:CHANNELGROUP" distName="MRBTS-844360/MNL-1/MNLENT-1/CELLMAPPING-1/LCELL-{cell}/CHANNELGROUP-1" version="MNL23R1_2221_110" operation="create"/>"""
            
        temp2="""
            <managedObject class="com.nokia.srbts.mnl:CHANNEL" distName="MRBTS-844360/MNL-1/MNLENT-1/CELLMAPPING-1/LCELL-{cell}/CHANNELGROUP-1/CHANNEL-{channel_1}" version="MNL23R1_2221_110" operation="create">
            <p name="antlDN">MRBTS-844360/EQM-1/APEQM-1/RMOD-{Rmod}/ANTL-{AnC}</p>
            <p name="direction">TX</p>
            </managedObject>
            <managedObject class="com.nokia.srbts.mnl:CHANNEL" distName="MRBTS-844360/MNL-1/MNLENT-1/CELLMAPPING-1/LCELL-{cell}/CHANNELGROUP-1/CHANNEL-{channel_2}" version="MNL23R1_2221_110" operation="create">
            <p name="antlDN">MRBTS-844360/EQM-1/APEQM-1/RMOD-{Rmod}/ANTL-{AnC}</p>
            <p name="direction">RX</p>
            </managedObject>
            """
            
        op_str=""" """
        ant_list=[]
        rmod_to_ant_dict={}

        for cells,mimo in cell_mimo_sorted.items():
            cell=cells[0]
            print("cell-",cell)
            in_temp1=""" """
            in_temp1= temp1.format(cell=cell)
            if mimo=="2T2R":
                R=2
            elif mimo=="4T4R":
                R=4
            else:
                pass
            for ant in range(AnC,AnC+R):
                # print(cell)
                if AnC%5==0:
                 
                    rmod_to_ant_dict[str(Rmod)]=ant_list
                    ant_list=[]
                    Rmod=Rmod+1
                    AnC=1
                   
                print("Rmod-"+str(Rmod),"Antena-"+str(AnC))
                #defining the channel
                channel_1=AnC+AnC-1
                channel_2=channel_1+1
                print("first_channel- "+ str(channel_1),"second_channel- "+ str(channel_2))
                in_temp1=in_temp1 + temp2.format(cell=cell,Rmod=Rmod,AnC=AnC,channel_1=channel_1,channel_2=channel_2)
                ant_list.append(AnC)
                AnC=AnC+1
            if len(cells) ==2:
                in_temp2=in_temp1.replace("LCELL-{cell}".format(cell=cell),"LCELL-"+str(cells[1]))
                # print(second_tpm)
                in_temp1=in_temp1 + in_temp2
            op_str=op_str+in_temp1
        rmod_to_ant_dict[str(Rmod)]=ant_list
        print(rmod_to_ant_dict)
        op_str="<root>" + op_str + "</root>"
        # print(op_str)
        Rmod_cellmapping_element=ET.fromstring(op_str)
        Rmod_element=dynamic_Rmod(Rmod,rmod_to_ant_dict)
        return Rmod_cellmapping_element,Rmod_element

def dynamic_Rmod(Rmod,rmod_to_ant_dict):
    create_Rmod_str=""" 
    <managedObject class="com.nokia.srbts.eqm:RMOD" distName="MRBTS-844360/EQM-1/APEQM-1/RMOD-{Rmod}" version="EQM23R1_2221_110" operation="create">
      <p name="actPimCancellation">false</p>
      <p name="actSharedRUIndControl">false</p>
      <p name="actSnapshotCollection">false</p>
      <p name="administrativeState">Unlocked</p>
      <p name="alVoltHighThreshold">0</p>
      <p name="alVoltLowThreshold">0</p>
      <p name="alVoltUnstableThreshold">0</p>
      <p name="energySavingMode">NORMAL</p>
      <p name="legacyWideCarrierMode">false</p>
      <p name="pimCancellingEnabled">true</p>
      <p name="prodCodePlanned">473914A.203</p>
      <p name="protocol">NOKIA</p>
    </managedObject>
    <managedObject class="com.nokia.srbts.eqm:ANTL" distName="MRBTS-844360/EQM-1/APEQM-1/RMOD-{Rmod}/ANTL-1" version="EQM23R1_2221_110" operation="create">
      <p name="antPortId">1</p>
      <p name="antennaPathDelayDL">20</p>
      <p name="antennaPathDelayUL">20</p>
      <p name="cwaThreshold">215</p>
      <p name="totalLoss">30</p>
      <p name="vswrMajorThreshold"></p>
      <p name="vswrMinorThreshold"></p>
    </managedObject>
    <managedObject class="com.nokia.srbts.eqm:ANTL" distName="MRBTS-844360/EQM-1/APEQM-1/RMOD-{Rmod}/ANTL-2" version="EQM23R1_2221_110" operation="create">
      <p name="antPortId">2</p>
      <p name="antennaPathDelayDL">20</p>
      <p name="antennaPathDelayUL">20</p>
      <p name="cwaThreshold">215</p>
      <p name="totalLoss">30</p>
      <p name="vswrMajorThreshold"></p>
      <p name="vswrMinorThreshold"></p>
    </managedObject>
    <managedObject class="com.nokia.srbts.eqm:ANTL" distName="MRBTS-844360/EQM-1/APEQM-1/RMOD-{Rmod}/ANTL-3" version="EQM23R1_2221_110" operation="create">
      <p name="antPortId">3</p>
      <p name="antennaPathDelayDL">20</p>
      <p name="antennaPathDelayUL">20</p>
      <p name="cwaThreshold">215</p>
      <p name="totalLoss">30</p>
      <p name="vswrMajorThreshold"></p>
      <p name="vswrMinorThreshold"></p>
    </managedObject>
    <managedObject class="com.nokia.srbts.eqm:ANTL" distName="MRBTS-844360/EQM-1/APEQM-1/RMOD-{Rmod}/ANTL-4" version="EQM23R1_2221_110" operation="create">
      <p name="antPortId">4</p>
      <p name="antennaPathDelayDL">20</p>
      <p name="antennaPathDelayUL">20</p>
      <p name="cwaThreshold">215</p>
      <p name="totalLoss">30</p>
      <p name="vswrMajorThreshold"></p>
      <p name="vswrMinorThreshold"></p>
    </managedObject>
    <managedObject class="com.nokia.srbts.eqm:RSL" distName="MRBTS-844360/EQM-1/APEQM-1/RMOD-{Rmod}/RSL-1" version="EQM23R1_2221_110" operation="create">
      <p name="dcVoltageEnabled">true</p>
      <p name="hdlcCommunicationAllowed">true</p>
    </managedObject>
    """
    op_str=""" """
    Rmod_len=Rmod
    for Rmod_id in range(1,Rmod_len+1):
        op_str=op_str + create_Rmod_str.format(Rmod=Rmod_id)
        op_str = "<root>" + op_str +  "</root>"
    # print(op_str) 
    Rmod_element=ET.fromstring(op_str)
    for Rmod,ant_list in rmod_to_ant_dict.items():
        for ant in ant_list:
           vswrMajorThreshold_element=Rmod_element.find(f".//managedObject[@class='com.nokia.srbts.eqm:ANTL'][@distName='MRBTS-844360/EQM-1/APEQM-1/RMOD-{Rmod}/ANTL-{ant}']/p[@name='vswrMajorThreshold']")
           vswrMajorThreshold_element.text="26"

           vswrMinorThreshold_element=Rmod_element.find(f".//managedObject[@class='com.nokia.srbts.eqm:ANTL'][@distName='MRBTS-844360/EQM-1/APEQM-1/RMOD-{Rmod}/ANTL-{ant}']/p[@name='vswrMinorThreshold']")
           vswrMinorThreshold_element.text="15"
    
    return Rmod_element
    

if __name__ =="__main__":
     cell_mimo={(11,21):"2T2R",(12,22):"4T4R",(13,23):"4T4R"}
     op=dynamic_Rmod_cellmapping(cell_mimo)
     print(op)
