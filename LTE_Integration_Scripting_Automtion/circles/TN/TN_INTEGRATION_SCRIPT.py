TN_s1_FOR_TN_IDL_B_PORT = """ 
                                           
gs+                                                                                                                                                                               
                                                                                                                                                                                  
crn Transport=1,SctpProfile=1                                                                                                                                                     
alphaIndex 3                                                                                                                                                                      
assocMaxRtx 8                                                                                                                                                                     
betaIndex 2                                                                                                                                                                       
bundlingActivated true                                                                                                                                                            
bundlingAdaptiveActivated true                                                                                                                                                    
bundlingTimer 0                                                                                                                                                                   
cookieLife 60                                                                                                                                                                     
dscp 46                                                                                                                                                                           
hbMaxBurst 1                                                                                                                                                                      
heartbeatActivated true                                                                                                                                                           
heartbeatInterval 2000                                                                                                                                                            
incCookieLife 30                                                                                                                                                                  
initARWnd 16384                                                                                                                                                                   
initRto 2000                                                                                                                                                                      
initialHeartbeatInterval 500                                                                                                                                                      
maxActivateThr 65535                                                                                                                                                              
maxBurst 4                                                                                                                                                                        
maxInStreams 2                                                                                                                                                                    
maxInitRt 5                                                                                                                                                                       
maxOutStreams 2                                                                                                                                                                   
maxRto 4000                                                                                                                                                                       
maxSctpPduSize 1480                                                                                                                                                               
maxShutdownRt 5                                                                                                                                                                   
minActivateThr 1                                                                                                                                                                  
minRto 1000                                                                                                                                                                       
noSwitchback true                                                                                                                                                                 
pathMaxRtx 4                                                                                                                                                                      
primaryPathAvoidance true                                                                                                                                                         
primaryPathMaxRtx 0                                                                                                                                                               
sackTimer 100                                                                                                                                                                     
thrTransmitBuffer 48                                                                                                                                                              
thrTransmitBufferCongCeased 85                                                                                                                                                    
transmitBufferSize 64                                                                                                                                                             
userLabel SCTP                                                                                                                                                                    
end                                                                                                                                                                               
gs-  

gs+

crn Transport=1,SctpEndpoint=1
dtls
dtlsNodeCredential
dtlsSctpSecurityMode 0
dtlsTrustCategory
localIpAddress Transport=1,Router=LTE_CP,InterfaceIPv4=LTE_CP,AddressIPv4=LTE_CP
portNumber 36422
sctpProfile SctpProfile=1
userLabel
end


crn Transport=1,QosProfiles=1,DscpPcpMap=1
defaultPcp 0
pcp0 0 1 2 3 4 5 6 7
pcp1 9 10 11 12 13 14 15
pcp2 16 17 18 19 20 21 22 23
pcp3 24 25 26 27 28 29 30 31
pcp4 32 33 34 35 36 37 38 39
pcp5 40 41 42 43 44 45 46 47
pcp6 48 49 50 51 52 53 54 55
pcp7 56 57 58 59 60 61 62 63
userLabel Traffic
end
#END Transport=1,QosProfiles=1,DscpPcpMap=1 --------------------

ld Transport=1,EthernetPort=TN_IDL_B
lset Transport=1,EthernetPort=TN_IDL_B$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

ld Transport=1,EthernetPort=TN_D
lset Transport=1,EthernetPort=TN_D$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

ld Transport=1,Router=OAM,InterfaceIPv4=TN_IDL_B_OAM
lset Transport=1,Router=OAM,InterfaceIPv4=TN_IDL_B_OAM$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

ld Transport=1,Router=LTEUP,InterfaceIPv4=TN_IDL_B_UP
lset Transport=1,Router=LTEUP,InterfaceIPv4=TN_IDL_B_UP$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

ld Transport=1,Router=LTECP,InterfaceIPv4=TN_IDL_B_CP
lset Transport=1,Router=LTECP,InterfaceIPv4=TN_IDL_B_CP$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

crn Transport=1,Router=LTEUP,TwampResponder=1
ipAddress Transport=1,Router=LTEUP,InterfaceIPv4=TN_IDL_B_UP,AddressIPv4=TN_IDL_B_UP
udpPort 4001
userLabel TWAMP1
end
#END Transport=1,Router=LTEUP,TwampResponder=1 --------------------

gs+

crn Transport=1,Synchronization=1,TimeSyncIO=1
compensationDelay 0
encapsulation FieldReplaceableUnit=BB-1,SyncPort=SYNC
filterTime 12
end

crn Transport=1,Synchronization=1,TimeSyncIO=1,GnssInfo=1
multipleGnssWanted 19
end

crn Transport=1,Synchronization=1,RadioEquipmentClock=1,NodeGroupSyncMember=1
administrativeState 1
selectionMode 1
syncNodePriority 1
syncRiPortCandidate Equipment=1,FieldReplaceableUnit=BB-1,RiPort=A Equipment=1,FieldReplaceableUnit=BB-1,RiPort=B Equipment=1,FieldReplaceableUnit=BB-1,RiPort=C Equipment=1,Field
ReplaceableUnit=BB-1,RiPort=D
userLabel
end

crn Equipment=1,FieldReplaceableUnit=BB-1,SyncPort=SYNC
userLabel
end
gs-

crn Transport=1,SctpEndpoint=1
localIpAddress Transport=1,Router=LTECP,InterfaceIPv4=TN_C_CP,AddressIPv4=TN_C_CP
portNumber 36422
sctpProfile Transport=1,SctpProfile=1
end
#END Transport=1,SctpEndpoint=1 --------------------

ld Transport=1,Synchronization=1 #SystemCreated
lset Transport=1,Synchronization=1$ fixedPosition true
lset Transport=1,Synchronization=1$ telecomStandard 1

crn Transport=1,Synchronization=1,RadioEquipmentClock=1
minQualityLevel qualityLevelValueOptionI=2,qualityLevelValueOptionII=2,qualityLevelValueOptionIII=1
end
#END Transport=1,Synchronization=1,RadioEquipmentClock=1 --------------------

crn Transport=1,Synchronization=1,TimeSyncIO=1
encapsulation Equipment=1,FieldReplaceableUnit=BB-1,SyncPort=1
end
#END Transport=1,Synchronization=1,TimeSyncIO=1 --------------------

crn Transport=1,Synchronization=1,RadioEquipmentClock=1,RadioEquipmentClockReference=1
adminQualityLevel qualityLevelValueOptionI=2,qualityLevelValueOptionII=2,qualityLevelValueOptionIII=1
administrativeState 1
encapsulation Transport=1,Synchronization=1,TimeSyncIO=1
priority 1
end
#END Transport=1,Synchronization=1,RadioEquipmentClock=1,RadioEquipmentClockReference=1 --------------------


gs+

crn Transport=1,Synchronization=1,RadioEquipmentClock=1,RadioEquipmentClockReference=1
adminQualityLevel qualityLevelValueOptionI=2,qualityLevelValueOptionII=2,qualityLevelValueOptionIII=1
administrativeState 1
encapsulation Synchronization=1,TimeSyncIO=1
holdOffTime 1000
priority 1
useQLFrom 1
waitToRestoreTime 60
end
gs-



confb+
gs+



crn ENodeBFunction=1
eNodeBPlmnId mcc=404,mnc=94,mncLength=2
alignTtiBundWUlTrigSinr 1
dscpLabel 46
eNBId {eNBId}

gtpuErrorIndicationDscp 46
measuringEcgiWithAgActive false
rrcConnReestActive true
s1GtpuEchoDscp 46
sctpRef Transport=1,SctpEndpoint=1
timeAndPhaseSynchAlignment true
tRelocOverall 5
tS1HoCancelTimer 3
upIpAddressRef Router=LTE_NR,InterfaceIPv4=LTE_UP,AddressIPv4=LTE_UP
x2GtpuEchoDscp 14
end
#END ENodeBFunction=1 --------------------

gs-
confb-
		 
                                           
"""
TN_s1_FOR_TN_IDLTN_C_AND_TN_E_PORT = """


confb+
gs+


crn Transport=1,QosProfiles=1,DscpPcpMap=1
defaultPcp 0
pcp0 0 1 2 3 4 5 6 7
pcp1 9 10 11 12 13 14 15
pcp2 16 17 18 19 20 21 22 23
pcp3 24 25 26 27 28 29 30 31
pcp4 32 33 34 35 36 37 38 39
pcp5 40 41 42 43 44 45 46 47
pcp6 48 49 50 51 52 53 54 55
pcp7 56 57 58 59 60 61 62 63
userLabel Traffic
end
#END Transport=1,QosProfiles=1,DscpPcpMap=1 --------------------

ld Transport=1,EthernetPort=TN_C
lset Transport=1,EthernetPort=TN_C$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

ld Transport=1,EthernetPort=TN_D
lset Transport=1,EthernetPort=TN_D$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

ld Transport=1,Router=OAM,InterfaceIPv4=TN_C_OAM
lset Transport=1,Router=OAM,InterfaceIPv4=TN_C_OAM$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

ld Transport=1,Router=LTEUP,InterfaceIPv4=TN_C_UP
lset Transport=1,Router=LTEUP,InterfaceIPv4=TN_C_UP$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

ld Transport=1,Router=LTECP,InterfaceIPv4=TN_C_CP
lset Transport=1,Router=LTECP,InterfaceIPv4=TN_C_CP$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

crn Transport=1,Router=LTEUP,TwampResponder=1
ipAddress Transport=1,Router=LTEUP,InterfaceIPv4=TN_C_UP,AddressIPv4=TN_C_UP
udpPort 4001
userLabel TWAMP1
end
#END Transport=1,Router=LTEUP,TwampResponder=1 --------------------

crn Transport=1,SctpProfile=1
alphaIndex 3
assocMaxRtx 20
betaIndex 2
bundlingActivated true
bundlingTimer 0
cookieLife 60
dscp 46
hbMaxBurst 1
heartbeatInterval 2000
incCookieLife 30
initARWnd 16384
initialHeartbeatInterval 500
initRto 2000
maxActivateThr 65535
maxBurst 4
maxInitRt 5
maxInStreams 2
maxOutStreams 2
maxRto 4000
maxSctpPduSize 1480
maxShutdownRt 5
minActivateThr 1
minRto 1000
pathMaxRtx 10
primaryPathMaxRtx 0
sackTimer 100
transmitBufferSize 64
userLabel SCTP
end
#END Transport=1,SctpProfile=1 --------------------

crn Transport=1,SctpEndpoint=1
localIpAddress Transport=1,Router=LTECP,InterfaceIPv4=TN_C_CP,AddressIPv4=TN_C_CP
portNumber 36422
sctpProfile Transport=1,SctpProfile=1
end
#END Transport=1,SctpEndpoint=1 --------------------

ld Transport=1,Synchronization=1 #SystemCreated
lset Transport=1,Synchronization=1$ fixedPosition true
lset Transport=1,Synchronization=1$ telecomStandard 1

crn Transport=1,Synchronization=1,RadioEquipmentClock=1
minQualityLevel qualityLevelValueOptionI=2,qualityLevelValueOptionII=2,qualityLevelValueOptionIII=1
end
#END Transport=1,Synchronization=1,RadioEquipmentClock=1 --------------------

crn Transport=1,Synchronization=1,TimeSyncIO=1
encapsulation Equipment=1,FieldReplaceableUnit=BB-1,SyncPort=1
end
#END Transport=1,Synchronization=1,TimeSyncIO=1 --------------------

crn Transport=1,Synchronization=1,RadioEquipmentClock=1,RadioEquipmentClockReference=1
adminQualityLevel qualityLevelValueOptionI=2,qualityLevelValueOptionII=2,qualityLevelValueOptionIII=1
administrativeState 1
encapsulation Transport=1,Synchronization=1,TimeSyncIO=1
priority 1
end
#END Transport=1,Synchronization=1,RadioEquipmentClock=1,RadioEquipmentClockReference=1 --------------------

ld Transport=1,VlanPort=TN_C_OAM
lset Transport=1,VlanPort=TN_C_OAM$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

ld Transport=1,VlanPort=TN_C_UP
lset Transport=1,VlanPort=TN_C_UP$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

ld Transport=1,VlanPort=TN_C_CP
lset Transport=1,VlanPort=TN_C_CP$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

ld Transport=1,VlanPort=TN_C_ABIS
lset Transport=1,VlanPort=TN_C_ABIS$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

ld Transport=1,VlanPort=TN_D_OAM
lset Transport=1,VlanPort=TN_D_OAM$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

ld Transport=1,VlanPort=TN_D_UP
lset Transport=1,VlanPort=TN_D_UP$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

ld Transport=1,VlanPort=TN_D_CP
lset Transport=1,VlanPort=TN_D_CP$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

ld Transport=1,VlanPort=TN_D_ABIS
lset Transport=1,VlanPort=TN_D_ABIS$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

gs-
confb-


confb+
gs+



crn ENodeBFunction=1
eNodeBPlmnId mcc=404,mnc=94,mncLength=2
alignTtiBundWUlTrigSinr 1
dscpLabel 46
eNBId 765887

gtpuErrorIndicationDscp 46
measuringEcgiWithAgActive false
rrcConnReestActive true
s1GtpuEchoDscp 46
sctpRef Transport=1,SctpEndpoint=1
timeAndPhaseSynchAlignment true
tRelocOverall 5
tS1HoCancelTimer 3
upIpAddressRef Transport=1,Router=LTEUP,InterfaceIPv4=TN_C_UP,AddressIPv4=TN_C_UP
x2GtpuEchoDscp 14
end
#END ENodeBFunction=1 --------------------

gs-
confb-

"""


