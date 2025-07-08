################################################################ UNIVERSAL CELL DEF FOR ALL CIRCLES ######################################################################################

tdd_cell_script = """ 
###################################### L2300 CELL & CARRIER SCRIPT ######################################

crn ENodeBFunction=1,SectorCarrier={sectorCarrierId}
configuredMaxTxPower {configuredMaxTxPower}
noOfRxAntennas {noOfRxAntennas}
noOfTxAntennas {noOfTxAntennas}
sectorFunctionRef NodeSupport=1,SectorEquipmentFunction={sectorEquipmentFunctionId}
end

crn ENodeBFunction=1,EUtranCellTDD={eUtranCellFDDId}
acBarringForCsfb acBarringFactor=95,acBarringForSpecialAC=false false false false false,acBarringTime=64
acBarringForMoData acBarringFactor=95,acBarringForSpecialAC=false false false false false,acBarringTime=64
acBarringForMoSignalling acBarringFactor=95,acBarringForSpecialAC=false false false false false,acBarringTime=64
acBarringPresence acBarringForCsfbPresence=0,acBarringForMoDataPresence=0,acBarringForMoSignPresence=0
changeNotification changeNotificationSIB1=true,changeNotificationSIB15=false,changeNotificationSIB16=false,changeNotificationSIB2=true,changeNotificationSIB3=true,changeNotificationSIB4=true,changeNotificationSIB5=true,changeNotificationSIB6=true,changeNotificationSIB7=true,changeNotificationSIB8=false
mappingInfo mappingInfoSIB10=1,mappingInfoSIB3=1,mappingInfoSIB4=0,mappingInfoSIB5=3,mappingInfoSIB6=4,mappingInfoSIB7=0,mappingInfoSIB8=0
siPeriodicity siPeriodicitySI1=8,siPeriodicitySI10=64,siPeriodicitySI2=64,siPeriodicitySI3=64,siPeriodicitySI4=64,siPeriodicitySI5=64,siPeriodicitySI6=64,siPeriodicitySI7=64,siPeriodicitySI8=64,siPeriodicitySI9=64
ssacBarringForMMTELVideo acBarringFactor=95,acBarringForSpecialAC=false false false false false,acBarringTime=64
ssacBarringForMMTELVoice acBarringFactor=95,acBarringForSpecialAC=false false false false false,acBarringTime=64
systemInformationBlock3 nCellChangeHigh=16,nCellChangeMedium=16,qHyst=4,qHystSfHigh=0,qHystSfMedium=0,sIntraSearch=44,sIntraSearchP=44,sIntraSearchQ=5,sIntraSearchv920Active=false,sNonIntraSearch=10,sNonIntraSearchP=10,sNonIntraSearchQ=4,sNonIntraSearchv920Active=false,tEvaluation=240,threshServingLowQ=1000,tHystNormal=240
systemInformationBlock6 tReselectionUtra=2,tReselectionUtraSfHigh=100,tReselectionUtraSfMedium=100
systemInformationBlock7 tReselectionGeran=2,tReselectionGeranSfHigh=100,tReselectionGeranSfMedium=100
systemInformationBlock8 searchWindowSizeCdma=8,tReselectionCdma1xRtt=2,tReselectionCdma1xRttSfHigh=100,tReselectionCdma1xRttSfMedium=100,tReselectionCdmaHrpd=2,tReselectionCdmaHrpdSfHigh=100,tReselectionCdmaHrpdSfMedium=100
acBarringInfoPresent true
acBarringSkipForMmtelVideo true
acBarringSkipForMmtelVoice true
acBarringSkipForSms true
administrativeState 0
advCellSupSensitivity 65
allocThrPucchFormat1 50
allocTimerPucchFormat1 50
alpha 10
cellBarred 1
cellId {cellId}
cfraEnable true
channelBandwidth {dlChannelBandwidth}
covTriggerdBlindHoAllowed false
crsGain {crsGain}
deallocThrPucchFormat1 100
deallocTimerPucchFormat1 6000
earfcn {earfcndl}
latitude {Latitude}
longitude {Longitude}
mobCtrlAtPoorCovActive true
noOfPucchCqiUsers 640
noOfPucchSrUsers 640
pdcchCfiMode 5
pdcchCovImproveDtx false
pdcchCovImproveQci1 true
pdcchCovImproveSrb false
pdcchPowerBoostMax 0
pdschTypeBGain 0
physicalLayerCellIdGroup {physicalLayerCellIdGroup}
physicalLayerSubCellId {physicalLayerSubCellId}
pMaxServingCell 1000
preambleInitialReceivedTargetPower -110
pucchOverdimensioning 0
pZeroNominalPucch -110
pZeroNominalPusch -100
qciTableRef ENodeBFunction=1,QciTable=default
qQualMin -34
qQualMinOffset 0
qRxLevMin -124
rachRootSequence {rachRootSequence}
sectorCarrierRef ENodeBFunction=1,SectorCarrier={sectorCarrierId}
subframeAssignment 2
tac {tac}
threshServingLow 8
tTimeAlignmentTimer 0
ulInterferenceManagementActive true
userLabel {eUtranCellFDDId}
end
##############################################################################################################

"""

