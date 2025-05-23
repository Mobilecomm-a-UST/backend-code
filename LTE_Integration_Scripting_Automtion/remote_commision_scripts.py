<<<<<<< HEAD
=======
kk_5G_RRU_creation = """ 
<?xml version="1.0" encoding="UTF-8"?>                                                                                                                            
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">                                                                                                           
  <capabilities>                                                                                                                                                  
    <capability>urn:ietf:params:netconf:base:1.0</capability>                                                                                                     
  </capabilities>                                                                                                                                                 
</hello>                                                                                                                                                          
]]>]]>                                                                                                                                                            
<rpc message-id="1" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">                                                                                              
  <edit-config>                                                                                                                                                   
    <target>                                                                                                                                                      
      <running />                                                                                                                                                 
    </target>                                                                                                                                                     
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">                                                                                                   
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">                                                                                                       
        <managedElementId>1</managedElementId>                                                                                                                    
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">                                                                                                    
          <equipmentId>1</equipmentId>                                                                                                                            
          <userLabel>Equip_1</userLabel>                                                                                                                          
          <FieldReplaceableUnit xmlns="urn:com:ericsson:ecim:ReqFieldReplaceableUnit">                                                                            
            <fieldReplaceableUnitId>{fieldReplaceableUnitId}</fieldReplaceableUnitId>                                                                                                    
            <administrativeState>UNLOCKED</administrativeState>                                                                                                   
            <isSharedWithExternalMe>false</isSharedWithExternalMe>                                                                                                
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">                                                                                                      
              <riPortId>K</riPortId>                                                                                                                              
              <administrativeState>UNLOCKED</administrativeState>                                                                                                 
            </RiPort>                                                                                                                                             
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">                                                                                                      
              <riPortId>L</riPortId>                                                                                                                              
              <administrativeState>UNLOCKED</administrativeState>                                                                                                 
            </RiPort>                                                                                                                                             
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">                                                                                                      
              <riPortId>M</riPortId>                                                                                                                              
              <administrativeState>UNLOCKED</administrativeState>                                                                                                 
            </RiPort>                                                                                                                                             
          </FieldReplaceableUnit>                                                                                                                                 
          <FieldReplaceableUnit xmlns="urn:com:ericsson:ecim:ReqFieldReplaceableUnit">                                                                            
            <fieldReplaceableUnitId>{Radio_UnitId}</fieldReplaceableUnitId>                                                                                            
            <administrativeState>UNLOCKED</administrativeState>                                                                                                   
            <isSharedWithExternalMe>false</isSharedWithExternalMe>                                                                                                
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">                                                                                                      
              <riPortId>DATA_1</riPortId>                                                                                                                         
              <administrativeState>UNLOCKED</administrativeState>                                                                                                 
            </RiPort>                                                                                                                                             
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">                                                                                                      
              <riPortId>DATA_2</riPortId>                                                                                                                         
              <administrativeState>UNLOCKED</administrativeState>                                                                                                 
            </RiPort>                                                                                                                                             
            <Transceiver xmlns="urn:com:ericsson:ecim:ReqTransceiver">                                                                                            
              <transceiverId>1</transceiverId>                                                                                                                    
              <mechanicalAntennaTilt>0</mechanicalAntennaTilt>                                                                                                    
              <maxTotalTilt>900</maxTotalTilt>                                                                                                                    
              <minTotalTilt>-900</minTotalTilt>                                                                                                                   
            </Transceiver>                                                                                                                                        
          </FieldReplaceableUnit>                                                                                                                                                                                                                                                       
          <RiLink xmlns="urn:com:ericsson:ecim:ReqRiLink">                                                                                                        
            <riLinkId>{riLinkId}</riLinkId>                                                                                                                          
            <riPortRef1>ManagedElement=1,Equipment=1,FieldReplaceableUnit={fieldReplaceableUnitId},RiPort={RiPort_BB}</riPortRef1>                                                                 
            <riPortRef2>ManagedElement=1,Equipment=1,FieldReplaceableUnit={Radio_UnitId},RiPort={RiPort_Radio}</riPortRef2>                                                    
          </RiLink>                                                                                                                                                                                                                                                                                           
        </Equipment>                                                                                                                                              
        <EquipmentSupportFunction xmlns="urn:com:ericsson:ecim:ResEquipmentSupportFunction">                                                                      
          <equipmentSupportFunctionId>1</equipmentSupportFunctionId>                                                                                              
          <supportSystemControl>true</supportSystemControl>                                                                                                       
          <autoCreateUnits>true</autoCreateUnits>                                                                                                                 
          <autoCreateExternalNodes>true</autoCreateExternalNodes>                                                                                                 
        </EquipmentSupportFunction>                                                                                                                               
        <NodeSupport xmlns="urn:com:ericsson:ecim:RmeSupport">                                                                                                    
          <nodeSupportId>1</nodeSupportId>                                                                                                                        
          <SectorEquipmentFunction xmlns="urn:com:ericsson:ecim:RmeSectorEquipmentFunction">                                                                      
            <sectorEquipmentFunctionId>{sectorEquipmentFunctionId}</sectorEquipmentFunctionId>                                                                                          
            <administrativeState>UNLOCKED</administrativeState>                                                                                                   
            <rfBranchRef>ManagedElement=1,Equipment=1,FieldReplaceableUnit={Radio_UnitId},Transceiver=1</rfBranchRef>                                                  
          </SectorEquipmentFunction>                                                                                                                                                                                                                                                  
        </NodeSupport>                                                                                                                                            
      </ManagedElement>                                                                                                                                           
    </config>                                                                                                                                                     
  </edit-config>                                                                                                                                                  
</rpc>                                                                                                                                                            
]]>]]>                                                                                                                                                            
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">                                                                                        
  <close-session></close-session>                                                                                                                                 
</rpc>                                                                                                                                                            
]]>]]>                                                                                                                                                            
                                                                                                                                                    
"""
>>>>>>> vinay_duke_work