TN_s3_LTE_GPL_LMS = """

lt all
rbs
rbs


Confbd+
gs+

get Router=OAM,RouteTableIPv.*Static=.*,Dst=.*,NextHop= address$ > $OAM-Nexthop
get Router=LTEUP,RouteTableIPv4Static=.*,Dst=.*,NextHop= address$ > $UP-Nexthop
get Router=LTECP,RouteTableIPv4Static=.*,Dst=.*,NextHop= address$ > $CP-Nexthop


rdel Router=LTEUP,RouteTableIPv4Static=2,Dst=

rdel Router=LTECP,RouteTableIPv4Static=3,Dst=






crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=OSS3
dst 10.45.86.0/23
end

crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=OSS3,NextHop=1
address $OAM-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference
end

crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=OSS1
dst 10.45.60.0/24
end

crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=OSS1,NextHop=1
address $OAM-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference
end

crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=OSS
dst 10.45.25.0/24
end

crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=OSS,NextHop=1
address $OAM-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference
end

crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=OSS-New
dst 100.74.16.0/20
end

crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=OSS-New,NextHop=1
address $OAM-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference
end

crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM1
dst 10.19.105.0/22
end

crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM1,NextHop=1
address $OAM-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference
end


crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM
dst 10.19.104.0/22
end

crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM,NextHop=1
address $OAM-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference
end

crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM2
dst 10.19.108.0/22
end

crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM2,NextHop=1
address $OAM-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference
end

crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM2_Raj
dst 10.19.109.0/24
end

crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM2_Raj,NextHop=1
address $OAM-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference
end

crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM3
dst 10.19.186.0/24
end

crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM3,NextHop=1
address $OAM-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference
end

crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM3_Raj
dst 10.19.186.0/25
end

crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM3_Raj,NextHop=1
address $OAM-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference
end

crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM4
dst 10.19.182.0/24
end

crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM4,NextHop=1
address $OAM-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference
end

crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM4_Raj
dst 10.19.182.0/25
end

crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM4_Raj,NextHop=1
address $OAM-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_95
dst 100.86.0.0/20
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_95,NextHop=8
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_94
dst 100.85.128.0/20
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_94,NextHop=94
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_93
dst 100.84.64.0/20
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_93,NextHop=4
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_92
dst 100.84.96.0/20
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_92,NextHop=8
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_82
dst 100.84.0.0/20
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_82,NextHop=82
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_77
dst 100.83.208.0/20
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_77,NextHop=77
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_76
dst 100.83.192.0/20
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_76,NextHop=76
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_75
dst 100.81.56.0/21
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_75,NextHop=75
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_73
dst 100.81.16.0/20
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_73,NextHop=73
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_71
dst 10.97.90.0/23
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_71,NextHop=71
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_67
dst 100.87.64.0/20
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_67,NextHop=67
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_66
dst 100.86.192.0/20
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_66,NextHop=66
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_59
dst 100.88.160.0/20
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_59,NextHop=2
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_57
dst 100.88.96.0/20
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_57,NextHop=2
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_5
dst 10.72.16.0/20
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_5,NextHop=15
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_43
dst 100.87.192.0/20
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_43,NextHop=43
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_32
dst 10.80.136.0/21
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_32,NextHop=41
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_31
dst 10.80.160.0/21
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_31,NextHop=41
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_30
dst 10.72.56.0/21
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_30,NextHop=41
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_28
dst 10.72.48.0/21
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_28,NextHop=41
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_26
dst 10.29.112.0/20
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_26,NextHop=41
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_25
dst 10.29.80.0/20
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_25,NextHop=41
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_23
dst 10.29.24.0/21
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_23,NextHop=41
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_22
dst 10.29.8.0/21
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_22,NextHop=41
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_2
dst 10.29.56.0/21
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_2,NextHop=8
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_1
dst 10.29.40.0/21
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2_1,NextHop=4
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=Twamp
dst 10.61.96.208/28
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=Twamp,NextHop=7
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW9
dst 10.61.86.248/29
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW9,NextHop=13
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW8
dst 10.75.212.142/32
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW8,NextHop=1
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW7
dst 10.75.212.27/32
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW7,NextHop=11
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW6
dst 10.206.17.12/32
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW6,NextHop=11
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW5
dst 10.50.98.17/32
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW5,NextHop=44
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW4
dst 10.50.98.5/32
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW4,NextHop=4
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW3
dst 10.40.18.96/28
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW3,NextHop=31
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW2
dst 10.206.32.65/32
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW2,NextHop=11
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW18
dst 10.19.207.133/32
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW18,NextHop=2
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW17
dst 10.1.253.189/32
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW17,NextHop=2
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW16
dst 10.1.170.192/32
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW16,NextHop=2
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW15
dst 10.19.187.133/32
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW15,NextHop=15
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW14
dst 10.19.131.245/32
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW14,NextHop=14
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW13
dst 10.19.131.229/32
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW13,NextHop=13
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW12
dst 10.19.131.213/32
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW12,NextHop=12
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW11
dst 10.1.131.250/32
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW11,NextHop=11
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW10
dst 10.92.7.118/32
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW10,NextHop=10
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW1
dst 10.206.0.0/19
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW1,NextHop=2
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SBRUP
dst 0.0.0.0/0
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SBRUP,NextHop=2
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=CUPGW
dst 10.1.159.128/27
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=CUPGW,NextHop=17
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_new_3
dst 100.83.208.0/20
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_new_3,NextHop=7
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_92
dst 100.86.16.0/20
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_92,NextHop=93
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_91
dst 100.84.80.0/20
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_91,NextHop=2
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_90
dst 100.84.112.0/20
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_90,NextHop=2
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_84
dst 100.84.16.0/20
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_84,NextHop=84
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_80
dst 100.85.144.0/20
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_80,NextHop=81
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_76
dst 100.83.192.0/20
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_76,NextHop=76
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_74
dst 100.81.48.0/21
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_74,NextHop=74
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_72
dst 100.81.0.0/20
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_72,NextHop=72
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_70
dst 10.97.88.0/23
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_70,NextHop=70
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_7
dst 10.29.96.0/20
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_7,NextHop=15
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_69
dst 100.88.176.0/20
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_69,NextHop=3
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_68
dst 100.87.80.0/20
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_68,NextHop=68
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_65
dst 100.86.208.0/20
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_65,NextHop=65
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_62
dst 10.29.32.0/21
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_62,NextHop=62
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_61
dst 10.29.64.0/20
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_61,NextHop=61
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_58
dst 100.88.112.0/20
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_58,NextHop=3
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_5
dst 10.72.0.0/20
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_5,NextHop=17
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_44
dst 100.87.208.0/20
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_44,NextHop=44
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_4
dst 10.0.235.0/24
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_4,NextHop=9
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_3
dst 10.206.32.0/24
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_3,NextHop=7
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_20
dst 10.80.128.0/21
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_20,NextHop=40
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_2
dst 10.29.48.0/21
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_2,NextHop=15
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_19
dst 10.80.152.0/21
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_19,NextHop=40
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_18
dst 10.72.40.0/21
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_18,NextHop=40
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_16
dst 10.72.32.0/21
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_16,NextHop=40
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_11
dst 10.29.16.0/21
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_11,NextHop=40
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_10
dst 10.29.0.0/21
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2_10,NextHop=40
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=SBRCP
dst 0.0.0.0/0
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=SBRCP,NextHop=2
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=RNC
dst 10.163.190.0/24
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=RNC,NextHop=6
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=MME9
dst 10.1.163.144/32
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=MME9,NextHop=20
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=MME8
dst 10.92.7.0/24
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=MME8,NextHop=20
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=MME7
dst 10.75.212.0/24
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=MME7,NextHop=20
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=MME6
dst 10.61.0.0/24
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=MME6,NextHop=20
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=MME3
dst 10.206.27.0/24
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=MME3,NextHop=30
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=MME2
dst 10.206.20.0/24
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=MME2,NextHop=5
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=MME1
dst 10.206.4.0/24
end

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=MME1,NextHop=3
address $CP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference 
end
gs-

cvms After_Routeaddd


Confbd-
gs-



lt all
rbs
rbs
confbd+
gs+

$date = `date +%y%m%d_%H%M`
cvms GPL_UpdatedLP_$date

rdel =38950
rdel =39250
rdel =10807
rdel =10782
rdel =539

###########
unset all

$Par[1] = L2100
$Par[2] = TDD20
$Par[3] = L1800
$Par[4] = L900
$Par[5] = TDD10
$Par[6] = TDD30
$Par[7] = TDD40

mr L2100
mr TDD20
mr L1800
mr L900
mr TDD10
mr TDD30
mr TDD40

ma L2100 EUtranCellFDD earfcn 515
ma TDD20 EUtranCellTDD earfcn 39150
ma L1800 EUtranCellFDD earfcn 1576
ma L900 EUtranCellFDD earfcn 3601
ma TDD10 EUtranCellTDD earfcn 39151
ma TDD30 EUtranCellTDD earfcn 39348
ma TDD40 EUtranCellTDD earfcn 39349

############################ FREQ Creation###########

cr ENodeBFunction=1,GeraNetwork=1

cr ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
1 #frequencyGroupId

cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39150
39150
0
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3601
3601
0
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1576
1576
0
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=515
515
0
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39151
39151
0

cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39348
39348
0

cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39349
39349
0

func Gran_rahul
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=$t
$t
0
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=$t geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
endfunc

for $t = 1 to 6
Gran_rahul
done


crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=30
arfcnValueGeranDl 30
bandIndicator 0
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
userLabel
end


lt all

################## Frequency Relation##########

func Gran_Rel
for $mo in $Par[$i]
 $mordn = rdn($mo)
 pr $mordn,GeranFreqGroupRelation=1
 if $nr_of_mos = 0
  cr ENodeBFunction=1,$mordn,GeranFreqGroupRelation=1
  ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
  1
 fi 
done
endfunc

func EURel_39150
for $mo in $Par[$i]
 $mordn = rdn($mo)
 pr $mordn,EUtranFreqRelation=39150
 if $nr_of_mos = 0
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=39150 
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39150
  7
 fi 
done
endfunc

func EURel_39151
for $mo in $Par[$i]
 $mordn = rdn($mo)
 pr $mordn,EUtranFreqRelation=39151
 if $nr_of_mos = 0
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=39151
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39151
  6
 fi 
done
endfunc

func EURel_39348
for $mo in $Par[$i]
 $mordn = rdn($mo)
 pr $mordn,EUtranFreqRelation=39348
 if $nr_of_mos = 0
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=39348
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39348
  7
 fi 
done
endfunc

func EURel_39349
for $mo in $Par[$i]
 $mordn = rdn($mo)
 pr $mordn,EUtranFreqRelation=39349
 if $nr_of_mos = 0
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=39349
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39349
  6
 fi 
done
endfunc

func EURel_515
for $mo in $Par[$i]
 $mordn = rdn($mo)
 pr $mordn,EUtranFreqRelation=515
 if $nr_of_mos = 0
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=515 
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=515
  5
 fi 
done
endfunc

func EURel_1576
for $mo in $Par[$i]
 $mordn = rdn($mo)
 pr $mordn,EUtranFreqRelation=1576
 if $nr_of_mos = 0
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=1576
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1576
  4
 fi 
done
endfunc

func EURel_3601
for $mo in $Par[$i]
 $mordn = rdn($mo)
 pr $mordn,EUtranFreqRelation=3601
 if $nr_of_mos = 0
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=3601
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3601
  3
 fi 
done
endfunc

 
for $i = 1 to 7
EURel_39150
EURel_39151
EURel_39348
EURel_39349
EURel_515
EURel_1576
EURel_3601
Gran_Rel
done



crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=30
arfcnValueGeranDl 30
bandIndicator 0
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
userLabel
end


######################

##########################GNSS MO##############

cr Transport=1,Synchronization=1,TimeSyncIO=1,GnssInfo=1
########################################


############################ Node Level Parameters #######################

########### ENodeBFunction ##################

set ENodeBFunction=1 alignTtiBundWUlTrigSinr 1
set ENodeBFunction=1 dscpLabel 46
set ENodeBFunction=1 rrcConnReestActive 1
set ENodeBFunction=1 tRelocOverall 20
set ENodeBFunction=1 tS1HoCancelTimer 3
set ENodeBFunction=1 enabledUlTrigMeas true
set ENodeBFunction=1 zzzTemporary52 1
set ENodeBFunction=1 x2GtpuEchoDscp 46
set ENodeBFunction=1 s1GtpuEchoDscp 46
set ENodeBFunction=1 x2SetupTwoWayRelations true
set ENodeBFunction=1 csfbMeasFromIdleMode true
set ENodeBFunction=1 dnsLookupOnTai 1
set ENodeBFunction=1 zzzTemporary13 -2000000000
set ENodeBFunction=1 caAwareMfbiIntraCellHo false
set ENodeBFunction=1 mfbiSupportPolicy false
set ENodeBFunction=1 s1HODirDataPathAvail true
set ENodeBFunction=1 gtpuErrorIndicationDscp 46
set ENodeBFunction=1 timePhaseMaxDeviationIeNbCa 30
set ENodeBFunction=1 s1GtpuEchoEnable  0
set ENodeBFunction=1 checkEmergencySoftLock false
set ENodeBFunction=1 combCellSectorSelectThreshRx 300
set ENodeBFunction=1 combCellSectorSelectThreshTx 300
set ENodeBFunction=1 licConnectedUsersPercentileConf 90
set ENodeBFunction=1 tddVoipDrxProfileId -1
set ENodeBFunction=1 timePhaseMaxDeviation 100
set ENodeBFunction=1 timePhaseMaxDeviationEdrx 10
set ENodeBFunction=1 timePhaseMaxDeviationMbms 50
set ENodeBFunction=1 timePhaseMaxDeviationOtdoa 9
set ENodeBFunction=1 timePhaseMaxDeviationSib16 100
set ENodeBFunction=1 timePhaseMaxDeviationTdd 15
set ENodeBFunction=1 timePhaseMaxDeviationTdd1 15
set ENodeBFunction=1 timePhaseMaxDeviationTdd2 15
set ENodeBFunction=1 timePhaseMaxDeviationTdd3 15
set ENodeBFunction=1 timePhaseMaxDeviationTdd4 15
set ENodeBFunction=1 timePhaseMaxDeviationTdd5 15
set ENodeBFunction=1 timePhaseMaxDeviationTdd6 15
set ENodeBFunction=1 timePhaseMaxDeviationTdd7 15
set ENodeBFunction=1 timePhaseMaxDevIeNBUlComp 30
set ENodeBFunction=1 ulMaxWaitingTimeGlobal 0
set ENodeBFunction=1 ulSchedulerDynamicBWAllocationEnabled true
set ENodeBFunction=1 useBandPrioritiesInSCellEval false
set ENodeBFunction=1 x2GtpuEchoEnable  0
set ENodeBFunction=1 x2IpAddrViaS1Active true
set ENodeBFunction=1 x2retryTimerMaxAuto 1440
set ENodeBFunction=1 timeAndPhaseSynchAlignment true
set ENodeBFunction=1 timeAndPhaseSynchCritical false
set ENodeBFunction=1,SecurityHandling=1 securityHandlingId 1
set ENodeBFunction=1 csmMinHighHitThreshold 50
set ENodeBFunction=1,RadioBearerTable=default,MACConfiguration=1$ ulMaxHARQTx 5
set ENodeBFunction=1,AdmissionControl=1$ dlAdmDifferentiationThr 750
set ENodeBFunction=1,AdmissionControl=1$ ulAdmDifferentiationThr 750
set ENodeBFunction=1$ enabledUlTrigMeas true
set ENodeBFunction=1$ s1HODirDataPathAvail true
set AutoCellCapEstFunction=1$ useEstimatedCellCap true
set ENodeBFunction=1,AnrFunction=1,AnrFunctionGeran=1$ anrStateGsm 1

################  QciProfilePredefined ########################

set QciTable=default,QciProfilePredefined=QCI1$ absPrioOverride 0
set QciTable=default,QciProfilePredefined=QCI2$ absPrioOverride 0
set QciTable=default,QciProfilePredefined=QCI5$ absPrioOverride 1
set QciTable=default,QciProfilePredefined=QCI1$ aqmMode 2
set QciTable=default,QciProfilePredefined=QCI2$ aqmMode 2
set QciTable=default,QciProfilePredefined=QCI5$ aqmMode 0
set QciTable=default,QciProfilePredefined=qci6$ counterActiveMode false
set QciTable=default,QciProfilePredefined=qci8$ counterActiveMode false
set QciTable=default,QciProfilePredefined=qci9$ counterActiveMode false
set QciTable=default,QciProfilePredefined=qci2$ counterActiveMode false
set QciTable=default,QciProfilePredefined=qci5$ counterActiveMode false
set QciTable=default,QciProfilePredefined=qci6$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci8$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci9$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci7$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=QCI1$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=QCI2$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=QCI5$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci1$ dlMaxHARQTxQci 7
set QciTable=default,QciProfilePredefined=QCI2$ dlMinBitRate 384
set QciTable=default,QciProfilePredefined=QCI1$ dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=QCI2$ dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=QCI5$ dlResourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=QCI6$ dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=QCI8$ dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=QCI9$ dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci1$ drxPriority 99
set QciTable=default,QciProfilePredefined=qci2$ drxPriority 100
set QciTable=default,QciProfilePredefined=qci3$ drxPriority 0
set QciTable=default,QciProfilePredefined=qci5$ drxPriority 1
set QciTable=default,QciProfilePredefined=qci1$ drxProfileRef DrxProfile=1
set QciTable=default,QciProfilePredefined=qci2$ drxProfileRef DrxProfile=2
set QciTable=default,QciProfilePredefined=qci5$ drxProfileRef DrxProfile=0
set QciTable=default,QciProfilePredefined=QCI6$ dscp 32
set QciTable=default,QciProfilePredefined=QCI7$ dscp 40
set QciTable=default,QciProfilePredefined=QCI8$ dscp 30
set QciTable=default,QciProfilePredefined=QCI9$ dscp 26
set QciTable=default,QciProfilePredefined=QCI1$ dscp 34
set QciTable=default,QciProfilePredefined=QCI2$ dscp 34
set QciTable=default,QciProfilePredefined=QCI5$ dscp 46
set QciTable=default,QciProfilePredefined=qci1$ harqPriority 1
set QciTable=default,QciProfilePredefined=QCI1$ inactivityTimerOffset 30
set QciTable=default,QciProfilePredefined=QCI2$ inactivityTimerOffset 30
set QciTable=default,QciProfilePredefined=QCI5$ inactivityTimerOffset 0
set QciTable=default,QciProfilePredefined=qci1$ logicalChannelGroupRef QciTable=default,LogicalChannelGroup=1
set QciTable=default,QciProfilePredefined=qci2$ logicalChannelGroupRef QciTable=default,LogicalChannelGroup=2
set QciTable=default,QciProfilePredefined=qci5$ logicalChannelGroupRef QciTable=default,LogicalChannelGroup=1
set QciTable=default,QciProfilePredefined=qci6$ logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set QciTable=default,QciProfilePredefined=qci7$ logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set QciTable=default,QciProfilePredefined=qci8$ logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set QciTable=default,QciProfilePredefined=qci9$ logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set QciTable=default,QciProfilePredefined=QCI1$ Pdb 80
set QciTable=default,QciProfilePredefined=QCI2$ Pdb 150
set QciTable=default,QciProfilePredefined=QCI5$ Pdb 100
set QciTable=default,QciProfilePredefined=QCI1$ PdbOffset 100
set QciTable=default,QciProfilePredefined=QCI2$ PdbOffset 50
set QciTable=default,QciProfilePredefined=QCI5$ PdbOffset 0
set QciTable=default,QciProfilePredefined=QCI1$ pdcpSNLength 12
set QciTable=default,QciProfilePredefined=QCI2$ pdcpSNLength 12
set QciTable=default,QciProfilePredefined=QCI5$ pdcpSNLength 12
set QciTable=default,QciProfilePredefined=QCI1$ Priority 1
set QciTable=default,QciProfilePredefined=QCI2$ Priority 4
set QciTable=default,QciProfilePredefined=QCI5$ Priority 2
set QciTable=default,QciProfilePredefined=qci1$ resourceType 1
set QciTable=default,QciProfilePredefined=qci2$ resourceType 1
set QciTable=default,QciProfilePredefined=qci5$ resourceType 0
set QciTable=default,QciProfilePredefined=QCI1$ rlcMode 1
set QciTable=default,QciProfilePredefined=QCI2$ rlcMode 1
set QciTable=default,QciProfilePredefined=QCI5$ rlcMode 0
set QciTable=default,QciProfilePredefined=QCI1$ rlcSNLength 10
set QciTable=default,QciProfilePredefined=QCI2$ rlcSNLength 10
set QciTable=default,QciProfilePredefined=QCI5$ rlcSNLength 10
set QciTable=default,QciProfilePredefined=QCI1$ rlfPriority 10
set QciTable=default,QciProfilePredefined=QCI1$ rohcEnabled TRUE
set QciTable=default,QciProfilePredefined=QCI2$ rohcEnabled FALSE
set QciTable=default,QciProfilePredefined=QCI5$ rohcEnabled FALSE
set QciTable=default,QciProfilePredefined=QCI1$ schedulingAlgorithm 6
set QciTable=default,QciProfilePredefined=QCI2$ schedulingAlgorithm 3
set QciTable=default,QciProfilePredefined=QCI5$ schedulingAlgorithm 0
set QciTable=default,QciProfilePredefined=QCI6$ schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=QCI7$ schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=QCI8$ schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=QCI9$ schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=QCI1$ serviceType 1
set QciTable=default,QciProfilePredefined=QCI2$ serviceType 0
set QciTable=default,QciProfilePredefined=QCI5$ serviceType 2
set QciTable=default,QciProfilePredefined=qci1$ tReorderingDl 120
set QciTable=default,QciProfilePredefined=qci1$ ulMaxHARQTxQci 7
set QciTable=default,QciProfilePredefined=QCI2$ UlMinBitRate 384
set QciTable=default,QciProfilePredefined=qci1$ tReorderingUl 50
set RadioBearerTable=default,SignalingRadioBearer=1 tReorderingUl 35
set QciTable=default,QciProfilePredefined=qci6$ dscp$ 32
set QciTable=default,QciProfilePredefined=qci7$ dscp$ 26
set QciTable=default,QciProfilePredefined=qci8$ dscp$ 26
set QciTable=default,QciProfilePredefined=qci9$ dscp$ 26
set QciTable=default,QciProfilePredefined=QCI6$ absPrioOverride 0
set QciTable=default,QciProfilePredefined=QCI7$ absPrioOverride 0
set QciTable=default,QciProfilePredefined=QCI8$ absPrioOverride 0
set QciTable=default,QciProfilePredefined=QCI9$ absPrioOverride 0
set QciTable=default,QciProfilePredefined=QCI6$ schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=QCI7$ schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=QCI8$ schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=QCI9$ schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=qci1$ qciSubscriptionQuanta 60
set QciTable=default,QciProfilePredefined=qci2$ qciSubscriptionQuanta 384
set QciTable=default,QciProfilePredefined=qci5$ qciSubscriptionQuanta 1
set QciTable=default,QciProfilePredefined=qci6$ qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci7$ qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci8$ qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci9$ qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci1 measReportConfigParams a1ThresholdRsrpPrimOffset=14
set QciTable=default,QciProfilePredefined=qci1 measReportConfigParams a2ThresholdRsrpPrimOffset=2
set QciTable=default,QciProfilePredefined=qci1 measReportConfigParams a5Threshold1RsrpOffset=2
set QciTable=default,QciProfilePredefined=qci1 measReportConfigParams a5Threshold2RsrpOffset=2
set QciTable=default,QciProfilePredefined=qci1 measReportConfigParams b2Threshold1RsrpUtraOffset=2
set QciTable=default,QciProfilePredefined=qci6$ resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci7$ resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci8$ resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci9$ resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=default bitRateRecommendationEnabled true
set QciTable=default,QciProfilePredefined=qci1    bitRateRecommendationEnabled true
set QciTable=default,QciProfilePredefined=qci2    bitRateRecommendationEnabled true
set QciTable=default,QciProfilePredefined=qci3    bitRateRecommendationEnabled true
set QciTable=default,QciProfilePredefined=qci4    bitRateRecommendationEnabled true
set QciTable=default,QciProfilePredefined=qci5    bitRateRecommendationEnabled true
set QciTable=default,QciProfilePredefined=qci6    bitRateRecommendationEnabled true
set QciTable=default,QciProfilePredefined=qci65   bitRateRecommendationEnabled true
set QciTable=default,QciProfilePredefined=qci66   bitRateRecommendationEnabled true
set QciTable=default,QciProfilePredefined=qci69   bitRateRecommendationEnabled true
set QciTable=default,QciProfilePredefined=qci7    bitRateRecommendationEnabled true
set QciTable=default,QciProfilePredefined=qci70   bitRateRecommendationEnabled true
set QciTable=default,QciProfilePredefined=qci8    bitRateRecommendationEnabled true
set QciTable=default,QciProfilePredefined=qci9    bitRateRecommendationEnabled true
set QciTable=default,QciProfilePredefined=qci1$ qciSubscriptionQuanta 60
set QciTable=default,QciProfilePredefined=qci2$ qciSubscriptionQuanta 384
set QciTable=default,QciProfilePredefined=qci6$ qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci7$ qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci8$ qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci9$ qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=default$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci1$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci2$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci3$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci4$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci5$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci6$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci7$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci8$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci9$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci1$ dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci2$ dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci1$ schedulingAlgorithm 6
set QciTable=default,QciProfilePredefined=qci2$ schedulingAlgorithm 3
set QciTable=default,QciProfilePredefined=qci6$ schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=qci8$ schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=qci9$ schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=qci1$ serviceType 1
set QciTable=default,QciProfilePredefined=qci1$ drxPriority 99
set QciTable=default,QciProfilePredefined=qci1$ dscp 34
set QciTable=default,QciProfilePredefined=qci1$ inactivityTimerOffset 30
set QciTable=default,QciProfilePredefined=qci1$ pdb 80
set QciTable=default,QciProfilePredefined=qci1$ pdbOffset 100
set QciTable=default,QciProfilePredefined=qci1$ priority 1
set QciTable=default,QciProfilePredefined=qci1$ rlcMode 1
set QciTable=default,QciProfilePredefined=qci1$ rlfPriority 10
set QciTable=default,QciProfilePredefined=qci1$ rohcEnabled true
set QciTable=default,QciProfilePredefined=qci1$ tReorderingDl 120
set QciTable=default,QciProfilePredefined=qci1$ tReorderingUl 50
set QciTable=default,QciProfilePredefined=qci2$ dlMinBitRate 384
set QciTable=default,QciProfilePredefined=qci2$ drxPriority 100
set QciTable=default,QciProfilePredefined=qci2$ dscp 34
set QciTable=default,QciProfilePredefined=qci2$ inactivityTimerOffset 30
set QciTable=default,QciProfilePredefined=qci2$ pdbOffset 50
set QciTable=default,QciProfilePredefined=qci2$ rlcMode 1
set QciTable=default,QciProfilePredefined=qci2$ ulMinBitRate 384
set QciTable=default,QciProfilePredefined=qci5$ drxPriority 1
set QciTable=default,QciProfilePredefined=qci5$ dscp 46
set QciTable=default,QciProfilePredefined=qci5$ priority 2
set QciTable=default,QciProfilePredefined=qci1$ resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci2$ resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci3$ resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci4$ resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci5$ resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci6$ resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci7$ resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci3$ schedulingAlgorithm 0
set QciTable=default,QciProfilePredefined=qci4$ schedulingAlgorithm 0


################ SCTP ####################

set Transport=1,SctpProfile=1 assocMaxRtx 20
set Transport=1,SctpProfile=1 heartbeatInterval 2000
set Transport=1,SctpProfile=1 initRto 2000
set Transport=1,SctpProfile=1 maxRto 4000
set Transport=1,SctpProfile=1 maxInStreams 2
set Transport=1,SctpProfile=1 maxInitRt 5
set Transport=1,SctpProfile=1 maxOutStreams 2
set Transport=1,SctpProfile=1 transmitBufferSize 64
set Transport=1,SctpProfile=1 minRto 1000
set Transport=1,SctpProfile=1 pathMaxRtx 10
set Transport=1,SctpProfile=1 hbMaxBurst 1
set Transport=1,SctpProfile=1 maxSctpPduSize 1480

##########  DRX Profile ##############

lset ENodeBFunction=1,DrxProfile=1$ drxInactivityTimer 6
lset ENodeBFunction=1,DrxProfile=2$ drxInactivityTimer 6
lset ENodeBFunction=1,DrxProfile=0$ drxInactivityTimer 14
lset ENodeBFunction=1,DrxProfile=1$ drxRetransmissionTimer 2
lset ENodeBFunction=1,DrxProfile=2$ drxRetransmissionTimer 1
lset ENodeBFunction=1,DrxProfile=0$ drxRetransmissionTimer 4
lset ENodeBFunction=1,DrxProfile=1$ longDrxCycle 3
lset ENodeBFunction=1,DrxProfile=2$ longDrxCycle 3
lset ENodeBFunction=1,DrxProfile=0$ longDrxCycle 9
lset ENodeBFunction=1,DrxProfile=1$ longDrxCycleonly 3
lset ENodeBFunction=1,DrxProfile=2$ longDrxCycleonly 3
lset ENodeBFunction=1,DrxProfile=0$ longDrxCycleonly 9
lset ENodeBFunction=1,DrxProfile=1$ onDurationTimer 7
lset ENodeBFunction=1,DrxProfile=2$ onDurationTimer 6
lset ENodeBFunction=1,DrxProfile=0$ onDurationTimer 7
lset ENodeBFunction=1,DrxProfile=1$ shortDrxCycle 7
lset ENodeBFunction=1,DrxProfile=2$ shortDrxCycle 7
lset ENodeBFunction=1,DrxProfile=0$ shortDrxCycle 9
lset ENodeBFunction=1,DrxProfile=1$ shortDrxCycleTimer 0
lset ENodeBFunction=1,DrxProfile=2$ shortDrxCycleTimer 0
lset ENodeBFunction=1,DrxProfile=0$ shortDrxCycleTimer 1
lset ENodeBFunction=1,DrxProfile=1$ drxState 1
set AnrPciConflictDrxProfile=1 anrPciConflictDrxInactivityTimer 8
set AnrPciConflictDrxProfile=1 anrPciConflictOnDurationTimer 4
set ENodeBFunction=1,DrxProfile=0$ drxInactivityTimer 14
set ENodeBFunction=1,DrxProfile=1$ drxInactivityTimer 6
set ENodeBFunction=1,DrxProfile=2$ drxInactivityTimer 6
set ENodeBFunction=1,DrxProfile=0$ drxRetransmissionTimer 4
set ENodeBFunction=1,DrxProfile=1$ drxRetransmissionTimer 2
set ENodeBFunction=1,DrxProfile=1$ drxState 0
set ENodeBFunction=1,DrxProfile=1$ longDrxCycle 3
set ENodeBFunction=1,DrxProfile=2$ longDrxCycle 3
set ENodeBFunction=1,DrxProfile=0$ longDrxCycleOnly 9
set ENodeBFunction=1,DrxProfile=1$ longDrxCycleOnly 3
set ENodeBFunction=1,DrxProfile=2$ longDrxCycleOnly 3
set ENodeBFunction=1,DrxProfile=2$ onDurationTimer 6
set ENodeBFunction=1,DrxProfile=0$ shortDrxCycle 9
set ENodeBFunction=1,DrxProfile=0$ shortDrxCycleTimer 1
set ENodeBFunction=1,DrxProfile=1$ shortDrxCycleTimer 0
set ENodeBFunction=1,DrxProfile=2$ shortDrxCycleTimer 0


###########  CarrierAggregationFunction ###################

set CarrierAggregationFunction=1 dynamicSCellSelectionMethod 2
set CarrierAggregationFunction=1 selectionPolicyUlWeighting 50
set CarrierAggregationFunction=1 fourLayerMimoPreferred false
set CarrierAggregationFunction=1 enhancedSelectionOfMimoAndCa false
set CarrierAggregationFunction=1 waitForAdditionalSCellOpportunity 10000
set CarrierAggregationFunction=1 sCellActProhibitTimer 10
set CarrierAggregationFunction=1 waitForBlindSelSCellRepLessTtt 600
set CarrierAggregationFunction=1 laaSCellDeactProhibitTimer 200


##################   ANR Function ##################

set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 anrInterFreqState 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 anrIntraFreqState 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 hoAllowedEutranPolicy true
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 x2SetupPolicy true
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 anrUesEUtraIntraFMax 0
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 anrUesEUtraIntraFMin 0
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 anrUesThreshInterFMax 0
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 anrUesThreshInterFMin 0
set ENodeBFunction=1,AnrFunction=1 maxNoPciReportsEvent 30
set ENodeBFunction=1,AnrFunction=1 removeNenbTime 3
set ENodeBFunction=1,AnrFunction=1 removeNrelTime 3
set ENodeBFunction=1,AnrFunction=1 probCellDetectMedHoSuccThres 50
set ENodeBFunction=1,AnrFunction=1,AnrFunctionGeran=1 anrStateGsm 1
set ENodeBFunction=1,AnrFunction=1 plmnWhiteListEnabled true
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 cellAddRsrpThresholdEutran -1240
set ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1 anrStateUtran 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1 hoAllowedUtranPolicy true
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 lbCellOffloadCapacityPolicy 30000
set ENodeBFunction=1,AnrFunction=1 plmnWhiteListEnabled false
set AutoCellCapEstFunction=1 useEstimatedCellCap true
set ENodeBFunction=1,AnrFunction=1$ removeNcellTime 3
set ENodeBFunction=1,AnrFunction=1$ removeNrelTime 3
set ENodeBFunction=1,AnrFunction=1$ removeNenbTime 3
set ENodeBFunction=1,AnrFunction=1$ cellRelHoAttRateThreshold 15
set ENodeBFunction=1,AnrFunction=1$ problematicCellPolicy 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1$ anrStateUtran 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1$ cellAddRsrpThresholdEutran -1240
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1$ anrInterFreqState 1
set ENodeBFunction=1,AnrFunction=1$ maxNoPciReportsEvent 30
set ENodeBFunction=1,AnrFunction=1$ probCellDetectLowHoSuccTime 4
set ENodeBFunction=1,AnrFunction=1$ probCellDetectMedHoSuccTime 2
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1$ lbCellOffloadCapacityPolicy 30000


######## Timer Profile ####################

set QciTable=default,QciProfilePredefined=qci1 rlfProfileRef RlfProfile=1
set RlfProfile=1$ n310 10
set RlfProfile=1$ n311 1
set RlfProfile=1$ t301 1000
set RlfProfile=1$ t310 500
set RlfProfile=1$ t311 5000
set RadioBearerTable=default,SignalingRadioBearer=1 tReorderingUl 35
set Rrc=1 t311 5000
set Rrc=1 tRrcConnReest 2
set Rrc=1 tWaitForRrcConnReest 9
cr ENodeBFunction=1,TimerProfile=0
6
8
3
10
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 timerProfileRef ENodeBFunction=1,TimerProfile=0
seti . tRrcConnectionSetup 10
set Rrc=1 t301 1000
set Rrc=1 t304 2000
set Rrc=1 t311 5000
set Rrc=1  tRrcConnectionReconfiguration 10
set Rcs=1 rlcDlDeliveryFailureAction 2
set Rcs=1 tInactivityTimer  10
set TimerProfile=0 tRelocOverall 20
set TimerProfile=0  tWaitForRrcConnReest 6
set TimerProfile=0  tRrcConnectionReconfiguration 8
set TimerProfile=0  tRrcConnReest 3
set RlfProfile=0$ n310 10
set RlfProfile=1$ n310 10
set RlfProfile=10$ n310 10
set RlfProfile=11$ n310 10
set RlfProfile=12$ n310 10
set RlfProfile=13$ n310 10
set RlfProfile=14$ n310 10
set RlfProfile=15$ n310 10
set RlfProfile=16$ n310 10
set RlfProfile=17$ n310 10
set RlfProfile=18$ n310 10
set RlfProfile=19$ n310 10
set RlfProfile=2$ n310 10
set RlfProfile=20$ n310 10
set RlfProfile=21$ n310 10
set RlfProfile=22$ n310 10
set RlfProfile=3$ n310 10
set RlfProfile=4$ n310 10
set RlfProfile=5$ n310 10
set RlfProfile=6$ n310 10
set RlfProfile=7$ n310 10
set RlfProfile=8$ n310 10
set RlfProfile=9$ n310 10
set RlfProfile=0$ t301 1000
set RlfProfile=0$ t310 500
set RlfProfile=1$ t311 5000
set ENodeBFunction=1,Rrc=1$ t301 1000
set ENodeBFunction=1,Rrc=1$ t311 5000
set ENodeBFunction=1,Rrc=1$ t304 2000
set ENodeBFunction=1,Rrc=1$ tRrcConnectionReconfiguration 10
set Rcs=1$ rlcDlDeliveryFailureAction 2
set ENodeBFunction=1$ tRelocOverall 20
set ENodeBFunction=1$ zzzTemporary52 1
set ENodeBFunction=1,Rrc=1$ tRrcConnReest 2
set ENodeBFunction=1,Rrc=1$ tWaitForRrcConnReest 9
set ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1$ dlMaxRetxThreshold 16
set ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1$ ulMaxRetxThreshold 16
set ENodeBFunction=1,RadioBearerTable=default,SignalingRadioBearer=1$ dlMaxRetxThreshold 16
set ENodeBFunction=1,RadioBearerTable=default,SignalingRadioBearer=1$ ulMaxRetxThreshold 16
set ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1$ tPollRetransmitUl 60
set RlfProfile=1$ t310 500
set RlfProfile=1$ t301 1000
set RlfProfile=5$ t301 1000

################   AdmissionControl #########################

set AdmissionControl=1 admNrRbDifferentiationThr 750
set AdmissionControl=1 admNrRrcDifferentiationThr 750
set AdmissionControl=1 arpBasedPreEmptionState 0
set AdmissionControl=1 ulAdmOverloadThr  950
set AdmissionControl=1 ulTransNwBandwidth 2000
set AdmissionControl=1 paArpOverride 7
set PmEventService=1 cellTraceFileSize 20000
set AdmissionControl dlAdmDifferentiationThr 750
set AdmissionControl ulAdmDifferentiationThr 750


################  MdtConfiguration  ######################

set MdtConfiguration=1 a2ThresholdRsrpMdt -140
set MdtConfiguration=1 a2ThresholdRsrqMdt -195
set MdtConfiguration=1 timeToTriggerA2Mdt 640
set MdtConfiguration=1 triggerQuantityA2Mdt 0

############### MACConfiguration ######################

set ENodeBFunction=1,RadioBearerTable=default,MACConfiguration=1 ulMaxHARQTx 5
set ENodeBFunction=1,RadioBearerTable=default,MACConfiguration=1 ulTtiBundlingMaxHARQTx 7
set ENodeBFunction=1,RadioBearerTable=default,MACConfiguration=1 dlMaxHARQTx 4

################# Signaling-DataRadioBearer-paging  ######################

set ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1 tPollRetransmitDl 80
set ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1 tPollRetransmitUl 60
set ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1 dlMaxRetxThreshold 16
set ENodeBFunction=1,RadioBearerTable=default,SignalingRadioBearer=1 tPollRetransmitUl 80
set ENodeBFunction=1,RadioBearerTable=default,SignalingRadioBearer=1 tPollRetransmitDl 80
set ENodeBFunction=1,RadioBearerTable=default,SignalingRadioBearer=1 dlMaxRetxThreshold 16
set ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1 ulMaxRetxThreshold 16
set ENodeBFunction=1,RadioBearerTable=default,SignalingRadioBearer=1 ulMaxRetxThreshold 16
set ENodeBFunction=1,Paging=1 pagingDiscardTimerDrxNb 3
set ENodeBFunction=1,Paging=1 maxNoOfPagingRecordsNb 3
set ENodeBFunction=1,Paging=1 noOfDefPagCyclPrim 8

################  Load Balancing Function #################

set LoadBalancingFunction=1 lbRateOffsetCoefficient 320
set LoadBalancingFunction=1 lbRateOffsetLoadThreshold 1000
set LoadBalancingFunction=1 lbCeiling 500
set LoadBalancingFunction=1 lbCaThreshold 2000
set LoadBalancingFunction=1 lbThreshold 40
set LoadBalancingFunction=1 lbHitRateEUtranAddThreshold 5
set LoadBalancingFunction=1 lbHitRateEUtranMeasUeIntensity 10
set LoadBalancingFunction=1 lbHitRateEUtranMeasUeThreshold 10
set LoadBalancingFunction=1 lbHitRateEUtranRemoveThreshold 2
set LoadBalancingFunction=1 lbMeasScalingLimit 30
set LoadBalancingFunction=1$ lbThreshold 20
set LoadBalancingFunction=1$ lbCeiling 500


################  Common Cell Parameters TDD + FDD    ###########################

set EUtranCell.*=.* allocThrPucchFormat1 50
set EUtranCell.*=.* allocTimerPucchFormat1 50
set EUtranCell.*=.* deallocThrPucchFormat1 100
set EUtranCell.*=.* deallocTimerPucchFormat1 6000
set EUtranCell.*=.* dlBlerTargetEnabled true
set EUtranCell.*=.* drxActive true
set EUtranCell.*=.* enableServiceSpecificHARQ true
set EUtranCell.*=.* pdcchCovImproveDtx true
set EUtranCell.*=.* pdcchCovImproveSrb false
set EUtranCell.*=.* pdcchTargetBler 24
set EUtranCell.*=.* pdcchTargetBlerPCell 22
set EUtranCell.*=.* pMaxServingCell 1000
set EUtranCell.*=.* tReorderingAutoConfiguration true
set EUtranCell.*=.* tTimeAlignmentTimer 0
set EUtranCell.*=.* ulBlerTargetEnabled true
set EUtranCell.*=.* ulHarqVolteBlerTarget 3
set EUtranCell.*=.* adaptiveCfiHoProhibit 0
set EUtranCell.*=.* enableSinrUplinkClpc true
set EUtranCell.*=.* pdcchCovImproveQci1 true
set EUtranCell.*=.* pdcchOuterLoopUpStepVolte 9
set EUtranCell.*=.* pdcchTargetBlerVolte 4
set EUtranCell.*=.* alpha 8
set EUtranCell.*=.* pZeroNominalPucch -110
set EUtranCell.*=.* cfraEnable true
set EUtranCell.*=.* changeNotification changeNotificationSIB15=true
set EUtranCell.*=.* changeNotification changeNotificationSIB16=true
set EUtranCell.*=.* changeNotification changeNotificationSIB7=true
set EUtranCell.*=.* changeNotification changeNotificationSIB2=true
set EUtranCell.*=.* changeNotification changeNotificationSIB3=true
set EUtranCell.*=.* changeNotification changeNotificationSIB4=true
set EUtranCell.*=.* changeNotification changeNotificationSIB1=true
set EUtranCell.*=.* changeNotification changeNotificationSIB6=true
set EUtranCell.*=.* changeNotification changeNotificationSIB5=true
set EUtranCell.*=.* changeNotification changeNotificationSIB13=true
set EUtranCell.*=.* changeNotification changeNotificationSIB8=true
set EUtranCell.*=.* mappingInfoCe mappingInfoSIB10=0
set EUtranCell.*=.* hoOptAdjThresholdAbs 5
set EUtranCell.*=.* hoOptAdjThresholdPerc 50
set EUtranCell.*=.* pdcchCfiMode 5
set EUtranCell.*=.* transmissionMode  4
set EUtranCell.*=.* ns05FullBandUsersInCellThres 1
set EUtranCell.*=.* puschNcpChannelEstWindowSize 1
set EUtranCell.*=.* mobCtrlAtPoorCovActive true
set EUtranCell.*=.* servOrPrioTriggeredIFHo 0
set EUtranCell.*=.* ul64qamEnabled true
set EUtranCell.*=.* dl256QamStatus 2
set EUtranCell.*=.* dl256QamEnabled true
set EUtranCell.*=.* qRxLevMinCe -140
set EUtranCell.*=.* pdcchLaGinrMargin 40
set EUtranCell.*=.* acBarringPresence acBarringForMmtelVideoPresence=0
set EUtranCell.*=.* acBarringPresence acBarringForMmtelVoicePresence=0
set EUtranCell.*=.* acBarringPresence acBarringPriorityMmtelVideo=0
set EUtranCell.*=.* acBarringPresence acBarringPriorityMmtelVoice=0
set EUtranCell.*=.* acBarringPresence acBarringForMoDataPresence=0
set EUtranCell.*=.* noOfEnhAdptReTxCand -1
set EUtranCell.*=.* dynUlResourceAllocEnabled true
set EUtranCell.*=.* systemInformationBlock6 tReselectionUtra=4
set EUtranCell.*=.* systemInformationBlock6 tReselectionUtraSfHigh=100
set EUtranCell.*=.* systemInformationBlock6 tReselectionUtraSfMedium=100
set EUtranCell.*=.* advCellSupAction  2
set EUtranCell.*=.* primaryPlmnReserved false
set EUtranCell.*=.* harqOffsetDl 3
set EUtranCell.*=.* harqOffsetUl 3
set EUtranCell.*=.* highSpeedUEActive false
set EUtranCell.*=.* initialBufferSizeDefault 86
set EUtranCell.*=.* prsTransmisScheme 0
set EUtranCell.*=.*  puschPwrOffset64qam 0
set EUtranCell.*=.* systemInformationBlock3 tEvaluation=240
set EUtranCell.*=.* cellRange 15
set EUtranCell.*=.* elcEnabled false
set EUtranCell.*=.* preambleInitialReceivedTargetPower -110
set EUtranCell.*=.* acBarringForCsfb acBarringFactor=95
set EUtranCell.*=.* acBarringForCsfb acBarringForSpecialAC=false false false false false
set EUtranCell.*=.* acBarringForCsfb acBarringTime=64
set EUtranCell.*=.* acBarringForEmergency false
set EUtranCell.*=.* acBarringForMoData acBarringFactor=95
set EUtranCell.*=.* acBarringForMoData acBarringForSpecialAC=false false false false false
set EUtranCell.*=.* acBarringForMoData acBarringTime=64
set EUtranCell.*=.* acBarringForMoSignalling acBarringFactor=95
set EUtranCell.*=.* acBarringForMoSignalling acBarringForSpecialAC=false false false false false
set EUtranCell.*=.* acBarringForMoSignalling acBarringTime=64
set EUtranCell.*=.* acBarringInfoPresent false
set EUtranCell.*=.* acBarringPresence acBarringForCsfbPresence=0
set EUtranCell.*=.* acBarringPresence acBarringForMoSignPresence=0
set EUtranCell.*=.* acBarringPresence acBarringPriorityCsfb=0
set EUtranCell.*=.* acBarringPresence acBarringPriorityMoData=0
set EUtranCell.*=.* acBarringPresence acBarringPriorityMoSignaling=0
set EUtranCell.*=.* spifhoSetupBearerAtInitialCtxtSetup false
set EUtranCell.*=.* srDetectHighThres 70
set EUtranCell.*=.* srProcessingLevel 0
set EUtranCell.*=.* ssacBarringForMMTELVideo acBarringFactor=95
set EUtranCell.*=.* ssacBarringForMMTELVideo acBarringForSpecialAC=false false false false false
set EUtranCell.*=.* ssacBarringForMMTELVideo acBarringTime=64
set EUtranCell.*=.* ssacBarringForMMTELVoice acBarringFactor=95
set EUtranCell.*=.* ssacBarringForMMTELVoice acBarringForSpecialAC=false false false false false
set EUtranCell.*=.* ssacBarringForMMTELVoice acBarringTime=64
set EUtranCell.*=.* systemInformationBlock3 tEvaluation=240
set EUtranCell.*=.* systemInformationBlock3 nCellChangeHigh=16
set EUtranCell.*=.* systemInformationBlock3 nCellChangeMedium=16
set EUtranCell.*=.* systemInformationBlock3 qHystSfHigh=0
set EUtranCell.*=.* systemInformationBlock3 qHystSfMedium=0
set EUtranCell.*=.* systemInformationBlock3 sIntraSearchQ=0
set EUtranCell.*=.* systemInformationBlock3 sNonIntraSearchv920Active=false
set EUtranCell.*=.* systemInformationBlock3 sIntraSearchv920Active=false
set EUtranCell.*=.* systemInformationBlock3 threshServingLowQ=1000
set EUtranCell.*=.* systemInformationBlock3 tHystNormal=240
set EUtranCell.*=.* systemInformationBlock7 tReselectionGeran=2
set EUtranCell.*=.* systemInformationBlock7 tReselectionGeranSfHigh=100
set EUtranCell.*=.* systemInformationBlock7 ReselectionGeranSfMedium=100
set EUtranCell.*=.* tUeBlockingTimer 200
set EUtranCell.*=.* ulImprovedUeSchedLastEnabled true
set EUtranCell.*=.* ulSCellPriority 5
set EUtranCell.*=.* ulSchedCtrlForOocUesEnabled true
set EUtranCell.*=.* ulSrsEnable False
set EUtranCell.*=.* ulTxPsdDistrThr 40
set EUtranCell.*=.* uncertAltitude 0
set EUtranCell.*=.* uncertSemiMajor 0
set EUtranCell.*=.* uncertSemiMinor 0
set EUtranCell.*=.* covTriggerdBlindHoAllowed false
set EUtranCell.*=.* qQualMin -34
set EUtranCell.*=.* qRxLevMin -124
set EUtranCell.*=.* srvccDelayTimer 3000
set EUtranCell.*=.* dlInterferenceManagementActive true
set EUtranCell.*=.* ulInterferenceManagementActive true
set EUtranCell.*=.* dlFrequencyAllocationProportion 100
set EUtranCell.*=.* ulConfigurableFrequencyStart 0
set EUtranCell.*=.* ulFrequencyAllocationProportion 100
set EUtranCell.*=.* outOfCoverageSparseGrantingBsr 8
set EUtranCell.*=.* eUlFssSwitchThresh 30
set EUtranCell.*=.* pdcchPowerBoostMax 2
set EUtranCell.*=.* dlMaxRetxRrcReleaseThr 8
set EUtranCell.*=.* sCellHandlingAtVolteCall 1


################  Common Cell Parameters FDD Technology   ###########################

set EUtranCellFDD=.* pdcchOuterLoopUpStep 8
set EUtranCellFDD=.* pdcchOuterLoopUpStepPCell 6
set EUtranCellFDD=.* ttiBundlingAfterHo 1
set EUtranCellFDD=.* ttiBundlingAfterReest 1
set EUtranCellFDD=.* ttiBundlingSwitchThres 150
set EUtranCellFDD=.* ttiBundlingSwitchThresHyst 30
set EUtranCellFDD=.* cellDownlinkCaCapacity 0
set EUtranCellFDD=.* mappingInfo mappingInfoSIB12=7
set EUtranCellFDD=.* mappingInfo mappingInfoSIB6$=4
set EUtranCellFDD=.* mappingInfo mappingInfoSIB4$=2
set EUtranCellFDD=.* mappingInfo mappingInfoSIB5=3
set EUtranCellFDD=.* servOrPrioTriggeredErabAction 3
set EUtranCellFDD=.* dlInternalChannelBandwidth 0
set EUtranCellFDD=.* ulInternalChannelBandwidth 0
set EUtranCellFDD=.* commonSrPeriodicity 10
set EUtranCellFDD=.* lbEUtranTriggerOffloadThreshold 30
set EUtranCellFDD=.* changeNotification changeNotificationSIB1=true
set EUtranCellFDD=.* changeNotification changeNotificationSIB2=true
set EUtranCellFDD=.* changeNotification changeNotificationSIB3=true
set EUtranCellFDD=.* changeNotification changeNotificationSIB4=true
set EUtranCellFDD=.* changeNotification changeNotificationSIB5=true
set EUtranCellFDD=.* changeNotification changeNotificationSIB6=true
set EUtranCellFDD=.* changeNotification changeNotificationSIB7=true
set EUtranCellFDD=.* changeNotification changeNotificationSIB13=true
set EUtranCellFDD=.* changeNotification changeNotificationSIB15=true
set EUtranCellFDD=.* changeNotification changeNotificationSIB16=true
set EUtranCellFDD=.* changeNotification changeNotificationSIB8=true
set EUtranCellFDD=RJ_E_F8.* pZeroNominalPusch -83
set EUtranCellFDD=RJ_E_F3.* pZeroNominalPusch -83
set EUtranCellFDD=RJ_E_F1.* pZeroNominalPusch -86
set EUtranCellFDD=RJ_E_F8.* crsGain 300
set EUtranCellFDD=RJ_E_F3.* crsGain 0
set EUtranCellFDD=RJ_E_F1.* crsGain 300
set EUtranCellFDD=.* ulTrigActive false
set EUtranCellFDD=RJ_E_F3.* pdschTypeBGain 0
set EUtranCellFDD=.* lbEUtranAcceptOffloadThreshold 10
set EUtranCellFDD=.* systemInformationBlock3 sNonIntraSearch=0
set EUtranCellFDD=.* systemInformationBlock3 sNonIntraSearchP=10




################  Common Cell Parameters TDD Technology   ###########################

set EUtranCellTDD=.* hoOptStatTime 24
set EUtranCellTDD=.* channelBandwidth 20000
set EUtranCellTDD=.* dlMaxMuMimoLayers 0
set EUtranCellTDD=.* ulMaxMuMimoLayers 0
set EUtranCellTDD=.* subframeAssignment 2
set EUtranCellTDD=.* timePhaseMaxDeviationTDDIndex 0
set EUtranCellTDD=.* commonSrPeriodicity 20
set EUtranCellTDD=.* mappingInfo mappingInfoSIB7=5
set EUtranCellTDD=.* pZeroNominalPusch -86
set EUtranCellTDD=.* crsGain 0
set EUtranCellTDD=.* pdschTypeBGain 0
set EUtranCellTDD=.* ulTrigActive true
set EUtranCellTDD=.* cellRange 10
set EUtranCellTDD=.* outOfCoverageSparseGrantingBsr 8
set EUtranCellTDD=.* interferenceThresholdSinrClpc -100
set EUtranCellTDD=.* rxSinrTargetClpc 20
set EUtranCellTDD=.* lbEUtranAcceptOffloadThreshold 50
set EUtranCellTDD=.* systemInformationBlock3 sNonIntraSearch=12
set EUtranCellTDD=.* systemInformationBlock3 sNonIntraSearchQ=0
set EUtranCellTDD=.*,UeMeasControl=1$ inhibitB2RsrqConfig true
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1$ hysteresisA2CriticalRsrp 0
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1,ReportConfigEUtraBestCellAnr=1$ a3offsetAnrDelta 3
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5=1$ timeToTriggerA5 480
set EUtranCellTDD=.* alpha 8
set EUtranCellTDD=.* cellCapMaxCellSubCap 60000
set EUtranCellTDD=.* cellCapMinCellSubCap 2000
set EUtranCellTDD=.* drxActive true
set EUtranCellTDD=.* pdcchLaGinrMargin 40
set EUtranCellTDD=.* pdcchOuterLoopUpStepVolte 9
set EUtranCellTDD=.* pdcchPowerBoostMax 0
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1$ timeToTriggerA1Search 480
set EUtranCellTDD=.* ulBlerTargetEnabled true
set EUtranCellTDD=.* enableServiceSpecificHARQ true
set EUtranCellTDD=.* tReorderingAutoConfiguration true
set EUtranCellTDD=.* srvccDelayTimer 3000
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigB2Geran=1$ b2Threshold2Geran -110
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigB2Utra=1$ hysteresisB2 20
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigB2Utra=1$ timeToTriggerB2 1280
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1$ timeToTriggerA3 480
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1,ReportConfigEUtraBestCellAnr=1$ timeToTriggerA3 480
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigEUtraIFBestCell=1$ timeToTriggerA3 480
set EUtranCellTDD=.*,UeMeasControl=1$ ueMeasurementsActive true
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1$ timeToTriggerA2Search 480
set EUtranCellTDD=.* advCellSupAction 2
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigB2Geran=1$ timeToTriggerB2 1280
set EUtranCellTDD=.* dlBlerTargetEnabled true
set EUtranCellTDD=.* pdcchCovImproveDtx true
set EUtranCellTDD=.* ulHarqVolteBlerTarget 3
set EUtranCellTDD=.* ns05FullBandUsersInCellThres 1
set EUtranCellTDD=.* puschNcpChannelEstWindowSize 1
set EUtranCellTDD=.* noOfEnhAdptReTxCand -1
set EUtranCellTDD=.* dynUlResourceAllocEnabled true
set EUtranCellTDD=.* acBarringInfoPresent false
set EUtranCellTDD=.* outOfCoverageSparseGrantingBsr 8
set EUtranCellTDD=.* eUlFssSwitchThresh 30
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1$ a5Threshold1Rsrp -140
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1$ a5Threshold1Rsrq -195
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1$ a5Threshold1Rsrq -195
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1$ a5Threshold2Rsrp -112
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1$ a5Threshold2Rsrq -195
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigB1GUtra=1$ b1ThresholdRsrq -435
set EUtranCellTDD=.* crsGain 0
set EUtranCellTDD=.* cellSubscriptionCapacity 20000
set EUtranCellTDD=.* pdschTypeBGain 0
set EUtranCellTDD=.* pZeroNominalPusch -86
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1$ a1a2SearchThresholdRsrp -114
set EUtranCellTDD=.* pdcchTargetBlerVolte 4
set EUtranCellTDD=.*,UeMeasControl=1$ excludeInterFreqAtCritical true
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5=1$ hysteresisA5 20
set EUtranCellTDD=.* enableSinrUplinkClpc true
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1$ timeToTriggerA1UlSearch 480
set EUtranCellTDD=.* systemInformationBlock6 tReselectionUtra=4
set EUtranCellTDD=.* systemInformationBlock3 sIntraSearchQ=0,sNonIntraSearchQ=0
set EUtranCellTDD=.* changeNotification changeNotificationSIB15=true,changeNotificationSIB16=true


###############  Relation Parameters #################

set EUtranCell.*=.*,EUtranFreqRelation=.* tReselectionEutra 2
set EUtranCell.*=.*,EUtranFreqRelation=.* anrMeasOn true
set EUtranCell.*=.*,GeranFreqGroupRelation=1 anrMeasOn true
set EUtranCell.*=.*,EUtranFreqRelation=.*,EUtranCellRelation=.* isHoAllowed true
set EUtranCell.*=.*,GeranFreqGroupRelation=1 anrMeasOn true
set EUtranCell.*=.*,GeranFreqGroupRelation=1 qRxLevMin -111
set EUtranCell.*=.*,EUtranFreqRelation=.* qRxLevMinCe -140
set EUtranCell.*=.*,EUtranFreqRelation=.* pMax 1000
set EUtranCell.*=.*,EUtranFreqRelation=.* tReselectionEutraSfHigh 100
set EUtranCell.*=.*,EUtranFreqRelation=.* tReselectionEutraSfMedium 100
set EUtranCell.*=.*,EUtranFreqRelation=.* qRxLevMin -124
set EUtranCell.*=.*,EUtranFreqRelation=.* mobilityAction 1
set EUtranCell.*=.*,EUtranFreqRelation=.* lbBnrAllowed true
set EUtranCell.*=.*,EUtranFreqRelation=.* lbBnrPolicy 2
set EUtranCell.*=.* altCsfbTargetPrio 2
set EUtranCell.*=.* altCsfbTargetPrioEC 2
set EUtranCell.*=.* mobilityActionCsfb 1
set EUtranCell.*=.* mobilityAction 1
set EUtranCell.*=.*,EUtranFreqRelation=39150 allowedMeasBandwidth 100
set EUtranCell.*=.*,EUtranFreqRelation=39348 allowedMeasBandwidth 100
set EUtranCell.*=.*,EUtranFreqRelation=515 allowedMeasBandwidth 75
set EUtranCell.*=.*,EUtranFreqRelation=1576 allowedMeasBandwidth 50
set EUtranCell.*=.*,EUtranFreqRelation=3601 allowedmeasbandwidth 25

########################  threshXHigh & threshXLow ####################


set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=39150 threshXHigh 14
set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=515     threshXHigh 14
set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=39150 threshXHigh 14
set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=39348 threshXHigh 14
set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=39348 threshXHigh 14
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=1576     threshXHigh 8
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=39150 threshXHigh 14
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=515     threshXHigh 14
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=39348 threshXHigh 14


set EUtranCellTDD=.*,GeranFreqGroupRelation=1 threshXLow 62
set EUtranCellFDD=.*,GeranFreqGroupRelation=1 threshXLow 62

set EUtranCellFDD=RJ_E_F3.*,eutranfreqrelation=3584 threshxlow 12
set EUtranCellFDD=RJ_E_F1.*,eutranfreqrelation=1576 threshxlow 12
set EUtranCellFDD=RJ_E_F1.*,eutranfreqrelation=3584 threshxlow 62
set EUtranCellTDD=.*,eutranfreqrelation=1576 threshxlow 16
set EUtranCellTDD=.*,eutranfreqrelation=3601 threshxlow 62
set EUtranCellFDD=RJ_E_F3.*,eutranfreqrelation=3601 threshxlow 12
set EUtranCellFDD=RJ_E_F1.*,eutranfreqrelation=3601 threshxlow 62



##################### UeMeasControl=1 ##############################
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigCsfbUtra=1 hysteresis 10
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigCsfbGeran=1 hysteresis 10
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSCellA6=1 triggerQuantityA6 0
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThresholdRsrp -140
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSearch=1 hysteresisA2CriticalRsrp 0
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1 hysteresisA3 10
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigA5=1 hysteresisA5 20
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB2Utra=1 hysteresisB2 20
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA1Search 480
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA1SearchRsrq 1024
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2Critical 480
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2CriticalRsrq 1024
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2Search 480
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2SearchRsrq 1024
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1 timeToTriggerA3 480
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigA5=1 timeToTriggerA5 480
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigA5=1 timeToTriggerA5Rsrq 1024
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB2Geran=1 timeToTriggerB2 1280
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1 triggerQuantityA3 0
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigA5=1 triggerQuantityA5 0
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSCellA6=1 timeToTriggerA6 40
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigElcA1A2=1 hysteresisA1A2Rsrp 10
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB1Geran=1 hysteresisB1 10
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB1Utra=1 hysteresisB1 10
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigElcA1A2=1 timeToTriggerA1 40
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSCellA1A2=1 timeToTriggerA1 40
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA1UlSearch 480
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSCellA1A2=1 timeToTriggerA2 40
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigElcA1A2=1 timeToTriggerA2 40
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2OutSearchRsrq -1
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB1Geran=1 timeToTriggerB1   640
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB2Geran=1 timeToTriggerB2Rsrq -1
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB2Utra=1 timeToTriggerB2Rsrq -1
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 hysteresisA5 10
set EUtranCell.*=.*,ReportConfigSearch=1 a2CriticalThrQci1RsrpOffset -20
set EUtranCell.*=.*,UeMeasControl=1 filterCoefficientEUtraRsrp 4
set EUtranCell.*=.*,UeMeasControl=1 ueMeasurementsActiveIF true
set EUtranCell.*=.*,UeMeasControl=1 zzzTemporary13    -2000000000
set EUtranCell.*=.*,UeMeasControl=1 sMeasure 0
set EUtranCell.*=.*,UeMeasControl=1 lowPrioMeasThresh 0
set EUtranCell.*=.*,UeMeasControl=1 maxUtranCellsToMeasure 32
set EUtranCell.*=.*,UeMeasControl=1 allowReleaseQci1 false
set EUtranCell.*=.*,UeMeasControl=1 ulSinrOffset 30
set EUtranCell.*=.*,UeMeasControl=1 ueMeasurementsActive true
set EUtranCell.*=.*,UeMeasControl=1 a5B2MobilityTimer 0
set EUtranCellFDD=.*,UeMeasControl=1 ueMeasurementsActiveGERAN true
set EUtranCellTDD=.*,UeMeasControl=1 ueMeasurementsActiveGERAN False
set EUtranCell.*=.*,UeMeasControl=1 excludeInterFreqAtCritical false
set EUtranCell.*=.*,UeMeasControl=1 a3SuspendCsgTimer 0
set EUtranCell.*=.*,UeMeasControl=1 ueMeasurementsActiveUTRAN true
set EUtranCellTDD=.*,UeMeasControl=1 excludeInterFreqAtCritical true
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2UlCritical 480
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2UlCritical 480
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2UlSearch 480
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2UlSearch 480
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigA5=1  hysteresisA5RsrqOffset 150
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold2Geran -102
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold1Rsrp  -119
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSCellA1A2=1 hysteresisA1A2RsrpBidirectional 10
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThrQci1RsrqOffset -100
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 a1a2UlSearchThreshold 60
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 hysteresisA2UlCritical 150
set EUtranCell.*=.*,UeMeasControl=1 csfbHoTargetSearchTimer 1200
set EUtranCell.*=.*,UeMeasControl=1      bothA5RsrpRsrqCheck false
set EUtranCell.*=.*,UeMeasControl=1      inhibitB2RsrqConfig true
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB2Geran=1 timeToTriggerB2Rsrq -1
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold1Rsrp  -140
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB1Geran=1 b1ThresholdGeran  -110
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB2GeranUlTrig=1 reportIntervalB2 4
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB2Geran=1 hysteresisB2 20
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold1Rsrq -195



######################  AnrFunction=1 ############################

set ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1  cellAddEcNoThresholdUtranDelta -10
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 cellAddRsrpThresholdEutran -1240
set ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1  cellAddRscpThresholdUtranDelta -1
set ENodeBFunction=1,AnrFunction=1 cellRelHoAttRateThreshold 15
set ENodeBFunction=1,AnrFunction=1 probCellDetectLowHoSuccTime 4
set ENodeBFunction=1,AnrFunction=1 probCellDetectMedHoSuccTime 2
set ENodeBFunction=1,AnrFunction=1 problematicCellPolicy 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionGeran=1 problematicCellPolicy 0
set ENodeBFunction=1,AnrFunction=1 removeNcellTime 3
set ENodeBFunction=1,AnrFunction=1 zzzTemporary13    -2000000000






######## TWAMP setting #######################


get Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW1,NextHop= address$ > $UP-Nexthop




crn Transport=1,Router=LTEUP,TwampResponder=1
ipAddress Router=LTEUP,InterfaceIPv4=TN_A_UP,AddressIPv4=TN_A_UP
udpPort 4001
userLabel
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=TWAMP
dst 10.61.96.208/28
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=TWAMP,NextHop=1
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference
end

get Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW1,NextHop= address$ > $UP-Nexthop

crn Transport=1,Router=LTEUP,TwampResponder=1
ipAddress Router=LTEUP,InterfaceIPv4=TN_C_UP,AddressIPv4=TN_C_UP
udpPort 4001
userLabel
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=TWAMP
dst 10.61.96.208/28
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=TWAMP,NextHop=1
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference
end

get Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW1,NextHop= address$ > $UP-Nexthop

crn Transport=1,Router=LTEUP,TwampResponder=1
ipAddress Router=LTEUP,InterfaceIPv4=TN_E_UP,AddressIPv4=TN_E_UP
udpPort 4001
userLabel
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=TWAMP
dst 10.61.96.208/28
end

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=TWAMP,NextHop=1
address $UP-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference
end

######## QOS setting #######################################

set ENodeBFunction=1 dscpLabel 46
set ENodeBFunction=1 gtpuErrorIndicationDscp 46
set ENodeBFunction=1 interEnbCaTunnelDscp 26
set ENodeBFunction=1 interEnbUlCompTunnelDscp 26
set ENodeBFunction=1 s1GtpuEchoDscp 46
set ENodeBFunction=1 x2GtpuEchoDscp 46
set ENodeBFunction=1 X2GtpuEchoDscp 46

cr Transport=1,QosProfiles=1,DscpPcpMap=1

set QciTable=default,QciProfilePredefined=qci1 dscp 34
set QciTable=default,QciProfilePredefined=qci2 dscp 34
set QciTable=default,QciProfilePredefined=qci3 dscp 26
set QciTable=default,QciProfilePredefined=qci4 dscp 26
set QciTable=default,QciProfilePredefined=qci5 dscp 46
set QciTable=default,QciProfilePredefined=qci6 dscp 26
set QciTable=default,QciProfilePredefined=qci7 dscp 26
set QciTable=default,QciProfilePredefined=qci8 dscp 26
set QciTable=default,QciProfilePredefined=qci9 dscp 26

set SysM=1,OamTrafficClass=1 dscp 28

set EthernetPort=TN_E egressQosMarking  QosProfiles=1,DscpPcpMap=1
set EthernetPort= egressQosMarking  QosProfiles=1,DscpPcpMap=1

set SctpProfile= dscp 46
set Ntp=1,NtpFrequencySync= dscp 34


lt all


set QosProfiles=1,DscpPcpMap=1  pcp0
set QosProfiles=1,DscpPcpMap=1  pcp1
set QosProfiles=1,DscpPcpMap=1  pcp2 
set QosProfiles=1,DscpPcpMap=1  pcp3
set QosProfiles=1,DscpPcpMap=1  pcp4
set QosProfiles=1,DscpPcpMap=1  pcp5
set QosProfiles=1,DscpPcpMap=1  pcp6
set QosProfiles=1,DscpPcpMap=1  pcp7


set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp0 0 1 2 3 5 7 9 11 13 15 17 19 21 23 25 27 29 31 33 35 36 37 38 39 41 43 45 47  48  49  50  51  52  53  54  55  56  57  58  59  60  61  62  63

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp2 22 24 26

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp3 6 8 10 30 32

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp4 12 14 40

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp5 28

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp6 16 18 34 42 44

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp7 46

set Router=OAM,DnsClient=1 dscp 28

et Router=.*,InterfaceIPv4= egressQosMarking  QosProfiles=1,DscpPcpMap=1
set Router=.*,InterfaceIPv4= ingressQosMarking QosProfiles=1,DscpPcpMap=1
set Router=LTECP,InterfaceIPv4=TN_E_CP  egressQosMarking  QosProfiles=1,DscpPcpMap=1
set Router=LTEUP,InterfaceIPv4=TN_E_UP  egressQosMarking  QosProfiles=1,DscpPcpMap=1
set Router=OAM,InterfaceIPv4=TN_E_OAM   egressQosMarking  QosProfiles=1,DscpPcpMap=1
set Router=OAM,InterfaceIPv4=TN_E_ABIS  egressQosMarking  QosProfiles=1,DscpPcpMap=1
set Router=OAM,InterfaceIPv4=TN_E_IUB   egressQosMarking  QosProfiles=1,DscpPcpMap=1
set VlanPort=     egressQosMarking  QosProfiles=1,DscpPcpMap=1
set VlanPort=TN_E_CP    egressQosMarking  QosProfiles=1,DscpPcpMap=1
set VlanPort=TN_E_OAM   egressQosMarking  QosProfiles=1,DscpPcpMap=1
set VlanPort=TN_E_UP    egressQosMarking  QosProfiles=1,DscpPcpMap=1
set VlanPort=TN_E_IUB   egressQosMarking  QosProfiles=1,DscpPcpMap=1
set VlanPort=TN_E_ABIS  egressQosMarking  QosProfiles=1,DscpPcpMap=1




######## QOS setting #######################################

$date = `date +%y%m%d_%H%M`
cvms BEFORE_Baseline-twamp_$date

set ENodeBFunction=1 dscpLabel 46
set ENodeBFunction=1 gtpuErrorIndicationDscp 46
set ENodeBFunction=1 interEnbCaTunnelDscp 26
set ENodeBFunction=1 interEnbUlCompTunnelDscp 26
set ENodeBFunction=1 s1GtpuEchoDscp 46
set ENodeBFunction=1 x2GtpuEchoDscp 46
set ENodeBFunction=1 X2GtpuEchoDscp 46

cr Transport=1,QosProfiles=1,DscpPcpMap=1

set QciTable=default,QciProfilePredefined=qci1 dscp 34
set QciTable=default,QciProfilePredefined=qci2 dscp 34
set QciTable=default,QciProfilePredefined=qci3 dscp 26
set QciTable=default,QciProfilePredefined=qci4 dscp 26
set QciTable=default,QciProfilePredefined=qci5 dscp 46
set QciTable=default,QciProfilePredefined=qci6 dscp 26
set QciTable=default,QciProfilePredefined=qci7 dscp 26
set QciTable=default,QciProfilePredefined=qci8 dscp 26
set QciTable=default,QciProfilePredefined=qci9 dscp 26

set SysM=1,OamTrafficClass=1 dscp 28

set EthernetPort=TN_A egressQosMarking  QosProfiles=1,DscpPcpMap=1
set EthernetPort=TN_E egressQosMarking  QosProfiles=1,DscpPcpMap=1
set EthernetPort=TN_C egressQosMarking  QosProfiles=1,DscpPcpMap=1
set EthernetPort= egressQosMarking  QosProfiles=1,DscpPcpMap=1

set SctpProfile= dscp 46
set Ntp=1,NtpFrequencySync= dscp 34


lt all


set QosProfiles=1,DscpPcpMap=1  pcp0
set QosProfiles=1,DscpPcpMap=1  pcp1
set QosProfiles=1,DscpPcpMap=1  pcp2 
set QosProfiles=1,DscpPcpMap=1  pcp3
set QosProfiles=1,DscpPcpMap=1  pcp4
set QosProfiles=1,DscpPcpMap=1  pcp5
set QosProfiles=1,DscpPcpMap=1  pcp6
set QosProfiles=1,DscpPcpMap=1  pcp7


set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp0 0 1 2 3 5 7 9 11 13 15 17 19 21 23 25 27 29 31 33 35 36 37 38 39 41 43 45 47  48  49  50  51  52  53  54  55  56  57  58  59  60  61  62  63

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp2 22 24 26

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp3 6 8 10 30 32

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp4 12 14 40

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp5 28

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp6 16 18 34 42 44

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp7 46

set Router=OAM,DnsClient=1 dscp 28

set Router=.*,InterfaceIPv4= egressQosMarking  QosProfiles=1,DscpPcpMap=1
set Router=.*,InterfaceIPv4= ingressQosMarking QosProfiles=1,DscpPcpMap=1
set Router=LTECP,InterfaceIPv4=TN_A_CP  egressQosMarking  QosProfiles=1,DscpPcpMap=1
set Router=LTEUP,InterfaceIPv4=TN_A_UP  egressQosMarking  QosProfiles=1,DscpPcpMap=1
set Router=OAM,InterfaceIPv4=TN_A_OAM   egressQosMarking  QosProfiles=1,DscpPcpMap=1
set Router=OAM,InterfaceIPv4=TN_A_ABIS  egressQosMarking  QosProfiles=1,DscpPcpMap=1
set Router=OAM,InterfaceIPv4=TN_A_IUB   egressQosMarking  QosProfiles=1,DscpPcpMap=1
set VlanPort=     egressQosMarking  QosProfiles=1,DscpPcpMap=1
set VlanPort=TN_A_CP    egressQosMarking  QosProfiles=1,DscpPcpMap=1
set VlanPort=TN_A_OAM   egressQosMarking  QosProfiles=1,DscpPcpMap=1
set VlanPort=TN_A_UP    egressQosMarking  QosProfiles=1,DscpPcpMap=1
set VlanPort=TN_A_IUB   egressQosMarking  QosProfiles=1,DscpPcpMap=1
set VlanPort=TN_A_ABIS  egressQosMarking  QosProfiles=1,DscpPcpMap=1

##Features_GPL

set CXC4011713 featurestate 0
set CXC4012238 featurestate 1
set CXC4012097 featurestate 1
set CXC4011368 featurestate 0
set CXC4012036 featurestate 1
set CXC4010512 featurestate 0
set CXC4010955 featurestate 0
set CXC4010973 featurestate 1
set CXC4011055 featurestate 0
set CXC4011246 featurestate 0
set CXC4011346 featurestate 1
set CXC4011478 featurestate 0
set cxc4011554 featurestate 0
set CXC4011663 featurestate 0
set CXC4011664 featurestate 0
set CXC4011736 featurestate 0
set CXC4011810 featurestate 0
set cxc4011911 featurestate 0
set cxc4011966 featurestate 0
set CXC4011983 featurestate 1
set CXC4011714 featurestate 0
set CXC4010319 featurestate 1
set CXC4010320 featurestate 1
set CXC4010609 featurestate 1
set CXC4010613 featurestate 1
set CXC4010616 featurestate 1
set CXC4010618 featurestate 1
set CXC4010620 featurestate 1
set CXC4010717 featurestate 1
set CXC4010723 featurestate 1
set CXC4010770 featurestate 1
set CXC4010841 featurestate 1
set CXC4010856 featurestate 1
set CXC4010912 featurestate 1
set CXC4010956 featurestate 1
set CXC4010959 featurestate 1
set CXC4010961 featurestate 1
set CXC4010962 featurestate 1
set CXC4010967 featurestate 1
set CXC4010974 featurestate 1
set CXC4010980 featurestate 1
set CXC4010990 featurestate 1
set CXC4011011 featurestate 1
set CXC4011033 featurestate 1
set CXC4011034 featurestate 1
set CXC4011050 featurestate 1
set CXC4011057 featurestate 1
set CXC4011059 featurestate 1
set CXC4011060 featurestate 1
set CXC4011061 featurestate 1
set CXC4011062 featurestate 1
set CXC4011064 featurestate 1
set CXC4011074 featurestate 1
set CXC4011075 featurestate 1
set CXC4011157 featurestate 1
set CXC4011183 featurestate 1
set CXC4011245 featurestate 1
set CXC4011247 featurestate 1
set CXC4011251 featurestate 1
set CXC4011252 featurestate 1
set CXC4011253 featurestate 1
set CXC4011255 featurestate 1
set CXC4011258 featurestate 1
set CXC4011319 featurestate 1
set CXC4011327 featurestate 1
set CXC4011345 featurestate 1
set CXC4011366 featurestate 1
set CXC4011370 featurestate 1
set CXC4011372 featurestate 1
set CXC4011373 featurestate 1
set CXC4011376 featurestate 1
set CXC4011378 featurestate 1
set CXC4011422 featurestate 1
set CXC4011443 featurestate 1
set CXC4011444 featurestate 1
set CXC4011477 featurestate 1
set CXC4011479 featurestate 1
set CXC4011481 featurestate 1
set CXC4011482 featurestate 1
set CXC4011485 featurestate 1
set CXC4011515 featurestate 1
set CXC4011698 featurestate 1
set CXC4011711 featurestate 1
set CXC4011715 featurestate 1
set CXC4011813 featurestate 1
set CXC4011815 featurestate 1
set CXC4011910 featurestate 1
set CXC4011913 featurestate 0
set CXC4011914 featurestate 1
set CXC4011918 featurestate 1
set CXC4011940 featurestate 1
set CXC4011941 featurestate 1
set CXC4011969 featurestate 1
set CXC4012003 featurestate 1
set CXC4012018 featurestate 1
set CXC4012070 featurestate 1
set CXC4012089 featurestate 1
set CXC4011559 featurestate 1
set CXC4011922 featurestate 1
set CXC4011946 featurestate 1
set CXC4012129 featurestate 1
set CXC4012240 featurestate 1
set CXC4011072 featurestate 1
set CXC4011974 featurestate 1

##20Q2 Features-

set CXC4012316 featurestate 1
set CXC4012271 featurestate 1
set CXC4012260 featurestate 1
set CXC4012374 featurestate 1
set CXC4012344 featurestate 0
set CXC4012370 featurestate 0
set CXC4012326 featurestate 1
set CXC4012349 featurestate 1
set CXC4012261 featurestate 1


#FORTDDSITEONLY4x4Quad

set CXC4011667 featurestate 1
set CXC4011056 featurestate 1

#OLD Running Features

set CXC4010949 featurestate 1
set CXC4010963 featurestate 1
set CXC4010964 featurestate 1
set CXC4011063 featurestate 1
set CXC4011065 featurestate 1
set CXC4011067 featurestate 1
set CXC4011068 featurestate 1
set CXC4011069 featurestate 1
set CXC4011155 featurestate 1
set CXC4011163 featurestate 1
set CXC4011256 featurestate 1
set CXC4011317 featurestate 1
set CXC4011356 featurestate 1
set CXC4011427 featurestate 1
set CXC4011512 featurestate 1
set CXC4011557 featurestate 1
set CXC4011618 featurestate 1
set CXC4011666 featurestate 1
set CXC4011699 featurestate 1
set CXC4011707 featurestate 1
set CXC4011710 featurestate 1
set CXC4011716 featurestate 1
set CXC4011803 featurestate 1
set CXC4011804 featurestate 1
set CXC4011807 featurestate 1
set CXC4011808 featurestate 1
set CXC4011809 featurestate 1
set CXC4011811 featurestate 1
set CXC4011814 featurestate 1
set CXC4011817 featurestate 1
set CXC4011820 featurestate 1
set CXC4011917 featurestate 1
set CXC4011930 featurestate 1
set CXC4011933 featurestate 1
set CXC4011937 featurestate 1
set CXC4011938 featurestate 1
set CXC4011939 featurestate 1
set CXC4011942 featurestate 1
set CXC4011951 featurestate 1
set CXC4011958 featurestate 1
set CXC4011967 featurestate 1
set CXC4011973 featurestate 1
set CXC4011975 featurestate 1
set CXC4011982 featurestate 1
set CXC4011991 featurestate 1
set CXC4012022 featurestate 1
set CXC4040004 featurestate 1
set CXC4040005 featurestate 1
set CXC4040006 featurestate 1
set CXC4040008 featurestate 1
set CXC4040009 featurestate 1
set CXC4040010 featurestate 1
set CXC4040013 featurestate 1
set CXC4040014 featurestate 1
set CXC4012259 featurestate 1
set CXC4011664 featurestate 0
set CXC4011663 featurestate 0
set CXC4010956 featurestate 1

set CXC4011823 featurestate  1

##Basic Intelligence

set CXC4012218 featurestate 1

###############  PRB Muting Scripts 1800 Layer only #####################

set EUtranCellFDD=RJ_E_F3.* dlFrequencyAllocationProportion 94
set EUtranCellFDD=RJ_E_F8.* dlFrequencyAllocationProportion 80
set EUtranCellFDD=RJ_E_F3.* ulFrequencyAllocationProportion 94
set EUtranCellFDD=RJ_E_F8.* ulFrequencyAllocationProportion 80
set EUtranCellFDD=RJ_E_F3.* dlConfigurableFrequencyStart 7
set EUtranCellFDD=RJ_E_F8.* dlConfigurableFrequencyStart 10
set EUtranCellFDD=RJ_E_F3.* ulConfigurableFrequencyStart 7
set EUtranCellFDD=RJ_E_F8.* ulConfigurableFrequencyStart 10
set EUtranCellFDD=RJ_E_F3.* dlInterferenceManagementActive false
set EUtranCellFDD=RJ_E_F8.* dlInterferenceManagementActive false
set EUtranCellFDD=RJ_E_F3.* ulInterferenceManagementActive false
set EUtranCellFDD=RJ_E_F8.* ulInterferenceManagementActive false
set EUtranCellFDD=RJ_E_F3.* ulSrsEnable       true
set EUtranCellFDD=RJ_E_F8.* ulSrsEnable       true
set EUtranCellFDD=RJ_E_F3.* pucchOverdimensioning 5
set EUtranCellFDD=RJ_E_F8.* pucchOverdimensioning 4
set EUtranCellFDD=RJ_E_F3.* dlCchAndRefSigBlockActive true
set EUtranCellFDD=RJ_E_F8.* dlCchAndRefSigBlockActive true
set EUtranCellFDD=RJ_E_F3.* dlCchAndRefSigBoost true
set EUtranCellFDD=RJ_E_F8.* dlCchAndRefSigBoost true

Set Lm=1,FeatureState=CXC4011255 featureState 1
Set Lm=1,FeatureState=CXC4011074 featureState 1
Set Lm=1,FeatureState=CXC4010980 featureState 1

###############  GERAN CSFB/SRVCC Parameter ################

set GeranFreqGroupRelation=1 csFallbackPrio 4
set GeranFreqGroupRelation=1 csFallbackPrioEC 4
set AnrFunction=1,AnrFunctionGeran=1 anrStateGsm 1
set GeranFreqGroup pmaxgeran 1000
set GeranFreqGroup Qoffsetfreq 0
set GeranFreqGroup nccpermitted 11111111
set GeranFreqGroup anrMeasOn TRUE
set GeranFreqGroup mobilityAction 1
set GeranFreqGroup mobilityActionCsfb 1
set GeranFreqGroup userLabel SIB7
set CXC4011664 featurestate 0
set CXC4011346 featurestate 1
set CXC4012240 featurestate 1
set CXC4010618 featurestate 1


##################  Power Savings Features ###########################

---------------  Mimo Sleep Function All Layers -------------

set EUtranCell.*=.*,MimoSleepFunction=1 sleepMode 4
set EUtranCell.*=.*,MimoSleepFunction=1 sleepStartTime 18:30
set EUtranCell.*=.*,MimoSleepFunction=1 sleepEndTime 02:30
set EUtranCell.*=.*,MimoSleepFunction=1 sleepPowerControl 1
set EUtranCell.*=.*,MimoSleepFunction=1 switchDownMonitorDurTimer 5
set EUtranCell.*=.*,MimoSleepFunction=1 switchDownPrbThreshold 40
set EUtranCell.*=.*,MimoSleepFunction=1 switchDownRrcConnThreshold 50
set EUtranCell.*=.*,MimoSleepFunction=1 switchUpMonitorDurTimer 15
set EUtranCell.*=.*,MimoSleepFunction=1 switchUpPrbThreshold 55
set EUtranCell.*=.*,MimoSleepFunction=1 switchUpRrcConnThreshold 60

_______________ Cell Sleep Function ___________________________

#################### 2100  ############################

set EUtranCellFDD=LW.*,CellSleepFunction=1 sleepMode 1
set EUtranCellFDD=LW.*,CellSleepFunction=1 sleepStartTime 18:30
set EUtranCellFDD=LW.*,CellSleepFunction=1 sleepEndTime 00:30
set EUtranCellFDD=LW.*,CellSleepFunction=1 capCellSleepMonitorDurTimer 5
set EUtranCellFDD=LW.*,CellSleepFunction=1 capCellDlPrbSleepThreshold 40
set EUtranCellFDD=LW.*,CellSleepFunction=1 capCellRrcConnSleepThreshold 90
set EUtranCellFDD=LW.*,CellSleepFunction=1 covCellWakeUpMonitorDurTimer 5
set EUtranCellFDD=LW.*,CellSleepFunction=1 covCellDlPrbWakeUpThreshold 55
set EUtranCellFDD=LW.*,CellSleepFunction=1 covCellRrcConnWakeUpThreshold 15
set EUtranCellFDD=LW.*,CellSleepFunction=1 coverageCellDiscovery true
set EUtranCellTDD=LW.*,CellSleepFunction=1 capCellSleepProhibitInterval 0
set EUtranCellFDD=LW.*,CellSleepFunction=1 isAllowedMsmOnCovCell true

set EUtranCellFDD=RJ_E_F1.*,CellSleepFunction=1 sleepMode 1
set EUtranCellFDD=RJ_E_F1.*,CellSleepFunction=1 sleepStartTime 18:30
set EUtranCellFDD=RJ_E_F1.*,CellSleepFunction=1 sleepEndTime 00:30
set EUtranCellFDD=RJ_E_F1.*,CellSleepFunction=1 capCellSleepMonitorDurTimer 5
set EUtranCellFDD=RJ_E_F1.*,CellSleepFunction=1 capCellDlPrbSleepThreshold 40
set EUtranCellFDD=RJ_E_F1.*,CellSleepFunction=1 capCellRrcConnSleepThreshold 90
set EUtranCellFDD=RJ_E_F1.*,CellSleepFunction=1 covCellWakeUpMonitorDurTimer 5
set EUtranCellFDD=RJ_E_F1.*,CellSleepFunction=1 covCellDlPrbWakeUpThreshold 55
set EUtranCellFDD=RJ_E_F1.*,CellSleepFunction=1 covCellRrcConnWakeUpThreshold 15
set EUtranCellFDD=RJ_E_F1.*,CellSleepFunction=1 coverageCellDiscovery true
set EUtranCellFDD=RJ_E_F1.*,CellSleepFunction=1 capCellSleepProhibitInterval 0
set EUtranCellFDD=RJ_E_F1.*,CellSleepFunction=1 isAllowedMsmOnCovCell true




#################### TDD  ############################

set EUtranCellTDD=.*,CellSleepFunction=1 sleepMode 1
set EUtranCellTDD=.*,CellSleepFunction=1             sleepStartTime 18:30
set EUtranCellFDD=LW.*,CellSleepFunction=1              sleepStartTime 18:30
set EUtranCellFDD=RJ_E_F1.*,CellSleepFunction=1              sleepStartTime 18:30
set EUtranCellTDD=.*,CellSleepFunction=1              sleepEndTime      02:30
set EUtranCellFDD=LW.*,CellSleepFunction=1              sleepEndTime      02:30
set EUtranCellFDD=RJ_E_F1.*,CellSleepFunction=1              sleepEndTime      02:30
set EUtranCellFDD=LW.*,CellSleepFunction=1              capCellSleepMonitorDurTimer 5
set EUtranCellFDD=RJ_E_F1.*,CellSleepFunction=1              capCellSleepMonitorDurTimer 5
set EUtranCellTDD=.*,CellSleepFunction=1              capCellSleepMonitorDurTimer 5
set EUtranCellTDD=.*,CellSleepFunction=1              capCellDlPrbSleepThreshold 40
set EUtranCellFDD=LW.*,CellSleepFunction=1              capCellDlPrbSleepThreshold 40
set EUtranCellFDD=RJ_E_F1.*,CellSleepFunction=1              capCellDlPrbSleepThreshold 40
set EUtranCellTDD=.*,CellSleepFunction=1              capCellRrcConnSleepThreshold 90
set EUtranCellFDD=LW.*,CellSleepFunction=1              capCellRrcConnSleepThreshold 90
set EUtranCellFDD=RJ_E_F1.*,CellSleepFunction=1              capCellRrcConnSleepThreshold 90
set EUtranCellTDD=.*,CellSleepFunction=1              covCellWakeUpMonitorDurTimer 15
set EUtranCellFDD=LW.*,CellSleepFunction=1              covCellWakeUpMonitorDurTimer 15
set EUtranCellFDD=RJ_E_F1.*,CellSleepFunction=1              covCellWakeUpMonitorDurTimer 15
set EUtranCellTDD=.*,CellSleepFunction=1              covCellDlPrbWakeUpThreshold 55
set EUtranCellFDD=LW.*,CellSleepFunction=1              covCellDlPrbWakeUpThreshold 55
set EUtranCellFDD=RJ_E_F1.*,CellSleepFunction=1              covCellDlPrbWakeUpThreshold 55
set EUtranCellTDD=.*,CellSleepFunction=1              covCellRrcConnWakeUpThreshold 100
set EUtranCellFDD=LW.*,CellSleepFunction=1              covCellRrcConnWakeUpThreshold 100
set EUtranCellFDD=RJ_E_F1.*,CellSleepFunction=1              covCellRrcConnWakeUpThreshold 100
set EUtranCellFDD=LW.*,CellSleepFunction=1              coverageCellDiscovery true
set EUtranCellFDD=RJ_E_F1.*,CellSleepFunction=1              coverageCellDiscovery true
set EUtranCellTDD=.*,CellSleepFunction=1              coverageCellDiscovery true
set EUtranCellTDD=.*,CellSleepFunction=1              capCellSleepProhibitInterval 0
set EUtranCellFDD=LW.*,CellSleepFunction=1              capCellSleepProhibitInterval 0
set EUtranCellFDD=RJ_E_F1.*,CellSleepFunction=1              capCellSleepProhibitInterval 0

----------------  cellSleepCovCellMeasOn ---------------------------

set EUtranCellTDD=.* EUtranFreqRelation=1576  cellSleepCovCellMeasOn true
set EUtranCellTDD=.* EUtranFreqRelation=3601  cellSleepCovCellMeasOn true
set EUtranCellTDD=.* EUtranFreqRelation=39150 cellSleepCovCellMeasOn false
set EUtranCellTDD=.* EUtranFreqRelation=39348 cellSleepCovCellMeasOn false
set EUtranCellTDD=.* EUtranFreqRelation=515   cellSleepCovCellMeasOn true

set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=1576  cellSleepCovCellMeasOn false
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=3601  cellSleepCovCellMeasOn false
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=39150 cellSleepCovCellMeasOn false
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=39348 cellSleepCovCellMeasOn false
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=515   cellSleepCovCellMeasOn false

set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=1576  cellSleepCovCellMeasOn false
set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=3601  cellSleepCovCellMeasOn true
set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=39150 cellSleepCovCellMeasOn false
set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=39348 cellSleepCovCellMeasOn false
set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=515   cellSleepCovCellMeasOn false

set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=1576  cellSleepCovCellMeasOn true
set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=3601  cellSleepCovCellMeasOn true
set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=39150 cellSleepCovCellMeasOn false
set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=39348 cellSleepCovCellMeasOn false
set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=515   cellSleepCovCellMeasOn false


###############  AMS & CA Scripts ############################


set SystemFunctions=1,Lm=1,FeatureState=CXC4011476 featureState 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4011922 featureState 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4011666 featureState 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4011559 featureState 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4012259 featureState 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4012123 featureState 1
set Licensing=1,OptionalFeatureLicense=CarrierAggregation$  featureState  1
set Licensing=1,OptionalFeatureLicense=CarrierAggregationFddTdd$  featureState  1
set Licensing=1,OptionalFeatureLicense=CarrierAggregationAwareIFLB$  featureState  1
set Licensing=1,OptionalFeatureLicense=DynamicScellSelection$  featureState  1
set Licensing=1,OptionalFeatureLicense=VoLTEOptimizedCA$  featureState  1
set▒FeatureState=CXC4012123▒featureState▒1
set Licensing=1,OptionalFeatureLicense=AutomaticSCellManagement$  featureState  1
set SystemFunctions=1,Lm=1,FeatureState=CXC4011983 featureState 1
set Licensing=1,OptionalFeatureLicense=InterENBCarrierAggregation$  featureState  1
set EUtranCell.*=.* sCellHandlingAtVolteCall 1
set EUtranCell.*=.*,EUtranFreqRelation=.*,EUtranCellRelation=.* sCellCandidate    2

set CXC4011958|CXC4011808|CXC4011803|CXC4011378 FeatureState 1

set EUtranCellFDD=RJ_E_F3_.*,EUtranFreqRelation=39150 asmSCellDetection 3
set EUtranCellFDD=RJ_E_F3_.*,EUtranFreqRelation=39348 asmSCellDetection 3

set EUtranCellTDD=RJ_E_T1_.*,EUtranFreqRelation=39151 asmSCellDetection 3
set EUtranCellTDD=RJ_E_T1_.*,EUtranFreqRelation=39150 asmSCellDetection 3
set EUtranCellTDD=RJ_E_T2_.*,EUtranFreqRelation=39150 asmSCellDetection 3
set EUtranCellTDD=RJ_E_T2_.*,EUtranFreqRelation=39151 asmSCellDetection 3

set EUtranCellTDD=RJ_E_T1_.*,EUtranFreqRelation=515 asmSCellDetection 0
set EUtranCellTDD=RJ_E_T2_.*,EUtranFreqRelation=515 asmSCellDetection 0
set EUtranCellTDD=RJ_E_T1_.*,EUtranFreqRelation=3601 asmSCellDetection 0
set EUtranCellTDD=RJ_E_T2_.*,EUtranFreqRelation=3601 asmSCellDetection 0
set EUtranCellTDD=RJ_E_T1_.*,EUtranFreqRelation=1576 asmSCellDetection 0
set EUtranCellTDD=RJ_E_T2_.*,EUtranFreqRelation=1576 asmSCellDetection 0

set EUtranCellFDD=RJ_E_F3_.*,EUtranFreqRelation=515 asmSCellDetection 0
set EUtranCellFDD=RJ_E_F3_.*,EUtranFreqRelation=3601 asmSCellDetection 0
set EUtranCellFDD=RJ_E_F3_.*,EUtranFreqRelation=1576 asmSCellDetection 0
set EUtranCellFDD=RJ_E_F3_.*,EUtranFreqRelation=39151 asmSCellDetection 0
set EUtranCellFDD=RJ_E_F3_.*,EUtranFreqRelation=39147 asmSCellDetection 0

set EUtranCellFDD=RJ_E_F1_.*,EUtranFreqRelation=515 asmSCellDetection 0
set EUtranCellFDD=RJ_E_F1_.*,EUtranFreqRelation=3601 asmSCellDetection 0
set EUtranCellFDD=RJ_E_F1_.*,EUtranFreqRelation=1576 asmSCellDetection 0
set EUtranCellFDD=RJ_E_F1_.*,EUtranFreqRelation=39151 asmSCellDetection 0
set EUtranCellFDD=RJ_E_F1_.*,EUtranFreqRelation=39147 asmSCellDetection 0
set EUtranCellFDD=RJ_E_F1_.*,EUtranFreqRelation=39150 asmSCellDetection 0
set EUtranCellFDD=RJ_E_F1_.*,EUtranFreqRelation=39148 asmSCellDetection 0

set EUtranCellFDD=RJ_E_F8_.*,EUtranFreqRelation=515 asmSCellDetection 0
set EUtranCellFDD=RJ_E_F8_.*,EUtranFreqRelation=3601 asmSCellDetection 0
set EUtranCellFDD=RJ_E_F8_.*,EUtranFreqRelation=1576 asmSCellDetection 0
set EUtranCellFDD=RJ_E_F8_.*,EUtranFreqRelation=39151 asmSCellDetection 0
set EUtranCellFDD=RJ_E_F8_.*,EUtranFreqRelation=39147 asmSCellDetection 0
set EUtranCellFDD=RJ_E_F8_.*,EUtranFreqRelation=39150 asmSCellDetection 0
set EUtranCellFDD=RJ_E_F8_.*,EUtranFreqRelation=39148 asmSCellDetection 0

set EUtranCellFDD=RJ_E_F3_.*,EUtranFreqRelation=39150  caTriggeredRedirectionActive true
set EUtranCellFDD=RJ_E_F3_.*,EUtranFreqRelation=39348  caTriggeredRedirectionActive true

set EUtranCell.*=.*,GeranFreqGroupRelation=1 connectedModeMobilityPrio -1
set EUtranCellTDD=.*,GeranFreqGroupRelation=1 voicePrio -1
set EUtranCellFDD=.*,GeranFreqGroupRelation=1 voicePrio -1
set EUtranCellTDD=.* cellSubscriptionCapacity 20000


#######################  22.Q2 Feature Massification #######################


##############  LTE PIM Detection in Baseband #################

set EUtranCellFDD=.* pimDetectionEnabled true
set ENodeBFunction=1 pimAutoDetectionEnabled false
set CXC4010955|CXC4011368|CXC4011842 featurestate 0
set PreschedProfile=.* preschedulingDataSize 86
set PreschedProfile=.* preschedulingPeriod 5
set PreschedProfile=.* preschedulingDuration 200
set PreschedProfile=0 preschedulingSinrThreshold 15

##############  ASGH based Pre-Scheduling  ###################

set SubscriberGroupProfile=1 preschedulingMode 2
set CXC4012200|CXC4011715 featureState 1

############# Differential Uplink Power Contr ####################

set EUtranCellTDD=.* enableSinrUplinkClpc true
set EUtranCellTDD=.* rxSinrTargetClpc 16
set EUtranCellTDD=.* interferenceThresholdSinrClpc -105
set EUtranCellTDD=.* ulPsdLoadThresholdSinrClpc 2
set EUtranCellTDD=.* ulTxPsdDistrThr 40
set EUtranCellTDD=.* p0ClpcExGoodEnabled true
set EUtranCellTDD=.* p0ClpcExBadEnabled true
set EUtranCellTDD=.* p0ClpcExBadSinrThr -10
set EUtranCellTDD=.* p0ClpcExGoodSinrThr 16
set EUtranCellTDD=.* p0ClpcExGoodSinrOffset64Qam 3
set EUtranCellTDD=.* p0ClpcExGoodSinrOffset256Qam 10
set EUtranCellTDD=.* assumedUePowerMsg3 1000
set CXC4012089 featureState 1

############### Increase number of GTP-U connec ######################

set CXC4012022 featureState 1
set ENodeBFunction=1 s1GtpuEchoEnable 1

################  Atmospheric Duct Int Reduction  #########################

set EUtranCellTDD=.* subframeAssignment 2
set EUtranCellTDD=.* specialSubframePattern 7
set EUtranCellTDD=.* ductIntOpMode 3
set EUtranCellTDD=.* ductIntPerfTuning ductIntBgNoiseThr=-105
set EUtranCellTDD=.* ductIntPerfTuning ductIntCharSeqCorrPeakThr=50
set EUtranCellTDD=.* ductIntPerfTuning ductIntCharSeqPwrDiff=5
set EUtranCellTDD=.* ductIntPerfTuning ductIntRedTriggerThr=14
set EUtranCellTDD=.* ductIntPerfTuning ductIntRedRecovThr=10
set EUtranCellTDD=.* ductIntPerfTuning ductIntCharSeqPwrThr=-105
set EUtranCellTDD=.* ductIntPerfTuning ductIntSlopePwrDiffThr=3
set EUtranCellTDD=.* ductIntPerfTuning ductIntSlopeDetectPeriod=10
set EUtranCellTDD=.* ductIntPerfTuning ductIntSlopeDetectRatioThr=50
set EUtranCellTDD=.* ductIntPerfTuning ductIntCharSeqTransThr=10
set ENodeBFunction=1 ductIntCharInfoScheme 0
set ENodeBFunction=1 ductIntFlexibleDetectionEnabled false
set CXC4012256 featureState 1

################# Dyn SCell Selection for CA ###########


set SctpProfile=1 pathMaxRtx 4
set SctpProfile=Node_Internal_F1 pathMaxRtx 4
set SctpProfile=1 assocMaxRtx 8
set SctpProfile=Node_Internal_F1 assocMaxRtx 8
set SctpProfile=1 initRto 2000
set SctpProfile=Node_Internal_F1 initRto 2000
set SctpProfile=1 maxRto 4000
set SctpProfile=Node_Internal_F1 maxRto 4000
set SctpProfile=1 minRto 1000
set SctpProfile=Node_Internal_F1 minRto 1000

###############


lt all
gs+
confbd+
st cell

### LMS WITHOUT LAYER FLIP  ####

set EUtranCell.*=.*,EUtranFreqRelation=39150 cellReselectionPriority 6
set EUtranCell.*=.*,EUtranFreqRelation=39348 cellReselectionPriority 6
set EUtranCell.*=.*,EUtranFreqRelation=515 cellReselectionPriority 4
set EUtranCell.*=.*,EUtranFreqRelation=3601 cellReselectionPriority 2
set EUtranCell.*=.*,EUtranFreqRelation=1576cellReselectionPriority 3
set EUtranCell.*=.*,GeranFreqGroupRelation=1 cellReselectionPriority 1

set EUtranCell.*=.*,EUtranFreqRelation=39150 connectedModeMobilityPrio 6
set EUtranCell.*=.*,EUtranFreqRelation=39348 connectedModeMobilityPrio 6
set EUtranCell.*=.*,EUtranFreqRelation=515 connectedModeMobilityPrio 4
set EUtranCell.*=.*,EUtranFreqRelation=1576 connectedModeMobilityPrio 3
set EUtranCellFDD=.*,EUtranFreqRelation=3601 connectedModeMobilityPrio -1
set EUtranCellTDD=.*,EUtranFreqRelation=3601 connectedModeMobilityPrio -1
set EUtranCell.*=.*,GeranFreqGroupRelation=1 connectedModeMobilityPrio -1


set EUtranCellFDD=RJ_E_F8.*,GeranFreqGroupRelation=1 voicePrio -1
set EUtranCellFDD=RJ_E_F1.*,GeranFreqGroupRelation=1 voicePrio -1
set EUtranCellFDD=RJ_E_F3.*,GeranFreqGroupRelation=1 voicePrio -1
set EUtranCellTDD=.*,GeranFreqGroupRelation=1 voicePrio -1
set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=1576 voicePrio 3
set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=3601 voicePrio 6
set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=39150 voicePrio -1
set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=39348 voicePrio -1
set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=515 voicePrio 4
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=1576 voicePrio 4
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=3601 voicePrio 6
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=39150 voicePrio -1
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=39348 voicePrio -1
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=515 voicePrio -1
set EUtranCellTDD=RJ_E_T2.*,EUtranFreqRelation=1576 voicePrio 3
set EUtranCellTDD=RJ_E_T2.*,EUtranFreqRelation=3601 voicePrio 4
set EUtranCellTDD=RJ_E_T2.*,EUtranFreqRelation=39150 voicePrio -1
set EUtranCellTDD=RJ_E_T2.*,EUtranFreqRelation=39348 voicePrio -1
set EUtranCellTDD=RJ_E_T2.*,EUtranFreqRelation=515 voicePrio 6
set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=1576 voicePrio 4
set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=3601 voicePrio 6
set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=39150 voicePrio -1
set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=39348 voicePrio -1
set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=515 voicePrio -1
set EUtranCellTDD=RJ_E_T1.*,EUtranFreqRelation=1576 voicePrio 3
set EUtranCellTDD=RJ_E_T1.*,EUtranFreqRelation=3601 voicePrio 4
set EUtranCellTDD=RJ_E_T1.*,EUtranFreqRelation=39150 voicePrio -1
set EUtranCellTDD=RJ_E_T1.*,EUtranFreqRelation=39348 voicePrio -1
set EUtranCellTDD=RJ_E_T1.*,EUtranFreqRelation=515 voicePrio 6
set EUtranCellFDD=.*,GeranFreqGroupRelation=1 voicePrio -1



### common ###

set EUtranCell.*=.*,EUtranFreqRelation=.* interFreqMeasType 0
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2SearchRsrp 20
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2SearchRsrq 10
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigA5=1 hysteresisA5 20
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigA5=1 hysteresisA5RsrqOffset 0
set EUtranCell.*=.*,EUtranFreqRelation=.* lbA5Thr1RsrpFreqOffset 97
set EUtranCell.*=.*,EUtranFreqRelation=3601 lbA5Thr1RsrpFreqOffset 0
set EUtranCell.*=.*,EUtranFreqRelation=.* qOffsetFreq 0
set EUtranCellTDD=RJ_E_T1.*,EUtranFreqRelation=39348 qOffsetFreq -3
set EUtranCellTDD=RJ_E_T2.*,EUtranFreqRelation=39150 qOffsetFreq -3
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThresholdRsrp -140
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSearch=1 hysteresisA2CriticalRsrp 0
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThresholdRsrq -195
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 hysteresisA5  10
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold2Rsrp -111
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold1Rsrp -140
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold2Rsrq  -170
set EUtranCell.*=.*,UeMeasControl=1 bothA5RsrpRsrqCheck true
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSearch=1 hysteresisA2CriticalRsrq 100

### RSRP ###

set EUtranCellFDD=RJ_E_F1.*,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrp -114
set EUtranCellFDD=RJ_E_F3.*,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrp -110
set EUtranCellFDD=RJ_E_F8.*,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrp -48
set EUtranCellTDD=RJ_E_T.*,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrp -112

set EUtranCellFDD=RJ_E_F1.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrp  -110
set EUtranCellFDD=RJ_E_F3.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrp  -114
set EUtranCellFDD=RJ_E_F8.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrp  -114
set EUtranCellTDD=RJ_E_T.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrp  -112

set EUtranCellFDD=RJ_E_F1.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp  -114
set EUtranCellFDD=RJ_E_F3.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp  -114
set EUtranCellFDD=RJ_E_F8.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp  -114
set EUtranCellTDD=RJ_E_T.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp  -112

set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=1576 a5Thr1RsrpFreqOffset 0
set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=3601 a5Thr1RsrpFreqOffset 0
set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=39150 a5Thr1RsrpFreqOffset 0
set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=39348 a5Thr1RsrpFreqOffset 0
set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=515 a5Thr1RsrpFreqOffset 0
set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=3601 a5Thr1RsrpFreqOffset 0
set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=39150 a5Thr1RsrpFreqOffset 0
set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=39348 a5Thr1RsrpFreqOffset 0
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=1576 a5Thr1RsrpFreqOffset 66
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=515 a5Thr1RsrpFreqOffset 66
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=39150 a5Thr1RsrpFreqOffset 66
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=39348 a5Thr1RsrpFreqOffset 66
set EUtranCellTDD=RJ_E_T.*,EUtranFreqRelation=1576 a5Thr1RsrpFreqOffset 0
set EUtranCellTDD=RJ_E_T.*,EUtranFreqRelation=515 a5Thr1RsrpFreqOffset 0
set EUtranCellTDD=RJ_E_T.*,EUtranFreqRelation=3601 a5Thr1RsrpFreqOffset 0
set EUtranCellTDD=RJ_E_T1.*,EUtranFreqRelation=39348 a5Thr1RsrpFreqOffset 0
set EUtranCellTDD=RJ_E_T2.*,EUtranFreqRelation=39150 a5Thr1RsrpFreqOffset 0

set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=1576 a5Thr2RsrpFreqOffset 2
set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=3601 a5Thr2RsrpFreqOffset 66
set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=39150 a5Thr2RsrpFreqOffset 4
set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=39348 a5Thr2RsrpFreqOffset 4
set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=515 a5Thr2RsrpFreqOffset 2
set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=3601 a5Thr2RsrpFreqOffset 0
set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=39150 a5Thr2RsrpFreqOffset 4
set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=39348 a5Thr2RsrpFreqOffset 4
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=515 a5Thr2RsrpFreqOffset 2
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=1576 a5Thr2RsrpFreqOffset 0
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=39150 a5Thr2RsrpFreqOffset 2
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=39348 a5Thr2RsrpFreqOffset 2
set EUtranCellTDD=RJ_E_T.*,EUtranFreqRelation=515 a5Thr2RsrpFreqOffset 0
set EUtranCellTDD=RJ_E_T.*,EUtranFreqRelation=1576 a5Thr2RsrpFreqOffset -2
set EUtranCellTDD=RJ_E_T.*,EUtranFreqRelation=3601 a5Thr2RsrpFreqOffset 66
set EUtranCellTDD=RJ_E_T1.*,EUtranFreqRelation=39348 a5Thr2RsrpFreqOffset 0
set EUtranCellTDD=RJ_E_T2.*,EUtranFreqRelation=39150 a5Thr2RsrpFreqOffset 0

### RSRQ ###

set EUtranCellFDD=RJ_E_F1.*,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrq -170
set EUtranCellFDD=RJ_E_F3.*,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrq -160
set EUtranCellFDD=RJ_E_F8.*,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrq -150
set EUtranCellTDD=RJ_E_T.*,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrq -160

set EUtranCellFDD=RJ_E_F1.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrq  -160
set EUtranCellFDD=RJ_E_F3.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrq  -160
set EUtranCellFDD=RJ_E_F8.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrq  -160
set EUtranCellTDD=RJ_E_T.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrq  -150

set EUtranCellFDD=RJ_E_F1.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrq  -180
set EUtranCellFDD=RJ_E_F3.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrq  -180
set EUtranCellFDD=RJ_E_F8.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrq  -180
set EUtranCellTDD=RJ_E_T.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrq  -180

set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=1576 a5Thr1RsrqFreqOffset 0
set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=3601 a5Thr1RsrqFreqOffset 0
set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=39150 a5Thr1RsrqFreqOffset 0
set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=39348 a5Thr1RsrqFreqOffset 0
set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=3601 a5Thr1RsrqFreqOffset 0
set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=515 a5Thr1RsrqFreqOffset 10
set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=39150 a5Thr1RsrqFreqOffset 10
set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=39348 a5Thr1RsrqFreqOffset 10
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=1576 a5Thr1RsrqFreqOffset 20
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=515 a5Thr1RsrqFreqOffset 20
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=39150 a5Thr1RsrqFreqOffset 20
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=39348 a5Thr1RsrqFreqOffset 20
set EUtranCellTDD=RJ_E_T.*,EUtranFreqRelation=1576 a5Thr1RsrqFreqOffset 0
set EUtranCellTDD=RJ_E_T.*,EUtranFreqRelation=3601 a5Thr1RsrqFreqOffset -10
set EUtranCellTDD=RJ_E_T.*,EUtranFreqRelation=515 a5Thr1RsrqFreqOffset 0
set EUtranCellTDD=RJ_E_T2.*,EUtranFreqRelation=39150 a5Thr1RsrqFreqOffset -10
set EUtranCellTDD=RJ_E_T1.*,EUtranFreqRelation=39348 a5Thr1RsrqFreqOffset -10

set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=1576 a5Thr2RsrqFreqOffset 20
set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=3601 a5Thr2RsrqFreqOffset 140
set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=39150 a5Thr2RsrqFreqOffset 10
set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=39348 a5Thr2RsrqFreqOffset 10
set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=515 a5Thr2RsrqFreqOffset 10
set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=3601 a5Thr2RsrqFreqOffset 40
set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=39150 a5Thr2RsrqFreqOffset 10
set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=39348 a5Thr2RsrqFreqOffset 10
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=1576 a5Thr2RsrqFreqOffset 20
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=515 a5Thr2RsrqFreqOffset 20
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=39150 a5Thr2RsrqFreqOffset 10
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=39348 a5Thr2RsrqFreqOffset 10
set EUtranCellTDD=RJ_E_T.*,EUtranFreqRelation=1576 a5Thr2RsrqFreqOffset 20
set EUtranCellTDD=RJ_E_T.*,EUtranFreqRelation=3584 a5Thr2RsrqFreqOffset 130
set EUtranCellTDD=RJ_E_T.*,EUtranFreqRelation=515 a5Thr2RsrqFreqOffset 20
set EUtranCellTDD=RJ_E_T2.*,EUtranFreqRelation=39348 a5Thr2RsrqFreqOffset 10
set EUtranCellTDD=RJ_E_T1.*,EUtranFreqRelation=39348 a5Thr2RsrqFreqOffset 10

############ IFLB ############

set CXC4011373 FeatureState 1
set CXC4011370 FeatureState 1
set EUtranCellTDD=.* cellSubscriptionCapacity 20000
set EUtranCellFDD=RJ_E_F3.* cellCapMinCellSubCap 2000
set EUtranCellFDD=RJ_E_F8.* cellCapMinCellSubCap 2000
set EUtranCellFDD=RJ_E_F1.* cellCapMinCellSubCap 2000
set EUtranCellTDD=RJ_E_T.* cellCapMinCellSubCap 500
set EUtranCell.*=.* cellCapMaxCellSubCap 60000
set EUtranCell.*=.* cellCapMinMaxWriProt true
set EUtranCell.*=.*,EUtranFreqRelation=.*,EUtranCellRelation=40470-.*-.* loadBalancing     1
set EUtranCell.*=.*,EUtranFreqRelation=3601,EUtranCellRelation=40470-.*-.* loadBalancing     0

set EUtranCell.*=.*,GeranFreqGroupRelation=1 connectedModeMobilityPrio -1

set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a1a2ThrRsrqQciOffset=-130,a1a2ThrRsrpQciOffset=50
set EUtranCellTDD=.*,EUtranFreqRelation=1576 EUtranFreqToQciProfileRelation lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=54,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=3,a5Thr2RsrqFreqQciOffset=-50,atoThresh1QciProfileHandling=0,atoThresh2QciProfileHandling=0,lbA5Threshold2RsrpOffset=0,lbA5Threshold2RsrqOffset=0,timeToTriggerA3=-1,timeToTriggerA3Rsrq=-1
set EUtranCellTDD=.*,EUtranFreqRelation=3601 EUtranFreqToQciProfileRelation lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=64,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=3,a5Thr2RsrqFreqQciOffset=-50,atoThresh1QciProfileHandling=0,atoThresh2QciProfileHandling=0,lbA5Threshold2RsrpOffset=0,lbA5Threshold2RsrqOffset=0,timeToTriggerA3=-1,timeToTriggerA3Rsrq=-1
set EUtranCellTDD=.*,EUtranFreqRelation=515 EUtranFreqToQciProfileRelation lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=54,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=3,a5Thr2RsrqFreqQciOffset=-50,atoThresh1QciProfileHandling=0,atoThresh2QciProfileHandling=0,lbA5Threshold2RsrpOffset=0,lbA5Threshold2RsrqOffset=0,timeToTriggerA3=-1,timeToTriggerA3Rsrq=-1
set EUtranCellTDD=.*,EUtranFreqRelation=39150 EUtranFreqToQciProfileRelation lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=3,a5Thr2RsrqFreqQciOffset=240,atoThresh1QciProfileHandling=0,atoThresh2QciProfileHandling=0,lbA5Threshold2RsrpOffset=0,lbA5Threshold2RsrqOffset=0,timeToTriggerA3=-1,timeToTriggerA3Rsrq=-1
set EUtranCellTDD=.*,EUtranFreqRelation=39348 EUtranFreqToQciProfileRelation lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=3,a5Thr2RsrqFreqQciOffset=240,atoThresh1QciProfileHandling=0,atoThresh2QciProfileHandling=0,lbA5Threshold2RsrpOffset=0,lbA5Threshold2RsrqOffset=0,timeToTriggerA3=-1,timeToTriggerA3Rsrq=-1

set EUtranCellFDD=RJ_E_F1.*,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a1a2ThrRsrqQciOffset=-130,a1a2ThrRsrpQciOffset=10
set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=1576 EUtranFreqToQciProfileRelation lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=10,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=3,a5Thr2RsrqFreqQciOffset=-50,atoThresh1QciProfileHandling=0,atoThresh2QciProfileHandling=0,lbA5Threshold2RsrpOffset=0,lbA5Threshold2RsrqOffset=0,timeToTriggerA3=-1,timeToTriggerA3Rsrq=-1
set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=3601 EUtranFreqToQciProfileRelation lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=10,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=3,a5Thr2RsrqFreqQciOffset=-50,atoThresh1QciProfileHandling=0,atoThresh2QciProfileHandling=0,lbA5Threshold2RsrpOffset=0,lbA5Threshold2RsrqOffset=0,timeToTriggerA3=-1,timeToTriggerA3Rsrq=-1
set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=515 EUtranFreqToQciProfileRelation lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=3,a5Thr2RsrqFreqQciOffset=0,atoThresh1QciProfileHandling=0,atoThresh2QciProfileHandling=0,lbA5Threshold2RsrpOffset=0,lbA5Threshold2RsrqOffset=0,timeToTriggerA3=-1,timeToTriggerA3Rsrq=-1
set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=39150 EUtranFreqToQciProfileRelation lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=3,a5Thr2RsrqFreqQciOffset=240,atoThresh1QciProfileHandling=0,atoThresh2QciProfileHandling=0,lbA5Threshold2RsrpOffset=0,lbA5Threshold2RsrqOffset=0,timeToTriggerA3=-1,timeToTriggerA3Rsrq=-1
set EUtranCellFDD=RJ_E_F1.*,EUtranFreqRelation=39348 EUtranFreqToQciProfileRelation lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=3,a5Thr2RsrqFreqQciOffset=240,atoThresh1QciProfileHandling=0,atoThresh2QciProfileHandling=0,lbA5Threshold2RsrpOffset=0,lbA5Threshold2RsrqOffset=0,timeToTriggerA3=-1,timeToTriggerA3Rsrq=-1

set EUtranCellFDD=RJ_E_F3.*,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a1a2ThrRsrqQciOffset=-130,a1a2ThrRsrpQciOffset=20
set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=1576 EUtranFreqToQciProfileRelation lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=3,a5Thr2RsrqFreqQciOffset=0,atoThresh1QciProfileHandling=0,atoThresh2QciProfileHandling=0,lbA5Threshold2RsrpOffset=0,lbA5Threshold2RsrqOffset=0,timeToTriggerA3=-1,timeToTriggerA3Rsrq=-1
set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=3601 EUtranFreqToQciProfileRelation lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=20,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=3,a5Thr2RsrqFreqQciOffset=-50,atoThresh1QciProfileHandling=0,atoThresh2QciProfileHandling=0,lbA5Threshold2RsrpOffset=0,lbA5Threshold2RsrqOffset=0,timeToTriggerA3=-1,timeToTriggerA3Rsrq=-1
set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=515 EUtranFreqToQciProfileRelation lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=3,a5Thr2RsrqFreqQciOffset=-50,atoThresh1QciProfileHandling=0,atoThresh2QciProfileHandling=0,lbA5Threshold2RsrpOffset=0,lbA5Threshold2RsrqOffset=0,timeToTriggerA3=-1,timeToTriggerA3Rsrq=-1
set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=39150 EUtranFreqToQciProfileRelation lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=3,a5Thr2RsrqFreqQciOffset=240,atoThresh1QciProfileHandling=0,atoThresh2QciProfileHandling=0,lbA5Threshold2RsrpOffset=0,lbA5Threshold2RsrqOffset=0,timeToTriggerA3=-1,timeToTriggerA3Rsrq=-1
set EUtranCellFDD=RJ_E_F3.*,EUtranFreqRelation=39348 EUtranFreqToQciProfileRelation lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=3,a5Thr2RsrqFreqQciOffset=240,atoThresh1QciProfileHandling=0,atoThresh2QciProfileHandling=0,lbA5Threshold2RsrpOffset=0,lbA5Threshold2RsrqOffset=0,timeToTriggerA3=-1,timeToTriggerA3Rsrq=-1

set EUtranCellFDD=RJ_E_F8.*,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a1a2ThrRsrqQciOffset=-130,a1a2ThrRsrpQciOffset=64
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=1576 EUtranFreqToQciProfileRelation lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=-66,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=3,a5Thr2RsrqFreqQciOffset=-130,atoThresh1QciProfileHandling=0,atoThresh2QciProfileHandling=0,lbA5Threshold2RsrpOffset=0,lbA5Threshold2RsrqOffset=0,timeToTriggerA3=-1,timeToTriggerA3Rsrq=-1
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=3601 EUtranFreqToQciProfileRelation lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=3,a5Thr2RsrqFreqQciOffset=0,atoThresh1QciProfileHandling=0,atoThresh2QciProfileHandling=0,lbA5Threshold2RsrpOffset=0,lbA5Threshold2RsrqOffset=0,timeToTriggerA3=-1,timeToTriggerA3Rsrq=-1
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=515 EUtranFreqToQciProfileRelation lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=3,a5Thr2RsrqFreqQciOffset=240,atoThresh1QciProfileHandling=0,atoThresh2QciProfileHandling=0,lbA5Threshold2RsrpOffset=0,lbA5Threshold2RsrqOffset=0,timeToTriggerA3=-1,timeToTriggerA3Rsrq=-1
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=39150 EUtranFreqToQciProfileRelation lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=3,a5Thr2RsrqFreqQciOffset=240,atoThresh1QciProfileHandling=0,atoThresh2QciProfileHandling=0,lbA5Threshold2RsrpOffset=0,lbA5Threshold2RsrqOffset=0,timeToTriggerA3=-1,timeToTriggerA3Rsrq=-1
set EUtranCellFDD=RJ_E_F8.*,EUtranFreqRelation=39348 EUtranFreqToQciProfileRelation lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=3,a5Thr2RsrqFreqQciOffset=240,atoThresh1QciProfileHandling=0,atoThresh2QciProfileHandling=0,lbA5Threshold2RsrpOffset=0,lbA5Threshold2RsrqOffset=0,timeToTriggerA3=-1,timeToTriggerA3Rsrq=-1
set SctpProfile=1 pathMaxRtx 4
set SctpProfile=Node_Internal_F1 pathMaxRtx 4
set SctpProfile=1 assocMaxRtx 8
set SctpProfile=Node_Internal_F1 assocMaxRtx 8
set SctpProfile=1 initRto 2000
set SctpProfile=Node_Internal_F1 initRto 2000
set SctpProfile=1 maxRto 4000
set SctpProfile=Node_Internal_F1 maxRto 4000
set SctpProfile=1 minRto 1000
set SctpProfile=Node_Internal_F1 minRto 1000


###################################


set EUtranCell.*=.*,EUtranFreqRelation=39150 connectedModeMobilityPrio 6
set EUtranCell.*=.*,EUtranFreqRelation=39348 connectedModeMobilityPrio 6
set EUtranCell.*=.*,EUtranFreqRelation=39151 connectedModeMobilityPrio 6
set EUtranCell.*=.*,EUtranFreqRelation=39349 connectedModeMobilityPrio 6
set EUtranCell.*=.*,EUtranFreqRelation=515 connectedModeMobilityPrio 4
set EUtranCell.*=.*,EUtranFreqRelation=1576 connectedModeMobilityPrio 3
set EUtranCell.*=.*,EUtranFreqRelation=3601 connectedModeMobilityPrio 2
set EUtranCell.*=.*,EUtranFreqRelation=39150 cellreselectionPriority 6
set EUtranCell.*=.*,EUtranFreqRelation=39348 cellreselectionPriority 6
set EUtranCell.*=.*,EUtranFreqRelation=39151 cellreselectionPriority 6
set EUtranCell.*=.*,EUtranFreqRelation=39349 cellreselectionPriority 6
set EUtranCell.*=.*,EUtranFreqRelation=515 cellreselectionPriority 4
set EUtranCell.*=.*,EUtranFreqRelation=1576 cellreselectionPriority 3
set EUtranCell.*=.*,EUtranFreqRelation=3601 cellreselectionPriority 2
set EUtranCell.*=.*,EUtranFreqRelation=39348 voicePrio -1
set EUtranCell.*=.*,EUtranFreqRelation=39349 voicePrio -1
set EUtranCell.*=.*,EUtranFreqRelation=39150 voicePrio -1
set EUtranCell.*=.*,EUtranFreqRelation=39151 voicePrio -1

cvms pre_dotparameter

set Lm=1,FeatureState=CXC4011060$ featureState 1
set Lm=1,FeatureState=CXC4011062$ featureState 0
set ENodeBFunction=1,AdmissionControl=1$ dlAdmDifferentiationThr 950
set ENodeBFunction=1,AdmissionControl=0$ ulAdmDifferentiationThr 950
set ENodeBFunction=1,AdmissionControl=1                     paArpOverride     2
set ENodeBFunction=1,AdmissionControl=1                     paArpOverrideHpa  2


cvms post_dotparameter


set CXC4011958 featureState 1
set CXC4011808 featureState 1
set CXC4011803 featureState 1
set CXC4011983 featureState 0
set CXC4011378 featureState 1

set CXC4012017 featureState 1
set CXC4012015 featureState 1
set CXC4012026 featureState 1
set CXC4011018 featureState 1


confb+
set SectorCarrier=1  configuredMaxTxPower 80000
set SectorCarrier=2  configuredMaxTxPower 80000
set SectorCarrier=3  configuredMaxTxPower 80000
set SectorCarrier=21  configuredMaxTxPower 40000
set SectorCarrier=22  configuredMaxTxPower 40000
set SectorCarrier=23  configuredMaxTxPower 40000
set SectorCarrier=31  configuredMaxTxPower 80000
set SectorCarrier=32  configuredMaxTxPower 80000
set SectorCarrier=33  configuredMaxTxPower 80000
set SectorCarrier=11  configuredMaxTxPower 80000
set SectorCarrier=12  configuredMaxTxPower 80000
set SectorCarrier=13  configuredMaxTxPower 80000

set . vswrSupervisionSensitivity 100
set . vswrSupervisionActive true

$date = `date +%y%m%d_%H%M`
cvms Baseline_Updated_$date

confbd-
gs-

"""

