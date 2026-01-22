import xml.etree.ElementTree as ET
def dynamic_NRDCDPR(cell_list):
    xml_element=""" <managedObject class="NOKLTE:NRDCDPR" distName="MRBTS-844360/LNBTS-844360/NRDCDPR-0" version="xL23R1_2221_110" operation="create">
        <p name="actSortBcListEnDc">false</p>
        <p name="allowedBcSelectMethod">max MIMO layers with max CCs</p>
        <p name="dlPathlossChg">3 db</p>
        <p name="enDCpMaxEUTRApowerOffset">0</p>
        <p name="enDCpMaxNRpowerOffset">0</p>
        <p name="tPeriodicPhr">20sf</p>
        <p name="tProhibitPhr">0sf</p>
        <list name="cAggrLteNrDcCellList">
            <p>-1</p>
        </list>
        <list name="dynTriggerLteNrDcConfList"> """
            
    item_str=""" 
            <item>
            <p name="actB1NrBeamMeas">true</p>
            <p name="lcrId">{cell}</p>
            <p name="method">coverageBased</p>
            </item>"""
            
    op=""" """

    
    for cell in cell_list:
        op=op + item_str.format(cell=cell)
    op=xml_element +op + """ 
        </list>
        </managedObject>
        """
    print(op)

    NRDCDPR_element=ET.fromstring(op)
    return NRDCDPR_element


if __name__ == "__main__":
    cell_list=[1,2,3,4,5]
    element=dynamic_NRDCDPR(cell_list)
    print(element)