<<<<<<< HEAD
=======
RRU_2219_B0_B1_B3_2X2 = """
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="sectorEquipmentFunctionId={sectorEquipmentFunctionId}" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>{eNodeBName}</managedElementId>
		<userLabel>{eNodeBName}</userLabel>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
		  <FieldReplaceableUnit xmlns="urn:com:ericsson:ecim:ReqFieldReplaceableUnit">
            <fieldReplaceableUnitId>RRU-{Radio_UnitId}</fieldReplaceableUnitId>
			<administrativeState>UNLOCKED</administrativeState>
			<isSharedWithExternalMe>false</isSharedWithExternalMe>			
            <RfPort xmlns="urn:com:ericsson:ecim:ReqRfPort">
              <rfPortId>A</rfPortId>
              <vswrSupervisionActive>true</vswrSupervisionActive>
              <vswrSupervisionSensitivity>100</vswrSupervisionSensitivity>
              <administrativeState>UNLOCKED</administrativeState>
              <antennaSupervisionActive>false</antennaSupervisionActive>
            </RfPort>
            <RfPort xmlns="urn:com:ericsson:ecim:ReqRfPort">
              <rfPortId>B</rfPortId>
              <vswrSupervisionActive>true</vswrSupervisionActive>
              <vswrSupervisionSensitivity>100</vswrSupervisionSensitivity>
              <administrativeState>UNLOCKED</administrativeState>
              <antennaSupervisionActive>false</antennaSupervisionActive>
            </RfPort>
            <RfPort xmlns="urn:com:ericsson:ecim:ReqRfPort">
              <rfPortId>R</rfPortId>
              <vswrSupervisionActive>false</vswrSupervisionActive>
              <vswrSupervisionSensitivity>-1</vswrSupervisionSensitivity>
              <administrativeState>UNLOCKED</administrativeState>
              <antennaSupervisionActive>false</antennaSupervisionActive>
            </RfPort>			
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>DATA_1</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>DATA_2</riPortId>
            </RiPort>
          </FieldReplaceableUnit>
        </Equipment>
		
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <AntennaUnitGroup xmlns="urn:com:ericsson:ecim:ReqAntennaSystem">
            <antennaUnitGroupId>{Radio_UnitId}</antennaUnitGroupId>
          </AntennaUnitGroup>		  
        </Equipment>
		<Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <AntennaUnitGroup xmlns="urn:com:ericsson:ecim:ReqAntennaSystem">
            <antennaUnitGroupId>{Radio_UnitId}</antennaUnitGroupId>
			<AntennaUnit>
              <antennaUnitId>1</antennaUnitId>
              <mechanicalAntennaTilt>0</mechanicalAntennaTilt>
			  <AntennaSubunit>
                <antennaSubunitId>1</antennaSubunitId>  
                <maxTotalTilt>250</maxTotalTilt>
                <minTotalTilt>-250</minTotalTilt>				
				<AuPort>
                  <auPortId>1</auPortId>
                </AuPort>
				<AuPort>
                  <auPortId>2</auPortId>
                </AuPort>				
			  </AntennaSubunit>
            </AntennaUnit>
          </AntennaUnitGroup>
        </Equipment>		
		<Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <AntennaUnitGroup xmlns="urn:com:ericsson:ecim:ReqAntennaSystem">
            <antennaUnitGroupId>{Radio_UnitId}</antennaUnitGroupId>
            <RfBranch>
              <rfBranchId>1</rfBranchId>
              <auPortRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},AntennaUnit=1,AntennaSubunit=1,AuPort=1</auPortRef>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <rfPortRef>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=RRU-{Radio_UnitId},RfPort=A</rfPortRef>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
            </RfBranch>	
            <RfBranch>
              <rfBranchId>2</rfBranchId>
              <auPortRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},AntennaUnit=1,AntennaSubunit=1,AuPort=2</auPortRef>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <rfPortRef>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=RRU-{Radio_UnitId},RfPort=B</rfPortRef>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
            </RfBranch>			
          </AntennaUnitGroup>
		</Equipment>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>		  
          <RiLink xmlns="urn:com:ericsson:ecim:ReqRiLink">
            <riLinkId>{Radio_UnitId}</riLinkId>
            <riPortRef1>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit={fieldReplaceableUnitId},RiPort={RiPort_BB}</riPortRef1>
            <riPortRef2>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=RRU-{Radio_UnitId},RiPort={RiPort_Radio}</riPortRef2>
          </RiLink>
		</Equipment>
        <NodeSupport xmlns="urn:com:ericsson:ecim:RmeSupport">
          <nodeSupportId>1</nodeSupportId>		  
          <SectorEquipmentFunction xmlns="urn:com:ericsson:ecim:RmeSectorEquipmentFunction">
            <sectorEquipmentFunctionId>{sectorEquipmentFunctionId}</sectorEquipmentFunctionId>
            <administrativeState>LOCKED</administrativeState>
				<rfBranchRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},RfBranch=1</rfBranchRef>
				<rfBranchRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},RfBranch=2</rfBranchRef>
          </SectorEquipmentFunction>  
        </NodeSupport>
	  </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>
"""