# --------------------------------------------------- 5G in TN ------------------------------------------------------------------#
NR_TN_RN_Cell_Def = """ 
## TN STARTED - DscpPcpMap=1/TwampResponder/SctpProfile=1/SctpEndpoint=1/SctpEndpoint=F1/SctpProfile=Node_Internal_F1/SctpEndpoint=NG/SctpEndpoint=X2/CLOCK##

confb+
gs+



crn Transport=1,QosProfiles=1,DscpPcpMap=1
defaultPcp 0
pcp0 0 1 2 3 4 5 6 7
pcp1 9 10 11 12 13 14 15
pcp2 16 17 18 19 20 21 22 23
pcp3 24 25 26 27 28 29 30 31
pcp4 32 33 34 35 36 37 38 39
pcp5 40 41 42 43 44 45 46 47
pcp6 48 49 50 51 52 53 54 55
pcp7 56 57 58 59 60 61 62 63
userLabel Traffic
end
#END Transport=1,QosProfiles=1,DscpPcpMap=1 --------------------

ld Transport=1,EthernetPort=TN_IDL_B
lset Transport=1,EthernetPort=TN_IDL_B$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

ld Transport=1,Router=LTE_NR,InterfaceIPv4=LTE_UP
lset Transport=1,Router=LTE_NR,InterfaceIPv4=LTE_UP$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

ld Transport=1,Router=LTE_CP,InterfaceIPv4=LTE_CP
lset Transport=1,Router=LTE_CP,InterfaceIPv4=LTE_CP$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

ld Transport=1,Router=LTE_NR,InterfaceIPv6=NR
lset Transport=1,Router=LTE_NR,InterfaceIPv6=NR$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

crn Transport=1,Router=LTE_NR,TwampResponder=1
ipAddress Transport=1,Router=LTE_NR,InterfaceIPv6=NR,AddressIPv6=NR_S1U_OAM
udpPort 4001
userLabel TWAMP1
end
#END Transport=1,Router=LTE_NR,TwampResponder=1 --------------------

crn Transport=1,SctpProfile=1
alphaIndex 3
assocMaxRtx 8
betaIndex 2
bundlingActivated true
bundlingAdaptiveActivated true
bundlingTimer 0
cookieLife 60
dscp 46
hbMaxBurst 1
heartbeatActivated true
heartbeatInterval 2000
incCookieLife 30
initARWnd 16384
initialHeartbeatInterval 500
initRto 2000
maxActivateThr 65535
maxBurst 4
maxInitRt 5
maxInStreams 2
maxOutStreams 2
maxRto 4000
maxSctpPduSize 1480
maxShutdownRt 5
minActivateThr 1
minRto 1000
noSwitchback true
pathMaxRtx 4
primaryPathAvoidance true
primaryPathMaxRtx 0
sackTimer 100
thrTransmitBuffer 48
thrTransmitBufferCongCeased 85
transmitBufferSize 64
userLabel SCTP
end
#END Transport=1,SctpProfile=1 --------------------

crn Transport=1,SctpEndpoint=1
localIpAddress Transport=1,Router=LTE_CP,InterfaceIPv4=LTE_CP,AddressIPv4=LTE_CP
portNumber 36422
sctpProfile Transport=1,SctpProfile=1
end
#END Transport=1,SctpEndpoint=1 --------------------

crn Transport=1,SctpEndpoint=F1
localIpAddress Transport=1,Router=LTE_NR,InterfaceIPv6=NR,AddressIPv6=NR_S1U_OAM
portNumber 38472
sctpProfile Transport=1,SctpProfile=1
end
#END Transport=1,SctpEndpoint=F1 --------------------

crn Transport=1,SctpProfile=Node_Internal_F1
alphaIndex 3
assocMaxRtx 8
betaIndex 2
bundlingActivated true
bundlingAdaptiveActivated true
bundlingTimer 0
cookieLife 60
dscp 46
hbMaxBurst 1
heartbeatActivated true
heartbeatInterval 2000
incCookieLife 30
initARWnd 16384
initialHeartbeatInterval 500
initRto 2000
maxActivateThr 65535
maxBurst 4
maxInitRt 5
maxInStreams 2
maxOutStreams 2
maxRto 4000
maxSctpPduSize 1480
maxShutdownRt 5
minActivateThr 1
minRto 1000
noSwitchback true
pathMaxRtx 4
primaryPathAvoidance true
primaryPathMaxRtx 0
sackTimer 100
thrTransmitBuffer 48
thrTransmitBufferCongCeased 85
transmitBufferSize 64
userLabel SCTP
end
#END Transport=1,SctpProfile=Node_Internal_F1 --------------------

crn Transport=1,SctpEndpoint=F1_NRCUCP
localIpAddress Transport=1,Router=Node_Internal_F1,InterfaceIPv4=NR_CUCP,AddressIPv4=1
portNumber 38472
sctpProfile Transport=1,SctpProfile=Node_Internal_F1
end
#END Transport=1,SctpEndpoint=F1_NRCUCP --------------------

crn Transport=1,SctpEndpoint=F1_NRDU
localIpAddress Transport=1,Router=Node_Internal_F1,InterfaceIPv4=NR_DU,AddressIPv4=1
portNumber 38472
sctpProfile Transport=1,SctpProfile=Node_Internal_F1
end
#END Transport=1,SctpEndpoint=F1_NRDU --------------------

crn Transport=1,SctpEndpoint=NG
localIpAddress Transport=1,Router=LTE_NR,InterfaceIPv6=NR,AddressIPv6=NR_S1U_OAM
portNumber 38412
sctpProfile Transport=1,SctpProfile=1
end
#END Transport=1,SctpEndpoint=NG --------------------

crn Transport=1,SctpEndpoint=X2
localIpAddress Transport=1,Router=LTE_NR,InterfaceIPv6=NR,AddressIPv6=NR_S1U_OAM
portNumber 36422
sctpProfile Transport=1,SctpProfile=1
end
#END Transport=1,SctpEndpoint=X2 --------------------

ld Transport=1,Synchronization=1 #SystemCreated
lset Transport=1,Synchronization=1$ fixedPosition true
lset Transport=1,Synchronization=1$ telecomStandard 1

crn Transport=1,Synchronization=1,RadioEquipmentClock=1
minQualityLevel qualityLevelValueOptionI=2,qualityLevelValueOptionII=2,qualityLevelValueOptionIII=1
end
#END Transport=1,Synchronization=1,RadioEquipmentClock=1 --------------------

crn Transport=1,Synchronization=1,TimeSyncIO=1
encapsulation Equipment=1,FieldReplaceableUnit=BB-1,SyncPort=SYNC
end
#END Transport=1,Synchronization=1,TimeSyncIO=1 --------------------

crn Transport=1,Synchronization=1,RadioEquipmentClock=1,RadioEquipmentClockReference=1
adminQualityLevel qualityLevelValueOptionI=2,qualityLevelValueOptionII=2,qualityLevelValueOptionIII=1
administrativeState 1
encapsulation Transport=1,Synchronization=1,TimeSyncIO=1
priority 1
end
#END Transport=1,Synchronization=1,RadioEquipmentClock=1,RadioEquipmentClockReference=1 --------------------

ld Transport=1,VlanPort=LTE_NR
lset Transport=1,VlanPort=LTE_NR$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

ld Transport=1,VlanPort=LTE_CP
lset Transport=1,VlanPort=LTE_CP$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

gs-
confb-

## TN ENDED - DscpPcpMap=1/TwampResponder/SctpProfile=1/SctpEndpoint=1/SctpEndpoint=F1/SctpProfile=Node_Internal_F1/SctpEndpoint=NG/SctpEndpoint=X2/CLOCK##


######################################RN - GNBCUUPFunction=1####################################

confb+
gs+

crn GNBCUUPFunction=1
pLMNIdList mcc=404,mnc=94
dcDlAggActTime 1
dcDlAggExpiryTimer 100
dlPdcpSpsTargetTimeLTE 25
dlPdcpSpsTargetTimeNR 25
endcDataUsageReportEnabled false
endcDlNrRetProhibTimer 400
endcUlNrRetProhibTimer 1000
gNBId {gNBId}
gNBIdLength 26
end
#END GNBCUUPFunction=1 --------------------

crn GNBCUUPFunction=1,EndpointResource=1
end
#END GNBCUUPFunction=1,EndpointResource=1 --------------------

crn GNBCUUPFunction=1,EndpointResource=1,LocalIpEndpoint=1
addressRef Transport=1,Router=LTE_NR,InterfaceIPv6=NR,AddressIPv6=NR_S1U_OAM
interfaceList 4 5 7 6
end
#END GNBCUUPFunction=1,EndpointResource=1,LocalIpEndpoint=1 --------------------

ld GNBCUUPFunction=1
lset GNBCUUPFunction=1$ endpointResourceRef GNBCUUPFunction=1,EndpointResource=1

gs-
confb-



######################################RN - GNBDUFunction=1####################################


confb+
gs+

crn GNBDUFunction=1
gNBDUId 1
gNBId {gNBId}
gNBIdLength 26
pwsEtwsPrimaryInd 8
end
#END GNBDUFunction=1 --------------------

crn GNBDUFunction=1,EndpointResource=1
end
#END GNBDUFunction=1,EndpointResource=1 --------------------

crn GNBDUFunction=1,EndpointResource=1,LocalSctpEndpoint=1
interfaceUsed 3
sctpEndpointRef Transport=1,SctpEndpoint=F1_NRDU
end
#END GNBDUFunction=1,EndpointResource=1,LocalSctpEndpoint=1 --------------------

##############################-----------------------------RN - GNBDUFunction=1 Cell specific Started ------------------###################################

{TN_GNPDUFUNCTION_ELEMENT}

##############################----------------------- RN - GNBDUFunction=1 Cell specific Ended -------------------------###################################

##RN - TermPointToGNBCUCP=1##

crn GNBDUFunction=1,TermPointToGNBCUCP=1
administrativeState 1
ipv4Address 10.0.0.1
ipv6Address ::
end
#END GNBDUFunction=1,TermPointToGNBCUCP=1 --------------------

ld GNBDUFunction=1
lset GNBDUFunction=1$ endpointResourceRef GNBDUFunction=1,EndpointResource=1

gs-
confb-

#################################RN - GNBCUCPFunction=1##############################

confb+
gs+


crn GNBCUCPFunction=1
pLMNId mcc=404,mnc=94
gNBId {gNBId}
gNBIdLength 26
maxCommonProcTime 30
maxNgRetryTime 30
nasInactivityTime 5
ngcDedProcTime 5
tDcOverall 7
end
#END GNBCUCPFunction=1 --------------------

crn GNBCUCPFunction=1,EndpointResource=1
end
#END GNBCUCPFunction=1,EndpointResource=1 --------------------

ld GNBCUCPFunction=1
lset GNBCUCPFunction=1$ endpointResourceRef GNBCUCPFunction=1,EndpointResource=1


crn GNBCUCPFunction=1,AnrFunction=1
end
#END GNBCUCPFunction=1,AnrFunction=1 --------------------

crn GNBCUCPFunction=1,AnrFunction=1,AnrFunctionNR=1
anrCgiMeasIntraFreqEnabled true
anrEndcX2Enabled true
end
#END GNBCUCPFunction=1,AnrFunction=1,AnrFunctionNR=1 --------------------

crn GNBCUCPFunction=1,EUtraNetwork=1
end
#END GNBCUCPFunction=1,EUtraNetwork=1 --------------------

crn GNBCUCPFunction=1,EndpointResource=1,LocalSctpEndpoint=1
interfaceUsed 4
sctpEndpointRef Transport=1,SctpEndpoint=NG
end
#END GNBCUCPFunction=1,EndpointResource=1,LocalSctpEndpoint=1 --------------------

crn GNBCUCPFunction=1,EndpointResource=1,LocalSctpEndpoint=2
interfaceUsed 7
sctpEndpointRef Transport=1,SctpEndpoint=X2
end
#END GNBCUCPFunction=1,EndpointResource=1,LocalSctpEndpoint=2 --------------------

crn GNBCUCPFunction=1,EndpointResource=1,LocalSctpEndpoint=3
interfaceUsed 3
sctpEndpointRef Transport=1,SctpEndpoint=F1_NRCUCP
end
#END GNBCUCPFunction=1,EndpointResource=1,LocalSctpEndpoint=3 --------------------









##############################--RN - GNBCUCPFunction=1 Cell specific Started-------------------###################################

{TN_GNBCUCPFUNCTION_ELEMENT}

##############################RN - GNBCUCPFunction=1 Cell specific ENDED-------------------###################################


crn NodeSupport=1,CpriLinkSupervision=1
end
#END NodeSupport=1,CpriLinkSupervision=1 --------------------

gs-
confb-

################Post Install Parameters#################

confb+
gs+


ld GNBCUCPFunction=1,QciProfileEndcConfigExt=1 #SystemCreated
lset GNBCUCPFunction=1,QciProfileEndcConfigExt=1$ initialUplinkConf 1

ld GNBCUCPFunction=1,SecurityHandling=1 #SystemCreated
lset GNBCUCPFunction=1,SecurityHandling=1$ cipheringAlgoPrio 1 2 0
lset GNBCUCPFunction=1,SecurityHandling=1$ integrityProtectAlgoPrio 2 1
lset GNBCUCPFunction=1,SecurityHandling=1$ personalDataProtectionEnabled true

ld GNBDUFunction=1,Paging=1 #SystemCreated
lset GNBDUFunction=1,Paging=1$ defaultPagingCycle 128
lset GNBDUFunction=1,Paging=1$ n 0
lset GNBDUFunction=1,Paging=1$ nS 1

ld GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 #SystemCreated
lset GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1$ dlMaxRetxThreshold 16
lset GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1$ tPollRetransmitDl 65
lset GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1$ tPollRetransmitUl 65
lset GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1$ tReassemblyDl 50
lset GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1$ tReassemblyUl 50
lset GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1$ ulMaxRetxThreshold 16

ld GNBDUFunction=1,Rrc=1 #SystemCreated
lset GNBDUFunction=1,Rrc=1$ n310 20
lset GNBDUFunction=1,Rrc=1$ n311 1
lset GNBDUFunction=1,Rrc=1$ t300 1500
lset GNBDUFunction=1,Rrc=1$ t301 600
lset GNBDUFunction=1,Rrc=1$ t304 1000
lset GNBDUFunction=1,Rrc=1$ t310 4000
lset GNBDUFunction=1,Rrc=1$ t311 10000

gs-
confb-

"""