######################################################## FDD CELL SCRIPT ########################################################################################
fdd_cell_script = """ 
confb+
gs+

crn ENodeBFunction=1,SectorCarrier={sectorCarrierId}
configuredMaxTxPower {configuredMaxTxPower}
noOfRxAntennas {noOfRxAntennas}
noOfTxAntennas {noOfTxAntennas}
sectorFunctionRef NodeSupport=1,SectorEquipmentFunction={sectorEquipmentFunctionId}
end
#END ENodeBFunction=1,SectorCarrier={sectorCarrierId} --------------------

crn ENodeBFunction=1,EUtranCellFDD={eUtranCellFDDId}
acBarringForCsfb acBarringFactor=95,acBarringForSpecialAC=false false false false false,acBarringTime=64
acBarringForMoData acBarringFactor=95,acBarringForSpecialAC=false false false false false,acBarringTime=64
acBarringForMoSignalling acBarringFactor=95,acBarringForSpecialAC=false false false false false,acBarringTime=64
acBarringPresence acBarringForCsfbPresence=0,acBarringForMoDataPresence=0,acBarringForMoSignPresence=0
changeNotification changeNotificationSIB1=true,changeNotificationSIB15=false,changeNotificationSIB16=false,changeNotificationSIB2=true,changeNotificationSIB3=true,changeNotificationSIB4=true,changeNotificationSIB5=true,changeNotificationSIB6=true,changeNotificationSIB7=true,changeNotificationSIB8=false
frameStartOffset subFrameOffset=0
mappingInfo mappingInfoSIB10=1,mappingInfoSIB11=0,mappingInfoSIB12=7,mappingInfoSIB15=0,mappingInfoSIB16=0,mappingInfoSIB3=1,mappingInfoSIB4=2,mappingInfoSIB5=3,mappingInfoSIB6=4,mappingInfoSIB7=5,mappingInfoSIB8=0
siPeriodicity siPeriodicitySI1=8,siPeriodicitySI10=64,siPeriodicitySI2=64,siPeriodicitySI3=64,siPeriodicitySI4=64,siPeriodicitySI5=64,siPeriodicitySI6=64,siPeriodicitySI7=64,siPeriodicitySI8=64,siPeriodicitySI9=64
ssacBarringForMMTELVideo acBarringFactor=95,acBarringForSpecialAC=false false false false false,acBarringTime=64
ssacBarringForMMTELVoice acBarringFactor=95,acBarringForSpecialAC=false false false false false,acBarringTime=64
systemInformationBlock3 nCellChangeHigh=16,nCellChangeMedium=16,qHyst=4,qHystSfHigh=0,qHystSfMedium=0,sIntraSearch=44,sIntraSearchP=44,sIntraSearchQ=0,sIntraSearchv920Active=false,sNonIntraSearch=16,sNonIntraSearchP=16,sNonIntraSearchQ=0,sNonIntraSearchv920Active=false,tEvaluation=240,threshServingLowQ=1000,tHystNormal=240
systemInformationBlock6 tReselectionUtra=2,tReselectionUtraSfHigh=100,tReselectionUtraSfMedium=100
systemInformationBlock7 tReselectionGeran=2,tReselectionGeranSfHigh=100,tReselectionGeranSfMedium=100
systemInformationBlock8 searchWindowSizeCdma=8,tReselectionCdma1xRtt=2,tReselectionCdma1xRttSfHigh=100,tReselectionCdma1xRttSfMedium=100,tReselectionCdmaHrpd=2,tReselectionCdmaHrpdSfHigh=100,tReselectionCdmaHrpdSfMedium=100
administrativeState 0
alpha 8
cellId {cellId}
cfraEnable true
covTriggerdBlindHoAllowed false
crsGain {crsGain}
dlChannelBandwidth {dlChannelBandwidth}
dlInterferenceManagementActive true
drxActive true
earfcndl {earfcndl}
earfcnul {earfcnul}
latitude {Latitude}
longitude {Longitude}
mobCtrlAtPoorCovActive true
noOfPucchCqiUsers 240
noOfPucchSrUsers 350
pdcchCfiMode 5
pdcchPowerBoostMax 0
pdschTypeBGain 1
physicalLayerCellIdGroup {physicalLayerCellIdGroup}
physicalLayerSubCellId {physicalLayerSubCellId}
preambleInitialReceivedTargetPower -108
pZeroNominalPucch -110
pZeroNominalPusch -86
qQualMin -34
qRxLevMin -124
rachRootSequence {rachRootSequence}
sectorCarrierRef ENodeBFunction=1,SectorCarrier={sectorCarrierId}
tac {tac}
threshServingLow 0
ulChannelBandwidth {ulChannelBandwidth}
ulInterferenceManagementActive true
userLabel {eUtranCellFDDId}
end
#END ENodeBFunction=1,EUtranCellFDD={eUtranCellFDDId}

###########################################################################################################################

"""
############################################################################# UNIVERSAL SCRIPT FOR 5G RRU CREATION AND RBSSummary ##########################################################################