RRU_4412_4418_4427_4471_4X4 = """
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="sectorEquipmentFunctionId={sectorEquipmentFunctionId}" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>{eNodeBName}</managedElementId>
		<userLabel>{eNodeBName}</userLabel>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
		  <FieldReplaceableUnit xmlns="urn:com:ericsson:ecim:ReqFieldReplaceableUnit">
            <fieldReplaceableUnitId>RRU-{Radio_UnitId}</fieldReplaceableUnitId>
			<administrativeState>UNLOCKED</administrativeState>
			<isSharedWithExternalMe>false</isSharedWithExternalMe>			
            <RfPort xmlns="urn:com:ericsson:ecim:ReqRfPort">
              <rfPortId>A</rfPortId>
              <vswrSupervisionActive>true</vswrSupervisionActive>
              <vswrSupervisionSensitivity>100</vswrSupervisionSensitivity>
              <administrativeState>UNLOCKED</administrativeState>
              <antennaSupervisionActive>false</antennaSupervisionActive>
            </RfPort>
            <RfPort xmlns="urn:com:ericsson:ecim:ReqRfPort">
              <rfPortId>B</rfPortId>
              <vswrSupervisionActive>true</vswrSupervisionActive>
              <vswrSupervisionSensitivity>100</vswrSupervisionSensitivity>
              <administrativeState>UNLOCKED</administrativeState>
              <antennaSupervisionActive>false</antennaSupervisionActive>
            </RfPort>
            <RfPort xmlns="urn:com:ericsson:ecim:ReqRfPort">
              <rfPortId>C</rfPortId>
              <vswrSupervisionActive>true</vswrSupervisionActive>
              <vswrSupervisionSensitivity>100</vswrSupervisionSensitivity>
              <administrativeState>UNLOCKED</administrativeState>
              <antennaSupervisionActive>false</antennaSupervisionActive>
            </RfPort>
            <RfPort xmlns="urn:com:ericsson:ecim:ReqRfPort">
              <rfPortId>D</rfPortId>
              <vswrSupervisionActive>true</vswrSupervisionActive>
              <vswrSupervisionSensitivity>100</vswrSupervisionSensitivity>
              <administrativeState>UNLOCKED</administrativeState>
              <antennaSupervisionActive>false</antennaSupervisionActive>
            </RfPort>
            <RfPort xmlns="urn:com:ericsson:ecim:ReqRfPort">
              <rfPortId>R</rfPortId>
              <vswrSupervisionActive>false</vswrSupervisionActive>
              <vswrSupervisionSensitivity>-1</vswrSupervisionSensitivity>
              <administrativeState>UNLOCKED</administrativeState>
              <antennaSupervisionActive>false</antennaSupervisionActive>
            </RfPort>			
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>DATA_1</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>DATA_2</riPortId>
            </RiPort>
          </FieldReplaceableUnit>
        </Equipment>
		
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <AntennaUnitGroup xmlns="urn:com:ericsson:ecim:ReqAntennaSystem">
            <antennaUnitGroupId>{Radio_UnitId}</antennaUnitGroupId>
          </AntennaUnitGroup>		  
        </Equipment>
		<Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <AntennaUnitGroup xmlns="urn:com:ericsson:ecim:ReqAntennaSystem">
            <antennaUnitGroupId>{Radio_UnitId}</antennaUnitGroupId>
			<AntennaUnit>
              <antennaUnitId>1</antennaUnitId>
              <mechanicalAntennaTilt>0</mechanicalAntennaTilt>
			  <AntennaSubunit>
                <antennaSubunitId>1</antennaSubunitId>  
                <maxTotalTilt>250</maxTotalTilt>
                <minTotalTilt>-250</minTotalTilt>				
				<AuPort>
                  <auPortId>1</auPortId>
                </AuPort>
				<AuPort>
                  <auPortId>2</auPortId>
                </AuPort>
				<AuPort>
                  <auPortId>3</auPortId>
                </AuPort>
				<AuPort>
                  <auPortId>4</auPortId>
                </AuPort>				
			  </AntennaSubunit>
            </AntennaUnit>
          </AntennaUnitGroup>
        </Equipment>		
		<Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <AntennaUnitGroup xmlns="urn:com:ericsson:ecim:ReqAntennaSystem">
            <antennaUnitGroupId>{Radio_UnitId}</antennaUnitGroupId>
            <RfBranch>
              <rfBranchId>1</rfBranchId>
              <auPortRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},AntennaUnit=1,AntennaSubunit=1,AuPort=1</auPortRef>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <rfPortRef>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=RRU-{Radio_UnitId},RfPort=A</rfPortRef>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
            </RfBranch>	
            <RfBranch>
              <rfBranchId>2</rfBranchId>
              <auPortRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},AntennaUnit=1,AntennaSubunit=1,AuPort=2</auPortRef>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <rfPortRef>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=RRU-{Radio_UnitId},RfPort=B</rfPortRef>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
            </RfBranch>	
            <RfBranch>
              <rfBranchId>3</rfBranchId>
              <auPortRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},AntennaUnit=1,AntennaSubunit=1,AuPort=3</auPortRef>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <rfPortRef>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=RRU-{Radio_UnitId},RfPort=C</rfPortRef>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
            </RfBranch>	
            <RfBranch>
              <rfBranchId>4</rfBranchId>
              <auPortRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},AntennaUnit=1,AntennaSubunit=1,AuPort=4</auPortRef>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <rfPortRef>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=RRU-{Radio_UnitId},RfPort=D</rfPortRef>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
            </RfBranch>			
          </AntennaUnitGroup>
		</Equipment>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>		  
          <RiLink xmlns="urn:com:ericsson:ecim:ReqRiLink">
            <riLinkId>{Radio_UnitId}</riLinkId>
            <riPortRef1>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit={fieldReplaceableUnitId},RiPort={RiPort_BB}</riPortRef1>
            <riPortRef2>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=RRU-{Radio_UnitId},RiPort={RiPort_Radio}</riPortRef2>
          </RiLink>
		</Equipment>
        <NodeSupport xmlns="urn:com:ericsson:ecim:RmeSupport">
          <nodeSupportId>1</nodeSupportId>		  
          <SectorEquipmentFunction xmlns="urn:com:ericsson:ecim:RmeSectorEquipmentFunction">
            <sectorEquipmentFunctionId>{sectorEquipmentFunctionId}</sectorEquipmentFunctionId>
            <administrativeState>LOCKED</administrativeState>
				<rfBranchRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},RfBranch=1</rfBranchRef>
				<rfBranchRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},RfBranch=2</rfBranchRef>
				<rfBranchRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},RfBranch=3</rfBranchRef>
				<rfBranchRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},RfBranch=4</rfBranchRef>
          </SectorEquipmentFunction>  
        </NodeSupport>
	  </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>


"""