TN_02_IPV6creationforanchor = """ 
#########01_IPV6creationforanchor##########

cvms pre_sctp_ENDC_NR

confb+

$reqip = readinput( ipv6 IP for X2 ENDC )
$reqhopadd = readinput( ipv6 nexthop )

get Router=LTEUP,InterfaceIPv4=TN_._UP                      encapsulation  > $encapsulation

gs+

crn Transport=1,Router=LTEUP,InterfaceIPv6=NR
aclEgress
aclIngress
bfdProfile
bfdStaticRoutes 0
dscpNdp 48
egressQosMarking
encapsulation $encapsulation
ingressQosMarking
loopback false
mtu 1500
neighborDiscoveryTimeout 30000
neighborSolicitationInterval 1000
routesHoldDownTimer
trackedInterface				
userLabel
end


crn Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
address  $reqip
configurationMode 0
duidType 0
primaryAddress true
userLabel
end

crn Transport=1,Router=LTEUP,RouteTableIPv6Static=1
end

crn Transport=1,Router=LTEUP,RouteTableIPv6Static=1,Dst=default
dst ::/0
end

crn Transport=1,Router=LTEUP,RouteTableIPv6Static=1,Dst=default,NextHop=NR
address $reqhopadd
adminDistance 1
bfdMonitoring true
discard false
reference
end
gs-

set CXC4012095 FeatureState 1

confbd-





confb+

set CXC4011559 FeatureState 1

set CXC4012504|CXC4012381 featurestate 1


crn ENodeBFunction=1,EndcProfile=1
end

set ENodeBFunction=1,EndcProfile=1 meNbS1TermReqArpLev 0
set ENodeBFunction=1,EndcProfile=1 splitNotAllowedUeArpLev 0

lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci[6789]$ endcProfileRef ENodeBFunction=1,EndcProfile=1

gs+
crn Transport=1,SctpEndpoint=NR
dtlsNodeCredential
dtlsSctpSecurityMode 0
dtlsTrustCategory
localIpAddress Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
portNumber 36422
sctpProfile SctpProfile=1
userLabel
end
gs-

set ENodeBFunction=1       sctpEndcX2Ref Transport=1,SctpEndpoint=NR

set ENodeBFunction=1       upEndcX2IpAddressRef Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR

set ENodeBFunction=1       intraRanIpAddressRef Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR


set ^EUtranCell.*= endcAllowedPlmnList mcc=404,mnc=94,mncLength=2


set SystemFunctions=1,Lm=1,FeatureState=CXC4012218 featurestate 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4010960 featurestate 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4012371 featurestate 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4040008 featurestate 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4012051 featurestate 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4012381 featurestate 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4040005 featurestate 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4011559 featurestate 1


set ENodeBFunction=1  endcX2IpAddrViaS1Active  true



crn ENodeBFunction=1,EndcProfile=2
meNbS1TermReqArpLev 15
splitNotAllowedUeArpLev 0
userLabel
end
gs-

set  ENodeBFunction=1,EndcProfile=2  meNbS1TermReqArpLev  15

set  ENodeBFunction=1,EndcProfile=2 splitNotAllowedUeArpLev 0

set QciTable=default,QciProfilePredefined=qci5$              endcProfileRef    EndcProfile=2
set QciTable=default,QciProfilePredefined=qci1$              endcProfileRef    ENodeBFunction=1,EndcProfilePredefined=3
set QciTable=default,QciProfilePredefined=qci2$              endcProfileRef    ENodeBFunction=1,EndcProfilePredefined=3


confb-


################################02_Anchornodesctp##################





confb+

set CXC4011559 FeatureState 1

set CXC4012504|CXC4012381 featurestate 1


crn ENodeBFunction=1,EndcProfile=1
end

set ENodeBFunction=1,EndcProfile=1 meNbS1TermReqArpLev 0
set ENodeBFunction=1,EndcProfile=1 splitNotAllowedUeArpLev 0

lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci[6789]$ endcProfileRef ENodeBFunction=1,EndcProfile=1

gs+
crn Transport=1,SctpEndpoint=NR
dtlsNodeCredential
dtlsSctpSecurityMode 0
dtlsTrustCategory
localIpAddress Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
portNumber 36422
sctpProfile SctpProfile=1
userLabel
end
gs-

set ENodeBFunction=1       sctpEndcX2Ref Transport=1,SctpEndpoint=NR

set ENodeBFunction=1       upEndcX2IpAddressRef Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR

set ENodeBFunction=1       intraRanIpAddressRef Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR


set ^EUtranCell.*= endcAllowedPlmnList mcc=404,mnc=94,mncLength=2


set SystemFunctions=1,Lm=1,FeatureState=CXC4012218 featurestate 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4010960 featurestate 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4012371 featurestate 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4040008 featurestate 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4012051 featurestate 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4012381 featurestate 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4040005 featurestate 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4011559 featurestate 1


set ENodeBFunction=1  endcX2IpAddrViaS1Active  true



crn ENodeBFunction=1,EndcProfile=2
meNbS1TermReqArpLev 15
splitNotAllowedUeArpLev 0
userLabel
end
gs-

set  ENodeBFunction=1,EndcProfile=2  meNbS1TermReqArpLev  15

set  ENodeBFunction=1,EndcProfile=2 splitNotAllowedUeArpLev 0

set QciTable=default,QciProfilePredefined=qci5$              endcProfileRef    EndcProfile=2
set QciTable=default,QciProfilePredefined=qci1$              endcProfileRef    ENodeBFunction=1,EndcProfilePredefined=3
set QciTable=default,QciProfilePredefined=qci2$              endcProfileRef    ENodeBFunction=1,EndcProfilePredefined=3


confb-

"""