RRU_5G_CREATION = """ 
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

##################################################### UNIVERSAL RRU CONFIGRATION FOR RRU2219,RRU4412_RRU4418_RRU4427_RRU4471,RRU6626, RRU8863 #######################################################################
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

###############################################################################################################################################################################################################################













RBSSummary_script = """
<summary:AutoIntegrationRbsSummaryFile xmlns:summary="http://www.ericsson.se/RbsSummaryFileSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.ericsson.se/RbsSummaryFileSchemaSummaryFile.xsd">
  <Format revision="F" />
  <ConfigurationFiles upgradePackageFilePath="/Baseband_Radio_Node-CXP2010174_1-R50J35/" siteEquipmentFilePath="{siteEquipmentFilePath}" siteBasicFilePath="{siteBasicFilePath}" />
</summary:AutoIntegrationRbsSummaryFile>
"""



AIR_5G_GENERATION_SCRIPT = """
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


SiteEquipment_5216 = """
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
          <Cabinet xmlns="urn:com:ericsson:ecim:ReqCabinet">
            <cabinetId>1</cabinetId>
            <smokeDetector>false</smokeDetector>
            <climateSystem>STANDARD</climateSystem>
          </Cabinet>
          <FieldReplaceableUnit xmlns="urn:com:ericsson:ecim:ReqFieldReplaceableUnit">
            <fieldReplaceableUnitId>{fieldReplaceableUnitId}</fieldReplaceableUnitId>
            <administrativeState>UNLOCKED</administrativeState>
            <EcPort xmlns="urn:com:ericsson:ecim:ReqEcPort">
              <ecPortId>1</ecPortId>
              <hubPosition>A</hubPosition>
            </EcPort>
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
            <SyncPort xmlns="urn:com:ericsson:ecim:ReqSyncPort">
              <syncPortId>1</syncPortId>
            </SyncPort>
          </FieldReplaceableUnit>
        </Equipment>
        <EquipmentSupportFunction xmlns="urn:com:ericsson:ecim:ResEquipmentSupportFunction">
          <equipmentSupportFunctionId>1</equipmentSupportFunctionId>
          <supportSystemControl>true</supportSystemControl>
          <PowerDistribution xmlns="urn:com:ericsson:ecim:ResPowerDistribution">
            <powerDistributionId>1</powerDistributionId>
            <controlDomainRef>ManagedElement=1,Equipment=1,Cabinet=1</controlDomainRef>
          </PowerDistribution>
          <PowerSupply xmlns="urn:com:ericsson:ecim:ResPowerSupply">
            <powerSupplyId>1</powerSupplyId>
            <controlDomainRef>ManagedElement=1,Equipment=1,Cabinet=1</controlDomainRef>
          </PowerSupply>
        </EquipmentSupportFunction>
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
SiteEquipment_6303 = """
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
SiteEquipment_6339 = """
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
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>N</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>P</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>Q</riPortId>
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
SiteEquipment_6353 = """
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
SiteEquipment_6630 = """
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
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>N</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>P</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>Q</riPortId>
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
SiteEquipment_6631 = """
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
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>N</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>P</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>Q</riPortId>
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
SiteEquipment_6651 = """
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

SiteEquipment_6648 = """
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
SiteEquipment_R503 = """
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
    <capability>urn:com:ericsson:ebase:0.1.0</capability>
    <capability>urn:com:ericsson:ebase:1.1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="Equipment=XMU" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running/>
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>{eNodeBName}</managedElementId>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <FieldReplaceableUnit xmlns="urn:com:ericsson:ecim:ReqFieldReplaceableUnit">
            <administrativeState>UNLOCKED</administrativeState>
            <fieldReplaceableUnitId>R503</fieldReplaceableUnitId>
            <isSharedWithExternalMe>false</isSharedWithExternalMe>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>1</riPortId>
              <administrativeState>UNLOCKED</administrativeState>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>2</riPortId>
              <administrativeState>UNLOCKED</administrativeState>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>3</riPortId>
              <administrativeState>UNLOCKED</administrativeState>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>4</riPortId>
              <administrativeState>UNLOCKED</administrativeState>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>5</riPortId>
              <administrativeState>UNLOCKED</administrativeState>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>6</riPortId>
              <administrativeState>UNLOCKED</administrativeState>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>7</riPortId>
              <administrativeState>UNLOCKED</administrativeState>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>9</riPortId>
              <administrativeState>UNLOCKED</administrativeState>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>10</riPortId>
              <administrativeState>UNLOCKED</administrativeState>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>11</riPortId>
              <administrativeState>UNLOCKED</administrativeState>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>12</riPortId>
              <administrativeState>UNLOCKED</administrativeState>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>13</riPortId>
              <administrativeState>UNLOCKED</administrativeState>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>14</riPortId>
              <administrativeState>UNLOCKED</administrativeState>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>15</riPortId>
              <administrativeState>UNLOCKED</administrativeState>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>16</riPortId>
              <administrativeState>UNLOCKED</administrativeState>
            </RiPort>
          </FieldReplaceableUnit>
		  </Equipment>
		</ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session/>
</rpc>
]]>]]>


<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
    <capability>urn:com:ericsson:ebase:0.1.0</capability>
    <capability>urn:com:ericsson:ebase:1.1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="Equipment=data,NodeSupport=data" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running/>
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>{eNodeBName}</managedElementId>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <RiLink xmlns="urn:com:ericsson:ecim:ReqRiLink">
            <riLinkId>1</riLinkId>
            <riPortRef1>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=1,RiPort=A</riPortRef1>
            <riPortRef2>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=R503,RiPort=1</riPortRef2>
            <transportType>NOT_SET</transportType>
          </RiLink>
  		  </Equipment>
		</ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session/>
</rpc>
]]>]]>


<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
    <capability>urn:com:ericsson:ebase:0.1.0</capability>
    <capability>urn:com:ericsson:ebase:1.1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="Equipment=data,NodeSupport=data" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running/>
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>{eNodeBName}</managedElementId>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <RiLink xmlns="urn:com:ericsson:ecim:ReqRiLink">
            <riLinkId>2</riLinkId>
            <riPortRef1>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=1,RiPort=B</riPortRef1>
            <riPortRef2>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=R503,RiPort=2</riPortRef2>
            <transportType>NOT_SET</transportType>
          </RiLink>
  		  </Equipment>
		</ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session/>
</rpc>
]]>]]>



<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
    <capability>urn:com:ericsson:ebase:0.1.0</capability>
    <capability>urn:com:ericsson:ebase:1.1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="Equipment=data,NodeSupport=data" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running/>
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>{eNodeBName}</managedElementId>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <RiLink xmlns="urn:com:ericsson:ecim:ReqRiLink">
            <riLinkId>3</riLinkId>
            <riPortRef1>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=1,RiPort=C</riPortRef1>
            <riPortRef2>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=R503,RiPort=3</riPortRef2>
            <transportType>NOT_SET</transportType>
          </RiLink>
  		  </Equipment>
		</ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session/>
</rpc>
]]>]]>

"""