RRU_6626_6X6 = """
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="sectorEquipmentFunctionId={sectorEquipmentFunctionId}" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>{eNodeBName}</managedElementId>
		<userLabel>{eNodeBName}</userLabel>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
		  <FieldReplaceableUnit xmlns="urn:com:ericsson:ecim:ReqFieldReplaceableUnit">
            <fieldReplaceableUnitId>RRU-{Radio_UnitId}</fieldReplaceableUnitId>
			<administrativeState>UNLOCKED</administrativeState>
			<isSharedWithExternalMe>false</isSharedWithExternalMe>			
            <RfPort xmlns="urn:com:ericsson:ecim:ReqRfPort">
              <rfPortId>A</rfPortId>
              <vswrSupervisionActive>true</vswrSupervisionActive>
              <vswrSupervisionSensitivity>100</vswrSupervisionSensitivity>
              <administrativeState>UNLOCKED</administrativeState>
              <antennaSupervisionActive>false</antennaSupervisionActive>
            </RfPort>
            <RfPort xmlns="urn:com:ericsson:ecim:ReqRfPort">
              <rfPortId>B</rfPortId>
              <vswrSupervisionActive>true</vswrSupervisionActive>
              <vswrSupervisionSensitivity>100</vswrSupervisionSensitivity>
              <administrativeState>UNLOCKED</administrativeState>
              <antennaSupervisionActive>false</antennaSupervisionActive>
            </RfPort>
            <RfPort xmlns="urn:com:ericsson:ecim:ReqRfPort">
              <rfPortId>C</rfPortId>
              <vswrSupervisionActive>true</vswrSupervisionActive>
              <vswrSupervisionSensitivity>100</vswrSupervisionSensitivity>
              <administrativeState>UNLOCKED</administrativeState>
              <antennaSupervisionActive>false</antennaSupervisionActive>
            </RfPort>
            <RfPort xmlns="urn:com:ericsson:ecim:ReqRfPort">
              <rfPortId>D</rfPortId>
              <vswrSupervisionActive>true</vswrSupervisionActive>
              <vswrSupervisionSensitivity>100</vswrSupervisionSensitivity>
              <administrativeState>UNLOCKED</administrativeState>
              <antennaSupervisionActive>false</antennaSupervisionActive>
            </RfPort>
            <RfPort xmlns="urn:com:ericsson:ecim:ReqRfPort">
              <rfPortId>E</rfPortId>
              <vswrSupervisionActive>true</vswrSupervisionActive>
              <vswrSupervisionSensitivity>100</vswrSupervisionSensitivity>
              <administrativeState>UNLOCKED</administrativeState>
              <antennaSupervisionActive>false</antennaSupervisionActive>
            </RfPort>
            <RfPort xmlns="urn:com:ericsson:ecim:ReqRfPort">
              <rfPortId>F</rfPortId>
              <vswrSupervisionActive>true</vswrSupervisionActive>
              <vswrSupervisionSensitivity>100</vswrSupervisionSensitivity>
              <administrativeState>UNLOCKED</administrativeState>
              <antennaSupervisionActive>false</antennaSupervisionActive>
            </RfPort>			
            <RfPort xmlns="urn:com:ericsson:ecim:ReqRfPort">
              <rfPortId>R</rfPortId>
              <vswrSupervisionActive>false</vswrSupervisionActive>
              <vswrSupervisionSensitivity>-1</vswrSupervisionSensitivity>
              <administrativeState>UNLOCKED</administrativeState>
              <antennaSupervisionActive>false</antennaSupervisionActive>
            </RfPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>DATA_1</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>DATA_2</riPortId>
            </RiPort>
          </FieldReplaceableUnit>
        </Equipment>
		
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <AntennaUnitGroup xmlns="urn:com:ericsson:ecim:ReqAntennaSystem">
            <antennaUnitGroupId>{Radio_UnitId}</antennaUnitGroupId>
          </AntennaUnitGroup>		  
        </Equipment>
		<Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <AntennaUnitGroup xmlns="urn:com:ericsson:ecim:ReqAntennaSystem">
            <antennaUnitGroupId>{Radio_UnitId}</antennaUnitGroupId>
			<AntennaUnit>
              <antennaUnitId>1</antennaUnitId>
              <mechanicalAntennaTilt>0</mechanicalAntennaTilt>
			  <AntennaSubunit>
                <antennaSubunitId>1</antennaSubunitId>  
                <maxTotalTilt>250</maxTotalTilt>
                <minTotalTilt>-250</minTotalTilt>				
				<AuPort>
                  <auPortId>1</auPortId>
                </AuPort>
				<AuPort>
                  <auPortId>2</auPortId>
                </AuPort>
				<AuPort>
                  <auPortId>3</auPortId>
                </AuPort>
				<AuPort>
                  <auPortId>4</auPortId>
                </AuPort>
                <AuPort>
                  <auPortId>5</auPortId>
                </AuPort>
				<AuPort>
                  <auPortId>6</auPortId>
                </AuPort>
			  </AntennaSubunit>
            </AntennaUnit>
          </AntennaUnitGroup>
        </Equipment>		
		<Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <AntennaUnitGroup xmlns="urn:com:ericsson:ecim:ReqAntennaSystem">
            <antennaUnitGroupId>{Radio_UnitId}</antennaUnitGroupId>
            <RfBranch>
              <rfBranchId>1</rfBranchId>
              <auPortRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},AntennaUnit=1,AntennaSubunit=1,AuPort=1</auPortRef>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <rfPortRef>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=RRU-{Radio_UnitId},RfPort=A</rfPortRef>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
            </RfBranch>	
            <RfBranch>
              <rfBranchId>2</rfBranchId>
              <auPortRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},AntennaUnit=1,AntennaSubunit=1,AuPort=2</auPortRef>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <rfPortRef>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=RRU-{Radio_UnitId},RfPort=B</rfPortRef>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
            </RfBranch>	
            <RfBranch>
              <rfBranchId>3</rfBranchId>
              <auPortRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},AntennaUnit=1,AntennaSubunit=1,AuPort=3</auPortRef>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <rfPortRef>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=RRU-{Radio_UnitId},RfPort=C</rfPortRef>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
            </RfBranch>	
            <RfBranch>
              <rfBranchId>4</rfBranchId>
              <auPortRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},AntennaUnit=1,AntennaSubunit=1,AuPort=4</auPortRef>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <rfPortRef>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=RRU-{Radio_UnitId},RfPort=D</rfPortRef>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
            </RfBranch>
            <RfBranch>
              <rfBranchId>5</rfBranchId>
              <auPortRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},AntennaUnit=1,AntennaSubunit=1,AuPort=5</auPortRef>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <rfPortRef>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=RRU-{Radio_UnitId},RfPort=E</rfPortRef>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
            </RfBranch>				

            <RfBranch>
              <rfBranchId>6</rfBranchId>
              <auPortRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},AntennaUnit=1,AntennaSubunit=1,AuPort=6</auPortRef>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <rfPortRef>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=RRU-{Radio_UnitId},RfPort=F</rfPortRef>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
            </RfBranch>							
          </AntennaUnitGroup>
		</Equipment>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>		  
          <RiLink xmlns="urn:com:ericsson:ecim:ReqRiLink">
            <riLinkId>{Radio_UnitId}</riLinkId>
            <riPortRef1>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit={fieldReplaceableUnitId},RiPort={RiPort_BB}</riPortRef1>
            <riPortRef2>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=RRU-{Radio_UnitId},RiPort={RiPort_Radio}</riPortRef2>
          </RiLink>
		</Equipment>
        <NodeSupport xmlns="urn:com:ericsson:ecim:RmeSupport">
          <nodeSupportId>1</nodeSupportId>		  
          <SectorEquipmentFunction xmlns="urn:com:ericsson:ecim:RmeSectorEquipmentFunction">
            <sectorEquipmentFunctionId>{sectorEquipmentFunctionId}</sectorEquipmentFunctionId>
            <administrativeState>LOCKED</administrativeState>
				<rfBranchRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},RfBranch=1</rfBranchRef>
				<rfBranchRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},RfBranch=2</rfBranchRef>
				<rfBranchRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},RfBranch=3</rfBranchRef>
				<rfBranchRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},RfBranch=4</rfBranchRef>
                <rfBranchRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},RfBranch=5</rfBranchRef>
				<rfBranchRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},RfBranch=6</rfBranchRef>
          </SectorEquipmentFunction>  
        </NodeSupport>
	  </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>


"""
>>>>>>> vinay_duke_work