TN_03_ENDCanchornode_ROTN = """ 

cvms pre_Termpoint_cre22q2

$gnbid = readinput(gnbid from 5g node )
$reqip = readinput(AddressIPv6=NR )

crn ENodeBFunction=1,GUtraNetwork=1
userLabel
end

crn ENodeBFunction=1,GUtraNetwork=1,ExternalGNodeBFunction=40494-$gnbid
dirDataPathAvail true
eNBVlanPortRef
gNodeBId $gnbid
gNodeBIdLength 26
gNodeBPlmnId mcc=404,mnc=94,mncLength=2
userLabel
end

crn ENodeBFunction=1,GUtraNetwork=1,ExternalGNodeBFunction=40494-$gnbid,TermPointToGNB=40494-$gnbid
additionalCnRef
administrativeState 0
domainName
ipAddress 0.0.0.0
ipAddress2
ipsecEpAddress ::
ipv6Address $reqip
ipv6Address2
upIpAddress ::
end

deb TermPointToGNB


"""


TN_Termpoint_GUtranFreqRelation = """ 
#########01_IPV6creationforanchor##########

cvms pre_sctp_ENDC_NR

confb+

lt all

get Router=LTE_NR,InterfaceIPv6=NR,AddressIPv6=NR_S1U_OAM usedAddress > $reqip

get outer=LTE_NR,RouteTableIPv6Static=2,Dst=.*,NextHop= address > $reqhopadd

get Router=.*,InterfaceIPv4=.*_UP   encapsulation  > $encapsulation

get GNBDUFunction=1 gNBId$ > $gnbid


gs+

crn Transport=1,Router=LTEUP,InterfaceIPv6=NR
aclEgress
aclIngress
bfdProfile
bfdStaticRoutes 0
dscpNdp 48
egressQosMarking
encapsulation $encapsulation
ingressQosMarking
loopback false
mtu 1500
neighborDiscoveryTimeout 30000
neighborSolicitationInterval 1000
routesHoldDownTimer
trackedInterface				
userLabel
end


crn Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
address  $reqip
configurationMode 0
duidType 0
primaryAddress true
userLabel
end

crn Transport=1,Router=LTEUP,RouteTableIPv6Static=1
end

crn Transport=1,Router=LTEUP,RouteTableIPv6Static=1,Dst=default
dst ::/0
end

crn Transport=1,Router=LTEUP,RouteTableIPv6Static=1,Dst=default,NextHop=NR
address $reqhopadd
adminDistance 1
bfdMonitoring true
discard false
reference
end
gs-

set CXC4012095 FeatureState 1

confbd-





confb+

set CXC4011559 FeatureState 1

set CXC4012504|CXC4012381 featurestate 1


crn ENodeBFunction=1,EndcProfile=1
end

set ENodeBFunction=1,EndcProfile=1 meNbS1TermReqArpLev 0
set ENodeBFunction=1,EndcProfile=1 splitNotAllowedUeArpLev 0

lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci[6789]$ endcProfileRef ENodeBFunction=1,EndcProfile=1

gs+
crn Transport=1,SctpEndpoint=NR
dtlsNodeCredential
dtlsSctpSecurityMode 0
dtlsTrustCategory
localIpAddress Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
portNumber 36422
sctpProfile SctpProfile=1
userLabel
end
gs-

set ENodeBFunction=1       sctpEndcX2Ref Transport=1,SctpEndpoint=NR

set ENodeBFunction=1       upEndcX2IpAddressRef Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR

set ENodeBFunction=1       intraRanIpAddressRef Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR


set ^EUtranCell.*= endcAllowedPlmnList mcc=404,mnc=94,mncLength=2


set SystemFunctions=1,Lm=1,FeatureState=CXC4012218 featurestate 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4010960 featurestate 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4012371 featurestate 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4040008 featurestate 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4012051 featurestate 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4012381 featurestate 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4040005 featurestate 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4011559 featurestate 1


set ENodeBFunction=1  endcX2IpAddrViaS1Active  true



crn ENodeBFunction=1,EndcProfile=2
meNbS1TermReqArpLev 15
splitNotAllowedUeArpLev 0
userLabel
end
gs-

set  ENodeBFunction=1,EndcProfile=2  meNbS1TermReqArpLev  15

set  ENodeBFunction=1,EndcProfile=2 splitNotAllowedUeArpLev 0

set QciTable=default,QciProfilePredefined=qci5$              endcProfileRef    EndcProfile=2
set QciTable=default,QciProfilePredefined=qci1$              endcProfileRef    ENodeBFunction=1,EndcProfilePredefined=3
set QciTable=default,QciProfilePredefined=qci2$              endcProfileRef    ENodeBFunction=1,EndcProfilePredefined=3


confb-


##############################################Termpoint###########################################################


crn ENodeBFunction=1,GUtraNetwork=1
userLabel
end

crn ENodeBFunction=1,GUtraNetwork=1,ExternalGNodeBFunction=40494-$gnbid
dirDataPathAvail true
eNBVlanPortRef
gNodeBId $gnbid
gNodeBIdLength 26
gNodeBPlmnId mcc=404,mnc=94,mncLength=2
userLabel
end

crn ENodeBFunction=1,GUtraNetwork=1,ExternalGNodeBFunction=40494-$gnbid,TermPointToGNB=40494-$gnbid
additionalCnRef
administrativeState 0
domainName
ipAddress 0.0.0.0
ipAddress2
ipsecEpAddress ::
ipv6Address $reqip
ipv6Address2
upIpAddress ::
end

deb TermPointToGNB


##################################GutranFreqRelation Creation#########################################



ma L21_12_21 ^EUtranCell.DD
for $mo in L21_12_21
$mordn = rdn($mo)
pr ENodeBFunction=1,$mordn,GUtranFreqRelation=629952
if $nr_of_mos = 0
cr ENodeBFunction=1,$mordn,GUtranFreqRelation=629952
GUtraNetwork=1,GUtranSyncSignalFrequency=629952-30
fi
done
func Relation_121L21
for $j = 1 to 5
pr GUtraNetwork=1,ExternalGNodeBFunction=40494-$gnbid,ExternalGUtranCell=40494-000000$gnbid-31$j
if $nr_of_mos = 1
crn ENodeBFunction=1,$mordn,GUtranFreqRelation=629952,GUtranCellRelation=40494-000000$gnbid-31$j
essEnabled false
isRemoveAllowed false
neighborCellRef GUtraNetwork=1,ExternalGNodeBFunction=40494-$gnbid,ExternalGUtranCell=40494-000000$gnbid-31$j
userLabel
end
fi
done
endfunc

func Relation_121L2_18L
for $mo in L21_12_21
$mordn = rdn($mo)
Relation_121L21
done
endfunc

Relation_121L2_18L


lt all
get lgutran res


"""