ABIS_Site_Basic_script = """
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
        <Transport>                                                                                                                                          
          <transportId>1</transportId>                                                                                                                       
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">                                                                                                 
            <routerId>ABIS</routerId>                                                                                                                        
            <ttl>64</ttl>                                                                                                                                    
          </Router>                                                                                                                                          
          <VlanPort xmlns="urn:com:ericsson:ecim:RtnL2VlanPort">                                                                                             
            <vlanPortId>{tnPortId}_ABIS</vlanPortId>                                                                                                               
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>                                                                    
            <isTagged>true</isTagged>                                                                                                                        
            <userLabel>ABIS</userLabel>                                                                                                                      
            <vlanId>{ABIS_vlan}</vlanId>                                                                                                                            
          </VlanPort>                                                                                                                                        
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">                                                                                                 
            <routerId>ABIS</routerId>                                                                                                                        
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">                                                                                 
              <interfaceIPv4Id>{tnPortId}_ABIS</interfaceIPv4Id>                                                                                                   
              <encapsulation>ManagedElement=1,Transport=1,VlanPort={tnPortId}_ABIS</encapsulation>                                                                 
              <mtu>1500</mtu>                                                                                                                                
              <userLabel>ABIS</userLabel>                                                                                                                    
              <AddressIPv4>                                                                                                                                  
                <addressIPv4Id>{tnPortId}_ABIS</addressIPv4Id>                                                                                                     
                <address>{ABIS_IP}</address>                                                                                                         
              </AddressIPv4>                                                                                                                                 
            </InterfaceIPv4>                                                                                                                                 
            <RouteTableIPv4Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv4">                                                                    
              <routeTableIPv4StaticId>4</routeTableIPv4StaticId>                                                                                             
              <Dst>                                                                                                                                          
                <dstId>BSC</dstId>                                                                                                                           
                <dst>0.0.0.0/0</dst>                                                                                                                         
                <NextHop>                                                                                                                                    
                  <nextHopId>13</nextHopId>                                                                                                                  
                  <address>{ABIS_GW}</address>                                                                                                          
                  <adminDistance>1</adminDistance>                                                                                                           
                </NextHop>                                                                                                                                   
              </Dst>                                                                                                                                         
            </RouteTableIPv4Static>                                                                                                                          
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
"""