<<<<<<< HEAD


















=======
RRU_8863_8X8 = """
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="sectorEquipmentFunctionId={sectorEquipmentFunctionId}" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>{eNodeBName}</managedElementId>
		<userLabel>{eNodeBName}</userLabel>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
		  <FieldReplaceableUnit xmlns="urn:com:ericsson:ecim:ReqFieldReplaceableUnit">
            <fieldReplaceableUnitId>RRU-{Radio_UnitId}</fieldReplaceableUnitId>
			<administrativeState>UNLOCKED</administrativeState>
			<isSharedWithExternalMe>false</isSharedWithExternalMe>			
            <RfPort xmlns="urn:com:ericsson:ecim:ReqRfPort">
              <rfPortId>A</rfPortId>
              <vswrSupervisionActive>true</vswrSupervisionActive>
              <vswrSupervisionSensitivity>100</vswrSupervisionSensitivity>
              <administrativeState>UNLOCKED</administrativeState>
              <antennaSupervisionActive>false</antennaSupervisionActive>
            </RfPort>
            <RfPort xmlns="urn:com:ericsson:ecim:ReqRfPort">
              <rfPortId>B</rfPortId>
              <vswrSupervisionActive>true</vswrSupervisionActive>
              <vswrSupervisionSensitivity>100</vswrSupervisionSensitivity>
              <administrativeState>UNLOCKED</administrativeState>
              <antennaSupervisionActive>false</antennaSupervisionActive>
            </RfPort>
            <RfPort xmlns="urn:com:ericsson:ecim:ReqRfPort">
              <rfPortId>C</rfPortId>
              <vswrSupervisionActive>true</vswrSupervisionActive>
              <vswrSupervisionSensitivity>100</vswrSupervisionSensitivity>
              <administrativeState>UNLOCKED</administrativeState>
              <antennaSupervisionActive>false</antennaSupervisionActive>
            </RfPort>
            <RfPort xmlns="urn:com:ericsson:ecim:ReqRfPort">
              <rfPortId>D</rfPortId>
              <vswrSupervisionActive>true</vswrSupervisionActive>
              <vswrSupervisionSensitivity>100</vswrSupervisionSensitivity>
              <administrativeState>UNLOCKED</administrativeState>
              <antennaSupervisionActive>false</antennaSupervisionActive>
            </RfPort>
            <RfPort xmlns="urn:com:ericsson:ecim:ReqRfPort">
              <rfPortId>E</rfPortId>
              <vswrSupervisionActive>true</vswrSupervisionActive>
              <vswrSupervisionSensitivity>100</vswrSupervisionSensitivity>
              <administrativeState>UNLOCKED</administrativeState>
              <antennaSupervisionActive>false</antennaSupervisionActive>
            </RfPort>
            <RfPort xmlns="urn:com:ericsson:ecim:ReqRfPort">
              <rfPortId>F</rfPortId>
              <vswrSupervisionActive>true</vswrSupervisionActive>
              <vswrSupervisionSensitivity>100</vswrSupervisionSensitivity>
              <administrativeState>UNLOCKED</administrativeState>
              <antennaSupervisionActive>false</antennaSupervisionActive>
            </RfPort>
            <RfPort xmlns="urn:com:ericsson:ecim:ReqRfPort">
              <rfPortId>G</rfPortId>
              <vswrSupervisionActive>true</vswrSupervisionActive>
              <vswrSupervisionSensitivity>100</vswrSupervisionSensitivity>
              <administrativeState>UNLOCKED</administrativeState>
              <antennaSupervisionActive>false</antennaSupervisionActive>
            </RfPort>
            <RfPort xmlns="urn:com:ericsson:ecim:ReqRfPort">
              <rfPortId>H</rfPortId>
              <vswrSupervisionActive>true</vswrSupervisionActive>
              <vswrSupervisionSensitivity>100</vswrSupervisionSensitivity>
              <administrativeState>UNLOCKED</administrativeState>
              <antennaSupervisionActive>false</antennaSupervisionActive>
            </RfPort>			
            <RfPort xmlns="urn:com:ericsson:ecim:ReqRfPort">
              <rfPortId>R</rfPortId>
              <vswrSupervisionActive>false</vswrSupervisionActive>
              <vswrSupervisionSensitivity>-1</vswrSupervisionSensitivity>
              <administrativeState>UNLOCKED</administrativeState>
              <antennaSupervisionActive>false</antennaSupervisionActive>
            </RfPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>DATA_1</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>DATA_2</riPortId>
            </RiPort>
          </FieldReplaceableUnit>
        </Equipment>
		
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <AntennaUnitGroup xmlns="urn:com:ericsson:ecim:ReqAntennaSystem">
            <antennaUnitGroupId>{Radio_UnitId}</antennaUnitGroupId>
          </AntennaUnitGroup>		  
        </Equipment>
		<Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <AntennaUnitGroup xmlns="urn:com:ericsson:ecim:ReqAntennaSystem">
            <antennaUnitGroupId>{Radio_UnitId}</antennaUnitGroupId>
			<AntennaUnit>
              <antennaUnitId>1</antennaUnitId>
              <mechanicalAntennaTilt>0</mechanicalAntennaTilt>
			  <AntennaSubunit>
                <antennaSubunitId>1</antennaSubunitId>  
                <maxTotalTilt>250</maxTotalTilt>
                <minTotalTilt>-250</minTotalTilt>				
				<AuPort>
                  <auPortId>1</auPortId>
                </AuPort>
				<AuPort>
                  <auPortId>2</auPortId>
                </AuPort>
				<AuPort>
                  <auPortId>3</auPortId>
                </AuPort>
				<AuPort>
                  <auPortId>4</auPortId>
                </AuPort>
                <AuPort>
                  <auPortId>5</auPortId>
                </AuPort>
				<AuPort>
                  <auPortId>6</auPortId>
                </AuPort>
				<AuPort>
                  <auPortId>7</auPortId>
                </AuPort>
				<AuPort>
                  <auPortId>8</auPortId>
                </AuPort>				
			  </AntennaSubunit>
            </AntennaUnit>
          </AntennaUnitGroup>
        </Equipment>		
		<Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <AntennaUnitGroup xmlns="urn:com:ericsson:ecim:ReqAntennaSystem">
            <antennaUnitGroupId>{Radio_UnitId}</antennaUnitGroupId>
            <RfBranch>
              <rfBranchId>1</rfBranchId>
              <auPortRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},AntennaUnit=1,AntennaSubunit=1,AuPort=1</auPortRef>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <rfPortRef>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=RRU-{Radio_UnitId},RfPort=A</rfPortRef>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
            </RfBranch>	
            <RfBranch>
              <rfBranchId>2</rfBranchId>
              <auPortRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},AntennaUnit=1,AntennaSubunit=1,AuPort=2</auPortRef>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <rfPortRef>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=RRU-{Radio_UnitId},RfPort=B</rfPortRef>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
            </RfBranch>	
            <RfBranch>
              <rfBranchId>3</rfBranchId>
              <auPortRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},AntennaUnit=1,AntennaSubunit=1,AuPort=3</auPortRef>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <rfPortRef>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=RRU-{Radio_UnitId},RfPort=C</rfPortRef>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
            </RfBranch>	
            <RfBranch>
              <rfBranchId>4</rfBranchId>
              <auPortRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},AntennaUnit=1,AntennaSubunit=1,AuPort=4</auPortRef>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <rfPortRef>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=RRU-{Radio_UnitId},RfPort=D</rfPortRef>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
            </RfBranch>
            <RfBranch>
              <rfBranchId>5</rfBranchId>
              <auPortRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},AntennaUnit=1,AntennaSubunit=1,AuPort=5</auPortRef>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <rfPortRef>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=RRU-{Radio_UnitId},RfPort=E</rfPortRef>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
            </RfBranch>				
            <RfBranch>
              <rfBranchId>6</rfBranchId>
              <auPortRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},AntennaUnit=1,AntennaSubunit=1,AuPort=6</auPortRef>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <rfPortRef>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=RRU-{Radio_UnitId},RfPort=F</rfPortRef>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
            </RfBranch>
            <RfBranch>
              <rfBranchId>7</rfBranchId>
              <auPortRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},AntennaUnit=1,AntennaSubunit=1,AuPort=7</auPortRef>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <rfPortRef>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=RRU-{Radio_UnitId},RfPort=G</rfPortRef>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
            </RfBranch>
            <RfBranch>
              <rfBranchId>8</rfBranchId>
              <auPortRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},AntennaUnit=1,AntennaSubunit=1,AuPort=8</auPortRef>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <rfPortRef>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=RRU-{Radio_UnitId},RfPort=H</rfPortRef>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
            </RfBranch>			
          </AntennaUnitGroup>
		</Equipment>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>		  
          <RiLink xmlns="urn:com:ericsson:ecim:ReqRiLink">
            <riLinkId>{Radio_UnitId}</riLinkId>
            <riPortRef1>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit={fieldReplaceableUnitId},RiPort={RiPort_BB}</riPortRef1>
            <riPortRef2>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=RRU-{Radio_UnitId},RiPort={RiPort_Radio}</riPortRef2>
          </RiLink>
		</Equipment>
        <NodeSupport xmlns="urn:com:ericsson:ecim:RmeSupport">
          <nodeSupportId>1</nodeSupportId>		  
          <SectorEquipmentFunction xmlns="urn:com:ericsson:ecim:RmeSectorEquipmentFunction">
            <sectorEquipmentFunctionId>{sectorEquipmentFunctionId}</sectorEquipmentFunctionId>
            <administrativeState>LOCKED</administrativeState>
				<rfBranchRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},RfBranch=1</rfBranchRef>
				<rfBranchRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},RfBranch=2</rfBranchRef>
				<rfBranchRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},RfBranch=3</rfBranchRef>
				<rfBranchRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},RfBranch=4</rfBranchRef>
                <rfBranchRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},RfBranch=5</rfBranchRef>
				<rfBranchRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},RfBranch=6</rfBranchRef>
				<rfBranchRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},RfBranch=7</rfBranchRef>
				<rfBranchRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},RfBranch=8</rfBranchRef>				
          </SectorEquipmentFunction>  
        </NodeSupport>
	  </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>

"""