TN_05_5G_LMS_GPL_ROTN = """

lt all
rbs
rbs

confb+

crn NodeSupport=1,ServiceDiscovery=1
localAddress Transport=1,Router=LTE_NR,InterfaceIPv6=NR,AddressIPv6=NR_S1U_OAM
nodeCredential
primaryGsds host=localhost,hostIPs=,port=8301,serviceArea=NR_NSA
secondaryGsds
trustCategory SecM=1,CertM=1,TrustCategory=1
end

set NodeSupport=1,ServiceDiscovery=1 trustCategory SecM=1,CertM=1,TrustCategory=1

crn ENodeBFunction=1,EndcProfile=1
end

set ENodeBFunction=1,EndcProfile=1 meNbS1TermReqArpLev 0
set ENodeBFunction=1,EndcProfile=1 splitNotAllowedUeArpLev 0

lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci[6789]$ endcProfileRef ENodeBFunction=1,EndcProfile=1

lbl NRCellDU|carrier



cr Transport=1,Router=LTE_NR,DnsClient=1
set DnsClient=1 dscp 28



confbd+

set Transport=1,SctpEndpoint=F1$ localIpAddress Router=LTE_NR,InterfaceIPv6=NR,AddressIPv6=NR_S1U_OAM

set  Transport=1,SctpEndpoint=NG localIpAddress Router=LTE_NR,InterfaceIPv6=NR,AddressIPv6=NR_S1U_OAM

set Transport=1,SctpEndpoint=X2 localIpAddress Router=LTE_NR,InterfaceIPv6=NR,AddressIPv6=NR_S1U_OAM

set GNBCUUPFunction=1,EndpointResource=1,LocalIpEndpoint=1 addressRef Router=LTE_NR,InterfaceIPv6=NR,AddressIPv6=NR_S1U_OAM


crn Transport=1,SctpEndpoint=X2_ENDC
dtls
dtlsNodeCredential
dtlsSctpSecurityMode 0
dtlsTrustCategory
localIpAddress Transport=1,Router=LTE_NR,InterfaceIPv6=NR,AddressIPv6=X2_ENDC
portNumber 36422
sctpProfile SctpProfile=1
userLabel
end

set ENodeBFunction=1     upEndcX2IpAddressRef Router=LTE_NR,InterfaceIPv6=NR,AddressIPv6=X2_ENDC

set ENodeBFunction=1     sctpEndcX2Ref Transport=1,SctpEndpoint=X2_ENDC

set TwampResponder=1 ipAddress Router=LTE_NR,InterfaceIPv6=NR,AddressIPv6=NR_S1U_OAM

set ENodeBFunction=1 dlBbCapacityTarget 300

confd-

lbl NRCellDU|carrier


get GNBCUUPFunction=1                                       gNBId$ > $gnbid

get nrcelldu ssbFrequency$
set NRCellDU=.* ssbFrequency 629952


get GNBCUUPFunction=1                                       gNBId$ > $gnbid

get Router=LTE_NR,InterfaceIPv6=NR,AddressIPv6=NR_S1U_OAM ^address$ > $reqip

crn ENodeBFunction=1,GUtraNetwork=1
simpleGUtranFreqSmtc false
userLabel
end


crn ENodeBFunction=1,GUtraNetwork=1,ExternalGNodeBFunction=40494-$gnbid
dirDataPathAvail true
eNBVlanPortRef
gNodeBId $gnbid
gNodeBIdLength 26
gNodeBPlmnId mcc=404,mnc=94,mncLength=2
userLabel
end

crn ENodeBFunction=1,GUtraNetwork=1,ExternalGNodeBFunction=40494-$gnbid,TermPointToGNB=40494-$gnbid
additionalCnRef
administrativeState 0
domainName
ipAddress 0.0.0.0
ipAddress2
ipsecEpAddress ::
ipv6Address $reqip
ipv6Address2
upIpAddress ::
end

deb TermPointToGNB

get Router=LTE_NR,RouteTableIPv6Static=1,Dst=ENM_SGW,NextHop=1  address > $nexthop

mcc Router=LTE_NR,InterfaceIPv6=NR,AddressIPv6=NR_S1U_OAM ping6 $nexthop

cr Transport=1,Router=LTE_NR,TwampResponder=LTE
Router=LTE_NR,InterfaceIPv4=LTE_UP,AddressIPv4=LTE_UP
4001
set Router=LTE_NR,TwampResponder=LTE userLabel TWAMP_LTE



set CommonBeamforming=1 digitalTilt 30

confbd-

########################################### 5G GPL+LMS #####################################################################################
                                                                                                                    
lt all                                                                                                                                                                                                                 
rbs                                                                                                                                                                                                                    
rbs                                                                                                                                                                                                                    
                                                                                                                                                                                                                       
confbd+                                                                                                                                                                                                                
$date = `date +%y%m%d_%H%M`                                                                                                                                                                                            
cvms Pre_GPL_LMS_LTE_TN_R_PA_19_$date=                                                                                                                                                                                 
                                                                                                                                                                                                                       
#GPL                                                                                                                                                                                                                   
                                                                                                                                                                                                                       
                                                                                                                                                                                                                       
set CXC4012371 featurestate 1                                                                                                                                                                                          
set CXC4012381 featurestate 1                                                                                                                                                                                          
set CXC4012504 featurestate 1                                                                                                                                                                                          
set CXC4012218 featurestate 1                                                                                                                                                                                          
set CXC4011559 featurestate 1                                                                                                                                                                                          
set CXC4012324 featurestate 1                                                                                                                                                                                          
set CXC4012385 featurestate 1                                                                                                                                                                                          
set CXC4012503 featurestate 1                                                                                                                                                                                          
set CXC4011967 featurestate 1                                                                                                                                                                                          
set CXC4011251 featurestate 1                                                                                                                                                                                          
set CXC4011163 featurestate 1                                                                                                                                                                                          
set CXC4011063 featurestate 1                                                                                                                                                                                          
set CXC4011345 featurestate 1                                                                                                                                                                                          
set CXC4011815 featurestate 1                                                                                                                                                                                          
set CXC4011477 featurestate 1                                                                                                                                                                                          
set CXC4012480 featurestate 0                                                                                                                                                                                          
set CXC4010620 featurestate 1                                                                                                                                                                                          
set CXC4012015 featurestate 1                                                                                                                                                                                          
                                                                                                                                                                                                                       
cr ENodeBFunction=1,GeraNetwork=1                                                                                                                                                                                      
                                                                                                                                                                                                                       
                                                                                                                                                                                                                       
cr ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1                                                                                                                                                                     
1 #frequencyGroupId                                                                                                                                                                                                    
                                                                                                                                                                                                                       
func Gran_freq                                                                                                                                                                                                         
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=$t                                                                                                                                                                    
$t                                                                                                                                                                                                                     
0                                                                                                                                                                                                                      
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=$t geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1                                                                                                 
endfunc                                                                                                                                                                                                                
                                                                                                                                                                                                                       
for $t = 744 to 768                                                                                                                                                                                                    
Gran_freq                                                                                                                                                                                                              
done                                                                                                                                                                                                                   
                                                                                                                                                                                                                       
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39150                                                                                                                                                               
39150                                                                                                                                                                                                                  
                                                                                                                                                                                                                       
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39294                                                                                                                                                               
39294                                                                                                                                                                                                                  
                                                                                                                                                                                                                       
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3710                                                                                                                                                                
3710                                                                                                                                                                                                                   
                                                                                                                                                                                                                       
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=390                                                                                                                                                                 
390                                                                                                                                                                                                                    
                                                                                                                                                                                                                       
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1615                                                                                                                                                                
1615                                                                                                                                                                                                                   
                                                                                                                                                                                                                       
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39151                                                                                                                                                               
39151                                                                                                                                                                                                                  
                                                                                                                                                                                                                       
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39295                                                                                                                                                               
39295                                                                                                                                                                                                                  
                                                                                                                                                                                                                       
                                                                                                                                                                                                                       
unset all                                                                                                                                                                                                              
                                                                                                                                                                                                                       
$Par[1] = L2100                                                                                                                                                                                                        
$Par[2] = TDD20                                                                                                                                                                                                        
$Par[3] = TDD10                                                                                                                                                                                                        
$Par[4] = L1800                                                                                                                                                                                                        
$Par[5] = L900                                                                                                                                                                                                         
                                                                                                                                                                                                                       
mr L2100                                                                                                                                                                                                               
mr TDD20                                                                                                                                                                                                               
mr TDD10                                                                                                                                                                                                               
mr L1800                                                                                                                                                                                                               
mr L900                                                                                                                                                                                                                
                                                                                                                                                                                                                       
                                                                                                                                                                                                                       
ma L2100 EUtranCellFDD earfcn 390                                                                                                                                                                                      
ma L1800 EUtranCellFDD earfcn 1615                                                                                                                                                                                     
ma TDD10 EUtranCellTDD earfcn 39294                                                                                                                                                                                    
ma TDD20 EUtranCellTDD earfcn 39150                                                                                                                                                                                    
ma L900 EUtranCellFDD earfcn 3710                                                                                                                                                                                      
                                                                                                                                                                                                                       
func Gran_Rel                                                                                                                                                                                                          
for $mo in $Par[$i]                                                                                                                                                                                                    
 $mordn = rdn($mo)                                                                                                                                                                                                     
 pr $mordn,GeranFreqGroupRelation=1                                                                                                                                                                                    
 if $nr_of_mos = 0                                                                                                                                                                                                     
  cr ENodeBFunction=1,$mordn,GeranFreqGroupRelation=1                                                                                                                                                                  
  ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1                                                                                                                                                                      
  1                                                                                                                                                                                                                    
 fi                                                                                                                                                                                                                    
done                                                                                                                                                                                                                   
endfunc                                                                                                                                                                                                                
                                                                                                                                                                                                                       
func EURel_39150                                                                                                                                                                                                       
for $mo in $Par[$i]                                                                                                                                                                                                    
 $mordn = rdn($mo)                                                                                                                                                                                                     
 pr $mordn,EUtranFreqRelation=39150                                                                                                                                                                                    
 if $nr_of_mos = 0                                                                                                                                                                                                     
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=39150                                                                                                                                                                  
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39150                                                                                                                                                                
  6                                                                                                                                                                                                                    
 fi                                                                                                                                                                                                                    
done                                                                                                                                                                                                                   
endfunc                                                                                                                                                                                                                
                                                                                                                                                                                                                       
func EURel_39294                                                                                                                                                                                                       
for $mo in $Par[$i]                                                                                                                                                                                                    
 $mordn = rdn($mo)                                                                                                                                                                                                     
 pr $mordn,EUtranFreqRelation=39294                                                                                                                                                                                    
 if $nr_of_mos = 0                                                                                                                                                                                                     
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=39294                                                                                                                                                                  
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39294                                                                                                                                                                
  5                                                                                                                                                                                                                    
 fi                                                                                                                                                                                                                    
done                                                                                                                                                                                                                   
endfunc                                                                                                                                                                                                                
                                                                                                                                                                                                                       
func EURel_390                                                                                                                                                                                                         
for $mo in $Par[$i]                                                                                                                                                                                                    
 $mordn = rdn($mo)                                                                                                                                                                                                     
 pr $mordn,EUtranFreqRelation=390$                                                                                                                                                                                     
 if $nr_of_mos = 0                                                                                                                                                                                                     
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=390                                                                                                                                                                    
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=390                                                                                                                                                                  
  3                                                                                                                                                                                                                    
 fi                                                                                                                                                                                                                    
done                                                                                                                                                                                                                   
endfunc                                                                                                                                                                                                                
                                                                                                                                                                                                                       
func EURel_1615                                                                                                                                                                                                        
for $mo in $Par[$i]                                                                                                                                                                                                    
 $mordn = rdn($mo)                                                                                                                                                                                                     
 pr $mordn,EUtranFreqRelation=1615                                                                                                                                                                                     
 if $nr_of_mos = 0                                                                                                                                                                                                     
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=1615                                                                                                                                                                   
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1615                                                                                                                                                                 
  4                                                                                                                                                                                                                    
 fi                                                                                                                                                                                                                    
done                                                                                                                                                                                                                   
endfunc                                                                                                                                                                                                                
                                                                                                                                                                                                                       
func EURel_3710                                                                                                                                                                                                        
for $mo in $Par[$i]                                                                                                                                                                                                    
 $mordn = rdn($mo)                                                                                                                                                                                                     
 pr $mordn,EUtranFreqRelation=3710                                                                                                                                                                                     
 if $nr_of_mos = 0                                                                                                                                                                                                     
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=3710                                                                                                                                                                   
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3710                                                                                                                                                                 
  2                                                                                                                                                                                                                    
 fi                                                                                                                                                                                                                    
done                                                                                                                                                                                                                   
endfunc                                                                                                                                                                                                                
                                                                                                                                                                                                                       
func EURel_1529                                                                                                                                                                                                        
for $mo in $Par[$i]                                                                                                                                                                                                    
 $mordn = rdn($mo)                                                                                                                                                                                                     
 pr $mordn,EUtranFreqRelation=1529                                                                                                                                                                                     
 if $nr_of_mos = 0                                                                                                                                                                                                     
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=1529                                                                                                                                                                   
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1529                                                                                                                                                                 
  7                                                                                                                                                                                                                    
 fi                                                                                                                                                                                                                    
done                                                                                                                                                                                                                   
endfunc                                                                                                                                                                                                                
                                                                                                                                                                                                                       
for $i = 1 to 5                                                                                                                                                                                                        
EURel_39294                                                                                                                                                                                                            
EURel_39150                                                                                                                                                                                                            
EURel_390                                                                                                                                                                                                              
EURel_1615                                                                                                                                                                                                             
EURel_3710                                                                                                                                                                                                             
Gran_Rel                                                                                                                                                                                                               
done                                                                                                                                                                                                                   
                                                                                                                                                                                                                       
######                                                                                                                                                                                                                 
                                                                                                                                                                                                                       
                                                                                                                                                                                                                       
set ENodeBFunction=1,EUtranCell.*DD= endcSetupDlPktVolThr 5                                                                                                                                                            
set EUtranCell.*DD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1 hysteresisA5 20                                                                                                                                           
set UePolicyOptimization=1  endcAwareImc 2                                                                                                                                                                             
                                                                                                                                                                                                                       
set CarrierAggregationFunction=1 dcSCellActDeactDataThres 30                                                                                                                                                           
set CarrierAggregationFunction=1 dcSCellActDeactDataThresHyst 30                                                                                                                                                       
set CarrierAggregationFunction=1 dcSCellDeactDelayTimer 200                                                                                                                                                            
set CarrierAggregationFunction=1 endcCaPolicy 1                                                                                                                                                                        
set EUtranCell.DD=.*,UeMeasControl=1 endcMeasRestartTime 10000                                                                                                                                                         
set EUtranCell.DD=.*  measGapPattEndc 1                                                                                                                                                                                
set ENodeBFunction=1   endcS1OverlapMode True                                                                                                                                                                          
set ENodeBFunction=1   x2retryTimerMaxAuto 1440                                                                                                                                                                        
set EUtranCell.DD=.*,UeMeasControl=1 endcMeasTime 2000                                                                                                                                                                 
set EUtranCell.DD=.*,UeMeasControl=1 endcB1MeasWindow 40                                                                                                                                                               
set EUtranCell.DD=.*,UeMeasControl=1 maxMeasB1Endc 3                                                                                                                                                                   
set ENodeBFunction=1       endcDataUsageReportEnabled true                                                                                                                                                             
set ENodeBFunction=1       zzzTemporary81    1                                                                                                                                                                         
crn ENodeBFunction=1,EndcProfile=2                                                                                                                                                                                     
meNbS1TermReqArpLev 15                                                                                                                                                                                                 
splitNotAllowedUeArpLev 0                                                                                                                                                                                              
userLabel                                                                                                                                                                                                              
end                                                                                                                                                                                                                    
                                                                                                                                                                                                                       
set  ENodeBFunction=1,EndcProfile=2  meNbS1TermReqArpLev  15                                                                                                                                                           
set  ENodeBFunction=1,EndcProfile=2 splitNotAllowedUeArpLev 0                                                                                                                                                          
set QciTable=default,QciProfilePredefined=qci5              endcProfileRef    EndcProfile=2                                                                                                                            
set QciTable=default,QciProfilePredefined=qci1              endcProfileRef    ENodeBFunction=1,EndcProfilePredefined=3                                                                                                 
set QciTable=default,QciProfilePredefined=qci2              endcProfileRef    ENodeBFunction=1,EndcProfilePredefined=3                                                                                                 
                                                                                                                                                                                                                       
                                                                                                                                                                                                                       
ma cellockqqwer  ^eutrancell administrativeState 0                                                                                                                                                                     
lbl  cell                                                                                                                                                                                                              
ldeb cell                                                                                                                                                                                                              
lbl cellockqqwer                                                                                                                                                                                                       
                                                                                                                                                                                                                       
#LMS                                                                                                                                                                                                                   
                                                                                                                                                                                                                       
#set EUtranCell.DD=.*  primaryUpperLayerInd 1                                                                                                                                                                          
#set EUtranCell.DD=.*  additionalUpperLayerIndList 1 1 1 1 1                                                                                                                                                           
set ^EUtranCell.DD=.* endcAllowedPlmnList mcc=404,mnc=94,mnclength=2                                                                                                                                                   
                                                                                                                                                                                                                       
                                                                                                                                                                                                                       
set EUtranFreqRelation=390$ endcHoFreqPriority 7                                                                                                                                                                       
set EUtranFreqRelation=1615 endcHoFreqPriority 2                                                                                                                                                                       
set EUtranFreqRelation=39151 endcHoFreqPriority -1                                                                                                                                                                     
set EUtranFreqRelation=39295 endcHoFreqPriority -1                                                                                                                                                                     
set EUtranFreqRelation=39150 endcHoFreqPriority -1                                                                                                                                                                     
set EUtranFreqRelation=39294 endcHoFreqPriority -1                                                                                                                                                                     
set EUtranFreqRelation=3710 endcHoFreqPriority 6                                                                                                                                                                       
                                                                                                                                                                                                                       
set EUtranFreqRelation=390$ endcAwareIdleModePriority 6                                                                                                                                                                
set EUtranFreqRelation=1615 endcAwareIdleModePriority 2                                                                                                                                                                
set EUtranFreqRelation=39151 endcAwareIdleModePriority 7                                                                                                                                                               
set EUtranFreqRelation=39295 endcAwareIdleModePriority 7                                                                                                                                                               
set EUtranFreqRelation=39150 endcAwareIdleModePriority 5                                                                                                                                                               
set EUtranFreqRelation=39294 endcAwareIdleModePriority 4                                                                                                                                                               
set EUtranFreqRelation=3710 endcAwareIdleModePriority 3                                                                                                                                                                
                                                                                                                                                                                                                       
                                                                                                                                                                                                                       
                                                                                                                                                                                                                       
##need to add small cell arfcn                                                                                                                                                                                         
                                                                                                                                                                                                                       
cr ENodeBFunction=1,UePolicyOptimization=1                                                                                                                                                                             
set UePolicyOptimization=1 endcAwareImc 2                                                                                                                                                                              
set UePolicyOptimization=1      t320              180                                                                                                                                                                  
set UePolicyOptimization=1      zzzTemporary1 1                                                                                                                                                                        
set GUtranFreqRelation=629952    endcB1MeasPriority 7                                                                                                                                                                  
set ENodeBFunction=1       endcAllowed       true                                                                                                                                                                      
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= triggerQuantityA5 0                                                                                                                                         
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= reportQuantityA5  0                                                                                                                                         
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= timeToTriggerA5  100                                                                                                                                        
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= a5Threshold1Rsrp -44                                                                                                                                        
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= a5Threshold1Rsrq -195                                                                                                                                       
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= a5Threshold2Rsrp -112                                                                                                                                       
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= a5Threshold2Rsrq -195                                                                                                                                       
#set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= hysteresisA5 20                                                                                                                                            
                                                                                                                                                                                                                       
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB1GUtra=1 triggerQuantityB1 0                                                                                                                                         
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB1GUtra=1 b1ThresholdRsrp -110                                                                                                                                        
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB1GUtra=1 b1ThresholdRsrq -435                                                                                                                                        
                                                                                                                                                                                                                       
set EUtranCell.DD=.*,GUtranFreqRelation=629952 b1ThrRsrpFreqOffset 0                                                                                                                                                   
set EUtranCell.DD=.*,GUtranFreqRelation=629952 b1ThrRsrqFreqOffset 0                                                                                                                                                   
set EUtranCell.DD=.*,GUtranFreqRelation=629952 qOffsetFreq 0                                                                                                                                                           
set EUtranCell.DD=.*,GUtranFreqRelation=629952 anrMeasOn true                                                                                                                                                          
                                                                                                                                                                                                                       
set EUtranCell.DD=.*,EUtranFreqRelation qOffsetFreq 0                                                                                                                                                                  
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB1GUtra=1 hysteresisB1     0                                                                                                                                          
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB1GUtra=1 timeToTriggerB1  480                                                                                                                                        
                                                                                                                                                                                                                       
set LoadBalancingFunction=1        lbAllowedForEndcUe False                                                                                                                                                            
set EUtranCell.DD=.* lbActionForEndcUe 0                                                                                                                                                                               
set ENodeBFunction=1               endcSplitAllowedMoVoice false                                                                                                                                                       
                                                                                                                                                                                                                       
set EUtranCellRelation cellIndividualOffsetEUtran 0                                                                                                                                                                    
                                                                                                                                                                                                                       
###added SubscriberGroupProfile=ENDC(PA13)                                                                                                                                                                             
#set ENodeBFunction=1,SubscriberGroupProfile=ENDC                                                                                                                                                                      
#customTriggerType 2                                                                                                                                                                                                   
#customTriggerList 2                                                                                                                                                                                                   
#qciOffsetForQCI6 0                                                                                                                                                                                                    
#qciOffsetForQCI9 0                                                                                                                                                                                                    
#end                                                                                                                                                                                                                   
#set SubscriberGroupProfile=ENDC profilePriority 5                                                                                                                                                                     
                                                                                                                                                                                                                       
###added Qci30=Qci6 and Qci31=Qci9//set eutranFreqToQciProfileRelation values (PA13)                                                                                                                                   
                                                                                                                                                                                                                       
#crn ENodeBFunction=1,QciTable=default,QciProfileOperatordefined=qci30                                                                                                                                                 
#absPrioOverride                      0                                                                                                                                                                                
#aqmMode                              1                                                                                                                                                                                
#bitRateRecommendationEnabled         false                                                                                                                                                                            
#caOffloadingEnabled                  false                                                                                                                                                                            
#counterActiveMode                    false                                                                                                                                                                            
#dataFwdPerQciEnabled                 true                                                                                                                                                                             
#dlMaxHARQTxQci                       5                                                                                                                                                                                
#dlMaxWaitingTime                     0                                                                                                                                                                                
#dlMinBitRate                         2000                                                                                                                                                                             
#dlResourceAllocationStrategy         1                                                                                                                                                                                
#drxPriority                          0                                                                                                                                                                                
#drxProfileRef                        ENodeBFunction=1,DrxProfile=0                                                                                                                                                    
#dscp                                 32                                                                                                                                                                               
#endcProfileRef                       EndcProfile=1                                                                                                                                                                    
#harqPriority                         0                                                                                                                                                                                
#inactivityTimerOffset                0                                                                                                                                                                                
#laaSupported                         true                                                                                                                                                                             
#lessMaxDelayThreshold                0                                                                                                                                                                                
#logicalChannelGroupRef               QciTable=default,LogicalChannelGroup=3                                                                                                                                           
#paPartitionOverride                  false                                                                                                                                                                            
#pdb                                  300                                                                                                                                                                              
#pdbOffset                            0                                                                                                                                                                                
#pdcpSNLength                         12                                                                                                                                                                               
#priority                             6                                                                                                                                                                                
#priorityFraction                     0                                                                                                                                                                                
#qci                                  30                                                                                                                                                                               
#qciACTuning                          1000                                                                                                                                                                             
#qciSubscriptionQuanta                200                                                                                                                                                                              
#relativePriority                     2                                                                                                                                                                                
#resourceAllocationStrategy           1                                                                                                                                                                                
#resourceType                         0                                                                                                                                                                                
#rlcMode                              0                                                                                                                                                                                
#rlcSNLength                          10                                                                                                                                                                               
#rlfPriority                          0                                                                                                                                                                                
#rlfProfileRef                        RlfProfile=0                                                                                                                                                                     
#rohcEnabled                          false                                                                                                                                                                            
#rohcForUlDataEnabled                 false                                                                                                                                                                            
#schedulingAlgorithm                  4                                                                                                                                                                                
#serviceType                          0                                                                                                                                                                                
#srsAllocationStrategy                0                                                                                                                                                                                
#tReorderingDl                        35                                                                                                                                                                               
#tReorderingUl                        60                                                                                                                                                                               
#timerPriority                        0                                                                                                                                                                                
#timerProfileRef                                                                                                                                                                                                       
#ulMaxHARQTxQci                       5                                                                                                                                                                                
#ulMaxWaitingTime                     0                                                                                                                                                                                
#ulMinBitRate                         300                                                                                                                                                                              
#zzzTemporary1                                                                                                                                                                                                         
#zzzTemporary2                                                                                                                                                                                                         
#zzzTemporary3                        -2000000000                                                                                                                                                                      
#zzzTemporary4                        -2000000000                                                                                                                                                                      
#zzzTemporary5                        -2000000000                                                                                                                                                                      
#end                                                                                                                                                                                                                   
                                                                                                                                                                                                                       
#crn ENodeBFunction=1,QciTable=default,QciProfileOperatordefined=qci31                                                                                                                                                 
#absPrioOverride                      0                                                                                                                                                                                
#aqmMode                              1                                                                                                                                                                                
#bitRateRecommendationEnabled         false                                                                                                                                                                            
#caOffloadingEnabled                  false                                                                                                                                                                            
#counterActiveMode                    false                                                                                                                                                                            
#dataFwdPerQciEnabled                 true                                                                                                                                                                             
#dlMaxHARQTxQci                       5                                                                                                                                                                                
#dlMaxWaitingTime                     0                                                                                                                                                                                
#dlMinBitRate                         0                                                                                                                                                                                
#dlResourceAllocationStrategy         1                                                                                                                                                                                
#drxPriority                          0                                                                                                                                                                                
#drxProfileRef                        ENodeBFunction=1,DrxProfile=0                                                                                                                                                    
#dscp                                 26                                                                                                                                                                               
#endcProfileRef                       EndcProfile=1                                                                                                                                                                    
#harqPriority                         0                                                                                                                                                                                
#inactivityTimerOffset                0                                                                                                                                                                                
#laaSupported                         true                                                                                                                                                                             
#lessMaxDelayThreshold                0                                                                                                                                                                                
#logicalChannelGroupRef               QciTable=default,LogicalChannelGroup=3                                                                                                                                           
#paPartitionOverride                  false                                                                                                                                                                            
#pdb                                  300                                                                                                                                                                              
#pdbOffset                            0                                                                                                                                                                                
#pdcpSNLength                         12                                                                                                                                                                               
#priority                             9                                                                                                                                                                                
#priorityFraction                     0                                                                                                                                                                                
#qci                                  31                                                                                                                                                                               
#qciACTuning                          1000                                                                                                                                                                             
#qciSubscriptionQuanta                200                                                                                                                                                                              
#relativePriority                     1                                                                                                                                                                                
#resourceAllocationStrategy           1                                                                                                                                                                                
#resourceType                         0                                                                                                                                                                                
#rlcMode                              0                                                                                                                                                                                
#rlcSNLength                          10                                                                                                                                                                               
#rlfPriority                          0                                                                                                                                                                                
#rlfProfileRef                        RlfProfile=0                                                                                                                                                                     
#rohcEnabled                          false                                                                                                                                                                            
#rohcForUlDataEnabled                 false                                                                                                                                                                            
#schedulingAlgorithm                  4                                                                                                                                                                                
#serviceType                          0                                                                                                                                                                                
#srsAllocationStrategy                0                                                                                                                                                                                
#tReorderingDl                        35                                                                                                                                                                               
#tReorderingUl                        35                                                                                                                                                                               
#timerPriority                        0                                                                                                                                                                                
#timerProfileRef                                                                                                                                                                                                       
#ulMaxHARQTxQci                       5                                                                                                                                                                                
#ulMaxWaitingTime                     0                                                                                                                                                                                
#ulMinBitRate                         0                                                                                                                                                                                
#zzzTemporary1                                                                                                                                                                                                         
#zzzTemporary2                                                                                                                                                                                                         
#zzzTemporary3                        -2000000000                                                                                                                                                                      
#zzzTemporary4                        -2000000000                                                                                                                                                                      
#zzzTemporary5                        -2000000000                                                                                                                                                                      
#end                                                                                                                                                                                                                   
                                                                                                                                                                                                                       
lt all                                                                                                                                                                                                                 
                                                                                                                                                                                                                       
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA1A2Endc=1 qciA1A2ThrOffsetsEndc  a1a2ThrRsrpQciOffsetEndc=0,a1a2ThrRsrqQciOffsetEndc=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2
ThrRsrpQciOffsetEndc=0,a1a2ThrRsrqQciOffsetEndc=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6                                                                                            
                                                                                                                                                                                                                       
mr TABTAB21                                                                                                                                                                                                            
ma TABTAB21 ^eutrancell arfcn ^390$                                                                                                                                                                                    
pr TABTAB21                                                                                                                                                                                                            
if $nr_of_mos >= 1                                                                                                                                                                                                     
for $mo in TABTAB21                                                                                                                                                                                                    
$mordn = rdn($mo)                                                                                                                                                                                                      
set $mordn,UeMeasControl=1,ReportConfigA1A2Endc=1 qciA1A2ThrOffsetsEndc  a1a2ThrRsrpQciOffsetEndc=0,a1a2ThrRsrqQciOffsetEndc=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQci
OffsetEndc=0,a1a2ThrRsrqQciOffsetEndc=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6                                                                                                      
set $mordn,UeMeasControl=1,ReportConfigSearch qciA1A2ThrOffsets     qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1                                                                          
done                                                                                                                                                                                                                   
fi                                                                                                                                                                                                                     
                                                                                                                                                                                                                       
mr TABTAB23                                                                                                                                                                                                            
ma TABTAB23 ^eutrancelltdd=                                                                                                                                                                                            
pr TABTAB23                                                                                                                                                                                                            
if $nr_of_mos >= 1                                                                                                                                                                                                     
for $mo in TABTAB23                                                                                                                                                                                                    
$mordn = rdn($mo)                                                                                                                                                                                                      
set $mordn,EUtranFreqRelation=390$  eutranFreqToQciProfileRelation   qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1                                                                         
set $mordn,UeMeasControl=1,ReportConfigSearch qciA1A2ThrOffsets     qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1                                                                          
done                                                                                                                                                                                                                   
fi                                                                                                                                                                                                                     
                                                                                                                                                                                                                       
#mr     TABTAB18                                                                                                                                                                                                       
#ma TABTAB18 ^eutrancell earfcn  ^1615                                                                                                                                                                                 
#pr TABTAB18                                                                                                                                                                                                           
#if $nr_of_mos >= 1                                                                                                                                                                                                    
#for $mo in TABTAB18                                                                                                                                                                                                   
#$mordn = rdn($mo)                                                                                                                                                                                                     
#set $mordn,EUtranFreqRelation=390$  eutranFreqToQciProfileRelation   qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1                                                                        
#set $mordn,UeMeasControl=1,ReportConfigSearch qciA1A2ThrOffsets     qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1                                                                         
#done                                                                                                                                                                                                                  
#fi                                                                                                                                                                                                                    
                                                                                                                                                                                                                       
mr      TABTAB09                                                                                                                                                                                                       
ma TABTAB09 ^eutrancell earfcn  ^3710                                                                                                                                                                                  
pr TABTAB09                                                                                                                                                                                                            
if $nr_of_mos >= 1                                                                                                                                                                                                     
for $mo in TABTAB09                                                                                                                                                                                                    
$mordn = rdn($mo)                                                                                                                                                                                                      
set $mordn,EUtranFreqRelation=390$  eutranFreqToQciProfileRelation   qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1                                                                         
set $mordn,UeMeasControl=1,ReportConfigSearch qciA1A2ThrOffsets     qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1                                                                          
done                                                                                                                                                                                                                   
fi                                                                                                                                                                                                                     
                                                                                                                                                                                                                       
set QciTable=default,QciProfilePredefined=qci6$ relativePriority 2                                                                                                                                                     
#set QciTable=default,QciProfileOperatorDefined=qci30$ relativePriority 100                                                                                                                                            
                                                                                                                                                                                                                       
set ANRFunction anrstateNR 1                                                                                                                                                                                           
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1 gNodebIdLength 26                                                                                                                                                   
                                                                                                                                                                                                                       
cr EnodeBfunction=1,PmFlexCounterFilter=ENDC                                                                                                                                                                           
set EnodeBfunction=1,PmFlexCounterFilter=ENDC endcFilterEnabled true                                                                                                                                                   
set EnodeBFunction=1,PmFlexCounterFilter=ENDC endcFilterMin 2                                                                                                                                                          
                                                                                                                                                                                                                       
#New Addition                                                                                                                                                                                                          
                                                                                                                                                                                                                       
set QciTable=default,QciProfilePredefined=qci1$ dscp 34                                                                                                                                                                
set QciTable=default,QciProfilePredefined=qci2$ dscp 34                                                                                                                                                                
set QciTable=default,QciProfilePredefined=qci3$ dscp 26                                                                                                                                                                
set QciTable=default,QciProfilePredefined=qci4$ dscp 26                                                                                                                                                                
set QciTable=default,QciProfilePredefined=qci5$ dscp 46                                                                                                                                                                
set QciTable=default,QciProfilePredefined=qci6$ dscp 32                                                                                                                                                                
set QciTable=default,QciProfilePredefined=qci7$ dscp 40                                                                                                                                                                
set QciTable=default,QciProfilePredefined=qci8$ dscp 30                                                                                                                                                                
set QciTable=default,QciProfilePredefined=qci9$ dscp 26                                                                                                                                                                
#set QciTable=default,QciProfilePredefined=qci30$ dscp 32                                                                                                                                                              
#set QciTable=default,QciProfilePredefined=qci31$ dscp 26                                                                                                                                                              
cr Transport=1,QosProfiles=1,DscpPcpMap=1                                                                                                                                                                              
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp0                                                                                                                                                                        
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp1                                                                                                                                                                        
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp2                                                                                                                                                                        
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp3                                                                                                                                                                        
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp4                                                                                                                                                                        
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp5                                                                                                                                                                        
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp6                                                                                                                                                                        
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp7                                                                                                                                                                        
                                                                                                                                                                                                                       
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp0 0,1,2,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,36,37,38,39,41,43,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63                                           
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp2 22,24,26                                                                                                                                                               
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp3 6,8,10,30,32                                                                                                                                                           
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp4 12,14,40                                                                                                                                                               
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp5 4,28                                                                                                                                                                   
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp6 16,18,34,42,44                                                                                                                                                         
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp7 20,46                                                                                                                                                                  
                                                                                                                                                                                                                       
cr Transport=1,Router=LTEUP,TwampResponder=NR                                                                                                                                                                          
Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR                                                                                                                                                               
4001                                                                                                                                                                                                                   
set Transport=1,Router=LTEUP,TwampResponder=NR userLabel TWAMP-Anchor                                                                                                                                                  
rdel ENodeBFunction=1,SubscriberGroupProfile=ENDC                                                                                                                                                                      
rdel ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci30                                                                                                                                                 
rdel ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci31                                                                                                                                                 
                                                                                                                                                                                                                       
### 23.Q2 ###                                                                                                                                                                                                          
set ANRFunction pciConflictMobilityEcgiMeas true                                                                                                                                                                       
set ANRFunction pciConflictDetectionEcgiMeas false                                                                                                                                                                     
set ENodeBFunction=1 endcAllowed true                                                                                                                                                                                  
                                                                                                                                                                                                                       
                                                                                                                                                                                                                       
ma cellockqqwer  ^eutrancell administrativeState 0                                                                                                                                                                     
lbl  cell                                                                                                                                                                                                              
ldeb cell                                                                                                                                                                                                              
lbl cellockqqwer                                                                                                                                                                                                       
                                                                                                                                                                                                                       
$date = `date +%y%m%d_%H%M`                                                                                                                                                                                            
cvms Post_LMS_LTE_TN_R_PA_19_$date                                                                                                                                                                                     
confbd-                                                                                                                                                                                                                
  
lt all                                                                                                                                                                                                                 
rbs                                                                                                                                                                                                                    
rbs                                                                                                                                                                                                                    
confbd+                                                                                                                                                                                                                
$date = `date +%y%m%d_%H%M`                                                                                                                                                                                            
cvms Pre_GPL_NR_R_PA_19_$date                                                                                                                                                                                          
                                                                                                                                                                                                                       
lbl NRCellDU=.*                                                                                                                                                                                                        
lbl NRSectorCarrier=                                                                                                                                                                                                   
                                                                                                                                                                                                                       
set CXC4012500 featureState 1                                                                                                                                                                                          
set CXC4012273 featurestate 1                                                                                                                                                                                          
set CXC4012375 featurestate 1                                                                                                                                                                                          
set CXC4012549 featurestate 1                                                                                                                                                                                          
set CXC4012492 featurestate 1                                                                                                                                                                                          
set CXC4012534 featurestate 1                                                                                                                                                                                          
set CXC4012347 featurestate 1                                                                                                                                                                                          
set CXC4012325 featurestate 1                                                                                                                                                                                          
set CXC4012493 featurestate 1                                                                                                                                                                                          
set CXC4012558 featurestate 1                                                                                                                                                                                          
set CXC4012272 featurestate 1                                                                                                                                                                                          
set CXC4012502 featurestate 1                                                                                                                                                                                          
set CXC4012510 FeatureState 1                                                                                                                                                                                          
set CXC4012587 FeatureState 1                                                                                                                                                                                          
set CXC4010319 featureState 1                                                                                                                                                                                          
set CXC4010320 featureState 1                                                                                                                                                                                          
set CXC4010609 featureState 1                                                                                                                                                                                          
set CXC4010613 featureState 1                                                                                                                                                                                          
set CXC4010616 featureState 1                                                                                                                                                                                          
set CXC4010618 featureState 1                                                                                                                                                                                          
set CXC4010620 featureState 1                                                                                                                                                                                          
set CXC4010717 featureState 1                                                                                                                                                                                          
set CXC4010723 featureState 1                                                                                                                                                                                          
set CXC4010770 featureState 1                                                                                                                                                                                          
set CXC4010841 featureState 1                                                                                                                                                                                          
set CXC4010856 featureState 1                                                                                                                                                                                          
set CXC4010912 featureState 1                                                                                                                                                                                          
set CXC4010949 featureState 1                                                                                                                                                                                          
set CXC4010956 featureState 1                                                                                                                                                                                          
set CXC4010959 featureState 1                                                                                                                                                                                          
set CXC4010961 featureState 1                                                                                                                                                                                          
set CXC4010962 featureState 1                                                                                                                                                                                          
set CXC4010963 featureState 1                                                                                                                                                                                          
set CXC4010964 featureState 1                                                                                                                                                                                          
set CXC4010967 featureState 1                                                                                                                                                                                          
set CXC4010973 featureState 1                                                                                                                                                                                          
set CXC4010974 featureState 1                                                                                                                                                                                          
set CXC4010980 featureState 1                                                                                                                                                                                          
set CXC4010990 featureState 1                                                                                                                                                                                          
set CXC4011011 featureState 1                                                                                                                                                                                          
set CXC4011018 featureState 1                                                                                                                                                                                          
set CXC4011033 featureState 1                                                                                                                                                                                          
set CXC4011034 featureState 1                                                                                                                                                                                          
set CXC4011050 featureState 1                                                                                                                                                                                          
set CXC4011056 featureState 1                                                                                                                                                                                          
set CXC4011057 featureState 1                                                                                                                                                                                          
set CXC4011059 featureState 1                                                                                                                                                                                          
set CXC4011060 featureState 1                                                                                                                                                                                          
set CXC4011061 featureState 1                                                                                                                                                                                          
set CXC4011062 featureState 1                                                                                                                                                                                          
set CXC4011063 featureState 1                                                                                                                                                                                          
set CXC4011064 featureState 1                                                                                                                                                                                          
set CXC4011067 featureState 1                                                                                                                                                                                          
set CXC4011068 featureState 1                                                                                                                                                                                          
set CXC4011069 featureState 1                                                                                                                                                                                          
set CXC4011072 featureState 1                                                                                                                                                                                          
set CXC4011074 featureState 1                                                                                                                                                                                          
set CXC4011075 featureState 1                                                                                                                                                                                          
set CXC4011155 featureState 1                                                                                                                                                                                          
set CXC4011157 featureState 1                                                                                                                                                                                          
set CXC4011163 featureState 1                                                                                                                                                                                          
set CXC4011183 featureState 1                                                                                                                                                                                          
set CXC4011245 featureState 1                                                                                                                                                                                          
set CXC4011247 featureState 1                                                                                                                                                                                          
set CXC4011251 featureState 1                                                                                                                                                                                          
set CXC4011252 featureState 1                                                                                                                                                                                          
set CXC4011253 featureState 1                                                                                                                                                                                          
set CXC4011255 featureState 1                                                                                                                                                                                          
set CXC4011256 featureState 1                                                                                                                                                                                          
set CXC4011258 featureState 1                                                                                                                                                                                          
set CXC4011317 featureState 1                                                                                                                                                                                          
set CXC4011319 featureState 1                                                                                                                                                                                          
set CXC4011327 featureState 1                                                                                                                                                                                          
set CXC4011345 featureState 1                                                                                                                                                                                          
set CXC4011346 featureState 1                                                                                                                                                                                          
set CXC4011356 featureState 1                                                                                                                                                                                          
set CXC4011366 featureState 1                                                                                                                                                                                          
set CXC4011370 featureState 1                                                                                                                                                                                          
set CXC4011372 featureState 1                                                                                                                                                                                          
set CXC4011373 featureState 1                                                                                                                                                                                          
set CXC4011376 featureState 1                                                                                                                                                                                          
set CXC4011378 featureState 1                                                                                                                                                                                          
set CXC4011422 featureState 1                                                                                                                                                                                          
set CXC4011427 featureState 1                                                                                                                                                                                          
set CXC4011443 featureState 1                                                                                                                                                                                          
set CXC4011444 featureState 1                                                                                                                                                                                          
set CXC4011476 featureState 1                                                                                                                                                                                          
set CXC4011477 featureState 1                                                                                                                                                                                          
set CXC4011479 featureState 1                                                                                                                                                                                          
set CXC4011481 featureState 1                                                                                                                                                                                          
set CXC4011482 featureState 1                                                                                                                                                                                          
set CXC4011485 featureState 1                                                                                                                                                                                          
set CXC4011515 featureState 1                                                                                                                                                                                          
set CXC4011557 featureState 1                                                                                                                                                                                          
set CXC4011559 featureState 1                                                                                                                                                                                          
set CXC4011618 featureState 1                                                                                                                                                                                          
set CXC4011666 featureState 1                                                                                                                                                                                          
set CXC4011667 featureState 1                                                                                                                                                                                          
set CXC4011698 featureState 1                                                                                                                                                                                          
set CXC4011699 featureState 1                                                                                                                                                                                          
set CXC4011710 featureState 1                                                                                                                                                                                          
set CXC4011711 featureState 1                                                                                                                                                                                          
set CXC4011715 featureState 1                                                                                                                                                                                          
set CXC4011716 featureState 1                                                                                                                                                                                          
set CXC4011804 featureState 1                                                                                                                                                                                          
set CXC4011807 featureState 1                                                                                                                                                                                          
set CXC4011808 featureState 1                                                                                                                                                                                          
set CXC4011811 featureState 1                                                                                                                                                                                          
set CXC4011813 featureState 1                                                                                                                                                                                          
set CXC4011814 featureState 1                                                                                                                                                                                          
set CXC4011815 featureState 1                                                                                                                                                                                          
set CXC4011820 featureState 1                                                                                                                                                                                          
set CXC4011823 featureState 1                                                                                                                                                                                          
set CXC4011910 featureState 1                                                                                                                                                                                          
set CXC4011914 featureState 1                                                                                                                                                                                          
set CXC4011917 featureState 1                                                                                                                                                                                          
set CXC4011918 featureState 1                                                                                                                                                                                          
set CXC4011922 featureState 1                                                                                                                                                                                          
set CXC4011930 featureState 1                                                                                                                                                                                          
set CXC4011933 featureState 1                                                                                                                                                                                          
set CXC4011937 featureState 1                                                                                                                                                                                          
set CXC4011938 featureState 1                                                                                                                                                                                          
set CXC4011939 featureState 1                                                                                                                                                                                          
set CXC4011940 featureState 1                                                                                                                                                                                          
set CXC4011941 featureState 1                                                                                                                                                                                          
set CXC4011942 featureState 1                                                                                                                                                                                          
set CXC4011946 featureState 1                                                                                                                                                                                          
set CXC4011951 featureState 1                                                                                                                                                                                          
set CXC4011958 featureState 1                                                                                                                                                                                          
set CXC4011967 featureState 1                                                                                                                                                                                          
set CXC4011969 featureState 1                                                                                                                                                                                          
set CXC4011973 featureState 1                                                                                                                                                                                          
set CXC4011974 featureState 1                                                                                                                                                                                          
set CXC4011975 featureState 1                                                                                                                                                                                          
set CXC4011982 featureState 1                                                                                                                                                                                          
set CXC4011983 featureState 1                                                                                                                                                                                          
set CXC4011991 featureState 1                                                                                                                                                                                          
set CXC4012003 featureState 1                                                                                                                                                                                          
set CXC4012015 featureState 1                                                                                                                                                                                          
set CXC4012018 featureState 1                                                                                                                                                                                          
set CXC4012022 featureState 1                                                                                                                                                                                          
set CXC4012036 featureState 1                                                                                                                                                                                          
set CXC4012070 featureState 1                                                                                                                                                                                          
set CXC4012089 featureState 1                                                                                                                                                                                          
set CXC4012097 featureState 1                                                                                                                                                                                          
set CXC4012111 featureState 1                                                                                                                                                                                          
set CXC4012123 featureState 1                                                                                                                                                                                          
set CXC4012129 featureState 1                                                                                                                                                                                          
set CXC4012199 featureState 1                                                                                                                                                                                          
set CXC4012218 featureState 1                                                                                                                                                                                          
set CXC4012238 featureState 1                                                                                                                                                                                          
set CXC4012240 featureState 1                                                                                                                                                                                          
set CXC4012256 featureState 1                                                                                                                                                                                          
set CXC4012259 featureState 1                                                                                                                                                                                          
set CXC4012260 featureState 1                                                                                                                                                                                          
set CXC4012261 featureState 1                                                                                                                                                                                          
set CXC4012271 featureState 1                                                                                                                                                                                          
set CXC4012316 featureState 1                                                                                                                                                                                          
set CXC4012324 featureState 1                                                                                                                                                                                          
set CXC4012326 featureState 1                                                                                                                                                                                          
set CXC4012349 featureState 1                                                                                                                                                                                          
set CXC4012356 featureState 1                                                                                                                                                                                          
set CXC4012371 featureState 1                                                                                                                                                                                          
set CXC4012374 featureState 1                                                                                                                                                                                          
set CXC4012381 featureState 1                                                                                                                                                                                          
set CXC4012385 featureState 1                                                                                                                                                                                          
set CXC4012485 featureState 1                                                                                                                                                                                          
set CXC4012503 featureState 1                                                                                                                                                                                          
set CXC4012504 featureState 1                                                                                                                                                                                          
set CXC4012505 featureState 1                                                                                                                                                                                          
set CXC4012578 featureState 1                                                                                                                                                                                          
set CXC4040004 featureState 1                                                                                                                                                                                          
set CXC4040005 featureState 1                                                                                                                                                                                          
set CXC4040006 featureState 1                                                                                                                                                                                          
set CXC4040008 featureState 1                                                                                                                                                                                          
set CXC4040009 featureState 1                                                                                                                                                                                          
set CXC4040010 featureState 1                                                                                                                                                                                          
set CXC4040014 featureState 1                                                                                                                                                                                          
set CXC4012590 FeatureState 1                                                                                                                                                                                          
set CXC4012480 featureState 0                                                                                                                                                                                          
set CXC4012562 FeatureState 1                                                                                                                                                                                          
                                                                                                                                                                                                                       
get NRCellCU=.*_A nRCellCUId$ > $nrcellcu_A                                                                                                                                                                            
get NRCellCU=.*_B nRCellCUId$ > $nrcellcu_B                                                                                                                                                                            
get NRCellCU=.*_C nRCellCUId$ > $nrcellcu_C                                                                                                                                                                            
                                                                                                                                                                                                                       
cr GNBCUCPFunction=1,NRCellCU=$nrcellcu_A,NRFreqRelation=629952                                                                                                                                                        
NRNetwork=1,NRFrequency=629952-30-20-0-1                                                                                                                                                                               
cr GNBCUCPFunction=1,NRCellCU=$nrcellcu_B,NRFreqRelation=629952                                                                                                                                                        
NRNetwork=1,NRFrequency=629952-30-20-0-1                                                                                                                                                                               
cr GNBCUCPFunction=1,NRCellCU=$nrcellcu_C,NRFreqRelation=629952                                                                                                                                                        
NRNetwork=1,NRFrequency=629952-30-20-0-1                                                                                                                                                                               
                                                                                                                                                                                                                       
set GNBCUCPFunction=1,NRCellCU=.*,NRFreqRelation=629952 cellReselectionPriority 7                                                                                                                                      
set GNBCUCPFunction=1,NRCellCU=.*,NRFreqRelation=629952 anrMeasOn true                                                                                                                                                 
                                                                                                                                                                                                                       
///common_Parameters_32t_8t                                                                                                                                                                                            
set NRSectorCarrier=.*,CommonBeamforming=1               cbfMacroTaperType 0                                                                                                                                           
set CUUP5qi=6$  estimatedE2ERTT 50                                                                                                                                                                                     
set CUUP5qi=8$  estimatedE2ERTT 50                                                                                                                                                                                     
set GNBDUFunction=1,RadioBearerTable=1,DataRadioBearer=1  tPollRetransmitUl 80                                                                                                                                         
set GNBDUFunction=1,RadioBearerTable=1,DataRadioBearer=1 tStatusProhibitUl 10                                                                                                                                          
set GNBDUFunction=1,RadioBearerTable=1,DataRadioBearer=1 ulMaxRetxThreshold 32                                                                                                                                         
set GNBDUFunction=1,RadioBearerTable=1,DataRadioBearer=1 dlMaxRetxThreshold 32                                                                                                                                         
set GNBDUFunction=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base drxInactivityTimer 15                                                                                                                               
set GNBDUFunction=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base drxLongCycle      10                                                                                                                                
set GNBDUFunction=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base  drxOnDurationTimer  39                                                                                                                             
set GNBDUFunction=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base  drxRetransmissionTimerDl 8                                                                                                                         
set GNBDUFunction=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base  drxRetransmissionTimerUl 8                                                                                                                         
set GNBCUUPFunction=1          dcDlPdcpInitialScgRate 100                                                                                                                                                              
                                                                                                                                                                                                                       
set NRCellDU=.* tddSpecialSlotPattern 3                                                                                                                                                                                
set NRCellDU=.* tddUlDlPattern 1                                                                                                                                                                                       
set NRCellDU=.* rachPreambleFormat 0                                                                                                                                                                                   
set NRCellDU=.* cellRange 5000                                                                                                                                                                                         
set NRCellDU=.* csiRsShiftingPrimary 1                                                                                                                                                                                 
set NRCellDU=.* csiRsShiftingSecondary 1                                                                                                                                                                               
set NRCellDU=.* dl256QamEnabled true                                                                                                                                                                                   
set NRCellDU=.* drxProfileEnabled true                                                                                                                                                                                 
set NRCellDU=.* maxUeSpeed 2                                                                                                                                                                                           
set NRCellDU=.* pdschStartPrbStrategy 3                                                                                                                                                                                
set NRCellDU=.* puschStartPrbStrategy 3                                                                                                                                                                                
set NRCellDU=.* pZeroNomPucch -114                                                                                                                                                                                     
set NRCellDU=.* secondaryCellOnly False                                                                                                                                                                                
set NRCellDU=.* ssbDuration 1                                                                                                                                                                                          
set NRCellDU=.* ssbOffset 0                                                                                                                                                                                            
set NRCellDU=.* ssbPeriodicity 20                                                                                                                                                                                      
set NRCellDU=.* ssbSubCarrierSpacing 30                                                                                                                                                                                
set NRCellDU=.* subCarrierSpacing 30                                                                                                                                                                                   
set NRCellDU=.* trsPeriodicity 20                                                                                                                                                                                      
set NRCellDU=.* trsPowerBoosting 0                                                                                                                                                                                     
set NRCellDU=.* ul256QamEnabled true                                                                                                                                                                                   
set NRCellDU=.* rachPreambleRecTargetPower -110                                                                                                                                                                        
set NRCellDU=.* rachPreambleTransMax 10                                                                                                                                                                                
Set NRCellDU=.* maxUsersRachSchedPusch 100                                                                                                                                                                             
set NRCellDU=.* pZeroNomPuschGrant -102                                                                                                                                                                                
set NRCellDU=.* csiRsPeriodicity 40                                                                                                                                                                                    
set NRCellDU=.* additionalPucchForCaEnabled FALSE                                                                                                                                                                      
set NRSectorCarrier=.* configuredMaxTxPower    200000                                                                                                                                                                  
set NRCellDU=.*  maxNoOfAdvancedDlMuMimoLayers 8                                                                                                                                                                       
set NRCellDU=.* SrsHoppingBandwidth 0                                                                                                                                                                                  
set NRCellDU=.* dlDmrsMuxSinrThresh -10                                                                                                                                                                                
set NRCellDU=.* nrSrsDlBufferVolThr 100                                                                                                                                                                                
set NRCellDU=.* nrSrsDlPacketAgeThr 0                                                                                                                                                                                  
set NRCellDU=.* pdcchSymbConfig 0                                                                                                                                                                                      
set NRCellDU=.* ssbFrequency 629952                                                                                                                                                                                    
set NRCellDU=.* ssbGscn 7811                                                                                                                                                                                           
                                                                                                                                                                                                                       
                                                                                                                                                                                                                       
#lkf required with dmrs feature for bm                                                                                                                                                                                 
set NRCellDU=.* pdschAllowedInDmrsSym TRUE                                                                                                                                                                             
set NRCellDU=.* puschAllowedInDmrsSym TRUE                                                                                                                                                                             
                                                                                                                                                                                                                       
set QciProfileEndcConfigExt=1   initialUplinkConf 1                                                                                                                                                                    
set GNBCUCPFunction=1,UeCC=1,InactivityProfile=Default,InactivityProfileUeCfg=Base tInactivityTimerEndcSn 5                                                                                                            
set NRSectorCarrier= nRMicroSleepTxEnabled true                                                                                                                                                                        
set NRSectorCarrier=.*,CommonBeamforming=1  coverageShape 1                                                                                                                                                            
set GNBDUFunction=1,RadioBearerTable=1,DataRadioBearer=1    tPollRetransmitDl 80                                                                                                                                       
set AnrFunctionNR anrCgiMeasInterFreqMode 1                                                                                                                                                                            
set AnrFunctionNR anrCgiMeasIntraFreqEnabled TRUE                                                                                                                                                                      
set AnrFunctionNR anrEndcX2Enabled TRUE                                                                                                                                                                                
set AnrFunction removeEnbTime 7                                                                                                                                                                                        
set AnrFunction removeGnbTime 7                                                                                                                                                                                        
set GNBCUCPFunction=1,AnrFunction removeNrelTime 7                                                                                                                                                                     
set GNBDUFunction=1,Rrc= n310 20                                                                                                                                                                                       
set GNBDUFunction=1,Rrc= n311 1                                                                                                                                                                                        
set GNBDUFunction=1,Rrc= t300 1500                                                                                                                                                                                     
set GNBDUFunction=1,Rrc= t301 600                                                                                                                                                                                      
set GNBDUFunction=1,Rrc= t304 2000                                                                                                                                                                                     
set GNBDUFunction=1,Rrc= t310 2000                                                                                                                                                                                     
set GNBDUFunction=1,Rrc= t311 3000                                                                                                                                                                                     
set GNBDUFunction=1,Rrc= t319 400                                                                                                                                                                                      
                                                                                                                                                                                                                       
set GNBCUUPFunction=1    endcDataUsageReportEnabled true                                                                                                                                                               
set GNBDUFunction=1,UeCC=1,Prescheduling=1,PreschedulingUeCfg=Base preschedulingUeMode 1                                                                                                                               
set GNBDUFunction=1,UeCC=1,Prescheduling=1,PreschedulingUeCfg=Base preschedulingDataSize 86                                                                                                                            
set GNBDUFunction=1,UeCC=1,Prescheduling=1,PreschedulingUeCfg=Base preschedulingDuration 100                                                                                                                           
set . anrstateNR 1                                                                                                                                                                                                     
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          gNodebIdLength 26                                                                                                                                          
set . endcX2IpAddrViaS1Active 1                                                                                                                                                                                        
                                                                                                                                                                                                                       
set CaSCellHandlingUeCfg sCellActDeactDataThres -1                                                                                                                                                                     
set CaSCellHandlingUeCfg sCellActDeactDataThresHyst 90                                                                                                                                                                 
                                                                                                                                                                                                                       
#######32t#####                                                                                                                                                                                                        
set NRCellDU=.* csiRsConfig4P csiRsControl4Ports=0,i11Restriction=                                                                                                                                                     
set NRCellDU=.* csiRsConfig8P  csiRsControl8Ports=1,i11Restriction=FFFF,i12Restriction=                                                                                                                                
set NRCellDU=.* csiRsConfig32P csiRsControl32Ports=EIGHT_TWO_N1AZ,i11Restriction=FFFFFFFF,i12Restriction=FF                                                                                                            
set NRCellDU=.* ssbPowerBoost 6                                                                                                                                                                                        
set NRCellDU=.* advancedDlSuMimoEnabled TRUE                                                                                                                                                                           
set NRCellDU=.* pZeroNomSrs -110                                                                                                                                                                                       
set NRCellDU=.* srsPeriodicity 40                                                                                                                                                                                      
set NRCellDU=.* dlMaxMuMimoLayers 8                                                                                                                                                                                    
set NRCellDU=.* ulMaxMuMimoLayers 4                                                                                                                                                                                    
set NRCellDU=.* pZeroUePuschOffset256Qam 4                                                                                                                                                                             
set .  cbfMacroTaperType 0                                                                                                                                                                                             
set GNBCUCPFunction=1,AnrFunction=1,AnrFunctionNR=1         anrAutoCreateXnForEndc True                                                                                                                                
                                                                                                                                                                                                                       
#######64t#####                                                                                                                                                                                                        
#set NRCellDU=.* csiRsConfig4P csiRsControl4Ports=0,i11Restriction=                                                                                                                                                    
#set NRCellDU=.* csiRsConfig8P  csiRsControl8Ports=1,i11Restriction=FFFF,i12Restriction=                                                                                                                               
#set NRCellDU=.* csiRsConfig32P csiRsControl32Ports=EIGHT_TWO_N1AZ,i11Restriction=FFFFFFFF,i12Restriction=FF                                                                                                           
#set NRCellDU=.* ssbPowerBoost 6                                                                                                                                                                                       
#set NRCellDU=.* advancedDlSuMimoEnabled TRUE                                                                                                                                                                          
#set NRCellDU=.* pZeroNomSrs -110                                                                                                                                                                                      
#set NRCellDU=.* srsPeriodicity 40                                                                                                                                                                                     
#set NRCellDU=.* dlMaxMuMimoLayers 8                                                                                                                                                                                   
#set NRCellDU=.* ulMaxMuMimoLayers 4                                                                                                                                                                                   
#set NRCellDU=.* pZeroUePuschOffset256Qam 2                                                                                                                                                                            
                                                                                                                                                                                                                       
                                                                                                                                                                                                                       
#######8t#####                                                                                                                                                                                                         
#set NRCellDU=.* csiRsConfig4P csiRsControl4Ports=0,i11Restriction=                                                                                                                                                    
#set NRCellDU=.* csiRsConfig8P   csiRsControl8Ports=1,i11Restriction=FFFF,i12Restriction=                                                                                                                              
#set NRCellDU=.* csiRsConfig32P csiRsControl32Ports=0,i11Restriction=,i12Restriction=                                                                                                                                  
#set NRCellDU=.* ssbPowerBoost 3                                                                                                                                                                                       
#set NRCellDU=.* pZeroUePuschOffset256Qam 6                                                                                                                                                                            
                                                                                                                                                                                                                       
#######4t#####                                                                                                                                                                                                         
#set NRCellDU=.* csiRsConfig32P csiRsControl32Ports=0,i11Restriction=,i12Restriction=                                                                                                                                  
#set NRCellDU=.* csiRsConfig8P   csiRsControl8Ports=0,i11Restriction=,i12Restriction=                                                                                                                                  
#set NRCellDU=.* csiRsConfig4P csiRsControl4Ports=1,i11Restriction=FF                                                                                                                                                  
#set NRCellDU=.* pZeroUePuschOffset256Qam 8                                                                                                                                                                            
#set NRCellDU=.* ssbPowerBoost 3                                                                                                                                                                                       
#set NRSectorCarrier= configuredMaxTxPower    160000                                                                                                                                                                   
                                                                                                                                                                                                                       
set . endcDlNrRetProhibTimer 400                                                                                                                                                                                       
set . endcDlNrQualHyst 3                                                                                                                                                                                               
set . initialUplinkConf SCG                                                                                                                                                                                            
set . endcUlNrRetProhibTimer 1000                                                                                                                                                                                      
set . dcDlAggActTime 1                                                                                                                                                                                                 
set . dcDlAggExpiryTimer 100                                                                                                                                                                                           
                                                                                                                                                                                                                       
set NRCellRelation= isHoAllowed true                                                                                                                                                                                   
set NRCellDU=.* endcDlLegSwitchEnabled true                                                                                                                                                                            
set NRCellDU=.* endcDlNrLowQualThresh 0                                                                                                                                                                                
set NRCellDU=.* endcUlLegSwitchEnabled true                                                                                                                                                                            
set NRCellDU=.* endcUlNrLowQualThresh 10                                                                                                                                                                               
set NRCellDU=.* endcUlNrQualHyst 6                                                                                                                                                                                     
set NRCellCU=.* mcpcPSCellEnabled true                                                                                                                                                                                 
                                                                                                                                                                                                                       
cr GNBCUCPFunction=1,IntraFreqMC=1                                                                                                                                                                                     
cr GNBCUCPFunction=1,IntraFreqMC=1,IntraFreqMCCellProfile=1                                                                                                                                                            
                                                                                                                                                                                                                       
set IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base betterSpCellTriggerQuantity 0                                                                                                              
set IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base rsrpBetterSpCell hysteresis=10,offset=30,timeToTrigger=640                                                                                 
set IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base endcActionEvalFail 1                                                                                                                       
                                                                                                                                                                                                                       
set IntraFreqMC=1,IntraFreqMCCellProfile=1 rsrpSCellCoverage hysteresis=10,threshold=-117                                                                                                                              
set IntraFreqMC=1,IntraFreqMCCellProfile=1 rsrpBetterSCell offset=30,hysteresis=10                                                                                                                                     
set Mcpc=1,McpcPSCellProfile=.*,McpcPSCellProfileUeCfg=Base  rsrpCriticalEnabled true                                                                                                                                  
set Mcpc=1,McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base rsrpSearchZone threshold=-112,hysteresis=10,timeToTriggerA1=160                                                                                       
set Mcpc=1,McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base rsrpCandidateA5 threshold1=-118,threshold2=-112,hysteresis=10,timeToTrigger=640                                                                       
set Mcpc=1,McpcPSCellNrFreqRelProfile=Default,McpcPSCellNrFreqRelProfileUeCfg=Base rsrpCandidateA5Offsets threshold1Offset=0,threshold2Offset=0                                                                        
set Mcpc=1,McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base rsrpCritical threshold=-113,timeToTrigger=256,hysteresis=20                                                                                           
set FeatureState=CXC4012375 featurestate 1                                                                                                                                                                             
set FeatureState=CXC4012273 featurestate 1                                                                                                                                                                             
set FeatureState=CXC4012590 FeatureState 1                                                                                                                                                                             
                                                                                                                                                                                                                       
set PmEventService=1 cellTraceFileSize 30000                                                                                                                                                                           
set NRCellDU=.*  maxNoOfAdvancedDlMuMimoLayers 8                                                                                                                                                                       
set QciProfileEndcConfigExt=1 ulDataSplitThresholdMcg -1                                                                                                                                                               
set NRCellDU=.* drxProfileRef GNBDUFunction=1,UeCC=1,DrxProfile=Default                                                                                                                                                
set NRCellCU=.* mcpcPSCellProfileRef GNBCUCPFunction=1,Mcpc=1,McpcPSCellProfile=Default                                                                                                                                
                                                                                                                                                                                                                       
#### PDCCH Beamforming                                                                                                                                                                                                 
                                                                                                                                                                                                                       
set CXC4012589 featurestate 1                                                                                                                                                                                          
set NRCellDU pdcchLaSinrOffset -20                                                                                                                                                                                     
                                                                                                                                                                                                                       
                                                                                                                                                                                                                       
##### System Constant                                                                                                                                                                                                  
                                                                                                                                                                                                                       
scw RP136:20                                                                                                                                                                                                           
scw RP137:20                                                                                                                                                                                                           
scw RP138:20                                                                                                                                                                                                           
scw RP139:20                                                                                                                                                                                                           
                                                                                                                                                                                                                       
                                                                                                                                                                                                                       
#### Pmax                                                                                                                                                                                                              
                                                                                                                                                                                                                       
set NRCellDU pMax 26                                                                                                                                                                                                   
                                                                                                                                                                                                                       
##### DLMAX RETX                                                                                                                                                                                                       
                                                                                                                                                                                                                       
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 dlMaxRetxThreshold 32                                                                                                                                    
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 ulMaxRetxThreshold 32                                                                                                                                    
                                                                                                                                                                                                                       
                                                                                                                                                                                                                       
#### DFTS OFDM                                                                                                                                                                                                         
                                                                                                                                                                                                                       
set CXC4012373 featurestate 1                                                                                                                                                                                          
set NRCellDU dftSOfdmMsg3Enabled true                                                                                                                                                                                  
set NRCellDU dftSOfdmPuschEnabled true                                                                                                                                                                                 
                                                                                                                                                                                                                       
#####endcActionEvalFail                                                                                                                                                                                                
                                                                                                                                                                                                                       
set IntraFreqMCCellProfileUeCfg endcActionEvalFail 1                                                                                                                                                                   
                                                                                                                                                                                                                       
##Transport                                                                                                                                                                                                            
                                                                                                                                                                                                                       
cr Transport=1,Synchronization=1,TimeSyncIO=1,GnssInfo=1                                                                                                                                                               
cr Transport=1,Router=LTE_NR,TwampResponder=NR                                                                                                                                                                         
Transport=1,Router=LTE_NR,InterfaceIPv6=NR,AddressIPv6=NR_S1U_OAM                                                                                                                                                      
4001                                                                                                                                                                                                                   
set Transport=1,Router=LTE_NR,TwampResponder=NR userLabel TWAMP1                                                                                                                                                       
                                                                                                                                                                                                                       
set Transport=1,SctpProfile=Node_Internal_F1 maxRto 4000                                                                                                                                                               
set Transport=1,SctpProfile=Node_Internal_F1 initRto 2000                                                                                                                                                              
set Transport=1,SctpProfile=Node_Internal_F1 minRto 1000                                                                                                                                                               
set Transport=1,SctpProfile=Node_Internal_F1 maxInitRt 5                                                                                                                                                               
set Transport=1,SctpProfile=Node_Internal_F1 maxSctpPduSize 1480                                                                                                                                                       
set Transport=1,SctpProfile=Node_Internal_F1 sackTimer 100                                                                                                                                                             
set Transport=1,SctpProfile=Node_Internal_F1 userLabel SCTP                                                                                                                                                            
set Transport=1,SctpProfile=Node_Internal_F1 pathMaxRtx 4                                                                                                                                                              
set Transport=1,SctpProfile=Node_Internal_F1 assocMaxRtx 8                                                                                                                                                             
set Transport=1,SctpProfile=1 maxRto 4000                                                                                                                                                                              
set Transport=1,SctpProfile=1 initRto 2000                                                                                                                                                                             
set Transport=1,SctpProfile=1 minRto 1000                                                                                                                                                                              
set Transport=1,SctpProfile=1 maxInitRt 5                                                                                                                                                                              
set Transport=1,SctpProfile=1 maxSctpPduSize 1480                                                                                                                                                                      
set Transport=1,SctpProfile=1 sackTimer 100                                                                                                                                                                            
set Transport=1,SctpProfile=1 userLabel SCTP                                                                                                                                                                           
set Transport=1,SctpProfile=1 pathMaxRtx 4                                                                                                                                                                             
set Transport=1,SctpProfile=1 assocMaxRtx 8                                                                                                                                                                            
                                                                                                                                                                                                                       
/cm/sysconread                                                                                                                                                                                                         
/cm/sysconwrite 1225 50                                                                                                                                                                                                
/cm/sysconwrite 1566 33                                                                                                                                                                                                
/cm/sysconwrite 1627 3                                                                                                                                                                                                 
/cm/sysconwrite 153 128                                                                                                                                                                                                
/cm/sysconwrite 278 1                                                                                                                                                                                                  
/cm/sysconwrite 296 200                                                                                                                                                                                                
/cm/sysconwrite 1738 230                                                                                                                                                                                               
/cm/sysconwrite 2959 1                                                                                                                                                                                                 
/cm/sysconwrite L4885 1                                                                                                                                                                                                
/cm/sysconread                                                                                                                                                                                                         
                                                                                                                                                                                                                       
cr Transport=1,QosProfiles=1,DscpPcpMap=1                                                                                                                                                                              
                                                                                                                                                                                                                       
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp0                                                                                                                                                                        
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp1                                                                                                                                                                        
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp2                                                                                                                                                                        
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp3                                                                                                                                                                        
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp4                                                                                                                                                                        
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp5                                                                                                                                                                        
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp6                                                                                                                                                                        
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp7                                                                                                                                                                        
                                                                                                                                                                                                                       
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp0 0,1,2,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,36,37,38,39,41,43,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63                                           
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp2 22,24,26                                                                                                                                                               
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp3 6,8,10,30,32                                                                                                                                                           
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp4 12,14,40                                                                                                                                                               
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp5 4,28                                                                                                                                                                   
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp6 16,18,34,42,44                                                                                                                                                         
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp7 20,46                                                                                                                                                                  
                                                                                                                                                                                                                       
set GNBDUFunction=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base drxEnabled true                                                                                                                                     
                                                                                                                                                                                                                       
### GTP-U Supervision                                                                                                                                                                                                  
                                                                                                                                                                                                                       
set GtpuSupervision=1,GtpuSupervisionProfile=S1 gtpuEchoEnabled true                                                                                                                                                   
y                                                                                                                                                                                                                      
set GtpuSupervision=1,GtpuSupervisionProfile=X2 gtpuEchoEnabled true                                                                                                                                                   
y                                                                                                                                                                                                                      
set GtpuSupervision=1,GtpuSupervisionProfile=S1 gtpuEchoDscp 32                                                                                                                                                        
y                                                                                                                                                                                                                      
set GtpuSupervision=1,GtpuSupervisionProfile=X2 gtpuEchoDscp 32                                                                                                                                                        
y                                                                                                                                                                                                                      
                                                                                                                                                                                                                       
###  tDcOverall                                                                                                                                                                                                        
                                                                                                                                                                                                                       
set GNBCUCPFunction tDcOverall 11                                                                                                                                                                                      
                                                                                                                                                                                                                       
###  uldatasplitthreshold                                                                                                                                                                                              
                                                                                                                                                                                                                       
set QciProfileEndcConfigExt ulDataSplitThreshold 102400                                                                                                                                                                
                                                                                                                                                                                                                       
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 tPollRetransmitUl 80                                                                                                                                     
y                                                                                                                                                                                                                      
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 tPollRetransmitDl 80                                                                                                                                     
y                                                                                                                                                                                                                      
                                                                                                                                                                                                                       
                                                                                                                                                                                                                       
                                                                                                                                                                                                                       
#New features                                                                                                                                                                                                          
set CXC4012330 featureState 1                                                                                                                                                                                          
set CXC4012406 featureState 1                                                                                                                                                                                          
set CXC4012510 featureState 1                                                                                                                                                                                          
set CXC4012547 featureState 1                                                                                                                                                                                          
                                                                                                                                                                                                                       
#Repeat                                                                                                                                                                                                                
set . endcUlNrRetProhibTimer 1000                                                                                                                                                                                      
set IntraFreqMCCellProfileUeCfg endcActionEvalFail 1                                                                                                                                                                   
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 tPollRetransmitUl 80                                                                                                                                     
                                                                                                                                                                                                                       
set GtpuSupervision=1,GtpuSupervisionProfile=S1 gtpuEchoEnabled true                                                                                                                                                   
                                                                                                                                                                                                                       
set GtpuSupervision=1,GtpuSupervisionProfile=X2 gtpuEchoEnabled true                                                                                                                                                   
                                                                                                                                                                                                                       
set GtpuSupervision=1,GtpuSupervisionProfile=S1 gtpuEchoDscp 32                                                                                                                                                        
                                                                                                                                                                                                                       
set GtpuSupervision=1,GtpuSupervisionProfile=X2 gtpuEchoDscp 32                                                                                                                                                        
                                                                                                                                                                                                                       
wait 3                                                                                                                                                                                                                 
lt all                                                                                                                                                                                                                 
                                                                                                                                                                                                                       
set IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base betterSpCellTriggerQuantity 0                                                                                                              
set IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base rsrpBetterSpCell hysteresis=10,offset=30,timeToTrigger=640                                                                                 
set IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base endcActionEvalFail 1                                                                                                                       
                                                                                                                                                                                                                       
### 23.Q2 ###                                                                                                                                                                                                          
                                                                                                                                                                                                                       
scw RP1993:1                                                                                                                                                                                                           
scw RP1994:28                                                                                                                                                                                                          
scw RP1954:2                                                                                                                                                                                                           
                                                                                                                                                                                                                       
set IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base rsrpSCellCoverage hysteresis=10,threshold=-117                                                                                             
set IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base rsrpBetterSCell offset=30,hysteresis=10                                                                                                    
set DrbRlc=Default,DrbRlcUeCfg=Base tStatusProhibitUl 10                                                                                                                                                               
set DrbRlc=Default,DrbRlcUeCfg=Base ulMaxRetxThreshold 32                                                                                                                                                              
set DrbRlc=Default,DrbRlcUeCfg=Base dlMaxRetxThreshold 32                                                                                                                                                              
set DrbRlc=Default,DrbRlcUeCfg=Base tPollRetransmitDl 80                                                                                                                                                               
set DrbRlc=Default,DrbRlcUeCfg=Base tPollRetransmitUl 80                                                                                                                                                               
                                                                                                                                                                                                                       
set NRCellDU improvedUlLinkAdaptation false                                                                                                                                                                            
                                                                                                                                                                                                                       
#### 24.Q2 ####                                                                                                                                                                                                        
set Lm=1,FeatureState=CXC4011958$ FeatureState 1                                                                                                                                                                       
set Lm=1,FeatureState=CXC4010974$ FeatureState 1                                                                                                                                                                       
set EUtranCellRelation*.* sleepModeCovCellCandidate 2                                                                                                                                                                  
set CellSleepFunction*.* prbOffloadAdjust 100                                                                                                                                                                          
set CellSleepFunction*.* rrcOffloadAdjust 100                                                                                                                                                                          
set Lm=1,FeatureState=CXC4012563$ FeatureState 1                                                                                                                                                                       
set EUtranCell.*DD=.* pdcchFlexibleBlerEnabled TRUE                                                                                                                                                                    
set SubscriberGroupProfile*.* pdcchFlexibleBlerMode 2                                                                                                                                                                  
set EUtranCell.*DD=.* diffPdcchMaxTargetBlerEnabled TRUE                                                                                                                                                               
set EUtranCell.*DD=.* diffPdcchMaxTargetBlerThres -10                                                                                                                                                                  
set EUtranCell.*DD=.* pdcchCongestMeasurePeriod 1                                                                                                                                                                      
set EUtranCell.*DD=.* pdcchMaxTargetBlerHigh 400                                                                                                                                                                       
set EUtranCell.*DD=.* pdcchMaxTargetBlerLow 200                                                                                                                                                                        
set EUtranCell.*DD=.* pdcchTargetBler 24                                                                                                                                                                               
set EUtranCell.*DD=.* pdcchTargetBlerPCell 22                                                                                                                                                                          
set EUtranCell.*DD=.* optimizedPdcchMaxTargetBler 200                                                                                                                                                                  
set EUtranCell.*DD=.* optimizedPdcchCceUtilThres 30                                                                                                                                                                    
set EUtranCell.*DD=.* optimizedPdcchCongestThres 30                                                                                                                                                                    
set EUtranCell.*DD=.* optimizedPdcchDlPrbThres 100                                                                                                                                                                     
set EUtranCell.*DD=.* optimizedPdcchUlPrbThres 100                                                                                                                                                                     
set UePolicyOptimization=1$ zzzTemporary1 1                                                                                                                                                                            
set UePolicyOptimization=1$ ueCapPrioList 0                                                                                                                                                                            
set UePolicyOptimization=1$ loadAwareImc TRUE                                                                                                                                                                          
set UePolicyOptimization=1$ coverageAwareImc TRUE                                                                                                                                                                      
set UePolicyOptimization=1$ t320 180                                                                                                                                                                                   
set ENodeBFunction=1$ ChannelQualityMode 1                                                                                                                                                                             
set Lm=1,FeatureState=CXC4012677$ FeatureState 0                                                                                                                                                                       
set AnrFunctionNRUeCfg=Base$ anrRsrpThreshold -112                                                                                                                                                                     
set IntraFreqMCCellProfileUeCfg betterSpCellTriggerQuantity 0                                                                                                                                                          
set ENodeBFunction=1$ endcOverheatingAssistance TRUE                                                                                                                                                                   
set ENodeBFunction=1$ overheatingIndProhibitTimer 20                                                                                                                                                                   
set Lm=1,FeatureState=CXC4012690$ FeatureState 0                                                                                                                                                                       
set Lm=1,FeatureState=CXC4012677$ FeatureState 0                                                                                                                                                                       
set EUtranCell.*DD=.* loopingEndcProtectionEnabled TRUE                                                                                                                                                                
set EUtranCell.*DD=.* loopingEndcBackOffDuration 200                                                                                                                                                                   
set EUtranCell.*DD=.* loopingEndcShortScgSessTime 3000                                                                                                                                                                 
set EUtranCell.*DD=.* loopingEndcConsecFailThr 5                                                                                                                                                                       
set NRCellDU=.* advancedDlSuMimoEnabled TRUE                                                                                                                                                                           
set Lm=1,FeatureState=CXC4012536$ FeatureState 0                                                                                                                                                                       
set NRCellDU=.* maxNoOfAdvancedDlMuMimoLayers 8                                                                                                                                                                        
set Lm=1,FeatureState=CXC4012673$ FeatureState 1                                                                                                                                                                       
set NRCellDU=.* pZeroNomPuschGrant 1000                                                                                                                                                                                
set NRCellDU=.* autoSelectedModeOffset 6                                                                                                                                                                               
set PowerControlUeCfg pZeroNomPuschOffset 0                                                                                                                                                                            
cr GNBDUFunction=1,UeCC=1,PowerControl=1,PowerControlUeCfg=clpc                                                                                                                                                        
set GNBDUFunction=1,UeCC=1,PowerControl=1,PowerControlUeCfg=clpc puschPowerControlModeFr1 1                                                                                                                            
set ENodeBFunction pciConflictReportType 2                                                                                                                                                                             
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1 pciConflictDetectionType 3                                                                                                                                          
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1 endcRachFailThrPerUe 5                                                                                                                                              
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1 maxNoOfUeForPciConflictDetect 5                                                                                                                                     
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1 scgSessTimeForEndcRachFail 2500                                                                                                                                     
                                                                                                                                                                                                                       
                                                                                                                                                                                                                       
lbl NRCellDU=.*                                                                                                                                                                                                        
set Lm=1,FeatureState=CXC4012634$ FeatureState 1                                                                                                                                                                       
set NRCellDU=.* ssbTimeShiftEnabled TRUE                                                                                                                                                                               
set NRCellDU=.* tddBorderVersion 0                                                                                                                                                                                     
ldeb  NRCellDU=.*                                                                                                                                                                                                      
                                                                                                                                                                                                                       
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1 supportNrFreqChange 1                                                                                                                                               
set EUtranCell.*DD=.* endcSetupUlBsVolThr 5000                                                                                                                                                                         
set Lm=1,FeatureState=CXC4012638$ FeatureState 1                                                                                                                                                                       
set UeAdaptiveRlcUeCfg ueAdaptiveRlcRetxMode 0                                                                                                                                                                         
set Fm=1,FmAlarmModel=1,FmAlarmtype=RadioInterfaceConnectivityDisturbanceAlert isNotified 0                                                                                                                            
set GNBCUUPFunction=1,CardinalityLimits=1$ maxS1UPath 1800                                                                                                                                                             
                                                                                                                                                                                                                       
                                                                                                                                                                                                                       
set Lm=1,FeatureState=CXC4012378$ FeatureState 1                                                                                                                                                                       
cr GNBDUFunction=1,MassiveMimoSleep=1,MMimoSleepTimeGroup=1                                                                                                                                                            
set NRSectorCarrier=.* massiveMimoSleepEnabled ENABLED                                                                                                                                                                 
bl NRSectorCarrier=                                                                                                                                                                                                    
Set NRSectorCarrier=S.* mMimoSleepTimeGroupRef GNBDUFunction=1,MassiveMimoSleep=1,MMimoSleepTimeGroup=1                                                                                                                
deb NRSectorCarrier=                                                                                                                                                                                                   
                                                                                                                                                                                                                       
cr GNBDUFunction=1,MassiveMimoSleep=1,MMimoSleepProfile=1                                                                                                                                                              
cr GNBDUFunction=1,MassiveMimoSleep=1,MMimoSleepTimeGroup=1,MMimoSleepTimeWindow=1                                                                                                                                     
GNBDUFunction=1,MassiveMimoSleep=1,MMimoSleepProfile=1                                                                                                                                                                 
                                                                                                                                                                                                                       
set MMimoSleepProfile=1 sleepMode TXMUTE                                                                                                                                                                               
set MMimoSleepProfile=1 switchDownMonitorDurTimer 60                                                                                                                                                                   
set MMimoSleepProfile=1 switchDownPrbThreshDl 10                                                                                                                                                                       
set MMimoSleepProfile=1 switchDownRrcConnThresh 10                                                                                                                                                                     
set MMimoSleepProfile=1 switchUpMonitorDurTimer 30                                                                                                                                                                     
set MMimoSleepProfile=1 switchUpPrbThreshDl 20                                                                                                                                                                         
set MMimoSleepProfile=1 switchUpRrcConnThresh 20                                                                                                                                                                       
set MMimoSleepTimeWindow dayOfWeek ALL                                                                                                                                                                                 
set MMimoSleepTimeWindow stopTime 23:30                                                                                                                                                                                
set MMimoSleepTimeWindow startTime 20:30                                                                                                                                                                               
set Fm=1,FmAlarmModel=1,FmAlarmtype=RadioInterfaceConnectivityDisturbanceAlert isNotified 0                                                                                                                            
                                                                                                                                                                                                                       
set Lm=1,FeatureState=CXC4012563$ FeatureState 1                                                                                                                                                                       
set Lm=1,FeatureState=CXC4012199$ FeatureState 1                                                                                                                                                                       
set Lm=1,FeatureState=CXC4011482$ FeatureState 1                                                                                                                                                                       
set EUtranCell.*DD=.* pdcchFlexibleBlerEnabled TRUE                                                                                                                                                                    
set SubscriberGroupProfile=.* pdcchFlexibleBlerMode 2                                                                                                                                                                  
set EUtranCell.*DD=.* pdcchCongestMeasurePeriod 1                                                                                                                                                                      
set EUtranCell.*DD=.* pdcchTargetBler 24                                                                                                                                                                               
set EUtranCell.*DD=.* pdcchTargetBlerPCell 22                                                                                                                                                                          
set EUtranCell.*DD=.* optimizedPdcchMaxTargetBler 200                                                                                                                                                                  
set EUtranCell.*DD=.* optimizedPdcchDlPrbThres 100                                                                                                                                                                     
set EUtranCell.*DD=.* optimizedPdcchUlPrbThres 100                                                                                                                                                                     
set EUtranCell.*DD=.* optimizedPdcchCongestThres 30                                                                                                                                                                    
set EUtranCell.*DD=.* pdcchCongCtrlParamEnabled TRUE                                                                                                                                                                   
set CarrierAggregationFunction=1$ sCellPdcchOutLoopMarginCong 100                                                                                                                                                      
set EUtranCell.*DD=.* pdcchOutLoopInitAdjCong -40                                                                                                                                                                      
set EUtranCell.*DD=.* pdcchOutLoopInitAdjPCellCong -40                                                                                                                                                                 
set EUtranCell.*DD=.* pdcchPowerBoostMaxCong 0                                                                                                                                                                         
set EUtranCell.*DD=.* pdcchTargetBlerAdjStep 5                                                                                                                                                                         
set Lm=1,FeatureState=CXC4012687$ FeatureState 1                                                                                                                                                                       
set ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1$ ulMaxRetxThresholdLow 16                                                                                                                              
set ENodeBFunction=1,RadioBearerTable=default,RlcConfiguration=1$ ulRlcBufferCellThresUlMaxRetx 25                                                                                                                     
set ENodeBFunction=1,RadioBearerTable=default,RlcConfiguration=1$ ulRlcBufferMaxRetxThresHigh 90                                                                                                                       
set ENodeBFunction=1,RadioBearerTable=default,RlcConfiguration=1$ ulRlcBufferMaxRetxThresLow 80                                                                                                                        
set Lm=1,FeatureState=CXC4011319$ FeatureState 1                                                                                                                                                                       
set Lm=1,FeatureState=CXC4010974$ FeatureState 1                                                                                                                                                                       
set EUtranCell.*DD=.* lbUlHeavyUeDetectEnabled TRUE                                                                                                                                                                    
set ENodeBFunction=1$ ulHeavyUeDetectTime 500                                                                                                                                                                          
set ENodeBFunction=1$ ulHeavyUeBsrThresh 400                                                                                                                                                                           
set ENodeBFunction=1$ ulHeavyUeBsrHyst 100                                                                                                                                                                             
set Lm=1,FeatureState=CXC4010620$ FeatureState 1                                                                                                                                                                       
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1$ cellAddRsrpThresholdNR -110                                                                                                                                        
set EUtranCell.*DD=.*.,GUtranFreqRelation=.* cellAddRsrpThrNROverride -1000                                                                                                                                            
set Lm=1,FeatureState=CXC4012732$ FeatureState 1                                                                                                                                                                       
set Lm=1,FeatureState=CXC4011482$ FeatureState 1                                                                                                                                                                       
set EUtranCell.*DD=.* decoupledPdcchLaEnabled TRUE                                                                                                                                                                     
set EUtranCell.*DD=.* pdcchUlDtxWorseThres 10                                                                                                                                                                          
set Lm=1,FeatureState=CXC4011422$ FeatureState 1                                                                                                                                                                       
set ENodeBFunction=1$ rxBranchImbalanceThreshold 80                                                                                                                                                                    
set ENodeBFunction=1$ antSysMonitoringAlarmHandling TRUE                                                                                                                                                               
set Lm=1,FeatureState=CXC4012024$ FeatureState 1                                                                                                                                                                       
                                                                                                                                                                                                                       
mr L18bw20                                                                                                                                                                                                             
ma L18bw20 EUtranCellFDD.*F3 dlChannelBandwidth 20000                                                                                                                                                                  
bl L18bw20                                                                                                                                                                                                             
set L18bw20 zzzTemporary79 1                                                                                                                                                                                           
                                                                                                                                                                                                                       
mr NRssb                                                                                                                                                                                                               
ma NRssb NRCellDU ssbPowerBoost 0                                                                                                                                                                                      
set NRssb ssbPowerBoostMMimoSleep 3                                                                                                                                                                                    
                                                                                                                                                                                                                       
set Lm=1,FeatureState=CXC4012635 featureState 1                                                                                                                                                                        
set NRCellDU=.* rimDetectionEnabled TRUE                                                                                                                                                                               
set NRCellDU=.* rimPdschSlotBlankMode 1                                                                                                                                                                                
set NRCellDU=.* rimPdschSlotBlankTimer 1260                                                                                                                                                                            
                                                                                                                                                                                                                       
ldeb  NRSectorCarrier=                                                                                                                                                                                                 
ldeb  NRCellDU=.*                                                                                                                                                                                                      
                                                                                                                                                                                                                       
                                                                                                                                                                                                                       
$date = `date +%y%m%d_%H%M`                                                                                                                                                                                            
cvms Post_GPL_NR_R_PA_19_$date                                                                                                                                                                                         
                                                                                                                                                                                                                       
////////5G NSA LMS//////////////

lt all
rbs
rbs

confb+
gs+

cvms Pre_LMS_NR_TN_R_PA_19_$date

set . endcDlNrRetProhibTimer 400
set . endcDlNrQualHyst 3
set . initialUplinkConf SCG
set . endcUlNrRetProhibTimer 1000
set . dcDlAggActTime 1
set . dcDlAggExpiryTimer 100
set . ulDataSplitThreshold 102400
set . ulDataSplitThresholdMcg -1

set NRCellRelation= isHoAllowed true
set NRCellDU=.* endcDlLegSwitchEnabled true
set NRCellDU=.* endcDlNrLowQualThresh 0
set NRCellDU=.* endcUlLegSwitchEnabled true
set NRCellDU=.* endcUlNrLowQualThresh 5
set NRCellDU=.* endcUlNrQualHyst 6
set NRCellCU=.* mcpcPSCellEnabled true

cr GNBCUCPFunction=1,IntraFreqMC=1
cr GNBCUCPFunction=1,IntraFreqMC=1,IntraFreqMCCellProfile=1

set IntraFreqMC=1,IntraFreqMCCellProfile=1 betterSpCellTriggerQuantity 0
set IntraFreqMC=1,IntraFreqMCCellProfile=1 rsrpBetterSpCell hysteresis=10,offset=30,timeToTrigger=640


set IntraFreqMC=1,IntraFreqMCCellProfile=1 rsrpSCellCoverage hysteresis=10,threshold=-117
set IntraFreqMC=1,IntraFreqMCCellProfile=1 rsrpBetterSCell offset=30,hysteresis=10
set Mcpc=1,McpcPSCellProfile=.*,McpcPSCellProfileUeCfg=Base  rsrpCriticalEnabled true
set Mcpc=1,McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base rsrpSearchZone threshold=-112,hysteresis=10,timeToTriggerA1=160
set Mcpc=1,McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base rsrpCandidateA5 threshold1=-118,threshold2=-112,hysteresis=10,timeToTrigger=640
set Mcpc=1,McpcPSCellNrFreqRelProfile=Default,McpcPSCellNrFreqRelProfileUeCfg=Base rsrpCandidateA5Offsets threshold1Offset=0,threshold2Offset=0
set Mcpc=1,McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base rsrpCritical threshold=-110,timeToTrigger=256,hysteresis=20
set FeatureState=CXC4012375 featurestate 1
set FeatureState=CXC4012273 featurestate 1

cvms Post_LMS_NR_TN_R_PA_19_$date

confb-

lt all
Confb+
cvms Pre_Qos_Map

set QciTable=default,QciProfilePredefined=qci6$              dscp              32
set QciTable=default,QciProfilePredefined=qci7$              dscp              40
set QciTable=default,QciProfilePredefined=qci8$              dscp             30

set QosProfiles=1,DscpPcpMap=1  pcp0
set QosProfiles=1,DscpPcpMap=1  pcp1
set QosProfiles=1,DscpPcpMap=1  pcp2
set QosProfiles=1,DscpPcpMap=1  pcp3
set QosProfiles=1,DscpPcpMap=1  pcp4
set QosProfiles=1,DscpPcpMap=1  pcp5
set QosProfiles=1,DscpPcpMap=1  pcp6
set QosProfiles=1,DscpPcpMap=1  pcp7

lset Transport=1,QosProfiles=1,DscpPcpMap=1 pcp0 0,1,2,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,36,37,38,39,41,43,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp2 22,24,26

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp3 6,8,10,30,32

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp4 12,14,40

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp5 4,28

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp6 16,18,34,42,44

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp7 20,46

set SctpProfile=Node_Internal_F1  dscp 46


set ENodeBFunction=1              interEnbCaTunnelDscp 26
set ENodeBFunction=1              interEnbUlCompTunnelDscp 26
set ENodeBFunction=1              x2GtpuEchoDscp 46
set SctpProfile=1  dscp 46

cvms Post_Qos_Map

Confb-

                                                                                                                                                                           
"""


