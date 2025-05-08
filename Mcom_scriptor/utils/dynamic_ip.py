import xml.etree.ElementTree as ET


def dynamic_sgw_ip(SGW_IP):
    gtpu_mo_str ="""
    <managedObject class="NOKLTE:GTPU" distName="MRBTS-844360/LNBTS-844360/GTPU-1" version="xL23R1_2221_110" operation="create">
      <p name="gtpuN3Reqs">5</p>
      <p name="gtpuPathSupint">60</p>
      <p name="gtpuT3Resp">2</p>
      <list name="sgwIpAddressList">
    """

    ending_element_str= """   </list>
        </managedObject>
    """

    sgw_ip_item_str=""" 
            <item>
            <p name="sgwIpAddress">{sgw_ip}</p>
            <p name="transportNwId">0</p>
            </item>
            """
    op_str =""" """
    for sgw_ip in SGW_IP:
        op_str = op_str +sgw_ip_item_str.format(sgw_ip=sgw_ip)
    op_str =gtpu_mo_str + op_str + ending_element_str
    print(op_str)

    gtpu_mo =ET.fromstring(op_str)
    print(gtpu_mo)
    return gtpu_mo

def dynamic_mme_ip(MME_IP):
    lnmme_mo_str ="""
    <managedObject class="NOKLTE:LNMME" distName="MRBTS-844360/LNBTS-844360/LNMME-{counter}" version="xL23R1_2221_110" operation="create">
        <p name="administrativeState">unlocked</p>
        <p name="ipAddrPrim">{mme_ip}</p>
        <p name="mmeRatSupport">Wideband-LTE</p>
        <p name="transportNwId">0</p>
      </managedObject>

    """
    op_element_str=""" """
    for i,mme_ip in enumerate(MME_IP):
        op_element_str =op_element_str +lnmme_mo_str.format(counter=i,mme_ip=mme_ip)
        
    op_element_str = "<root>" + op_element_str + "</root>"  

    lnmme_mos = ET.fromstring(op_element_str)
    print(op_element_str)

    return lnmme_mos



if __name__ =="__main__":
    SGW_IP = ['10.50.103.6', '10.61.27.38', '10.75.212.210', '10.99.39.198', '10.99.51.102', '10.99.51.182', '10.99.51.198', '10.99.51.214', '10.58.112.6', '10.1.171.155', '10.206.250.6', '10.61.27.6', '10.61.27.22', '10.140.58.102', '2401:4900:0048:440c:0000:0000:0000:2c04', '2401:4900:0048:440c:0000:0000:0000:2c05', '2401:4900:0048:440c:0000:0000:0000:2c06', '2401:4900:0048:440c:0000:0000:0000:2c07', '2401:4900:0048:440c:0000:0000:0000:2c08', '2401:4900:0048:440c:0000:0000:0000:2c09', '2401:4900:0040:0003:0000:0000:0001:0942', '2401:4900:8:408::142b', '2401:4900:48:440c::3440']        
    MME_IP = ['10.206.252.5', '10.206.254.5', '10.75.212.187', '10.1.163.177']
    dynamic_sgw_ip(SGW_IP)
    dynamic_mme_ip(MME_IP)