SiteBasic_script = """ 
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="1" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>1</managedElementId>
        <dnPrefix>SubNetwork=ONRM_ROOT_MO_R,SubNetwork=LTE,MeContext={eNodeBName}</dnPrefix>
        <SystemFunctions>
          <systemFunctionsId>1</systemFunctionsId>
          <Lm xmlns="urn:com:ericsson:ecim:RcsLM">
            <lmId>1</lmId>
            <fingerprint>{eNodeBName}</fingerprint>
          </Lm>
          <SecM xmlns="urn:com:ericsson:ecim:RcsSecM">
            <secMId>1</secMId>
            <UserManagement>
              <userManagementId>1</userManagementId>
              <LdapAuthenticationMethod xmlns="urn:com:ericsson:ecim:RcsLdapAuthentication">
                <ldapAuthenticationMethodId>1</ldapAuthenticationMethodId>
                <administrativeState>UNLOCKED</administrativeState>
              </LdapAuthenticationMethod>
              <UserIdentity xmlns="urn:com:ericsson:ecim:RcsUser">
                <userIdentityId>1</userIdentityId>
                <MaintenanceUser>
                  <maintenanceUserId>1</maintenanceUserId>
                  <userName>rbs</userName>
                  <password>
                    <cleartext />
                    <password>rbs</password>
                  </password>
                </MaintenanceUser>
              </UserIdentity>
            </UserManagement>
          </SecM>
          <SysM xmlns="urn:com:ericsson:ecim:RcsSysM">
            <sysMId>1</sysMId>
            <CliTls>
              <cliTlsId>1</cliTlsId>
              <administrativeState>UNLOCKED</administrativeState>
            </CliTls>
          </SysM>
        </SystemFunctions>
        <Transport>
          <transportId>1</transportId>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTE_NR</routerId>
            <ttl>64</ttl>
          </Router>
        </Transport>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <FieldReplaceableUnit xmlns="urn:com:ericsson:ecim:ReqFieldReplaceableUnit">
            <fieldReplaceableUnitId>{fieldReplaceableUnitId}</fieldReplaceableUnitId>
            <TnPort xmlns="urn:com:ericsson:ecim:ReqTnPort">
              <tnPortId>{tnPortId}</tnPortId>
              <userLabel>{tnPortId}</userLabel>
            </TnPort>
          </FieldReplaceableUnit>
        </Equipment>
        <Transport>
          <transportId>1</transportId>
          <EthernetPort xmlns="urn:com:ericsson:ecim:RtnL2EthernetPort">
            <ethernetPortId>{tnPortId}</ethernetPortId>
            <administrativeState>UNLOCKED</administrativeState>
            <admOperatingMode>1G_FULL</admOperatingMode>
            <autoNegEnable>true</autoNegEnable>
            <encapsulation>ManagedElement=1,Equipment=1,FieldReplaceableUnit={fieldReplaceableUnitId},TnPort={tnPortId}</encapsulation>
            <userLabel>{tnPortId}</userLabel>
          </EthernetPort>
          <VlanPort xmlns="urn:com:ericsson:ecim:RtnL2VlanPort">
            <vlanPortId>LTE_NR</vlanPortId>
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>
            <isTagged>true</isTagged>
            <userLabel>LTE_NR</userLabel>
            <vlanId>{OAM_vlan}</vlanId>
          </VlanPort>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTE_NR</routerId>
            <InterfaceIPv6 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv6">
              <interfaceIPv6Id>NR</interfaceIPv6Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort=LTE_NR</encapsulation>
              <mtu>1500</mtu>
              <userLabel>NR_S1U_OAM</userLabel>
              <AddressIPv6>
                <addressIPv6Id>NR_S1U_OAM</addressIPv6Id>
                <address>{OAM_IP}</address>
                <primaryAddress>true</primaryAddress>
              </AddressIPv6>
            </InterfaceIPv6>
          </Router>
        </Transport>
        <SystemFunctions>
          <systemFunctionsId>1</systemFunctionsId>
          <SysM xmlns="urn:com:ericsson:ecim:RcsSysM">
            <sysMId>1</sysMId>
            <OamAccessPoint>
              <oamAccessPointId>1</oamAccessPointId>
              <accessPoint>ManagedElement=1,Transport=1,Router=LTE_NR,InterfaceIPv6=NR,AddressIPv6=NR_S1U_OAM</accessPoint>
            </OamAccessPoint>
            <OamTrafficClass>
              <oamTrafficClassId>1</oamTrafficClassId>
              <dscp>28</dscp>
            </OamTrafficClass>
            <Snmp xmlns="urn:com:ericsson:ecim:RcsSnmp">
              <snmpId>1</snmpId>
              <administrativeState>UNLOCKED</administrativeState>
              <agentAddress>
                <host>0.0.0.0</host>
                <port>161</port>
              </agentAddress>
              <SnmpTargetV2C>
                <snmpTargetV2CId>1</snmpTargetV2CId>
                <community>public</community>
                <address>10.142.90.203</address>
                <port>162</port>
                <administrativeState>UNLOCKED</administrativeState>
              </SnmpTargetV2C>
            </Snmp>
            <TimeM xmlns="urn:com:ericsson:ecim:RcsTimeM">
              <timeMId>1</timeMId>
              <Ntp>
                <ntpId>1</ntpId>
                <NtpServer>
                  <ntpServerId>1</ntpServerId>
                  <userLabel>NTP TOD</userLabel>
                  <serverAddress>2401:4900:00d4:1b00:0000:0000:0000:096D</serverAddress>
                  <administrativeState>UNLOCKED</administrativeState>
                </NtpServer>
                <NtpServer>
                  <ntpServerId>2</ntpServerId>
                  <userLabel>NTP TOD</userLabel>
                  <serverAddress>2401:4900:00d4:1b00:0000:0000:0000:096E</serverAddress>
                  <administrativeState>UNLOCKED</administrativeState>
                </NtpServer>
			  </Ntp>
            </TimeM>
          </SysM>
        </SystemFunctions>
        <Transport>
          <transportId>1</transportId>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>Node_Internal_F1</routerId>
            <hopLimit>64</hopLimit>
            <pathMtuExpiresIPv6>86400</pathMtuExpiresIPv6>
            <ttl>64</ttl>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTE_NR</routerId>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>LTE</interfaceIPv4Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort=LTE_NR</encapsulation>
              <mtu>1500</mtu>
              <userLabel>LTE_S1_CPUP</userLabel>
            </InterfaceIPv4>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>Node_Internal_F1</routerId>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>NR_CUCP</interfaceIPv4Id>
              <arpTimeout>300</arpTimeout>
              <bfdStaticRoutes>DISABLED</bfdStaticRoutes>
              <loopback />
              <mtu>1500</mtu>
              <pcpArp>6</pcpArp>
            </InterfaceIPv4>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>NR_DU</interfaceIPv4Id>
              <arpTimeout>300</arpTimeout>
              <bfdStaticRoutes>DISABLED</bfdStaticRoutes>
              <loopback />
              <mtu>1500</mtu>
              <pcpArp>6</pcpArp>
            </InterfaceIPv4>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTE_NR</routerId>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>LTE</interfaceIPv4Id>
              <AddressIPv4>
                <addressIPv4Id>LTE_S1_CPUP</addressIPv4Id>
                <address>{LTE_UP_IP}</address>
              </AddressIPv4>
            </InterfaceIPv4>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>Node_Internal_F1</routerId>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>NR_CUCP</interfaceIPv4Id>
              <AddressIPv4>
                <addressIPv4Id>1</addressIPv4Id>
                <address>10.0.0.1/32</address>
                <configurationMode>MANUAL</configurationMode>
                <dhcpClientIdentifierType>AUTOMATIC</dhcpClientIdentifierType>
              </AddressIPv4>
            </InterfaceIPv4>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>NR_DU</interfaceIPv4Id>
              <AddressIPv4>
                <addressIPv4Id>1</addressIPv4Id>
                <address>10.0.0.2/32</address>
                <configurationMode>MANUAL</configurationMode>
                <dhcpClientIdentifierType>AUTOMATIC</dhcpClientIdentifierType>
              </AddressIPv4>
            </InterfaceIPv4>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTE_NR</routerId>
            <InterfaceIPv6 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv6">
              <interfaceIPv6Id>NR</interfaceIPv6Id>
              <AddressIPv6>
                <addressIPv6Id>X2_ENDC</addressIPv6Id>
                <address>{NR_ENDC_IP}</address>
                <primaryAddress>false</primaryAddress>
              </AddressIPv6>
            </InterfaceIPv6>
            <RouteTableIPv4Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv4">
              <routeTableIPv4StaticId>2</routeTableIPv4StaticId>
              <Dst>
                <dstId>LTE_S1_CPUP</dstId>
                <dst>0.0.0.0/0</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
            </RouteTableIPv4Static>
            <RouteTableIPv6Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv6">
              <routeTableIPv6StaticId>2</routeTableIPv6StaticId>
              <Dst>
                <dstId>NR_S1U_OAM_X2</dstId>
                <dst>::/0</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{OAM_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
            </RouteTableIPv6Static>
          </Router>
        </Transport>
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="2" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>1</managedElementId>
        <networkManagedElementId>{eNodeBName}</networkManagedElementId>
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>

"""