####################################################### --- TN ----- ##########################################################


TN_GNBDUFUNCTION_ELEMENT = """ 
crn GNBDUFunction=1,NRSectorCarrier={nRSectorCarrierId}
administrativeState 1
arfcnDL {arfcnDL}
arfcnUL {arfcnUL}
bSChannelBwDL {bSChannelBwDLUL}
bSChannelBwUL {bSChannelBwDLUL}
configuredMaxTxPower {configuredMaxTxPower}
latitude {Latitude}
longitude {Longitude}
sectorEquipmentFunctionRef NodeSupport=1,SectorEquipmentFunction={sectorEquipmentFunctionId}
txDirection 0
txPowerChangeRate 1
txPowerPersistentLock false
txPowerRatio 100
end
#END GNBDUFunction=1,NRSectorCarrier={nRSectorCarrierId} --------------------

crn GNBDUFunction=1,NRCellDU={gUtranCell}
csiRsConfig16P csiRsControl16Ports=0
csiRsConfig2P aRestriction=3F,csiRsControl2Ports=1
csiRsConfig32P csiRsControl32Ports=0
csiRsConfig4P csiRsControl4Ports=1,i11Restriction=FF
csiRsConfig8P csiRsControl8Ports=1,i11Restriction=FFFF
pLMNIdList mcc=404,mnc=94
sibType2 siBroadcastStatus=0,siPeriodicity=64
sibType4 siBroadcastStatus=0,siPeriodicity=64
sibType5 siBroadcastStatus=0,siPeriodicity=64
sibType6 siBroadcastStatus=0,siPeriodicity=16
sibType7 siBroadcastStatus=0,siPeriodicity=64
sibType8 siBroadcastStatus=0,siPeriodicity=64
ailgDlPrbLoadLevel 0
ailgModType 0
ailgPdcchLoadLevel 0
bandListManual 78
cellBarred 1
cellLocalId {cellLocalId}
cellRange 12000
cellReservedForOperator 1
csiReportFormat 0
csiRsPeriodicity 40
dftSOfdmMsg3Enabled false
dftSOfdmPuschEnabled false
dl256QamEnabled true
dlMaxMuMimoLayers 0
dlStartCrb 0
endcUlLegSwitchEnabled true
endcUlNrLowQualThresh -4
endcUlNrQualHyst 6
maxUeSpeed 2
nRPCI {nRPCI}
nRSectorCarrierRef GNBDUFunction=1,NRSectorCarrier={nRSectorCarrierId}
nRTAC {nRTAC}
pdschStartPrbStrategy 3
pMax 23
puschStartPrbStrategy 3
pZeroNomPucch -110
pZeroNomPuschGrant -102
qRxLevMin -128
rachPreambleFormat 0
rachPreambleRecTargetPower -110
rachPreambleTransMax 10
rachRootSequence 733
secondaryCellOnly false
siWindowLength 20
ssbDuration 1
ssbFrequency {ssbFrequency}
ssbOffset 0
ssbPeriodicity 20
ssbSubCarrierSpacing 30
subCarrierSpacing 30
tddSpecialSlotPattern 1
tddUlDlPattern 1
trsPeriodicity 40
trsPowerBoosting 0
ul256QamEnabled true
ulMaxMuMimoLayers 0
ulStartCrb 0
userLabel {gUtranCell}
end
#END GNBDUFunction=1,NRCellDU={gUtranCell} --------------------


crn GNBDUFunction=1,NRSectorCarrier={nRSectorCarrierId},CommonBeamforming=1
cbfMacroTaperType 0
coverageShape 1
digitalTilt 30
end
#END GNBDUFunction=1,NRSectorCarrier={nRSectorCarrierId},CommonBeamforming=1 --------------------
"""


TN_GNBCUCPFUNCTION_ELEMENT = """ 
crn GNBCUCPFunction=1,NRCellCU={gUtranCell}
cellLocalId {cellLocalId}
qHyst 4
sNonIntraSearchP 0
threshServingLowP 0
transmitSib2 false
transmitSib4 false
transmitSib5 false
userLabel {gUtranCell}
end
#END GNBCUCPFunction=1,NRCellCU={gUtranCell} --------------------

crn GNBCUCPFunction=1,NRNetwork=1
end
#END GNBCUCPFunction=1,NRNetwork=1 --------------------

crn GNBCUCPFunction=1,NRNetwork=1,NRFrequency=629952-30
arfcnValueNRDl 629952
bandListManual 78
smtcDuration 1
smtcOffset 0
smtcPeriodicity 20
smtcScs 30
end
#END GNBCUCPFunction=1,NRNetwork=1,NRFrequency=629952-30 --------------------

crn GNBCUCPFunction=1,NRCellCU={gUtranCell},NRFreqRelation=629952
anrMeasOn true
cellReselectionPriority 7
nRFrequencyRef GNBCUCPFunction=1,NRNetwork=1,NRFrequency=629952-30
end
#END GNBCUCPFunction=1,NRCellCU={gUtranCell},NRFreqRelation=629952 --------------------
"""