site_equipment_script = """ 
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="1" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>1</managedElementId>
        <userLabel>{Phy_SiteID_Userlabel}</userLabel>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <FieldReplaceableUnit xmlns="urn:com:ericsson:ecim:ReqFieldReplaceableUnit">
            <fieldReplaceableUnitId>{fieldReplaceableUnitId}</fieldReplaceableUnitId>
            <administrativeState>UNLOCKED</administrativeState>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>A</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>B</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>C</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>D</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>E</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>F</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>G</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>H</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>J</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>K</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>L</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>M</riPortId>
            </RiPort>
            <SyncPort xmlns="urn:com:ericsson:ecim:ReqSyncPort">
              <syncPortId>1</syncPortId>
            </SyncPort>
          </FieldReplaceableUnit>
        </Equipment>
        <NodeSupport xmlns="urn:com:ericsson:ecim:RmeSupport">
          <nodeSupportId>1</nodeSupportId>
          <MpClusterHandling xmlns="urn:com:ericsson:ecim:RmeMpClusterHandling">
            <mpClusterHandlingId>1</mpClusterHandlingId>
            <primaryCoreRef>ManagedElement=1,Equipment=1,FieldReplaceableUnit={fieldReplaceableUnitId}</primaryCoreRef>
          </MpClusterHandling>
        </NodeSupport>
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>

"""


RBSSummary_script = """
<summary:AutoIntegrationRbsSummaryFile xmlns:summary="http://www.ericsson.se/RbsSummaryFileSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.ericsson.se/RbsSummaryFileSchemaSummaryFile.xsd">
  <Format revision="F" />
  <ConfigurationFiles upgradePackageFilePath="/Baseband_Radio_Node-CXP2010174_1-R50J35/" siteEquipmentFilePath="{siteEquipmentFilePath}" siteBasicFilePath="{siteBasicFilePath}" />
</summary:AutoIntegrationRbsSummaryFile>
"""
>>>>>>> vinay_duke_work
