UPW_GPL_LMS_DST_SCRIPT = """

lt all
rbs
rbs

$date = `date +%y%m%d_%H%M`
cvms Pre_GPL_LMS_LTE_DL_R_PA_15_$date

confbd+

set CXC4012371 featurestate 1
set CXC4011803 featurestate 1
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
set CXC4010620 featurestate 1
set CXC4012578 featurestate 1
set CXC4012015 featurestate 1
set CXC4012480 featurestate 0

set ENodeBFunction=1,EUtranCell.*DD= endcSetupDlPktVolThr 100
set EUtranCell.*DD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1 hysteresisA5 20
wait 5
set UePolicyOptimization=1  endcAwareImc 2

set CarrierAggregationFunction=1 dcSCellActDeactDataThres 30
set CarrierAggregationFunction=1 dcSCellActDeactDataThresHyst 30
set CarrierAggregationFunction=1 dcSCellDeactDelayTimer 200
set CarrierAggregationFunction=1 endcCaPolicy 1
set EUtranCell.DD=.*,UeMeasControl=1 endcMeasRestartTime 10000
set EUtranCell.DD=.*  measGapPattEndc 1
set ENodeBFunction=1   endcS1OverlapMode True
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




set EUtranCellFDD=UW_E_F1.* primaryUpperLayerInd 1
set EUtranCellFDD=UW_E_F1.* additionalUpperLayerIndList 1 1 1 1 1 

set EUtranCellFDD=UW_E_F5.* primaryUpperLayerInd 0
set EUtranCellFDD=UW_E_F5.* additionalUpperLayerIndList 0 0 0 0 0


set ^EUtranCell.DD=.* endcAllowedPlmnList mcc=404,mnc=97,mnclength=2



set EUtranFreqRelation=365      endcHoFreqPriority 7
set EUtranFreqRelation=2545      endcHoFreqPriority 6


set EUtranFreqRelation=365    endcAwareIdleModePriority 7
set EUtranFreqRelation=2545    endcAwareIdleModePriority 6




cr ENodeBFunction=1,UePolicyOptimization=1
set UePolicyOptimization=1      t320              180
set GUtranFreqRelation=627936    endcB1MeasPriority 7
set ENodeBFunction=1       endcAllowed       true
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= triggerQuantityA5 0
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= reportQuantityA5  0
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= timeToTriggerA5  100
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= a5Threshold1Rsrp -44
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= a5Threshold1Rsrq -195
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= a5Threshold2Rsrp -115
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= a5Threshold2Rsrq -195
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= hysteresisA5 20

set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB1GUtra=1 triggerQuantityB1 0
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB1GUtra=1 b1ThresholdRsrp -105
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB1GUtra=1 b1ThresholdRsrq -435

set EUtranCell.DD=.*,GUtranFreqRelation=627936 b1ThrRsrpFreqOffset 0
set EUtranCell.DD=.*,GUtranFreqRelation=627936 b1ThrRsrqFreqOffset 0
set EUtranCell.DD=.*,GUtranFreqRelation=627936 qOffsetFreq 0

set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB1GUtra=1 hysteresisB1     0
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB1GUtra=1 timeToTriggerB1  0

set LoadBalancingFunction=1        lbAllowedForEndcUe False
set ENodeBFunction=1               endcSplitAllowedMoVoice false

lt all


set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA1A2Endc=1 qciA1A2ThrOffsetsEndc  a1a2ThrRsrpQciOffsetEndc=0,a1a2ThrRsrqQciOffsetEndc=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffsetEndc=0,a1a2ThrRsrqQciOffsetEndc=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6

mr TABTAB21
ma TABTAB21 ^eutrancell arfcn ^2545
pr TABTAB21
if $nr_of_mos >= 1
for $mo in TABTAB21
$mordn = rdn($mo)
set $mordn,UeMeasControl=1,ReportConfigA1A2Endc=1 qciA1A2ThrOffsetsEndc  a1a2ThrRsrpQciOffsetEndc=-4,a1a2ThrRsrqQciOffsetEndc=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffsetEndc=-56,a1a2ThrRsrqQciOffsetEndc=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6
set $mordn,UeMeasControl=1,ReportConfigSearch qciA1A2ThrOffsets     qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffset=72,a1a2ThrRsrQQciOffset=140,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci30;a1a2ThrRsrpQciOffset=72,a1a2ThrRsrQQciOffset=140,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci31
done
fi

mr TABTAB85
ma TABTAB85 ^eutrancell arfcn ^365$
pr TABTAB85
if $nr_of_mos >= 1
for $mo in TABTAB85
$mordn = rdn($mo)
set $mordn,UeMeasControl=1,ReportConfigA1A2Endc=1 qciA1A2ThrOffsetsEndc  a1a2ThrRsrpQciOffsetEndc=-21,a1a2ThrRsrqQciOffsetEndc=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffsetEndc=-4,a1a2ThrRsrqQciOffsetEndc=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6
set $mordn,UeMeasControl=1,ReportConfigSearch qciA1A2ThrOffsets     qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffset=-2,a1a2ThrRsrQQciOffset=-30,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci30;a1a2ThrRsrpQciOffset=-2,a1a2ThrRsrQQciOffset=-30,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci31
done
fi



set QciTable=default,QciProfilePredefined=qci6$ relativePriority 2
set QciTable=default,QciProfileOperatorDefined=qci30$ relativePriority 100


cr EnodeBfunction=1,PmFlexCounterFilter=ENDC
set EnodeBfunction=1,PmFlexCounterFilter=ENDC endcFilterEnabled true
set EnodeBFunction=1,PmFlexCounterFilter=ENDC endcFilterMin 2

Set SubscriberGroupProfile=ENDC                             profilePriority   5

st EUtranCellTDD
if $nr_of_mos = 0
set Lm=1,FeatureState=CXC4011476 featurestate  0
set Lm=1,FeatureState=CXC4011559 featurestate  0
set Lm=1,FeatureState=CXC4011666 featurestate  0
set Lm=1,FeatureState=CXC4011922 featurestate  0
set Lm=1,FeatureState=CXC4011983 featurestate  0
set Lm=1,FeatureState=CXC4012111 featurestate  0
set Lm=1,FeatureState=CXC4012123 featurestate  0
set Lm=1,FeatureState=CXC4011973 featurestate  0
set Lm=1,FeatureState=CXC4012097 featurestate  0
else
st cell
fi


set CarrierAggregationFunction=1 endcCaPolicy 1
set EUtranCellFDD=.* lbActionForEndcUe 0

set . anrstateNR 1

set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          gNodebIdLength 26




mr TABTAB21
ma TABTAB21 ^eutrancell arfcn ^365
pr TABTAB21
if $nr_of_mos >= 1
for $mo in TABTAB21
$mordn = rdn($mo)
set $mordn,UeMeasControl=1,ReportConfigA1A2Endc=1 qciA1A2ThrOffsetsEndc  a1a2ThrRsrpQciOffsetEndc=-15,a1a2ThrRsrqQciOffsetEndc=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffsetEndc=0,a1a2ThrRsrqQciOffsetEndc=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6
done
fi


mr TABTAB85
ma TABTAB85 ^eutrancell arfcn ^2545
pr TABTAB85
if $nr_of_mos >= 1
for $mo in TABTAB85
$mordn = rdn($mo)
set $mordn,UeMeasControl=1,ReportConfigA1A2Endc=1 qciA1A2ThrOffsetsEndc  a1a2ThrRsrpQciOffsetEndc=0,a1a2ThrRsrqQciOffsetEndc=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffsetEndc=0,a1a2ThrRsrqQciOffsetEndc=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6
 
done
fi
 

rdel ENodeBFunction=1,SubscriberGroupProfile=ENDC

rdel ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci30

rdel ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci31


set UePolicyOptimization zzzTemporary1 1
set GUtranFreqRelation=.* anrMeasOn true

set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= a5Threshold2Rsrp -112
set ENodeBFunction=1,EUtranCell.*DD= endcSetupDlPktVolThr 100
set ENodeBFunction=1 x2retryTimerMaxAuto 1440
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB1GUtra=1 hysteresisB1     6
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB1GUtra=1 timeToTriggerB1  640



lt all
rbs
rbs

confb+

st nrcell
if $nr_of_mos = 0
set EUtranCellFDD=UW_E_F1.* additionalUpperLayerIndList 0 0 0 0 0
set EUtranCellFDD=UW_E_F1.* primaryUpperLayerInd 0
else
set EUtranCellFDD=UW_E_F1.* primaryUpperLayerInd 1
set EUtranCellFDD=UW_E_F1.* additionalUpperLayerIndList 1 1 1 1 1 
fi

lt all

set UePolicyOptimization=1  endcAwareImc 2

crn Transport=1,Router=LTEUP,TwampResponder=NR
ipAddress Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
udpPort 4001
userLabel 
end

confb-

confbd-
gs-


lt all

gs+

confbd+

###added SubscriberGroupProfile=ENDC(PA13)
crn ENodeBFunction=1,SubscriberGroupProfile=ENDC
customTriggerType 2
customTriggerList 2
qciOffsetForQCI6 24
qciOffsetForQCI9 22
end


###added Qci30=Qci6 and Qci31=Qci9//set eutranFreqToQciProfileRelation values (PA13)

crn ENodeBFunction=1,QciTable=default,QciProfileOperatordefined=qci30
absPrioOverride                      0
aqmMode                              1
bitRateRecommendationEnabled         false
caOffloadingEnabled                  false
counterActiveMode                    false
dataFwdPerQciEnabled                 true
dlMaxHARQTxQci                       5
dlMaxWaitingTime                     0
dlMinBitRate                         2000
dlResourceAllocationStrategy         1
drxPriority                          0
drxProfileRef                        ENodeBFunction=1,DrxProfile=0
dscp                                 26
endcProfileRef                       EndcProfile=1
harqPriority                         0
inactivityTimerOffset                0
laaSupported                         true
lessMaxDelayThreshold                0
logicalChannelGroupRef               QciTable=default,LogicalChannelGroup=3
paPartitionOverride                  false
pdb                                  300
pdbOffset                            0
pdcpSNLength                         12
priority                             6
priorityFraction                     0
qci                                  30
qciACTuning                          1000
qciSubscriptionQuanta                200
relativePriority                     2
resourceAllocationStrategy           1
resourceType                         0
rlcMode                              0
rlcSNLength                          10
rlfPriority                          0
rlfProfileRef                        RlfProfile=0
rohcEnabled                          false
rohcForUlDataEnabled                 false
schedulingAlgorithm                  4
serviceType                          0
srsAllocationStrategy                0
tReorderingDl                        35
tReorderingUl                        60
timerPriority                        0
timerProfileRef
ulMaxHARQTxQci                       5
ulMaxWaitingTime                     0
ulMinBitRate                         300
zzzTemporary1
zzzTemporary2
zzzTemporary3                        -2000000000
zzzTemporary4                        -2000000000
zzzTemporary5                        -2000000000
end

crn ENodeBFunction=1,QciTable=default,QciProfileOperatordefined=qci31
absPrioOverride                      0
aqmMode                              1
bitRateRecommendationEnabled         false
caOffloadingEnabled                  false
counterActiveMode                    false
dataFwdPerQciEnabled                 true
dlMaxHARQTxQci                       5
dlMaxWaitingTime                     0
dlMinBitRate                         0
dlResourceAllocationStrategy         1
drxPriority                          0
drxProfileRef                        ENodeBFunction=1,DrxProfile=0
dscp                                 26
endcProfileRef                       EndcProfile=1
harqPriority                         0
inactivityTimerOffset                0
laaSupported                         true
lessMaxDelayThreshold                0
logicalChannelGroupRef               QciTable=default,LogicalChannelGroup=3
paPartitionOverride                  false
pdb                                  300
pdbOffset                            0
pdcpSNLength                         12
priority                             9
priorityFraction                     0
qci                                  31
qciACTuning                          1000
qciSubscriptionQuanta                200
relativePriority                     1
resourceAllocationStrategy           1
resourceType                         0
rlcMode                              0
rlcSNLength                          10
rlfPriority                          0
rlfProfileRef                        RlfProfile=0
rohcEnabled                          false
rohcForUlDataEnabled                 false
schedulingAlgorithm                  4
serviceType                          0
srsAllocationStrategy                0
tReorderingDl                        35
tReorderingUl                        35
timerPriority                        0
timerProfileRef
ulMaxHARQTxQci                       5
ulMaxWaitingTime                     0
ulMinBitRate                         0
zzzTemporary1                        
zzzTemporary2
zzzTemporary3                        -2000000000
zzzTemporary4                        -2000000000
zzzTemporary5                        -2000000000
end

mr TABTAB21
ma TABTAB21 ^eutrancell arfcn ^2545
pr TABTAB21
if $nr_of_mos >= 1
for $mo in TABTAB21
$mordn = rdn($mo)

 

set $mordn,UeMeasControl=1,ReportConfigSearch qciA1A2ThrOffsets     qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffset=0,a1a2ThrRsrQQciOffset=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci30;a1a2ThrRsrpQciOffset=0,a1a2ThrRsrQQciOffset=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci31

 

done
fi

 

mr TABTAB85
ma TABTAB85 ^eutrancell arfcn ^365$
pr TABTAB85
if $nr_of_mos >= 1
for $mo in TABTAB85
$mordn = rdn($mo)

 

set $mordn,UeMeasControl=1,ReportConfigSearch qciA1A2ThrOffsets     qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffset=0,a1a2ThrRsrQQciOffset=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci30;a1a2ThrRsrpQciOffset=0,a1a2ThrRsrQQciOffset=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci31

 

done
fi

gs-
confbd-

gs+
confb+
set EUtranFreqRelation=365      endcHoFreqPriority 7
set EUtranFreqRelation=2545      endcHoFreqPriority 6
set EUtranFreqRelation=1526     endcHoFreqPriority -1
set EUtranFreqRelation=39348     endcHoFreqPriority -1
set EUtranFreqRelation=39150      endcHoFreqPriority -1
set EUtranFreqRelation=39349      endcHoFreqPriority -1
set EUtranFreqRelation=39151      endcHoFreqPriority -1


set EUtranFreqRelation=365      endcAwareIdleModePriority 6
set EUtranFreqRelation=2545      endcAwareIdleModePriority 5
set EUtranFreqRelation=1526     endcAwareIdleModePriority 3
set EUtranFreqRelation=39348     endcAwareIdleModePriority 4
set EUtranFreqRelation=39150      endcAwareIdleModePriority 4
set EUtranFreqRelation=39349      endcAwareIdleModePriority 6
set EUtranFreqRelation=39151      endcAwareIdleModePriority 6

set ENodeBFunction=1,EUtranCell.*DD= endcSetupDlPktVolThr 5

set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB1GUtra=1 hysteresisB1     0


set GUtranFreqRelation=627936    endcB1MeasPriority 7


set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          pciConflictDetectionType 3
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          endcRachFailThrPerUe 5
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          maxNoOfUeForPciConflictDetect 5
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          scgSessTimeForEndcRachFail 2500
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          supportNrFreqChange 1
set EUtranCellFDD=.*  endcSetupUlBsVolThr 5000
set FmAlarmType=RadioInterfaceConnectivityDisturbanceAlert isNotified 0 
set EUtranCellFDD=.* optimizedPdcchCongestThres 30



gs-
confb-

$date = `date +%y%m%d_%H%M`
cvms Post_GPL_LMS_LTE_DL_R_PA_15_$date


################UPW GPL V5 ###########EKUMNEE#######

lt all
rbs
rbs
confbd+

$date = `date +%y%m%d_%H%M`
cvms Pre_GPL_LMS_L2100swap_$date



rdel EUtranFreqRelation=36500

rdel EUtranFreqRelation=2539

rdel EUtranFrequency=2539

rdel EUtranFrequency=36500

rdel EUtranFreqRelation=1409

rdel EUtranFrequency=1409


########Frequency Creation##########

cr ENodeBFunction=1,GeraNetwork=1

cr ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
1 #frequencyGroupId

func Gran_freq
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=$t
$t
0
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=$t geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
endfunc


for $t = 637 to 639
Gran_freq
done

for $t = 709 to 711
Gran_freq
done

lt all

cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39150
39150
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39348
39348
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1526
1526
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=365
365
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=2545
2545
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39151
39151
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39349
39349

##########GERANFREQ##################

unset all


$Par[1] = L2100

mr L2100

ma L2100 EUtranCellFDD earfcn 365

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
  3
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
  3
 fi
done
endfunc

func EURel_365
for $mo in $Par[$i]
 $mordn = rdn($mo)
 pr $mordn,EUtranFreqRelation=365$
 if $nr_of_mos = 0
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=365
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=365
  4
 fi
done
endfunc

func EURel_1526
for $mo in $Par[$i]
 $mordn = rdn($mo)
 pr $mordn,EUtranFreqRelation=1526
 if $nr_of_mos = 0
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=1526
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1526
  6
 fi
done
endfunc

func EURel_2545
for $mo in $Par[$i]
 $mordn = rdn($mo)
 pr $mordn,EUtranFreqRelation=2545
 if $nr_of_mos = 0
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=2545
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=2545
  2
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
  3
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
  3
fi
done
endfunc


for $i = 1 to 2
EURel_39150
EURel_39348
EURel_365
EURel_1526
EURel_2545
EURel_39151
EURel_39349
Gran_Rel
done

########################################
cr Transport=1,Synchronization=1,TimeSyncIO=1,GnssInfo=1
########################################

### CRS GAIN

setm EUtranCellFDD crsGain 0 pdschTypeBGain 0



####Fixed Parameter

## Admission control

set AdmissionControl=1 admNrRrcDifferentiationThr 750
set AdmissionControl=1 admNrRbDifferentiationThr 750
set AdmissionControl=1 arpBasedPreEmptionState 0
set AdmissionControl=1 ulAdmOverloadThr 950
set AdmissionControl=1 ulTransNwBandwidth 2000
set AdmissionControl=1 dlAdmDifferentiationThr 750
set AdmissionControl=1 ulAdmDifferentiationThr 750

#ANRFUNCTION

set AnrFunction=1 cellRelHoAttRateThreshold 15
set AnrFunction=1 maxNoPciReportsEvent 30
set AnrFunction=1 probCellDetectLowHoSuccTime 4
set AnrFunction=1 probCellDetectMedHoSuccTime 2
set AnrFunction=1 problematicCellPolicy 1
set AnrFunction=1 removeNcellTime   3
set AnrFunction=1 removeNenbTime    3
set AnrFunction=1 removeNrelTime 1
set AnrFunction=1 probCellDetectMedHoSuccThres 50
set AnrFunction=1,AnrFunctionEUtran=1 cellAddRsrpThresholdEutran -1240
set AnrFunction=1,AnrFunctionEUtran=1 cellAddRsrqThresholdEutran -1530
set ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1 anrStateUtran 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionGeran=1 anrStateGsm 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 anrIntraFreqState 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 anrInterFreqState 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 hoAllowedEutranPolicy 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 x2SetupPolicy 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1 hoAllowedUtranPolicy 1
set AnrFunction=1,AnrFunctionEUtran=1 anrUesEUtraIntraFMax 0
set AnrFunction=1,AnrFunctionEUtran=1 anrUesThreshInterFMax 0
set AnrFunction=1,AnrFunctionEUtran=1 anrUesEUtraIntraFMin 0
set AnrFunction=1,AnrFunctionEUtran=1 anrUesThreshInterFMin 0
set AnrFunction=1,AnrFunctionUtran=1 cellAddEcNoThresholdUtranDelta -10
set AnrFunction=1,AnrFunctionUtran=1 cellAddRscpThresholdUtranDelta -1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1 hoAllowedUtranPolicy 1
set AnrPciConflictDrxProfile=1                              anrPciConflictDrxInactivityTimer 8
set AnrPciConflictDrxProfile=1                              anrPciConflictOnDurationTimer 4

#CarrierAggFunction

set CarrierAggregationFunction=1                            dynamicSCellSelectionMethod 2
set CarrierAggregationFunction=1                            fourLayerMimoPreferred false
set CarrierAggregationFunction=1                            enhancedSelectionOfMimoAndCa false
set CarrierAggregationFunction=1                            waitForAdditionalSCellOpportunity 10000
set CarrierAggregationFunction=1                            sCellActProhibitTimer 10
set CarrierAggregationFunction=1                            selectionPolicyUlWeighting 50
set CarrierAggregationFunction=1                            waitForBlindSelSCellRepLessTtt 600


#DRB

set RadioBearerTable=default,DataRadioBearer=1 tPollRetransmitUl 80
set RadioBearerTable=default,DataRadioBearer=1 tPollRetransmitDl 80
set DataRadioBearer dlMaxRetxThreshold 16
set DataRadioBearer ulMaxRetxThreshold 32


#DrxProfile

lset QciTable=default,QciProfilePredefined=qci1 drxProfileRef DrxProfile=1
lset QciTable=default,QciProfilePredefined=qci2 drxProfileRef DrxProfile=2
lset QciTable=default,QciProfilePredefined=qci5 drxProfileRef DrxProfile=0
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
lset QciTable=default,QciProfilePredefined=qci1 drxProfileRef DrxProfile=1
lset QciTable=default,QciProfilePredefined=qci2 drxProfileRef DrxProfile=2
lset QciTable=default,QciProfilePredefined=qci5 drxProfileRef DrxProfile=0
lset ENodeBFunction=1,DrxProfile=1$ drxInactivityTimer 6
lset ENodeBFunction=1,DrxProfile=2$ drxInactivityTimer 6
lset ENodeBFunction=1,DrxProfile=0$ drxInactivityTimer 14
lset ENodeBFunction=1,DrxProfile=1$ drxState 0

#EnodeBFunction

set ENodeBFunction alignTtiBundWUlTrigSinr 1
set ENodeBFunction=1 dscpLabel 46
set ENodeBFunction=1 gtpuErrorIndicationDscp 46
set ENodeBFunction rrcConnReestActive 1
set ENodeBFunction=1 tRelocOverall 20
set ENodeBFunction=1 tS1HoCancelTimer 3
set ENodeBFunction=1                                        enabledUlTrigMeas false
set ENodeBFunction=1                                        zzzTemporary52    1
set ENodeBFunction=1                                        zzzTemporary55    -2000000000
set ENodeBFunction=1                                        csfbMeasFromIdleMode 1
set ENodeBFunction=1 s1GtpuEchoDscp 46
set ENodeBFunction=1 x2GtpuEchoDscp 46
set ENodeBFunction=1                                        x2SetupTwoWayRelations true
set ENodeBFunction=1                                        dnsLookupOnTai 1
set ENodeBFunction=1                                        zzzTemporary13    -2000000000
set ENodeBFunction=1                                        caAwareMfbiIntraCellHo false
set ENodeBFunction=1                                        mfbiSupportPolicy false
set ENodeBFunction=1                                        s1HODirDataPathAvail True
set ENodeBFunction=1                                        gtpuErrorIndicationDscp         46
set ENodeBFunction=1                                        timePhaseMaxDeviationIeNbCa 30
set ENodeBFunction=1                                        s1GtpuEchoEnable 0
set ENodeBFunction=1                                        checkEmergencySoftLock false
set ENodeBFunction=1                                        combCellSectorSelectThreshRx 300
set ENodeBFunction=1                                        combCellSectorSelectThreshTx 300
set ENodeBFunction=1                                        licConnectedUsersPercentileConf 90
set ENodeBFunction=1                                        tddVoipDrxProfileId -1
set ENodeBFunction=1                                        timePhaseMaxDeviation 100
set ENodeBFunction=1                                        timePhaseMaxDeviationEdrx 10
set ENodeBFunction=1                                        timePhaseMaxDeviationMbms 50
set ENodeBFunction=1                                        timePhaseMaxDeviationOtdoa 9
set ENodeBFunction=1                                        timePhaseMaxDeviationSib16 100
set ENodeBFunction=1                                        timePhaseMaxDeviationTdd 15
set ENodeBFunction=1                                        timePhaseMaxDeviationTdd1 15
set ENodeBFunction=1                                        timePhaseMaxDeviationTdd2 15
set ENodeBFunction=1                                        timePhaseMaxDeviationTdd3 15
set ENodeBFunction=1                                        timePhaseMaxDeviationTdd4 15
set ENodeBFunction=1                                        timePhaseMaxDeviationTdd5 15
set ENodeBFunction=1                                        timePhaseMaxDeviationTdd6 15
set ENodeBFunction=1                                        timePhaseMaxDeviationTdd7 15
set ENodeBFunction=1                                        timePhaseMaxDevIeNBUlComp 30
set ENodeBFunction=1                                        ulMaxWaitingTimeGlobal 0
set ENodeBFunction=1                                        ulSchedulerDynamicBWAllocationEnabled true
set ENodeBFunction=1                                        useBandPrioritiesInSCellEval false
set ENodeBFunction=1                                        x2GtpuEchoEnable  0
set ENodeBFunction=1                                        x2IpAddrViaS1Active true
set ENodeBFunction=1                                        x2retryTimerMaxAuto 1440
set ENodeBFunction=1                                        forcedSiTunnelingActive false
set ENodeBFunction=1  timeAndPhaseSynchAlignment True
set ENodeBFunction=1  timeAndPhaseSynchCritical True


#EUTRANCELLFDD

set EUtranCellFDD pdcchOuterLoopUpStep 8
set EUtranCellFDD pdcchOuterLoopUpStepPCell 6
set EUtranCellFDD ttiBundlingAfterHO 1
set EUtranCellFDD ttiBundlingAfterReest 1
set EUtranCellFDD ttiBundlingSwitchThres 150
set EUtranCellFDD ttiBundlingSwitchThresHyst 30
set EUtranCellFDD cellDownlinkCaCapacity 0
set EUtranCellFDD mappingInfo mappingInfoSIB12=7
set EUtranCellFDD mappingInfo mappingInfoSIB4=2
set EUtranCellFDD mappingInfo mappingInfoSIB6=4
set EUtranCellFDD                                 servOrPrioTriggeredErabAction 3
set EUtranCellFDD  dlInternalChannelBandwidth 0
set EUtranCellFDD  ulInternalChannelBandwidth 0
set EUtranCellFDD  beamWeightSet16Tr 0
set EUtranCellFDD  srvccDelayTimer 3000

set Eutrancell adaptiveCfiHoProhibit 0
set EUtranCell enableSinrUplinkClpc 1
set EUtranCell pdcchCovImproveQci1 true
set EUtranCell pdcchOuterLoopUpStepVolte 9
set EUtranCell pdcchTargetBlervolte 4
set EUtranCell allocThrPucchFormat1 50
set EUtranCell allocTimerPucchFormat1 50
set EUtranCell deallocThrPucchFormat1 100
set EUtranCell deallocTimerPucchFormat1 6000
set EUtranCell drxActive true
set EUtranCell dlBlerTargetEnabled 1
set EUtranCell enableServiceSpecificHARQ true
set EUtranCell pdcchCovImproveDtx true
set EUtranCell pdcchCovImproveSrb false
set EUtranCell pdcchTargetBler 24
set EUtranCell pdcchTargetBlerPCell 22
set EUtranCell pMaxServingCell 1000
set EUtranCell qRxLevMinOffset 1000
set EUtranCell tReorderingAutoConfiguration true
set EUtranCell tTimeAlignmentTimer 0
set EUtranCell ulBlerTargetEnabled true
set EUtranCell ulHarqVolteBlerTarget 3
set EutranCellFDD=UW_E_F1.* alpha 10
set EUtranCellFDD=UW_E_F1.* pZeroNominalPusch -100
set EUtranCellFDD=UW_E_F1.* pZeroNominalPucch -110
set EUtranCellFDD cellRange 6
set EUtranCell cfraEnable true
set EUtranCell cellDownlinkCaCapacity 0
set EUtranCell changeNotification changeNotificationSIB15=true
set EUtranCell changeNotification changeNotificationSIB16=true
set EUtranCell changeNotification changeNotificationSIB8=true
set EUtranCell hoOptAdjThresholdAbs 5
set EUtranCell hoOptAdjThresholdPerc 50
set EUtranCell pdcchCfiMode 5
set EUtranCell prsPowerBoosting 0
set EUtranCell transmissionMode 4
set EUtrancell ns05FullBandUsersInCellThres 1
set EUtranCell ns05FullBandSchedEnabled false
set EUtranCell  puschNcpChannelEstWindowSize 1
set EUtranCell mobCtrlAtPoorCovActive true
set EUtranCell  servOrPrioTriggeredIFHo 0
set EUtranCell  ul64qamEnabled    true
set EUtranCell  dl256QamEnabled   true
set EUtranCellFDD  commonSrPeriodicity 10
set EUtranCellFDD mappingInfo mappingInfoSIB5=3
set EUtranCell changeNotification changeNotificationSIB7=true
set EUtranCell changeNotification changeNotificationSIB2=true
set EUtranCell changeNotification changeNotificationSIB3=true
set EUtranCell changeNotification changeNotificationSIB4=true
set EUtranCell changeNotification changeNotificationSIB1=true
set EUtranCell changeNotification changeNotificationSIB6=true
set EUtranCell changeNotification changeNotificationSIB5=true
set EUtranCell changeNotification changeNotificationSIB13=true
set EUtranCell mappingInfoCe mappingInfoSIB10=0
set EUtranCell  qRxLevMinCe       -140
set EUtranCell  pdcchLaGinrMargin 40
set EUtranCell  acBarringPresence acBarringForMmtelVideoPresence=0
set EUtranCell  acBarringPresence acBarringForMmtelVoicePresence=0
set EUtranCell  acBarringPresence acBarringPriorityMmtelVideo=0
set EUtranCell  acBarringPresence acBarringPriorityMmtelVoice=0
set EUtranCell  acBarringPresence acBarringForMoDataPresence=0
set EUtranCell  noOfEnhAdptReTxCand -1
set EUtranCell  dynUlResourceAllocEnabled false
set EUtranCell systemInformationBlock6 tReselectionUtra=4
set EUtranCell advCellSupAction 2
set EUtranCell  primaryPlmnReserved false
set EUtranCell  harqOffsetDl      3
set EUtranCell  harqOffsetUl      3
set EUtranCell  highSpeedUEActive false
set EUtranCell  initialBufferSizeDefault 86
set EUtranCell  prsTransmisScheme 0
set EUtranCell  puschPwrOffset64qam 0
set EUtranCell  systemInformationBlock3 tEvaluation=240
set EUtranCell  elcEnabled        false
set EUtranCell  preambleInitialReceivedTargetPower -110
set EUtranCell  acBarringForCsfb acBarringFactor=95
set EUtranCell  acBarringForCsfb acBarringForSpecialAC=false false false false false
set EUtranCell  acBarringForCsfb acBarringTime=64
set EUtranCell  acBarringForEmergency false
set EUtranCell  acBarringForMoData acBarringFactor=95
set EUtranCell  acBarringForMoData acBarringForSpecialAC=false false false false false
set EUtranCell  acBarringForMoData acBarringTime=64
set EUtranCell  acBarringForMoSignalling acBarringFactor=95
set EUtranCell  acBarringForMoSignalling acBarringForSpecialAC=false false false false false
set EUtranCell  acBarringForMoSignalling acBarringTime=64
set EUtranCell  acBarringInfoPresent false
set EUtranCell  acBarringPresence acBarringForCsfbPresence=0
set EUtranCell  acBarringPresence acBarringForMoSignPresence=0
set EUtranCell  acBarringPresence acBarringPriorityCsfb=0
set EUtranCell  acBarringPresence acBarringPriorityMoData=0
set EUtranCell  acBarringPresence acBarringPriorityMoSignaling=0
set EUtranCell  spifhoSetupBearerAtInitialCtxtSetup false
set EUtranCell  srDetectHighThres 70
set EUtranCell  srProcessingLevel 0
set EUtranCell  ssacBarringForMMTELVideo acBarringFactor=95
set EUtranCell  ssacBarringForMMTELVideo acBarringForSpecialAC=false false false false false
set EUtranCell  ssacBarringForMMTELVideo acBarringTime=64
set EUtranCell  ssacBarringForMMTELVoice acBarringFactor=95
set EUtranCell  ssacBarringForMMTELVoice acBarringForSpecialAC=false false false false false
set EUtranCell  ssacBarringForMMTELVoice acBarringTime=64
set EUtranCell  systemInformationBlock3 nCellChangeHigh=16
set EUtranCell  systemInformationBlock3 nCellChangeMedium=16
set EUtranCell  systemInformationBlock3 qHystSfHigh=0
set EUtranCell  systemInformationBlock3 qHystSfMedium=0
set EUtranCell  systemInformationBlock3 sIntraSearchQ=0
set EUtranCell  systemInformationBlock3 sNonIntraSearchv920Active=false
set EUtranCell  systemInformationBlock3 sIntraSearchv920Active=false
set EUtranCell  systemInformationBlock3 tHystNormal=240
set EUtranCell  systemInformationBlock6 tReselectionUtraSfHigh=100
set EUtranCell  systemInformationBlock6 tReselectionUtraSfMedium=100
set EUtranCell  systemInformationBlock3 threshServingLowQ=1000
set EUtranCell  systemInformationBlock7 tReselectionGeran=2
set EUtranCell  systemInformationBlock7 tReselectionGeranSfHigh=100
set EUtranCell  systemInformationBlock7 tReselectionGeranSfMedium=100

set EUtranCell  tUeBlockingTimer  200
set EUtranCell  ulImprovedUeSchedLastEnabled true
set EUtranCell  ulPsdLoadThresholdSinrClpc 2
set EUtranCell  ulSCellPriority   5
set EUtranCell  ulSchedCtrlForOocUesEnabled true
set EUtranCell  ulSrsEnable       false
set EUtranCell  ulTrigActive      false
set EUtranCell  ulTxPsdDistrThr   40
set EUtranCell  uncertAltitude    0
set EUtranCell  uncertSemiMajor   0
set EUtranCell  uncertSemiMinor   0

set EUtranCell covTriggerdBlindHoAllowed 0
set EUtranCell qQualMin -34
set EUtranCell qQualMinOffset 0
set Eutrancell dlInterferenceManagementActive TRUE
set Eutrancell ulInterferenceManagementActive true
set EUtranCell  dlFrequencyAllocationProportion 100
set EUtranCell  ulConfigurableFrequencyStart 0
set EUtranCell  ulFrequencyAllocationProportion 100
set EUtranCell eUlFssSwitchThresh 30
set EUtranCell outOfCoverageSrTimerPeriodicity 320
set EUtranCell outOfCoverageThreshold 20
set EUtranCell outOfCoverageDepth 1
set EUtranCell outOfCoverageSparseGrantingBsr 8



#EUTRANFREQRELATION

set EUtranFreqRelation tReselectionEutra 2
set EUtranFreqRelation=.*          allowedPlmnList   mcc=404,mnc=97,mncLength=2
set EUtranFreqRelation caTriggeredRedirectionActive false
set EUtranFreqRelation anrMeasOn true
set EUtranFreqRelation       qRxLevMinCe       -140
set EUtranFreqRelation pMax 1000
lset EUtranFreqRelation=.* mobilityAction 1
set EUtranFreqRelation=.* lbBnrPolicy 2
set EUtranFreqRelation        tReselectionEutraCe 2
set EUtranFreqRelation tReselectionEutraSfHigh 100
set EUtranFreqRelation tReselectionEutraSfMedium 100
set LoadBalancingFunction=1                txPwrForOverlaidCellDetect 370
set RadioBearerTable=default,MACConfiguration=1 ulMaxHARQTx 5
set RadioBearerTable=default,MACConfiguration=1 dlMaxHARQTx 4
set RadioBearerTable=default,MACConfiguration=1 ulTtiBundlingMaxHARQTx 7
set EUtranCell.*,MimoSleepFunction=1              switchUpMonitorDurTimer 5
set Paging=1                                                pagingDiscardTimerDrxNb 3
set Paging=1                                                maxNoOfPagingRecordsNb 3
set Paging=1                                                noOfDefPagCyclPrim 8
set MdtConfiguration=1                                      a2ThresholdRsrpMdt -140
set MdtConfiguration=1                                      a2ThresholdRsrqMdt -195
set MdtConfiguration=1                                      timeToTriggerA2Mdt 640
set MdtConfiguration=1                                      triggerQuantityA2Mdt 0



#QciProfilePredefined

set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 tReorderingUl 50
set RadioBearerTable=default,SignalingRadioBearer=1 tReorderingUl 35
set QciTable=default,QciProfilePredefined=QCI1 absPrioOverride 0
set QciTable=default,QciProfilePredefined=QCI2 absPrioOverride 0
set QciTable=default,QciProfilePredefined=QCI5 absPrioOverride 1

set QciTable=default,QciProfilePredefined=QCI1 aqmMode 2
set QciTable=default,QciProfilePredefined=QCI2 aqmMode 2
set QciTable=default,QciProfilePredefined=QCI5 aqmMode 0

set QciProfilePredefined=qci1 counterActiveMode 0
set QciProfilePredefined=qci2 counterActiveMode 0
set QciProfilePredefined=qci5 counterActiveMode 0
set QciProfilePredefined=qci6 counterActiveMode 0
set QciProfilePredefined=qci7 counterActiveMode 0
set QciProfilePredefined=qci8 counterActiveMode 0
set QciProfilePredefined=qci9 counterActiveMode 0

set QciTable=default,QciProfilePredefined=qci6 dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci8 dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci9 dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci7 dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=QCI1 dataFwdPerQciEnabled 1
set QciTable=default,QciProfilePredefined=QCI2 dataFwdPerQciEnabled 1
set QciTable=default,QciProfilePredefined=QCI5 dataFwdPerQciEnabled 1
set QciTable=default,QciProfilePredefined=qci1 harqPriority 1
set QciTable=default,QciProfilePredefined=qci1 dlMaxHARQTxQci 7
set QciTable=default,QciProfilePredefined=qci1 ulMaxHARQTxQci 7
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 dlMinBitRate 384
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 ulMinBitRate 384
set QciTable=default,QciProfilePredefined=QCI1 dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=QCI2 dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=QCI5 dlResourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci1 drxPriority 99
set QciTable=default,QciProfilePredefined=qci2 drxPriority 100
set QciTable=default,QciProfilePredefined=qci5 drxPriority 1
lset QciTable=default,QciProfilePredefined=qci1 drxProfileRef DrxProfile=1
lset QciTable=default,QciProfilePredefined=qci2 drxProfileRef DrxProfile=2
lset QciTable=default,QciProfilePredefined=qci5 drxProfileRef DrxProfile=0
set QciTable=default,QciProfilePredefined=QCI1 dscp 34
set QciTable=default,QciProfilePredefined=QCI2 dscp 34
set QciTable=default,QciProfilePredefined=QCI5 dscp 46
set QciTable=default,QciProfilePredefined=qci1 harqPriority 1
set QciTable=default,QciProfilePredefined=QCI1 inactivityTimerOffset 30
set QciTable=default,QciProfilePredefined=QCI2 inactivityTimerOffset 30
set QciTable=default,QciProfilePredefined=QCI5 inactivityTimerOffset 0
set QciProfilePredefined=qci6 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set QciProfilePredefined=qci7 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set QciProfilePredefined=qci8 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set QciProfilePredefined=qci9 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set QciProfilePredefined=qci1 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=1
set QciProfilePredefined=qci2 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=2
set QciProfilePredefined=qci5 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=1
set QciTable=default,QciProfilePredefined=QCI1 Pdb 80
set QciTable=default,QciProfilePredefined=QCI2 Pdb 150
set QciTable=default,QciProfilePredefined=QCI5 Pdb 100
set QciTable=default,QciProfilePredefined=QCI1 PdbOffset 100
set QciTable=default,QciProfilePredefined=QCI2 PdbOffset 50
set QciTable=default,QciProfilePredefined=QCI5 PdbOffset 0
set QciTable=default,QciProfilePredefined=QCI1 pdcpSNLength 12
set QciTable=default,QciProfilePredefined=QCI2 pdcpSNLength 12
set QciTable=default,QciProfilePredefined=QCI5 pdcpSNLength 12
set QciTable=default,QciProfilePredefined=QCI1 Priority 1
set QciTable=default,QciProfilePredefined=QCI2 Priority 4
set QciTable=default,QciProfilePredefined=QCI5 Priority 2
set QciTable=default,QciProfilePredefined=QCI1 resourcetype 1
set QciTable=default,QciProfilePredefined=QCI2 resourcetype 1
set QciTable=default,QciProfilePredefined=QCI5 resourcetype 0
set QciTable=default,QciProfilePredefined=QCI1 rlcMode 1
set QciTable=default,QciProfilePredefined=QCI2 rlcMode 1
set QciTable=default,QciProfilePredefined=QCI5 rlcMode 0
set QciTable=default,QciProfilePredefined=QCI1 rlcSNLength 10
set QciTable=default,QciProfilePredefined=QCI2 rlcSNLength 10
set QciTable=default,QciProfilePredefined=QCI5 rlcSNLength 10
set QciTable=default,QciProfilePredefined=QCI1 rlfPriority 10
set QciTable=default,QciProfilePredefined=QCI1 rohcEnabled 1
set QciTable=default,QciProfilePredefined=QCI2 rohcEnabled 0
set QciTable=default,QciProfilePredefined=QCI5 rohcEnabled 0
set QciTable=default,QciProfilePredefined=QCI1 schedulingAlgorithm 6
set QciTable=default,QciProfilePredefined=QCI2 schedulingAlgorithm 3
set QciTable=default,QciProfilePredefined=QCI5 schedulingAlgorithm 0
set QciTable=default,QciProfilePredefined=QCI1 serviceType 1
set QciTable=default,QciProfilePredefined=QCI2 serviceType 0
set QciTable=default,QciProfilePredefined=QCI5 serviceType 2
set QciTable=default,QciProfilePredefined=qci1 tReorderingDl 120
set QciTable=default,QciProfilePredefined=QCI6 dscp 26
set QciTable=default,QciProfilePredefined=QCI7 dscp 26
set QciTable=default,QciProfilePredefined=QCI8 dscp 26
set QciTable=default,QciProfilePredefined=QCI9 dscp 26
set QciTable=default,QciProfilePredefined=QCI6 schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=QCI7 schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=QCI8 schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=QCI9 schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=QCI6 absPrioOverride 0
set QciTable=default,QciProfilePredefined=QCI7 absPrioOverride 0
set QciTable=default,QciProfilePredefined=QCI8 absPrioOverride 0
set QciTable=default,QciProfilePredefined=QCI9 absPrioOverride 0

set QciTable=default,QciProfilePredefined=qci1              qciSubscriptionQuanta 60
set QciTable=default,QciProfilePredefined=qci2              qciSubscriptionQuanta 384
set QciTable=default,QciProfilePredefined=qci5              qciSubscriptionQuanta 1
set QciTable=default,QciProfilePredefined=qci6              qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci7              qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci8              qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci9              qciSubscriptionQuanta 200

set QciTable=default,QciProfilePredefined=qci6              resourceAllocationStrategy              1
set QciTable=default,QciProfilePredefined=qci7              resourceAllocationStrategy              1
set QciTable=default,QciProfilePredefined=qci8              resourceAllocationStrategy              1
set QciTable=default,QciProfilePredefined=qci9              resourceAllocationStrategy              1



set Rcs=1 rlcDlDeliveryFailureAction 2
set Rcs=1 tInactivityTimer 10
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5=1 timeToTriggerA5 480
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5=1 triggerquantitya5 0
set ReportConfigB1Geran=1 hysteresisB1      10
set ReportConfigB1Utra=1 hysteresisB1      10
set ReportConfigA5=1 timeToTriggerA5Rsrq 1024
set ReportConfigB1Geran=1 timeToTriggerB1   640
set ReportConfigB1Utra=1 timeToTriggerB1   640
set ReportConfigB2Geran=1 timeToTriggerB2Rsrq -1
set ReportConfigB2Utra=1 timeToTriggerB2Rsrq -1

for $mo in L2100
$mordn = rdn($mo)
cr $mordn,UeMeasControl=1,ReportConfigEUtraIntraFreqPm=1
done


set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigEUtraIntraFreqPm=1 maxReportCellsPm 8
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigEUtraIntraFreqPm=1 reportIntervalPm 5

set EUtranCell.*,UeMeasControl=1,ReportConfigCsfbUtra=1 hysteresis        10
set EUtranCell.*,UeMeasControl=1,ReportConfigSCellA6=1 triggerQuantityA6 0
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 a2criticalthresholdRSRp -140
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 hysteresisA2CriticalRsrp 0
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1 hysteresisA3 10
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA1Search 480
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2Search 480
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2Critical 480
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1 timeToTriggerA3 320
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1 triggerQuantityA3 0
set ReportConfigSCellA6=1 timeToTriggerA6   40
set ReportConfigSCellA1A2=1 hysteresisA1A2Rsrp 10
set ReportConfigElcA1A2=1 hysteresisA1A2Rsrp 10
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2OutSearch  40
set ReportConfigElcA1A2=1 timeToTriggerA1   40
set ReportConfigSCellA1A2=1 timeToTriggerA1   40
set ReportConfigSearch=1 timeToTriggerA1SearchRsrq 1024
set ReportConfigSearch=1 timeToTriggerA1UlSearch 480
set ReportConfigElcA1A2=1 timeToTriggerA2   40
set ReportConfigSCellA1A2=1 timeToTriggerA2   40
set ReportConfigSearch=1 timeToTriggerA2CriticalRsrq 1024
set ReportConfigSearch=1 timeToTriggerA2OutSearchRsrq -1
set ReportConfigSearch=1 timeToTriggerA2SearchRsrq 1024
set ReportConfigB2Utra=1 timeToTriggerB2Rsrq -1

set RlfProfile=1$ t301 1000
set RlfProfile=1$ t310 500
set RlfProfile=1$ t311 5000
set ENodeBFunction=1,Rrc=1 t311 5000
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 tReorderingUl 50
set ENodeBFunction=1,Rrc=1 tRrcConnReest 2
set ENodeBFunction=1,Rrc=1 tWaitForRrcConnReest 9
set ENodeBFunction=1,RlfProfile n310 10
set ENodeBFunction=1,RlfProfile n311 1
set ENodeBFunction=1,Rrc=1 t301 2000
set ENodeBFunction=1,Rrc=1 t304 2000
set RadioBearerTable=default,SignalingRadioBearer=1 tPollRetransmitDl 80
set RadioBearerTable=default,SignalingRadioBearer=1 tPollRetransmitUl 80
cr ENodeBFunction=1,TimerProfile=0
6
8
3
10
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 timerProfileRef ENodeBFunction=1,TimerProfile=0
set TimerProfile=0                                          tWaitForRrcConnReest 6
set TimerProfile=0                                          tRrcConnectionReconfiguration 8
set TimerProfile=0                                          tRrcConnReest 3
set TimerProfile=0                                          tRelocOverall 20

set . ulTrafficDelay -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1
set . dlTrafficDelay -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1

set EUtranCellFDD=.*,UeMeasControl=1                  filterCoefficientEUtraRsrp 4


set EUtranCellFDD=.*,UeMeasControl=1 ueMeasurementsActiveIF true


# UL COMP

pr EUtranCellFDD=UW_E_F1
if $nr_of_mos = 3
cr ENodeBFunction=1,UlCompGroup=2
ENodeBFunction=1,SectorCarrier=30 ENodeBFunction=1,SectorCarrier=31 ENodeBFunction=1,SectorCarrier=32
elseif $nr_of_mos = 2
cr ENodeBFunction=1,UlCompGroup=2
ENodeBFunction=1,SectorCarrier=30 ENodeBFunction=1,SectorCarrier=31
elseif $nr_of_mos = 1
cr ENodeBFunction=1,UlCompGroup=2
ENodeBFunction=1,SectorCarrier=30
elseif $nr_of_mos = 4
cr ENodeBFunction=1,UlCompGroup=2
ENodeBFunction=1,SectorCarrier=30 ENodeBFunction=1,SectorCarrier=31 ENodeBFunction=1,SectorCarrier=32 ENodeBFunction=1,SectorCarrier=33
fi
deb ENodeBFunction=1,UlCompGroup=2



set ENodeBFunction=1                                        zzzTemporary13    -2000000000
set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1 sMeasure 0
set SecurityHandling=1                                      cipheringAlgoPrio 1 2 0
set EUtranCell.*,UeMeasControl=1                  lowPrioMeasThresh 0
set EUtranCell.*,UeMeasControl=1                  maxUtranCellsToMeasure 32
set EUtranCell.*,UeMeasControl=1                  allowReleaseQci1 false
seti ENodeBFunction=1,Rrc=1        tRrcConnectionSetup  10
set EUtranCell.*,UeMeasControl=1                  ulSinrOffset 30
set SignalingRadioBearer dlMaxRetxThreshold 32
set EUtranCellFDD=.*,UeMeasControl=1 ueMeasurementsActive 1
set EutrancellFDD=.*,UeMeasControl=1                  a5B2MobilityTimer 0
set EUtranCellFDD=.*,UeMeasControl=1 excludeInterFreqAtCritical False
set ENodeBFunction=1,Rrc=1 tRrcConnectionReconfiguration 10
set UeMeasControl=1      a3SuspendCsgTimer 0


####IFLB


set LoadBalancingFunction=1 lbCeiling 500
set LoadBalancingFunction=1 lbThreshold 20
set LoadBalancingFunction=1 lbHitRateEUtranAddThreshold 5
set LoadBalancingFunction=1 lbHitRateEUtranMeasUeIntensity 10
set LoadBalancingFunction=1 lbHitRateEUtranMeasUeThreshold 10
set LoadBalancingFunction=1 lbHitRateEUtranRemoveThreshold 2
set LoadBalancingFunction=1 lbMeasScalingLimit 30
set LoadBalancingFunction=1 lbRateOffsetCoefficient 320
set LoadBalancingFunction=1 lbRateOffsetLoadThreshold 1500
set QciTable=default,QciProfilePredefined=qci1              qciSubscriptionQuanta 60
set QciTable=default,QciProfilePredefined=qci2              qciSubscriptionQuanta 384
set QciTable=default,QciProfilePredefined=qci5              qciSubscriptionQuanta 1
set QciTable=default,QciProfilePredefined=qci6              qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci7              qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci8              qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci9              qciSubscriptionQuanta 200
set AutoCellCapEstFunction=1 useEstimatedCellCap true

set EutrancellFDD=.* noOfPucchSrUsers 420
set EutrancellFDD=.* noOfPucchCqiUsers 320



############

set EutrancellFDD=.* cellCapMaxCellSubCap 60000
set EutrancellFDD=.* cellCapMinCellSubCap 1500
set EutrancellFDD=.* cellCapMinMaxWriProt true
set  CXC4011373   featurestate  1
set  CXC4011370   featurestate  1
set  CXC4011698   featurestate  1


set EutrancellFDD=.* dlInterferenceManagementActive TRUE
set EUtranCellFDD=.* noOfChannelSelectionsets 4
set EUtranCellFDD=.* channelSelectionsetSize 2
set EutrancellFDD=.* advCellSupSensitivity 25
set EUtranCellFDD=.*,EUtranFreqRelation=.* qoffsetfreq 0
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1 a3offset 30
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigB2Utra=1 triggerQuantityB2 0
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA1Search 480
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2Search 480
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2Critical 480
set EUtranCellFDD=.* pdcchOuterLoopInitialAdjVolte -46
set EUtranCellFDD=.* pdcchOuterLoopInitialAdj -70
set EUtranCellFDD=.* pdcchOuterLoopInitialAdjPCell -70
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 inhibitA2SearchConfig 1
set EutrancellFDD=.*,UeMeasControl=1         bothA5RsrpRsrqCheck False
set EutrancellFDD=.*,UeMeasControl=1                  inhibitB2RsrqConfig true
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2OutSearch  40
set EutrancellFDD=.* SystemInformationBlock3 snonintrasearchQ=0
set EutrancellFDD=.* SystemInformationBlock3 sintrasearchp=44
set EUtranCellFDD=.* mappingInfo mappingInfoSIB3=1
set EUtranCellFDD=.* mappingInfo mappingInfoSIB7=5


set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSCellA1A2=1 hysteresisA1A2RsrpBidirectional 10

set EUtranCellFDD=.* bsrThreshold 100
set EUtranCellFDD=.* noOfUlImprovedUe 2


#Common Parameter

set EUtranFreqRelation=39150 allowedmeasbandwidth 100
set EUtranFreqRelation=39348 allowedmeasbandwidth 100
set EUtranFreqRelation=365$ allowedmeasbandwidth 75
set EUtranFreqRelation=1526 allowedmeasbandwidth 75
set EUtranFreqRelation=2545 allowedmeasbandwidth 25
set EUtranFreqRelation=39351 allowedmeasbandwidth 100
set EUtranFreqRelation=39349 allowedmeasbandwidth 100

set EUtranFreqRelation=39150 anrMeasOn true
set EUtranFreqRelation=39348 anrMeasOn true
set EUtranFreqRelation=1526 anrMeasOn true
set EUtranFreqRelation=365$ anrMeasOn true
set EUtranFreqRelation=2545 anrMeasOn true
set EUtranFreqRelation=39351 anrMeasOn true
set EUtranFreqRelation=39349 anrMeasOn true


set . maxTimeEventBasedPciConf 30
set . measuringEcgiWithAgActive false
set AnrFunction=1 probCellDetectLowHoSuccThres 10

# UL COMP

set QciTable=default,QciProfilePredefined=qci1 rlfProfileRef RlfProfile=1
set QciTable=default,QciProfilePredefined=QCI6 dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=QCI8 dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=QCI9 dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci5              tReorderingUl 60
set QciTable=default,QciProfilePredefined=qci6             tReorderingUl 60
set ENodeBFunction=1,RadioBearerTable=default,SignalingRadioBearer=1 ulMaxRetxThreshold 32
set Rrc=1 t300 2000
set Rrc=1 t320 30
set RlfProfile=1$ n310 10
set RlfProfile=1$ n311 1
set RlfProfile=1$ t301 1000
set RlfProfile=1$ t310 500
set RlfProfile=1$ t311 5000
set RlfProfile=0$ n310 20
set RlfProfile=0$ n311 1
set RlfProfile=0$ t301 2000
set RlfProfile=0$ t310 2000
set RlfProfile=0$ t311 10000

#CA
set LoadBalancingFunction=1 lbDiffCaOffset 300
set CarrierAggregationFunction caRateAdjustCoeff 5
set CarrierAggregationFunction waitForCaOpportunity 2000
set CarrierAggregationFunction sCellScheduleSinrThres -50
set CarrierAggregationFunction sCellActDeactDataThres 20
set CarrierAggregationFunction sCellActDeactDataThresHyst 20
set CarrierAggregationFunction sCellDeactProhibitTimer 50
set CarrierAggregationFunction causagelimit 200
set CarrierAggregationFunction sCellActProhibitTimer 10
set CarrierAggregationFunction caPreemptionThreshold 50
set CarrierAggregationFunction sCellSelectionMode 0
set LoadBalancingFunction lbCaThreshold 2000
set LoadBalancingFunction lbCaCapHysteresis 20
set CarrierAggregationFunction pdcchEnhancedLaForVolte False

#GERAN

set GeranFreqGroupRelation=1         csFallbackPrio    7
set GeranFreqGroupRelation=1         csFallbackPrioEC    7
set GeranFreqGroupRelation=1         altCsfbTargetPrio   2
set AnrFunction=1,AnrFunctionGeran=1 anrStateGsm 1
set GeranFreqGroup qRxLevMin -111
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

#RIM

set CXC4010973 featurestate 1
set ENodeBFunction=1                                        forcedSiTunnelingActive false
set CXC4010956 featurestate 1

###Paging

set ENodeBFunction=1,Paging=1 maxNoOfPagingRecords                 7
set ENodeBFunction=1,Paging=1 nB                                   3

####

### Additional Parameters

lset UeMeasControl PrioOffsetPerQci qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,offsetPerQciPrio=7

set . zzzTemporary60 1

##Features_GPL

set  CXC4011368   featurestate  0
set  CXC4010512   featurestate  0
set  CXC4010955   featurestate  0
set  CXC4010973   featurestate  1
set  CXC4011055   featurestate  0
set  CXC4011246   featurestate  0
set  CXC4011346   featurestate  1
set  CXC4011478   featurestate  0
set  cxc4011554   featurestate  0
set  CXC4011663   featurestate  0
set  CXC4011664   featurestate  0
set  CXC4011736   featurestate  0
set  CXC4011810   featurestate  0
set  cxc4011911   featurestate  0
set  cxc4011966   featurestate  0
set  CXC4011983   featurestate  1
set  CXC4011714   featurestate  0
set  CXC4010319   featurestate  1
set  CXC4010320   featurestate  1
set  CXC4010609   featurestate  1
set  CXC4010613   featurestate  1
set  CXC4010616   featurestate  1
set  CXC4010618   featurestate  1
set  CXC4010620   featurestate  1
set  CXC4010717   featurestate  1
set  CXC4010723   featurestate  1
set  CXC4010770   featurestate  1
set  CXC4010841   featurestate  1
set  CXC4010856   featurestate  1
set  CXC4010912   featurestate  1
set  CXC4010956   featurestate  1
set  CXC4010959   featurestate  1
set  CXC4010961   featurestate  1
set  CXC4010962   featurestate  1
set  CXC4010967   featurestate  1
set  CXC4010974   featurestate  1
set  CXC4010980   featurestate  1
set  CXC4010990   featurestate  1
set  CXC4011011   featurestate  1
set  CXC4011033   featurestate  1
set  CXC4011034   featurestate  1
set  CXC4011050   featurestate  1
set  CXC4011057   featurestate  1
set  CXC4011059   featurestate  1
set  CXC4011060   featurestate  1
set  CXC4011061   featurestate  1
set  CXC4011062   featurestate  1
set  CXC4011064   featurestate  1
set  CXC4011074   featurestate  1
set  CXC4011075   featurestate  1
set  CXC4011157   featurestate  1
set  CXC4011183   featurestate  1
set  CXC4011245   featurestate  1
set  CXC4011247   featurestate  1
set  CXC4011251   featurestate  1
set  CXC4011252   featurestate  1
set  CXC4011253   featurestate  1
set  CXC4011255   featurestate  1
set  CXC4011258   featurestate  1
set  CXC4011319   featurestate  1
set  CXC4011327   featurestate  1
set  CXC4011345   featurestate  1
set  CXC4011366   featurestate  1
set  CXC4011370   featurestate  1
set  CXC4011372   featurestate  1
set  CXC4011373   featurestate  1
set  CXC4011376   featurestate  1
set  CXC4011378   featurestate  1
set  CXC4011422   featurestate  1
set  CXC4011443   featurestate  1
set  CXC4011444   featurestate  1
set  CXC4011477   featurestate  1
set  CXC4011479   featurestate  1
set  CXC4011481   featurestate  1
set  CXC4011482   featurestate  1
set  CXC4011485   featurestate  1
set  CXC4011515   featurestate  1
set  CXC4011698   featurestate  1
set  CXC4011711   featurestate  1
set  CXC4011715   featurestate  1
set  CXC4011813   featurestate  1
set  CXC4011815   featurestate  1
set  CXC4011910   featurestate  1
set  CXC4011913   featurestate  1
set  CXC4011914   featurestate  1
set  CXC4011918   featurestate  1
set  CXC4011940   featurestate  1
set  CXC4011941   featurestate  1
set  CXC4011955   featurestate  1
set  CXC4011969   featurestate  1
set  CXC4012003   featurestate  1
set  CXC4012018   featurestate  1
set  CXC4012070   featurestate  1
set  CXC4012089   featurestate  1
set  CXC4011476   featurestate  1
set  CXC4011559   featurestate  1
set  CXC4011922   featurestate  1
set  CXC4011946   featurestate  1
set  CXC4012129   featurestate  1
set  CXC4012240   featurestate  1
set  CXC4011072   featurestate  0
set  CXC4011974   featurestate  1

## old Features_GPL

set  CXC4011667   featurestate  1
set  CXC4011056   featurestate  1
set  CXC4010949   featurestate  1
set  CXC4010963   featurestate  1
set  CXC4010964   featurestate  1
set  CXC4011063   featurestate  1
set  CXC4011067   featurestate  1
set  CXC4011068   featurestate  1
set  CXC4011069   featurestate  1
set  CXC4011163   featurestate  1
set  CXC4011256   featurestate  1
set  CXC4011317   featurestate  1
set  CXC4011356   featurestate  1
set  CXC4011427   featurestate  1
set  CXC4011618   featurestate  1
set  CXC4011699   featurestate  1
set  CXC4011710   featurestate  1
set  CXC4011716   featurestate  1
set  CXC4011804   featurestate  1
set  CXC4011807   featurestate  1
set  CXC4011811   featurestate  1
set  CXC4011814   featurestate  1
set  CXC4011820   featurestate  1
set  CXC4011917   featurestate  1
set  CXC4011930   featurestate  1
set  CXC4011933   featurestate  1
set  CXC4011803   featurestate  1
set  CXC4011937   featurestate  1
set  CXC4011938   featurestate  1
set  CXC4011939   featurestate  1
set  CXC4011942   featurestate  1
set  CXC4011951   featurestate  1
set  CXC4011958   featurestate  0
set  CXC4011967   featurestate  1
set  CXC4011973   featurestate  0
set  CXC4011975   featurestate  1
set  CXC4011982   featurestate  1
set  CXC4011991   featurestate  1
set  CXC4012022   featurestate  1
set  CXC4040004   featurestate  1
set  CXC4040005   featurestate  1
set  CXC4040006   featurestate  1
set  CXC4040008   featurestate  1
set  CXC4040009   featurestate  1
set  CXC4040010   featurestate  1
set  CXC4040014   featurestate  1
set  CXC4011155   featurestate  1
set  CXC4012261   featurestate  1
set  CXC4012256   featurestate  1
set  CXC4012123   featurestate  1
set  CXC4012111   featurestate 1
set  CXC4012485   featurestate 1
set  CXC4012356 featurestate 1
set  CXC4011984 featurestate 0
set  CXC4012505 featurestate 1
set  CXC4012505 featurestate 1
set CXC4011666  featurestate 1
set CXC4012259  featurestate 1




## 20Q2Features

set CXC4012271 featurestate 1

## additional Feature

set CXC4012344 featurestate 0
set . ul256qamEnabled FALSE


set CXC4012316 featurestate 1
set . eUlFssSwitchThresh 30
set . noOfEnhAdptReTxCand -1


set ENodeBFunction=1 measuringEcgiWithAgActive false
set ENodeBFunction=1,AnrFunction=1 pciConflictDetectionEcgiMeas         false
set ENodeBFunction=1,AnrFunction=1 pciConflictMobilityEcgiMeas          false



set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThrQci1RsrqOffset -240

set EUtranCell prsPowerBoosting 3
set ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1 anrStateUtran 0
set ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1 hoAllowedUtranPolicy 0


##New Addition

set QciTable=default,QciProfilePredefined=qci1 measReportConfigParams a1ThresholdRsrpPrimOffset=2
set QciTable=default,QciProfilePredefined=qci1 measReportConfigParams a2ThresholdRsrpPrimOffset=2
set QciTable=default,QciProfilePredefined=qci1 measReportConfigParams a5Threshold1RsrpOffset=2
set QciTable=default,QciProfilePredefined=qci1 measReportConfigParams a5Threshold2RsrpOffset=2
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigEUtraBadCovPrim=1 a2ThresholdRsrpPrim -140
set EUtranCellFDD=.*,UeMeasControl=1                  filterCoefficientEUtraRsrq 11
set SectorCarrier radioTransmitPerfMode 2
set EUtranCellFDD=.*,UeMeasControl=1 ueMeasurementsActiveUTRAN False
set EUtranCellFDD=.*,UeMeasControl=1 ueMeasurementsActiveGERAN True
set ReportConfigCsfbUtra=1 hysteresis 10
set EUTRANCELL dlInternalChannelBandwidth 0
set EUTRANCELL UlInternalChannelBandwidth 0
set ReportConfigSCellA6=1 timeToTriggerA6   40
set EUtranCell  systemInformationBlock3 sNonIntraSearchP=10
set ReportConfigSearch=1 hysteresisA2CriticalRsrq 10
set ReportConfigElcA1A2=1 a1a2ThresholdRsrp -134
set ReportConfigSCellA1A2=1 a1a2ThresholdRsrp -126
set ReportConfigSCellA1A2=1 a1a2ThresholdRsrpBidir -140
set ReportConfigSCellA1A2=1 a1a2ThresholdRsrq -165
set GeranCellRelation=.* coverageIndicator 1
set EUtranCell.*DD=.*,UeMeasControl=1,ReportConfigB2GeranUlTrig=1 reportIntervalB2 4
set ReportConfigB2Geran=1 timeToTriggerB2   1280

set CXC4012238 featurestate 1

###Feature activation only
set CXC4012326 featurestate 1
set CXC4012260 featurestate 1
set CXC4012374 featurestate 1
set CXC4012019 featurestate 1

###ASGH BLER Target
set CXC4012199 featurestate 1
set ENodeBFunction=1,EUtranCell.*DD= dlBlerTargetEnabled TRUE
set ENodeBFunction=1,EUtranCell.*DD= blerTargetConfigEnabled TRUE
cr ENodeBFunction=1,SubscriberGroupProfile=1
set ENodeBFunction=1,SubscriberGroupProfile=1 bearerTriggerList qci=1
set ENodeBFunction=1,SubscriberGroupProfile=1 dlHarqBlerTarget 5
set ENodeBFunction=1,SubscriberGroupProfile=1 ulHarqBlerTarget 3
set enodebfunction=1,SubscriberGroupProfile fastACqiReportEnabled 1
set enodebfunction=1,SubscriberGroupProfile dlDynBlerTargetAlg 1
set enodebfunction=1,SubscriberGroupProfile dlDynBlerTargetMax 60
set enodebfunction=1,SubscriberGroupProfile dlDynBlerTargetMin 10



wait 2
lt all



st cell

##FDD L2100 ##################


ma L2100 EUtranCellFDD earfcn 365
wait 1
if $nr_of_mos != 0
for $mo in L2100
$mordn = rdn($mo)
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2SearchRsrp 20
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrp -98
set $mordn,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a1a2ThrRsrqQciOffset=0,a1a2ThrRsrpQciOffset=5
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2criticalthresholdRSRp -140
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThrQci1RsrpOffset -20
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThrQci1RsrqOffset -240
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrp -98
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp -98
set $mordn,UeMeasControl=1,ReportConfigA5=1 hysteresisA5 20
set $mordn,EUtranFreqRelation=.* a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39150 a5Thr2RsrpFreqOffset -16
set $mordn,EUtranFreqRelation=39348 a5Thr2RsrpFreqOffset -16
set $mordn,EUtranFreqRelation=39151 a5Thr2RsrpFreqOffset -16
set $mordn,EUtranFreqRelation=39349 a5Thr2RsrpFreqOffset -16
set $mordn,EUtranFreqRelation=1526 a5Thr2RsrpFreqOffset -10
set $mordn,EUtranFreqRelation=365$ a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=2545 a5Thr2RsrpFreqOffset 6
set $mordn,EUtranFreqRelation=39150 EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=5,a5Thr2RsrpFreqQciOffset=66,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=39348 EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=5,a5Thr2RsrpFreqQciOffset=66,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=39151 EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=5,a5Thr2RsrpFreqQciOffset=66,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=39349 EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=5,a5Thr2RsrpFreqQciOffset=66,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=1526 EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=5,a5Thr2RsrpFreqQciOffset=6,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=365$ EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=5,a5Thr2RsrpFreqQciOffset=0,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=2545 EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=5,a5Thr2RsrpFreqQciOffset=-20,lbQciProfileHandling=1
set $mordn,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold1Rsrp -140
set $mordn,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold2Geran -110
set $mordn,EUtranFreqRelation=39150 cellReselectionPriority 3
set $mordn,EUtranFreqRelation=39348 cellReselectionPriority 3
set $mordn,EUtranFreqRelation=39151 cellReselectionPriority 3
set $mordn,EUtranFreqRelation=39349 cellReselectionPriority 3
set $mordn,EUtranFreqRelation=1526 cellReselectionPriority 6
set $mordn,EUtranFreqRelation=365$ cellReselectionPriority 4
set $mordn,EUtranFreqRelation=2545 cellReselectionPriority 2
set $mordn,GeranFreqGroupRelation=1  cellReselectionPriority 1
set $mordn,EUtranFreqRelation=39150 connectedmodemobilityprio 3
set $mordn,EUtranFreqRelation=39348 connectedmodemobilityprio 3
set $mordn,EUtranFreqRelation=39151 connectedmodemobilityprio 3
set $mordn,EUtranFreqRelation=39349 connectedmodemobilityprio 3
set $mordn,EUtranFreqRelation=1526 connectedmodemobilityprio 6
set $mordn,EUtranFreqRelation=365$ connectedmodemobilityprio 4
set $mordn,EUtranFreqRelation=2545 connectedmodemobilityprio 2
set $mordn,GeranFreqGroupRelation=1  connectedModeMobilityPrio -1
set $mordn,EUtranFreqRelation=39150 voicePrio -1
set $mordn,EUtranFreqRelation=39348 voicePrio -1
set $mordn,EUtranFreqRelation=39151 voicePrio -1
set $mordn,EUtranFreqRelation=393489 voicePrio -1
set $mordn,EUtranFreqRelation=1526 voicePrio 4
set $mordn,EUtranFreqRelation=365$ voicePrio 3
set $mordn,EUtranFreqRelation=2545 voicePrio 2
set $mordn,GeranFreqGroupRelation=1  voicePrio  -1
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA2CriticalRsrp 0
set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1 hysteresisA3 10
set $mordn,UeMeasControl=1,ReportConfigB2Geran=1 hysteresisB2 20
set $mordn,EUtranFreqRelation=.* qRxLevMin -124
set $mordn,GeranFreqGroupRelation=1  qRxLevMin  -111
set $mordn qRxLevMin -124
set $mordn SystemInformationBlock3 sintrasearch=44
set $mordn SystemInformationBlock3 snonintrasearch=10
set $mordn SystemInformationBlock3 qhyst=4
set $mordn threshServingLow 8
set $mordn,EUtranFreqRelation=39150 threshXHigh 14
set $mordn,EUtranFreqRelation=39348 threshXHigh 14
set $mordn,EUtranFreqRelation=39151 threshXHigh 14
set $mordn,EUtranFreqRelation=39349 threshXHigh 14
set $mordn,EUtranFreqRelation=1526 threshXHigh 12
set $mordn,EUtranFreqRelation=2545 threshXLow 8
set $mordn,GeranFreqGroupRelation=1 threshXLow 62
set $mordn,EUtranFreqRelation interFreqMeasType 0
set $mordn,UeMeasControl=1   ueMeasurementsActiveGERAN True
set $mordn,EUtranFreqRelation=39150  lbA5Thr1RsrpFreqOffset 97
set $mordn,EUtranFreqRelation=39348  lbA5Thr1RsrpFreqOffset 97
set $mordn,EUtranFreqRelation=39151  lbA5Thr1RsrpFreqOffset 97
set $mordn,EUtranFreqRelation=39349  lbA5Thr1RsrpFreqOffset 97
set $mordn,EUtranFreqRelation=1526  lbA5Thr1RsrpFreqOffset 97
set $mordn,EUtranFreqRelation=2545  lbA5Thr1RsrpFreqOffset 0

done
else
fi

###############RSRQ


ma L2100 EUtranCellFDD earfcn 365
wait 1
if $nr_of_mos != 0 
for $mo in L2100
$mordn = rdn($mo)
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2SearchRsrq 10
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrq -160
set $mordn,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a1a2ThrRsrqQciOffset=-30,a1a2ThrRsrpQciOffset=5
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2criticalthresholdRSRq -195
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThrQci1RsrqOffset -100
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA2CriticalRsrq 100
set $mordn,UeMeasControl=1,ReportConfigSearch=1 InhibitA2SearchConfig 0
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA1SearchRsrq 1024
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2CriticalRsrq 1024
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2SearchRsrq 1024
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrq -170
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrq -180
set $mordn,UeMeasControl=1,ReportConfigA5=1 hysteresisA5 20
set $mordn,UeMeasControl=1,ReportConfigA5=1 hysteresisA5RsrqOffset 0
set $mordn,UeMeasControl=1,ReportConfigA5=1 timeToTriggerA5Rsrq 1024
set $mordn,EUtranFreqRelation=.* a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39150 a5Thr2RsrqFreqOffset -15
set $mordn,EUtranFreqRelation=39348 a5Thr2RsrqFreqOffset -15
set $mordn,EUtranFreqRelation=39151 a5Thr2RsrqFreqOffset -15
set $mordn,EUtranFreqRelation=39349 a5Thr2RsrqFreqOffset -15
set $mordn,EUtranFreqRelation=1526 a5Thr2RsrqFreqOffset  -15
set $mordn,EUtranFreqRelation=365$ a5Thr2RsrqFreqOffset  0
set $mordn,EUtranFreqRelation=2545 a5Thr2RsrqFreqOffset -15
set $mordn,EUtranFreqRelation=39150  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrqFreqQciOffset=-220,a5Thr2RsrqFreqQciOffset=155,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=39348  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrqFreqQciOffset=-220,a5Thr2RsrqFreqQciOffset=155,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=39151  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrqFreqQciOffset=-220,a5Thr2RsrqFreqQciOffset=155,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=39349  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrqFreqQciOffset=-220,a5Thr2RsrqFreqQciOffset=155,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=1526  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrqFreqQciOffset=-30,a5Thr2RsrqFreqQciOffset=-15,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=365$  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrqFreqQciOffset=-220,a5Thr2RsrqFreqQciOffset=155,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=2545  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrqFreqQciOffset=-30,a5Thr2RsrqFreqQciOffset=155,lbQciProfileHandling=1
set $mordn,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold2Rsrq -170
set $mordn,UeMeasControl=1 bothA5RsrpRsrqCheck True
done
else
fi


#### IFLB Parameters

set EUtranCellFDD=UW_E_F1.* cellSubscriptionCapacity 10000
set EutrancellFDD=.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold1Rsrp  -140
set EutrancellFDD=.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold2Rsrp   -111
set EutrancellFDD=.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 hysteresisA5 10
set CXC4011373 FeatureState 1
set CXC4011370 FeatureState 1
set EUtranCellFDD=UW_E_F1.* cellCapMinCellSubCap 3000
set EUtranCellFDD=UW_E_F5.* cellCapMinCellSubCap 1500
set EUtranCell.*=.* cellCapMaxCellSubCap 60000
set EUtranCell.*=.* cellCapMinMaxWriProt true
set EUtranCellFDD=UW_E_F1.*,EUtranFreqRelation=2545,EUtranCellRelation=40497-.*-.* loadBalancing     1
set EUtranCellFDD=UW_E_F5.*,EUtranFreqRelation=365,EUtranCellRelation=40497-.*-.* loadBalancing    1





### IFO Activation

set CXC4011370 featurestate 1
set CXC4011373 featurestate 1
set CXC4011557 featurestate 1
set CXC4011319 featurestate 1
set CXC4012349 featuerstate 1
set LoadBalancingFunction lbCycle 5
set AnrFunction=1,AnrFunctionEUtran=1                       lbCellOffloadCapacityPolicy 30000

set EUtranCellFDD=UW_E_F1.*,EUtranFreqRelation=39150, loadbalancing    2
set EUtranCellFDD=UW_E_F1.*,EUtranFreqRelation=39150, lbBnrallowed True
set EUtranCellFDD=UW_E_F1.*,EUtranFreqRelation=39348, loadbalancing    2
set EUtranCellFDD=UW_E_F1.*,EUtranFreqRelation=39348, lbBnrallowed True
set EUtranCellFDD=UW_E_F1.*,EUtranFreqRelation=39151, loadbalancing    2
set EUtranCellFDD=UW_E_F1.*,EUtranFreqRelation=39151, lbBnrallowed True
set EUtranCellFDD=UW_E_F1.*,EUtranFreqRelation=39349, loadbalancing    2
set EUtranCellFDD=UW_E_F1.*,EUtranFreqRelation=39349, lbBnrallowed True
set EUtranCellFDD=UW_E_F1.*,EUtranFreqRelation=1526, loadbalancing    2
set EUtranCellFDD=UW_E_F1.*,EUtranFreqRelation=1526, lbBnrallowed True


set ExternalEUtranCellFDD=.* lbEUtranCellOffloadCapacity 30000
set ExternalEUtranCellTDD=.* lbEUtranCellOffloadCapacity 40000
set LoadBalancingFunction=1                                 lbCauseCodeS1SourceTriggersOffload 0
set LoadBalancingFunction=1                                 lbCauseCodeS1TargetAcceptsOffload 0
set LoadBalancingFunction=1                                 lbCauseCodeX2SourceTriggersOffload 0
set LoadBalancingFunction=1                                 lbCauseCodeX2TargetAcceptsOffload 0
set LoadBalancingFunction=1                                 lbEUtranOffloadBackoffTime 30
set EUtranCellFDD=UW_E_F1.*      lbEUtranTriggerOffloadThreshold 40
set EUtranCellFDD=UW_E_F1.*      lbEUtranAcceptOffloadThreshold  1600





set EUtranCellFDD=UW_E_F1.* dlMaxRetxRrcReleaseThr 8
set EUtranCellFDD=UW_E_F1.* tPollRetxRrcReleaseDl 80


lt all


confb+
gs+

set ENodeBFunction=1                                        dscpLabel                       46
set ENodeBFunction=1                                        gtpuErrorIndicationDscp         46
set ENodeBFunction=1                                        interEnbCaTunnelDscp            26
set ENodeBFunction=1                                        interEnbUlCompTunnelDscp        26
set ENodeBFunction=1                                        s1GtpuEchoDscp                  46
set ENodeBFunction=1                                        x2GtpuEchoDscp                  46


cr Transport=1,QosProfiles=1,DscpPcpMap=1

set QciTable=default,QciProfilePredefined=qci1              dscp              34
set QciTable=default,QciProfilePredefined=qci2              dscp              34
set QciTable=default,QciProfilePredefined=qci3              dscp              26
set QciTable=default,QciProfilePredefined=qci4              dscp              26

set QciTable=default,QciProfilePredefined=qci5              dscp              46
set QciTable=default,QciProfilePredefined=qci6              dscp              26
set QciTable=default,QciProfilePredefined=qci7              dscp              26
set QciTable=default,QciProfilePredefined=qci8              dscp              26

set QciTable=default,QciProfilePredefined=qci9              dscp              26

set SysM=1,OamTrafficClass=1 dscp 28

set EthernetPort=TN_C                                       egressQosMarking  QosProfiles=1,DscpPcpMap=1


set SctpProfile= dscp 46
set Ntp=1,NtpFrequencySync= dscp 46



lt all


set QosProfiles=1,DscpPcpMap=1  pcp0
set QosProfiles=1,DscpPcpMap=1  pcp1
set QosProfiles=1,DscpPcpMap=1  pcp2
set QosProfiles=1,DscpPcpMap=1  pcp3
set QosProfiles=1,DscpPcpMap=1  pcp4
set QosProfiles=1,DscpPcpMap=1  pcp5
set QosProfiles=1,DscpPcpMap=1  pcp6
set QosProfiles=1,DscpPcpMap=1  pcp7


set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp0 0 1 2 3 4 5 6 7 8 9 10 11 19 20 21 27 29 30 31 32 33 35 36 37 38 39 40 41 42 43 44 45 47  48  49  50  51  52  53  54  55  56  57  58  59  60  61  62  63

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp3 12 13 14 15 16 17 18

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp4 22 23 24 25 26

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp5 28

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp6 34

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp7 46

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp1 0 1 2 3 5 7 9 11 19 21 23 25 27 29 31 33 35 36 37 38 39 41 43 45 47 48 49 50  51  52  53  54  55  56  57  58  59  60  61  62  63

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp2 22 24 26

set Router=OAM,DnsClient=1 dscp 28

set Router=.*,InterfaceIPv4= egressQosMarking               egressQosMarking  QosProfiles=1,DscpPcpMap=1
set Router=LTECP,InterfaceIPv4=TN_C_CP                      egressQosMarking  QosProfiles=1,DscpPcpMap=1
set Router=LTEUP,InterfaceIPv4=TN_C_UP                      egressQosMarking  QosProfiles=1,DscpPcpMap=1
set Router=OAM,InterfaceIPv4=TN_C_OAM                       egressQosMarking  QosProfiles=1,DscpPcpMap=1
set Router=ABIS,InterfaceIPv4=TN_A_ABIS                     egressQosMarking  QosProfiles=1,DscpPcpMap=1
set Router=ABIS,InterfaceIPv4=TN_B_ABIS                     egressQosMarking  QosProfiles=1,DscpPcpMap=1
set Router=ABIS,InterfaceIPv4=TN_C_ABIS                     egressQosMarking  QosProfiles=1,DscpPcpMap=1

set VlanPort=                                               egressQosMarking  QosProfiles=1,DscpPcpMap=1
set VlanPort=TN_C_CP                                        egressQosMarking  QosProfiles=1,DscpPcpMap=1
set VlanPort=TN_C_OAM                                       egressQosMarking  QosProfiles=1,DscpPcpMap=1
set VlanPort=TN_C_UP                                        egressQosMarking  QosProfiles=1,DscpPcpMap=1
set VlanPort=TN_A_ABIS                                      egressQosMarking  QosProfiles=1,DscpPcpMap=1
set VlanPort=TN_C_ABIS                                      egressQosMarking  QosProfiles=1,DscpPcpMap=1



get Router=LTEUP,RouteTableIPv4Static=2,Dst=LTEUP,NextHop= address$ > $UP-Nexthop
gs+
crn Transport=1,Router=LTEUP,TwampResponder=1
ipAddress Router=LTEUP,InterfaceIPv4=TN_C_UP,AddressIPv4=TN_C_UP
udpPort 4001
userLabel
end

set CXC4040009 featurestate 1

set ENodeBFunction=1 timeAndPhaseSynchAlignment true
set ENodeBFunction=1 timeAndPhaseSynchCritical false

set  ,RfPort=[AB] vswrSupervisionActive true

set  ,RfPort=[AB] vswrSupervisionSensitivity 100

set PmEventService=1 cellTraceFileSize 30000

cr ENodeBFunction=1,PlmnInfo=1
mcc=404,mnc=97,mnclength=2
set ENodeBFunction=1,PlmnInfo=1 plmnWhiteList mcc=404,mnc=97,mnclength=2
set AnrFunction=1                                           plmnWhiteListEnabled true
set AnrFunction=1                                           plmnWhiteListGeranEnabled true


set ENodeBFunction=1                                        enabledUlTrigMeas True
set AnrFunction=1 removeNcellTime   1
set AnrFunction=1 removeNenbTime    1
set ENodeBFunction=1  timeAndPhaseSynchCritical False
set GeranFreqGroupRelation=1         csFallbackPrio    7
set GeranFreqGroupRelation=1         csFallbackPrioEC    1
cr ENodeBFunction=1,TimerProfile=0
6
10
3
10
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 timerProfileRef ENodeBFunction=1,TimerProfile=0
set TimerProfile=0                                          tWaitForRrcConnReest 6
set TimerProfile=0                                          tRrcConnectionReconfiguration 10
set TimerProfile=0                                          tRrcConnReest 3
set TimerProfile=0                                          tRelocOverall 20

wait 2
set . measuringEcgiWithAgActive false

set SctpProfile= dscp 46
set Ntp=1,NtpFrequencySync= dscp 46

set CarrierAggregationFunction=1                            sCellDeactProhibitTimer 200


set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThrQci1RsrqOffset -100
set EUtranCellFDD=.*,UeMeasControl=1Ã‚Â Ã‚Â Ã‚Â Ã‚Â Ã‚Â Ã‚Â bothA5RsrpRsrqCheck true


set Lm=1,FeatureState=CXC4011476 featurestate  0
set Lm=1,FeatureState=CXC4011559 featurestate  0
set Lm=1,FeatureState=CXC4011666 featurestate  0
set Lm=1,FeatureState=CXC4011922 featurestate  0
set Lm=1,FeatureState=CXC4011983 featurestate  0
set Lm=1,FeatureState=CXC4012111 featurestate  0
set Lm=1,FeatureState=CXC4012123 featurestate  0
set Lm=1,FeatureState=CXC4011973 featurestate  0
set Lm=1,FeatureState=CXC4012097 featurestate  0



set ENodeBFunction=1,Rrc=1 t300 2000
set ENodeBFunction=1,Rrc=1 t311 5000
set ENodeBFunction=1,Rrc=1 t301 2000
set ENodeBFunction=1,Rrc=1 t304 2000

set EUtranCellFDD=UW_E_F1.*,GeranFreqGroupRelation=1 csFallbackPrio 4
set EUtranCellFDD=UW_E_F5.*,GeranFreqGroupRelation=1 csFallbackPrio 1




lt all
rbs
rbs
confbd+

set ENodeBFunction=1 dscpLabel 46
set ENodeBFunction=1 gtpuErrorIndicationDscp 46
set ENodeBFunction=1 interEnbCaTunnelDscp 26
set ENodeBFunction=1 interEnbUlCompTunnelDscp 26
set ENodeBFunction=1 s1GtpuEchoDscp 46
set ENodeBFunction=1 x2GtpuEchoDscp 46

cr Transport=1,QosProfiles=1,DscpPcpMap=1
set QciTable=default,QciProfilePredefined=qci1$ dscp 34
set QciTable=default,QciProfilePredefined=qci2$ dscp 34
set QciTable=default,QciProfilePredefined=qci3$ dscp 26
set QciTable=default,QciProfilePredefined=qci4$ dscp 26
set QciTable=default,QciProfilePredefined=qci5$ dscp 46
set QciTable=default,QciProfilePredefined=qci6$ dscp 32
set QciTable=default,QciProfilePredefined=qci7$ dscp 40
set QciTable=default,QciProfilePredefined=qci8$ dscp 30
set QciTable=default,QciProfilePredefined=qci9$ dscp 26
set SysM=1,OamTrafficClass=1 dscp 28
set SctpProfile= dscp 46
set Ntp=1,NtpFrequencySync= dscp 46

set QosProfiles=1,DscpPcpMap=1 pcp0
set QosProfiles=1,DscpPcpMap=1 pcp1
set QosProfiles=1,DscpPcpMap=1 pcp2
set QosProfiles=1,DscpPcpMap=1 pcp3
set QosProfiles=1,DscpPcpMap=1 pcp4
set QosProfiles=1,DscpPcpMap=1 pcp5
set QosProfiles=1,DscpPcpMap=1 pcp6
set QosProfiles=1,DscpPcpMap=1 pcp7

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp0 0,1,2,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,36,37,38,39,41,43,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp2 22,24,26
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp3 6,8,10,30,32
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp4 12,14,40
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp5 4,28
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp6 16,18,34,42,44
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp7 20,46
set SctpProfile=Node_Internal_F1  dscp 46
set SctpProfile=1 dscp 46
cr Router=.*,DnsClient=1
set Router=OAM,DnsClient=1 dscp 28

set . egressQosMarking QosProfiles=1,DscpPcpMap=1



set Transport=1,SctpProfile=1 alphaIndex 3
set Transport=1,SctpProfile=1 assocMaxRtx 8
set Transport=1,SctpProfile=1 betaIndex 2
set Transport=1,SctpProfile=1 bundlingActivated TRUE
set Transport=1,SctpProfile=1 bundlingAdaptiveActivated TRUE
set Transport=1,SctpProfile=1 bundlingTimer 0
set Transport=1,SctpProfile=1 cookieLife 60
set Transport=1,SctpProfile=1 dscp 46
set Transport=1,SctpProfile=1 hbMaxBurst 1
set Transport=1,SctpProfile=1 heartbeatActivated TRUE
set Transport=1,SctpProfile=1 heartbeatInterval 2000
set Transport=1,SctpProfile=1 incCookieLife 30
set Transport=1,SctpProfile=1 initARWnd 16384
set Transport=1,SctpProfile=1 maxRto 4000
set Transport=1,SctpProfile=1 initRto 2000
set Transport=1,SctpProfile=1 minRto 1000
set Transport=1,SctpProfile=1 initialHeartbeatInterval 500
set Transport=1,SctpProfile=1 maxActivateThr 65535
set Transport=1,SctpProfile=1 maxBurst 4
set Transport=1,SctpProfile=1 maxInStreams 2
set Transport=1,SctpProfile=1 maxInitRt 5
set Transport=1,SctpProfile=1 maxOutStreams 2
set Transport=1,SctpProfile=1 maxSctpPduSize 1480
set Transport=1,SctpProfile=1 maxShutdownRt 5
set Transport=1,SctpProfile=1 minActivateThr 1
set Transport=1,SctpProfile=1 noSwitchback TRUE
set Transport=1,SctpProfile=1 pathMaxRtx 4
set Transport=1,SctpProfile=1 primaryPathAvoidance TRUE
set Transport=1,SctpProfile=1 primaryPathMaxRtx 0
set Transport=1,SctpProfile=1 sackTimer 100
set Transport=1,SctpProfile=1 thrTransmitBuffer 48
set Transport=1,SctpProfile=1 thrTransmitBufferCongCeased 85
set Transport=1,SctpProfile=1 transmitBufferSize 64
set Transport=1,SctpProfile=1 userLabel SCTP
st cell

set Transport=1,SctpProfile=1 pathMaxRtx 4
set Transport=1,SctpProfile=1 assocMaxRtx 8

set Fm=1  heartbeatInterval 100


set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1 timeToTriggerA3  480

set EUtranCellFDD=UW_E_F1.*,EUtranFreqRelation=.* lbBnrPolicy 2


set EUtranCellFDD=UW_E_F1.*                       pdcchTargetBlerVolte 18
set EUtranCellFDD=UW_E_F1.*,EUtranFreqRelation=1526 tReselectionEutra 1
set EUtranCellFDD=UW_E_F1.*,EUtranFreqRelation=2545 tReselectionEutra 1
set EUtranCellFDD=UW_E_F1.*,EUtranFreqRelation=365 tReselectionEutra 1
set EUtranCellFDD=UW_E_F1.*,EUtranFreqRelation=39150 tReselectionEutra 1
set EUtranCellFDD=UW_E_F1.*,EUtranFreqRelation=39151 tReselectionEutra 1
set EUtranCellFDD=UW_E_F1.*,EUtranFreqRelation=39348 tReselectionEutra 1
set EUtranCellFDD=UW_E_F1.*,EUtranFreqRelation=39349 tReselectionEutra 1
set CXC4011913 FeatureState 0
set EUtranCellFDD=UW_E_F1.*,GeranFreqGroupRelation=1 qRxLevMin -95
set EUtranCellFDD=UW_E_F1.*,UeMeasControl=1,ReportConfigEUtraBestCell=1 timeToTriggerA3   480

set EUtranCellFDD=UW_E_F.*,EUtranFreqRelation=2545 tReselectionEutra 2
set EUtranCellFDD=UW_E_F.*,EUtranFreqRelation=365 tReselectionEutra 1
set EUtranCellFDD=UW_E_F1.*,GeranFreqGroupRelation=1 qRxLevMin -95
set TimerProfile=0                                          tRrcConnectionReconfiguration 8


set SubscriberGroupProfile=*. pdcchFlexibleBlerMode 2
set CXC4012563 featurestate 1


confb-
gs-


confbd-

$date = `date +%y%m%d_%H%M`
cvms Post_GPL_LMS_L2100swap_$date

xx
################UPW-GPL-V1###ERRNKKA#######

lt all
rbs
rbs
confbd+


$date = `date +%y%m%d_%H%M`
cvms Pre_GPL_LMS_L850_$date


rdel EUtranFreqRelation=36500

rdel EUtranFrequency=36500

rdel EUtranFreqRelation=1409

rdel EUtranFrequency=1409

rdel EUtranFreqRelation=2539

rdel EUtranFrequency=2539



########Frequency Creation##########

cr ENodeBFunction=1,GeraNetwork=1

cr ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
1 #frequencyGroupId

func Gran_freq
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=$t
$t
0
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=$t geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
endfunc


for $t = 637 to 639
Gran_freq
done

func Gran_freq
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=$t
$t
0
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=$t geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
endfunc


for $t = 709 to 711
Gran_freq
done


lt all


cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39150
39150
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39348
39348
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39151
39151
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39349
39349
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1526
1526
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=365
365
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=2545
2545


##########GERANFREQ##################

unset all

$Par[1] = L850

mr L850

ma L850 EUtranCellFDD earfcn 2545

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

func EURel_39348
for $mo in $Par[$i]
 $mordn = rdn($mo)
 pr $mordn,EUtranFreqRelation=39348
 if $nr_of_mos = 0
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=39348
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39348
6
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

func EURel_365
for $mo in $Par[$i]
 $mordn = rdn($mo)
 pr $mordn,EUtranFreqRelation=365$
 if $nr_of_mos = 0
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=365
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=365
3
 fi
done
endfunc

func EURel_1526
for $mo in $Par[$i]
 $mordn = rdn($mo)
 pr $mordn,EUtranFreqRelation=1526
 if $nr_of_mos = 0
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=1526
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1526
4
 fi
done
endfunc

func EURel_2545
for $mo in $Par[$i]
 $mordn = rdn($mo)
 pr $mordn,EUtranFreqRelation=2545
 if $nr_of_mos = 0
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=2545
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=2545
2
 fi
done
endfunc



for $i = 1 to 1
EURel_39150
EURel_39348
EURel_39151
EURel_39349
EURel_365
EURel_1526
EURel_2545
Gran_Rel
done

########################################
cr Transport=1,Synchronization=1,TimeSyncIO=1,GnssInfo=1
########################################

### CRS GAIN

setm EUtranCellFDD crsGain 0 pdschTypeBGain 0



####Fixed Parameter

## Admission control

set AdmissionControl=1 admNrRrcDifferentiationThr 750
set AdmissionControl=1 admNrRbDifferentiationThr 750
set AdmissionControl=1 arpBasedPreEmptionState 0
set AdmissionControl=1 ulAdmOverloadThr 950
set AdmissionControl=1 ulTransNwBandwidth 2000
set AdmissionControl=1 dlAdmDifferentiationThr 750
set AdmissionControl=1 ulAdmDifferentiationThr 750

#ANRFUNCTION

set AnrFunction=1 cellRelHoAttRateThreshold 15
set AnrFunction=1 maxNoPciReportsEvent 30
set AnrFunction=1 probCellDetectLowHoSuccTime 4
set AnrFunction=1 probCellDetectMedHoSuccTime 2
set AnrFunction=1 problematicCellPolicy 1
set AnrFunction=1 removeNcellTime   1
set AnrFunction=1 removeNenbTime    1
set AnrFunction=1 removeNrelTime 3
set AnrFunction=1 probCellDetectMedHoSuccThres 50
set AnrFunction=1,AnrFunctionEUtran=1 cellAddRsrpThresholdEutran -1240
set AnrFunction=1,AnrFunctionEUtran=1 cellAddRsrqThresholdEutran -1530
set ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1 anrStateUtran 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionGeran=1 anrStateGsm 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 anrIntraFreqState 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 anrInterFreqState 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 hoAllowedEutranPolicy 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 x2SetupPolicy 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1 hoAllowedUtranPolicy 1
set AnrFunction=1,AnrFunctionEUtran=1 anrUesEUtraIntraFMax 0
set AnrFunction=1,AnrFunctionEUtran=1 anrUesThreshInterFMax 0
set AnrFunction=1,AnrFunctionEUtran=1 anrUesEUtraIntraFMin 0
set AnrFunction=1,AnrFunctionEUtran=1 anrUesThreshInterFMin 0
set AnrFunction=1,AnrFunctionUtran=1 cellAddEcNoThresholdUtranDelta -10
set AnrFunction=1,AnrFunctionUtran=1 cellAddRscpThresholdUtranDelta -1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1 hoAllowedUtranPolicy 1
set AnrPciConflictDrxProfile=1                              anrPciConflictDrxInactivityTimer 8
set AnrPciConflictDrxProfile=1                              anrPciConflictOnDurationTimer 4

#CarrierAggFunction

set CarrierAggregationFunction=1                            dynamicSCellSelectionMethod 2
set CarrierAggregationFunction=1                            fourLayerMimoPreferred false
set CarrierAggregationFunction=1                            enhancedSelectionOfMimoAndCa false
set CarrierAggregationFunction=1                            waitForAdditionalSCellOpportunity 10000
set CarrierAggregationFunction=1                            sCellActProhibitTimer 10
set CarrierAggregationFunction=1                            selectionPolicyUlWeighting 50
set CarrierAggregationFunction=1                            waitForBlindSelSCellRepLessTtt 600


#DRB

set RadioBearerTable=default,DataRadioBearer=1 tPollRetransmitUl 80
set RadioBearerTable=default,DataRadioBearer=1 tPollRetransmitDl 80
set DataRadioBearer dlMaxRetxThreshold 16
set DataRadioBearer ulMaxRetxThreshold 32


#DrxProfile

lset QciTable=default,QciProfilePredefined=qci1 drxProfileRef DrxProfile=1
lset QciTable=default,QciProfilePredefined=qci2 drxProfileRef DrxProfile=2
lset QciTable=default,QciProfilePredefined=qci5 drxProfileRef DrxProfile=0
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
lset QciTable=default,QciProfilePredefined=qci1 drxProfileRef DrxProfile=1
lset QciTable=default,QciProfilePredefined=qci2 drxProfileRef DrxProfile=2
lset QciTable=default,QciProfilePredefined=qci5 drxProfileRef DrxProfile=0
lset ENodeBFunction=1,DrxProfile=1$ drxInactivityTimer 6
lset ENodeBFunction=1,DrxProfile=2$ drxInactivityTimer 6
lset ENodeBFunction=1,DrxProfile=0$ drxInactivityTimer 14
lset ENodeBFunction=1,DrxProfile=1$ drxState 0

#EnodeBFunction

set ENodeBFunction alignTtiBundWUlTrigSinr 1
set ENodeBFunction=1 dscpLabel 46
set ENodeBFunction=1 gtpuErrorIndicationDscp 46
set ENodeBFunction rrcConnReestActive 1
set ENodeBFunction=1 tRelocOverall 20
set ENodeBFunction=1 tS1HoCancelTimer 3
set ENodeBFunction=1                                        enabledUlTrigMeas false
set ENodeBFunction=1                                        zzzTemporary52    1
set ENodeBFunction=1                                        zzzTemporary55    -2000000000
set ENodeBFunction=1                                        csfbMeasFromIdleMode 1
set ENodeBFunction=1 s1GtpuEchoDscp 46
set ENodeBFunction=1 x2GtpuEchoDscp 46
set ENodeBFunction=1                                        x2SetupTwoWayRelations true
set ENodeBFunction=1                                        dnsLookupOnTai 1
set ENodeBFunction=1                                        zzzTemporary13    -2000000000
set ENodeBFunction=1                                        caAwareMfbiIntraCellHo false
set ENodeBFunction=1                                        mfbiSupportPolicy false
set ENodeBFunction=1                                        s1HODirDataPathAvail True
set ENodeBFunction=1                                        gtpuErrorIndicationDscp         46
set ENodeBFunction=1                                        timePhaseMaxDeviationIeNbCa 30
set ENodeBFunction=1                                        s1GtpuEchoEnable 0
set ENodeBFunction=1                                        checkEmergencySoftLock false
set ENodeBFunction=1                                        combCellSectorSelectThreshRx 300
set ENodeBFunction=1                                        combCellSectorSelectThreshTx 300
set ENodeBFunction=1                                        licConnectedUsersPercentileConf 90
set ENodeBFunction=1                                        tddVoipDrxProfileId -1
set ENodeBFunction=1                                        timePhaseMaxDeviation 100
set ENodeBFunction=1                                        timePhaseMaxDeviationEdrx 10
set ENodeBFunction=1                                        timePhaseMaxDeviationMbms 50
set ENodeBFunction=1                                        timePhaseMaxDeviationOtdoa 9
set ENodeBFunction=1                                        timePhaseMaxDeviationSib16 100
set ENodeBFunction=1                                        timePhaseMaxDeviationTdd 15
set ENodeBFunction=1                                        timePhaseMaxDeviationTdd1 15
set ENodeBFunction=1                                        timePhaseMaxDeviationTdd2 15
set ENodeBFunction=1                                        timePhaseMaxDeviationTdd3 15
set ENodeBFunction=1                                        timePhaseMaxDeviationTdd4 15
set ENodeBFunction=1                                        timePhaseMaxDeviationTdd5 15
set ENodeBFunction=1                                        timePhaseMaxDeviationTdd6 15
set ENodeBFunction=1                                        timePhaseMaxDeviationTdd7 15
set ENodeBFunction=1                                        timePhaseMaxDevIeNBUlComp 30
set ENodeBFunction=1                                        ulMaxWaitingTimeGlobal 0
set ENodeBFunction=1                                        ulSchedulerDynamicBWAllocationEnabled true
set ENodeBFunction=1                                        useBandPrioritiesInSCellEval false
set ENodeBFunction=1                                        x2GtpuEchoEnable  0
set ENodeBFunction=1                                        x2IpAddrViaS1Active true
set ENodeBFunction=1                                        x2retryTimerMaxAuto 1440
set ENodeBFunction=1                                        forcedSiTunnelingActive false
set ENodeBFunction=1  timeAndPhaseSynchAlignment True
set ENodeBFunction=1  timeAndPhaseSynchCritical False


#EUTRANCELLFDD

set EUtranCellFDD pdcchOuterLoopUpStep 8
set EUtranCellFDD pdcchOuterLoopUpStepPCell 6
set EUtranCellFDD ttiBundlingAfterHO 1
set EUtranCellFDD ttiBundlingAfterReest 1
set EUtranCellFDD ttiBundlingSwitchThres 150
set EUtranCellFDD ttiBundlingSwitchThresHyst 30
set EUtranCellFDD cellDownlinkCaCapacity 0
set EUtranCellFDD mappingInfo mappingInfoSIB12=7
set EUtranCellFDD mappingInfo mappingInfoSIB4=2
set EUtranCellFDD mappingInfo mappingInfoSIB6=4
set EUtranCellFDD                                 servOrPrioTriggeredErabAction 3
set EUtranCellFDD  dlInternalChannelBandwidth 0
set EUtranCellFDD  ulInternalChannelBandwidth 0
set EUtranCellFDD  beamWeightSet16Tr 0
set EUtranCellFDD  srvccDelayTimer 3000

set Eutrancell adaptiveCfiHoProhibit 0
set EUtranCell enableSinrUplinkClpc 1
set EUtranCell pdcchCovImproveQci1 true
set EUtranCell pdcchOuterLoopUpStepVolte 9
set EUtranCell pdcchTargetBlervolte 4
set EUtranCell allocThrPucchFormat1 50
set EUtranCell allocTimerPucchFormat1 50
set EUtranCell deallocThrPucchFormat1 100
set EUtranCell deallocTimerPucchFormat1 6000
set EUtranCell drxActive true
set EUtranCell dlBlerTargetEnabled 1
set EUtranCell enableServiceSpecificHARQ true
set EUtranCell pdcchCovImproveDtx true
set EUtranCell pdcchCovImproveSrb false
set EUtranCell pdcchTargetBler 24
set EUtranCell pdcchTargetBlerPCell 22
set EUtranCell pMaxServingCell 1000
set EUtranCell qRxLevMinOffset 1000
set EUtranCell tReorderingAutoConfiguration true
set EUtranCell tTimeAlignmentTimer 0
set EUtranCell ulBlerTargetEnabled true
set EUtranCell ulHarqVolteBlerTarget 3
set EutranCell alpha 8
set EUtranCellFDD pZeroNominalPusch -83
set EUtranCellFDD pZeroNominalPucch -110
set EUtranCellFDD cellRange 6
set EUtranCell cfraEnable true
set EUtranCell cellDownlinkCaCapacity 0
set EUtranCell changeNotification changeNotificationSIB15=true
set EUtranCell changeNotification changeNotificationSIB16=true
set EUtranCell changeNotification changeNotificationSIB8=true
set EUtranCell hoOptAdjThresholdAbs 5
set EUtranCell hoOptAdjThresholdPerc 50
set EUtranCell pdcchCfiMode 5
set EUtranCell prsPowerBoosting 0
set EUtranCell transmissionMode 4
set EUtrancell ns05FullBandUsersInCellThres 1
set EUtranCell ns05FullBandSchedEnabled false
set EUtranCell  puschNcpChannelEstWindowSize 1
set EUtranCell mobCtrlAtPoorCovActive true
set EUtranCell  servOrPrioTriggeredIFHo 0
set EUtranCell  ul64qamEnabled    true
set EUtranCell  dl256QamEnabled   true
set EUtranCellFDD  commonSrPeriodicity 10
set EUtranCellFDD mappingInfo mappingInfoSIB5=3
set EUtranCell changeNotification changeNotificationSIB7=true
set EUtranCell changeNotification changeNotificationSIB2=true
set EUtranCell changeNotification changeNotificationSIB3=true
set EUtranCell changeNotification changeNotificationSIB4=true
set EUtranCell changeNotification changeNotificationSIB1=true
set EUtranCell changeNotification changeNotificationSIB6=true
set EUtranCell changeNotification changeNotificationSIB5=true
set EUtranCell changeNotification changeNotificationSIB13=true
set EUtranCell mappingInfoCe mappingInfoSIB10=0
set EUtranCell  qRxLevMinCe       -140
set EUtranCell  pdcchLaGinrMargin 40
set EUtranCell  acBarringPresence acBarringForMmtelVideoPresence=0
set EUtranCell  acBarringPresence acBarringForMmtelVoicePresence=0
set EUtranCell  acBarringPresence acBarringPriorityMmtelVideo=0
set EUtranCell  acBarringPresence acBarringPriorityMmtelVoice=0
set EUtranCell  acBarringPresence acBarringForMoDataPresence=0
set EUtranCell  noOfEnhAdptReTxCand -1
set EUtranCell  dynUlResourceAllocEnabled false
set EUtranCell systemInformationBlock6 tReselectionUtra=4
set EUtranCell advCellSupAction 2
set EUtranCell  primaryPlmnReserved false
set EUtranCell  harqOffsetDl      3
set EUtranCell  harqOffsetUl      3
set EUtranCell  highSpeedUEActive false
set EUtranCell  initialBufferSizeDefault 86
set EUtranCell  prsTransmisScheme 0
set EUtranCell  puschPwrOffset64qam 0
set EUtranCell  systemInformationBlock3 tEvaluation=240
set EUtranCell  elcEnabled        false
set EUtranCell  preambleInitialReceivedTargetPower -110
set EUtranCell  acBarringForCsfb acBarringFactor=95
set EUtranCell  acBarringForCsfb acBarringForSpecialAC=false false false false false
set EUtranCell  acBarringForCsfb acBarringTime=64
set EUtranCell  acBarringForEmergency false
set EUtranCell  acBarringForMoData acBarringFactor=95
set EUtranCell  acBarringForMoData acBarringForSpecialAC=false false false false false
set EUtranCell  acBarringForMoData acBarringTime=64
set EUtranCell  acBarringForMoSignalling acBarringFactor=95
set EUtranCell  acBarringForMoSignalling acBarringForSpecialAC=false false false false false
set EUtranCell  acBarringForMoSignalling acBarringTime=64
set EUtranCell  acBarringInfoPresent false
set EUtranCell  acBarringPresence acBarringForCsfbPresence=0
set EUtranCell  acBarringPresence acBarringForMoSignPresence=0
set EUtranCell  acBarringPresence acBarringPriorityCsfb=0
set EUtranCell  acBarringPresence acBarringPriorityMoData=0
set EUtranCell  acBarringPresence acBarringPriorityMoSignaling=0
set EUtranCell  spifhoSetupBearerAtInitialCtxtSetup false
set EUtranCell  srDetectHighThres 70
set EUtranCell  srProcessingLevel 0
set EUtranCell  ssacBarringForMMTELVideo acBarringFactor=95
set EUtranCell  ssacBarringForMMTELVideo acBarringForSpecialAC=false false false false false
set EUtranCell  ssacBarringForMMTELVideo acBarringTime=64
set EUtranCell  ssacBarringForMMTELVoice acBarringFactor=95
set EUtranCell  ssacBarringForMMTELVoice acBarringForSpecialAC=false false false false false
set EUtranCell  ssacBarringForMMTELVoice acBarringTime=64
set EUtranCell  systemInformationBlock3 nCellChangeHigh=16
set EUtranCell  systemInformationBlock3 nCellChangeMedium=16
set EUtranCell  systemInformationBlock3 qHystSfHigh=0
set EUtranCell  systemInformationBlock3 qHystSfMedium=0
set EUtranCell  systemInformationBlock3 sIntraSearchQ=0
set EUtranCell  systemInformationBlock3 sNonIntraSearchv920Active=false
set EUtranCell  systemInformationBlock3 sIntraSearchv920Active=false
set EUtranCell  systemInformationBlock3 tHystNormal=240
set EUtranCell  systemInformationBlock6 tReselectionUtraSfHigh=100
set EUtranCell  systemInformationBlock6 tReselectionUtraSfMedium=100
set EUtranCell  systemInformationBlock3 threshServingLowQ=1000
set EUtranCell  systemInformationBlock7 tReselectionGeran=2
set EUtranCell  systemInformationBlock7 tReselectionGeranSfHigh=100
set EUtranCell  systemInformationBlock7 tReselectionGeranSfMedium=100

set EUtranCell  tUeBlockingTimer  200
set EUtranCell  ulImprovedUeSchedLastEnabled true
set EUtranCell  ulPsdLoadThresholdSinrClpc 2
set EUtranCell  ulSCellPriority   5
set EUtranCell  ulSchedCtrlForOocUesEnabled true
set EUtranCell  ulSrsEnable       false
set EUtranCell  ulTrigActive      false
set EUtranCell  ulTxPsdDistrThr   40
set EUtranCell  uncertAltitude    0
set EUtranCell  uncertSemiMajor   0
set EUtranCell  uncertSemiMinor   0

set EUtranCell covTriggerdBlindHoAllowed 0
set EUtranCell qQualMin -34
set EUtranCell qQualMinOffset 0
set Eutrancell dlInterferenceManagementActive TRUE
set Eutrancell ulInterferenceManagementActive true
set EUtranCell  dlFrequencyAllocationProportion 100
set EUtranCell  ulConfigurableFrequencyStart 0
set EUtranCell  ulFrequencyAllocationProportion 100
set EUtranCell eUlFssSwitchThresh 30
set EUtranCell outOfCoverageSrTimerPeriodicity 320
set EUtranCell outOfCoverageThreshold 20
set EUtranCell outOfCoverageDepth 1
set EUtranCell outOfCoverageSparseGrantingBsr 8



#EUTRANFREQRELATION

set EUtranFreqRelation tReselectionEutra 2
set EUtranFreqRelation=.*          allowedPlmnList   mcc=404,mnc=97,mncLength=2
set EUtranFreqRelation caTriggeredRedirectionActive false
set EUtranFreqRelation anrMeasOn true
set EUtranFreqRelation       qRxLevMinCe       -140
set EUtranFreqRelation pMax 1000
lset EUtranFreqRelation=.* mobilityAction 1
set EUtranFreqRelation=.* lbBnrPolicy 2
set EUtranFreqRelation        tReselectionEutraCe 2
set EUtranFreqRelation tReselectionEutraSfHigh 100
set EUtranFreqRelation tReselectionEutraSfMedium 100
set LoadBalancingFunction=1                txPwrForOverlaidCellDetect 370
set RadioBearerTable=default,MACConfiguration=1 ulMaxHARQTx 5
set RadioBearerTable=default,MACConfiguration=1 dlMaxHARQTx 4
set RadioBearerTable=default,MACConfiguration=1 ulTtiBundlingMaxHARQTx 7
set EUtranCell.*,MimoSleepFunction=1              switchUpMonitorDurTimer 5
set Paging=1                                                pagingDiscardTimerDrxNb 3
set Paging=1                                                maxNoOfPagingRecordsNb 3
set Paging=1                                                noOfDefPagCyclPrim 8
set MdtConfiguration=1                                      a2ThresholdRsrpMdt -140
set MdtConfiguration=1                                      a2ThresholdRsrqMdt -195
set MdtConfiguration=1                                      timeToTriggerA2Mdt 640
set MdtConfiguration=1                                      triggerQuantityA2Mdt 0



#QciProfilePredefined

set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 tReorderingUl 50
set RadioBearerTable=default,SignalingRadioBearer=1 tReorderingUl 35
set QciTable=default,QciProfilePredefined=QCI1 absPrioOverride 0
set QciTable=default,QciProfilePredefined=QCI2 absPrioOverride 0
set QciTable=default,QciProfilePredefined=QCI5 absPrioOverride 1

set QciTable=default,QciProfilePredefined=QCI1 aqmMode 2
set QciTable=default,QciProfilePredefined=QCI2 aqmMode 2
set QciTable=default,QciProfilePredefined=QCI5 aqmMode 0

set QciProfilePredefined=qci1 counterActiveMode 0
set QciProfilePredefined=qci2 counterActiveMode 0
set QciProfilePredefined=qci5 counterActiveMode 0
set QciProfilePredefined=qci6 counterActiveMode 0
set QciProfilePredefined=qci8 counterActiveMode 0
set QciProfilePredefined=qci9 counterActiveMode 0

set QciTable=default,QciProfilePredefined=qci6 dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci8 dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci9 dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci7 dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=QCI1 dataFwdPerQciEnabled 1
set QciTable=default,QciProfilePredefined=QCI2 dataFwdPerQciEnabled 1
set QciTable=default,QciProfilePredefined=QCI5 dataFwdPerQciEnabled 1
set QciTable=default,QciProfilePredefined=qci1 harqPriority 1
set QciTable=default,QciProfilePredefined=qci1 dlMaxHARQTxQci 7
set QciTable=default,QciProfilePredefined=qci1 ulMaxHARQTxQci 7
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 dlMinBitRate 384
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 ulMinBitRate 384
set QciTable=default,QciProfilePredefined=QCI1 dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=QCI2 dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=QCI5 dlResourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci1 drxPriority 99
set QciTable=default,QciProfilePredefined=qci2 drxPriority 100
set QciTable=default,QciProfilePredefined=qci5 drxPriority 1
lset QciTable=default,QciProfilePredefined=qci1 drxProfileRef DrxProfile=1
lset QciTable=default,QciProfilePredefined=qci2 drxProfileRef DrxProfile=2
lset QciTable=default,QciProfilePredefined=qci5 drxProfileRef DrxProfile=0
set QciTable=default,QciProfilePredefined=QCI1 dscp 34
set QciTable=default,QciProfilePredefined=QCI2 dscp 34
set QciTable=default,QciProfilePredefined=QCI5 dscp 46
set QciTable=default,QciProfilePredefined=qci1 harqPriority 1
set QciTable=default,QciProfilePredefined=QCI1 inactivityTimerOffset 30
set QciTable=default,QciProfilePredefined=QCI2 inactivityTimerOffset 30
set QciTable=default,QciProfilePredefined=QCI5 inactivityTimerOffset 0
set QciProfilePredefined=qci6 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set QciProfilePredefined=qci7 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set QciProfilePredefined=qci8 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set QciProfilePredefined=qci9 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set QciProfilePredefined=qci1 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=1
set QciProfilePredefined=qci2 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=2
set QciProfilePredefined=qci5 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=1
set QciTable=default,QciProfilePredefined=QCI1 Pdb 80
set QciTable=default,QciProfilePredefined=QCI2 Pdb 150
set QciTable=default,QciProfilePredefined=QCI5 Pdb 100
set QciTable=default,QciProfilePredefined=QCI1 PdbOffset 100
set QciTable=default,QciProfilePredefined=QCI2 PdbOffset 50
set QciTable=default,QciProfilePredefined=QCI5 PdbOffset 0
set QciTable=default,QciProfilePredefined=QCI1 pdcpSNLength 12
set QciTable=default,QciProfilePredefined=QCI2 pdcpSNLength 12
set QciTable=default,QciProfilePredefined=QCI5 pdcpSNLength 12
set QciTable=default,QciProfilePredefined=QCI1 Priority 1
set QciTable=default,QciProfilePredefined=QCI2 Priority 4
set QciTable=default,QciProfilePredefined=QCI5 Priority 2
set QciTable=default,QciProfilePredefined=QCI1 resourcetype 1
set QciTable=default,QciProfilePredefined=QCI2 resourcetype 1
set QciTable=default,QciProfilePredefined=QCI5 resourcetype 0
set QciTable=default,QciProfilePredefined=QCI1 rlcMode 1
set QciTable=default,QciProfilePredefined=QCI2 rlcMode 1
set QciTable=default,QciProfilePredefined=QCI5 rlcMode 0
set QciTable=default,QciProfilePredefined=QCI1 rlcSNLength 10
set QciTable=default,QciProfilePredefined=QCI2 rlcSNLength 10
set QciTable=default,QciProfilePredefined=QCI5 rlcSNLength 10
set QciTable=default,QciProfilePredefined=QCI1 rlfPriority 10
set QciTable=default,QciProfilePredefined=QCI1 rohcEnabled 1
set QciTable=default,QciProfilePredefined=QCI2 rohcEnabled 0
set QciTable=default,QciProfilePredefined=QCI5 rohcEnabled 0
set QciTable=default,QciProfilePredefined=QCI1 schedulingAlgorithm 6
set QciTable=default,QciProfilePredefined=QCI2 schedulingAlgorithm 3
set QciTable=default,QciProfilePredefined=QCI5 schedulingAlgorithm 0
set QciTable=default,QciProfilePredefined=QCI1 serviceType 1
set QciTable=default,QciProfilePredefined=QCI2 serviceType 0
set QciTable=default,QciProfilePredefined=QCI5 serviceType 2
set QciTable=default,QciProfilePredefined=qci1 tReorderingDl 120
set QciTable=default,QciProfilePredefined=QCI6 dscp 26
set QciTable=default,QciProfilePredefined=QCI7 dscp 26
set QciTable=default,QciProfilePredefined=QCI8 dscp 26
set QciTable=default,QciProfilePredefined=QCI9 dscp 26
set QciTable=default,QciProfilePredefined=QCI6 schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=QCI7 schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=QCI8 schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=QCI9 schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=QCI6 absPrioOverride 0
set QciTable=default,QciProfilePredefined=QCI7 absPrioOverride 0
set QciTable=default,QciProfilePredefined=QCI8 absPrioOverride 0
set QciTable=default,QciProfilePredefined=QCI9 absPrioOverride 0

set QciTable=default,QciProfilePredefined=qci1              qciSubscriptionQuanta 60
set QciTable=default,QciProfilePredefined=qci2              qciSubscriptionQuanta 384
set QciTable=default,QciProfilePredefined=qci5              qciSubscriptionQuanta 1
set QciTable=default,QciProfilePredefined=qci6              qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci7              qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci8              qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci9              qciSubscriptionQuanta 200

set QciTable=default,QciProfilePredefined=qci6              resourceAllocationStrategy              1
set QciTable=default,QciProfilePredefined=qci7              resourceAllocationStrategy              1
set QciTable=default,QciProfilePredefined=qci8              resourceAllocationStrategy              1
set QciTable=default,QciProfilePredefined=qci9              resourceAllocationStrategy              1



set Rcs=1 rlcDlDeliveryFailureAction 2
set Rcs=1 tInactivityTimer 10
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5=1 timeToTriggerA5 480
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5=1 triggerquantitya5 0
set ReportConfigB1Geran=1 hysteresisB1      10
set ReportConfigB1Utra=1 hysteresisB1      10
set ReportConfigA5=1 timeToTriggerA5Rsrq 1024
set ReportConfigB1Geran=1 timeToTriggerB1   640
set ReportConfigB1Utra=1 timeToTriggerB1   640
set ReportConfigB2Geran=1 timeToTriggerB2Rsrq -1
set ReportConfigB2Utra=1 timeToTriggerB2Rsrq -1


for $mo in L850
$mordn = rdn($mo)
cr $mordn,UeMeasControl=1,ReportConfigEUtraIntraFreqPm=1
done

set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigEUtraIntraFreqPm=1 maxReportCellsPm 8
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigEUtraIntraFreqPm=1 reportIntervalPm 5

set EUtranCell.*,UeMeasControl=1,ReportConfigCsfbUtra=1 hysteresis        10
set EUtranCell.*,UeMeasControl=1,ReportConfigSCellA6=1 triggerQuantityA6 0
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 a2criticalthresholdRSRp -140
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 hysteresisA2CriticalRsrp 0
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1 hysteresisA3 10
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA1Search 480
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2Search 480
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2Critical 480
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1 timeToTriggerA3 480
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1 triggerQuantityA3 0
set ReportConfigSCellA6=1 timeToTriggerA6   40
set ReportConfigSCellA1A2=1 hysteresisA1A2Rsrp 10
set ReportConfigElcA1A2=1 hysteresisA1A2Rsrp 10
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2OutSearch  40
set ReportConfigElcA1A2=1 timeToTriggerA1   40
set ReportConfigSCellA1A2=1 timeToTriggerA1   40
set ReportConfigSearch=1 timeToTriggerA1SearchRsrq 1024
set ReportConfigSearch=1 timeToTriggerA1UlSearch 480
set ReportConfigElcA1A2=1 timeToTriggerA2   40
set ReportConfigSCellA1A2=1 timeToTriggerA2   40
set ReportConfigSearch=1 timeToTriggerA2CriticalRsrq 1024
set ReportConfigSearch=1 timeToTriggerA2OutSearchRsrq -1
set ReportConfigSearch=1 timeToTriggerA2SearchRsrq 1024
set ReportConfigB2Utra=1 timeToTriggerB2Rsrq -1

set RlfProfile=1$ t301 1000
set RlfProfile=1$ t310 500
set RlfProfile=1$ t311 5000
set ENodeBFunction=1,Rrc=1 t311 5000
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 tReorderingUl 50
set ENodeBFunction=1,Rrc=1 tRrcConnReest 2
set ENodeBFunction=1,Rrc=1 tWaitForRrcConnReest 9
set ENodeBFunction=1,RlfProfile n310 10
set ENodeBFunction=1,RlfProfile n311 1
set ENodeBFunction=1,Rrc=1 t301 1000
set ENodeBFunction=1,Rrc=1 t304 2000
set RadioBearerTable=default,SignalingRadioBearer=1 tPollRetransmitDl 80
set RadioBearerTable=default,SignalingRadioBearer=1 tPollRetransmitUl 80
cr ENodeBFunction=1,TimerProfile=0
6
8
3
10
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 timerProfileRef ENodeBFunction=1,TimerProfile=0
set TimerProfile=0                                          tWaitForRrcConnReest 6
set TimerProfile=0                                          tRrcConnectionReconfiguration 8
set TimerProfile=0                                          tRrcConnReest 3
set TimerProfile=0                                          tRelocOverall 20

set . ulTrafficDelay -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1
set . dlTrafficDelay -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1

set EUtranCellFDD=.*,UeMeasControl=1                  filterCoefficientEUtraRsrp 4


set EUtranCellFDD=.*,UeMeasControl=1 ueMeasurementsActiveIF true


# UL COMP

pr EUtranCellFDD=UW
if $nr_of_mos = 3
cr ENodeBFunction=1,UlCompGroup=1
ENodeBFunction=1,SectorCarrier=60 ENodeBFunction=1,SectorCarrier=61 ENodeBFunction=1,SectorCarrier=62
elseif $nr_of_mos = 2
cr ENodeBFunction=1,UlCompGroup=1
ENodeBFunction=1,SectorCarrier=60 ENodeBFunction=1,SectorCarrier=61
elseif $nr_of_mos = 1
cr ENodeBFunction=1,UlCompGroup=1
ENodeBFunction=1,SectorCarrier=60
elseif $nr_of_mos = 4
cr ENodeBFunction=1,UlCompGroup=1
ENodeBFunction=1,SectorCarrier=60 ENodeBFunction=1,SectorCarrier=61 ENodeBFunction=1,SectorCarrier=62 ENodeBFunction=1,SectorCarrier=63
fi
deb ENodeBFunction=1,UlCompGroup=1


set ENodeBFunction=1                                        zzzTemporary13    -2000000000
set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1 sMeasure 0
set SecurityHandling=1                                      cipheringAlgoPrio 1 2 0
set EUtranCell.*,UeMeasControl=1                  lowPrioMeasThresh 0
set EUtranCell.*,UeMeasControl=1                  maxUtranCellsToMeasure 32
set EUtranCell.*,UeMeasControl=1                  allowReleaseQci1 false
seti ENodeBFunction=1,Rrc=1        tRrcConnectionSetup  10
set EUtranCell.*,UeMeasControl=1                  ulSinrOffset 30
set SignalingRadioBearer dlMaxRetxThreshold 16
set EUtranCellFDD=.*,UeMeasControl=1 ueMeasurementsActive 1
set EutrancellFDD=.*,UeMeasControl=1                  a5B2MobilityTimer 0
set EUtranCellFDD=.*,UeMeasControl=1 excludeInterFreqAtCritical False
set ENodeBFunction=1,Rrc=1 tRrcConnectionReconfiguration 10
set UeMeasControl=1      a3SuspendCsgTimer 0


####IFLB


set LoadBalancingFunction=1 lbCeiling 500
set LoadBalancingFunction=1 lbThreshold 20
set LoadBalancingFunction=1 lbHitRateEUtranAddThreshold 5
set LoadBalancingFunction=1 lbHitRateEUtranMeasUeIntensity 10
set LoadBalancingFunction=1 lbHitRateEUtranMeasUeThreshold 10
set LoadBalancingFunction=1 lbHitRateEUtranRemoveThreshold 2
set LoadBalancingFunction=1 lbMeasScalingLimit 30
set LoadBalancingFunction=1 lbRateOffsetCoefficient 320
set LoadBalancingFunction=1 lbRateOffsetLoadThreshold 1500
set QciTable=default,QciProfilePredefined=qci1              qciSubscriptionQuanta 60
set QciTable=default,QciProfilePredefined=qci2              qciSubscriptionQuanta 384
set QciTable=default,QciProfilePredefined=qci5              qciSubscriptionQuanta 1
set QciTable=default,QciProfilePredefined=qci6              qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci7              qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci8              qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci9              qciSubscriptionQuanta 200
set AutoCellCapEstFunction=1 useEstimatedCellCap true
set EutrancellFDD=.* cellSubscriptionCapacity 5000

set EutrancellFDD=.* noOfPucchSrUsers 420
set EutrancellFDD=.* noOfPucchCqiUsers 320



############

set EutrancellFDD=.* cellCapMaxCellSubCap 60000
set EutrancellFDD=.* cellCapMinCellSubCap 1500
set EutrancellFDD=.* cellCapMinMaxWriProt true
set  CXC4011373   featurestate  1
set  CXC4011370   featurestate  1
set  CXC4011698   featurestate  1


set EutrancellFDD=.* dlInterferenceManagementActive TRUE
set EUtranCellFDD=.* noOfChannelSelectionsets 4
set EUtranCellFDD=.* channelSelectionsetSize 2
set EutrancellFDD=.* advCellSupSensitivity 25
set EUtranCellFDD=.*,EUtranFreqRelation=.* qoffsetfreq 0
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1 a3offset 30
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigB2Utra=1 triggerQuantityB2 0
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA1Search 480
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2Search 480
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2Critical 480
set EUtranCellFDD=.* pdcchOuterLoopInitialAdjVolte -46
set EUtranCellFDD=.* pdcchOuterLoopInitialAdj -70
set EUtranCellFDD=.* pdcchOuterLoopInitialAdjPCell -70
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 inhibitA2SearchConfig 1
set EutrancellFDD=.*,UeMeasControl=1         bothA5RsrpRsrqCheck False
set EutrancellFDD=.*,UeMeasControl=1                  inhibitB2RsrqConfig true
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2OutSearch  40
set EutrancellFDD=.* SystemInformationBlock3 snonintrasearchQ=0
set EutrancellFDD=.* SystemInformationBlock3 sintrasearchp=44
set EUtranCellFDD=.* mappingInfo mappingInfoSIB3=1
set EUtranCellFDD=.* mappingInfo mappingInfoSIB7=5

set EUtranCellFDD=.*      lbEUtranAcceptOffloadThreshold  10
set EUtranCellFDD=.*      lbEUtranTriggerOffloadThreshold 30
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSCellA1A2=1 hysteresisA1A2RsrpBidirectional 10

set EUtranCellFDD=.* bsrThreshold 100
set EUtranCellFDD=.* noOfUlImprovedUe 2


#Common Parameter

set EUtranFreqRelation=39150 allowedmeasbandwidth 100
set EUtranFreqRelation=39348 allowedmeasbandwidth 100
set EUtranFreqRelation=39151 allowedmeasbandwidth 100
set EUtranFreqRelation=39349 allowedmeasbandwidth 100
set EUtranFreqRelation=365$ allowedmeasbandwidth 75
set EUtranFreqRelation=1526 allowedmeasbandwidth 75
set EUtranFreqRelation=2545 allowedmeasbandwidth 25


set EUtranFreqRelation=365$ anrMeasOn true
set EUtranFreqRelation=39150 anrMeasOn true
set EUtranFreqRelation=39348 anrMeasOn true
set EUtranFreqRelation=39151 anrMeasOn true
set EUtranFreqRelation=39349 anrMeasOn true
set EUtranFreqRelation=1526 anrMeasOn true
set EUtranFreqRelation=2545 anrMeasOn true


set . maxTimeEventBasedPciConf 30
set . measuringEcgiWithAgActive false
set AnrFunction=1 probCellDetectLowHoSuccThres 10

# UL COMP

set QciTable=default,QciProfilePredefined=qci1 rlfProfileRef RlfProfile=1
set QciTable=default,QciProfilePredefined=QCI6 dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=QCI8 dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=QCI9 dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci5              tReorderingUl 60
set QciTable=default,QciProfilePredefined=qci6             tReorderingUl 60
set DataRadioBearer ulMaxRetxThreshold 32
set Rrc=1 t300 2000
set Rrc=1 t320 30
set RlfProfile=1$ n310 10
set RlfProfile=1$ n311 1
set RlfProfile=1$ t301 1000
set RlfProfile=1$ t310 500
set RlfProfile=1$ t311 5000
set RlfProfile=0$ n310 20
set RlfProfile=0$ n311 1
set RlfProfile=0$ t301 2000
set RlfProfile=0$ t310 2000
set RlfProfile=0$ t311 10000

#CA
set LoadBalancingFunction=1 lbDiffCaOffset 300
set CarrierAggregationFunction caRateAdjustCoeff 5
set CarrierAggregationFunction waitForCaOpportunity 2000
set CarrierAggregationFunction sCellScheduleSinrThres -50
set CarrierAggregationFunction sCellActDeactDataThres 20
set CarrierAggregationFunction sCellActDeactDataThresHyst 20
set CarrierAggregationFunction sCellDeactProhibitTimer 50
set CarrierAggregationFunction causagelimit 200
set CarrierAggregationFunction sCellActProhibitTimer 10
set CarrierAggregationFunction caPreemptionThreshold 50
set CarrierAggregationFunction sCellSelectionMode 0
set LoadBalancingFunction lbCaThreshold 2000
set LoadBalancingFunction lbCaCapHysteresis 20
set CarrierAggregationFunction pdcchEnhancedLaForVolte False

#GERAN

set GeranFreqGroupRelation=1         csFallbackPrio    7
set GeranFreqGroupRelation=1         csFallbackPrioEC    7
set GeranFreqGroupRelation=1         altCsfbTargetPrio   2
set AnrFunction=1,AnrFunctionGeran=1 anrStateGsm 1
set GeranFreqGroup qRxLevMin -111
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

#RIM

set CXC4010973 featurestate 1
set ENodeBFunction=1                                        forcedSiTunnelingActive false
set CXC4010956 featurestate 1

###Paging

set ENodeBFunction=1,Paging=1 maxNoOfPagingRecords                 7
set ENodeBFunction=1,Paging=1 nB                                   3

####

### Additional Parameters

lset UeMeasControl PrioOffsetPerQci qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,offsetPerQciPrio=7

set . zzzTemporary60 1

##Features_GPL

set  CXC4011368   featurestate  0
set  CXC4010512   featurestate  0
set  CXC4010955   featurestate  0
set  CXC4010973   featurestate  1
set  CXC4011055   featurestate  0
set  CXC4011246   featurestate  0
set  CXC4011346   featurestate  1
set  CXC4011478   featurestate  0
set  cxc4011554   featurestate  0
set  CXC4011663   featurestate  0
set  CXC4011664   featurestate  0
set  CXC4011736   featurestate  0
set  CXC4011810   featurestate  0
set  cxc4011911   featurestate  0
set  cxc4011966   featurestate  0
set  CXC4011983   featurestate  0
set  CXC4011714   featurestate  0
set  CXC4010319   featurestate  1
set  CXC4010320   featurestate  1
set  CXC4010609   featurestate  1
set  CXC4010613   featurestate  1
set  CXC4010616   featurestate  1
set  CXC4010618   featurestate  1
set  CXC4010620   featurestate  1
set  CXC4010717   featurestate  1
set  CXC4010723   featurestate  1
set  CXC4010770   featurestate  1
set  CXC4010841   featurestate  1
set  CXC4010856   featurestate  1
set  CXC4010912   featurestate  1
set  CXC4010956   featurestate  1
set  CXC4010959   featurestate  1
set  CXC4010961   featurestate  1
set  CXC4010962   featurestate  1
set  CXC4010967   featurestate  1
set  CXC4010974   featurestate  1
set  CXC4010980   featurestate  1
set  CXC4010990   featurestate  1
set  CXC4011011   featurestate  1
set  CXC4011033   featurestate  1
set  CXC4011034   featurestate  1
set  CXC4011050   featurestate  1
set  CXC4011057   featurestate  1
set  CXC4011059   featurestate  1
set  CXC4011060   featurestate  1
set  CXC4011061   featurestate  1
set  CXC4011062   featurestate  1
set  CXC4011064   featurestate  1
set  CXC4011074   featurestate  1
set  CXC4011075   featurestate  1
set  CXC4011157   featurestate  1
set  CXC4011183   featurestate  1
set  CXC4011245   featurestate  1
set  CXC4011247   featurestate  1
set  CXC4011251   featurestate  1
set  CXC4011252   featurestate  1
set  CXC4011253   featurestate  1
set  CXC4011255   featurestate  1
set  CXC4011258   featurestate  1
set  CXC4011319   featurestate  1
set  CXC4011327   featurestate  1
set  CXC4011345   featurestate  1
set  CXC4011366   featurestate  1
set  CXC4011370   featurestate  1
set  CXC4011372   featurestate  1
set  CXC4011373   featurestate  1
set  CXC4011376   featurestate  1
set  CXC4011378   featurestate  1
set  CXC4011422   featurestate  1
set  CXC4011443   featurestate  1
set  CXC4011444   featurestate  1
set  CXC4011477   featurestate  1
set  CXC4011479   featurestate  1
set  CXC4011481   featurestate  1
set  CXC4011482   featurestate  1
set  CXC4011485   featurestate  1
set  CXC4011515   featurestate  1
set  CXC4011698   featurestate  1
set  CXC4011711   featurestate  1
set  CXC4011715   featurestate  1
set  CXC4011813   featurestate  1
set  CXC4011815   featurestate  1
set  CXC4011910   featurestate  1
set  CXC4011913   featurestate  1
set  CXC4011914   featurestate  1
set  CXC4011918   featurestate  1
set  CXC4011940   featurestate  1
set  CXC4011941   featurestate  1
set  CXC4011955   featurestate  1
set  CXC4011969   featurestate  1
set  CXC4012003   featurestate  1
set  CXC4012018   featurestate  1
set  CXC4012070   featurestate  1
set  CXC4012089   featurestate  1
set  CXC4011476   featurestate  1
set  CXC4011559   featurestate  1
set  CXC4011922   featurestate  1
set  CXC4011946   featurestate  1
set  CXC4012129   featurestate  1
set  CXC4012240   featurestate  1
set  CXC4011072   featurestate  0
set  CXC4011974   featurestate  1

## old Features_GPL

set  CXC4011667   featurestate  1
set  CXC4011056   featurestate  1
set  CXC4010949   featurestate  1
set  CXC4010963   featurestate  1
set  CXC4010964   featurestate  1
set  CXC4011063   featurestate  1
set  CXC4011067   featurestate  1
set  CXC4011068   featurestate  1
set  CXC4011069   featurestate  1
set  CXC4011163   featurestate  1
set  CXC4011256   featurestate  1
set  CXC4011317   featurestate  1
set  CXC4011356   featurestate  1
set  CXC4011427   featurestate  1
set  CXC4011618   featurestate  1
set  CXC4011699   featurestate  1
set  CXC4011710   featurestate  1
set  CXC4011716   featurestate  1
set  CXC4011804   featurestate  1
set  CXC4011807   featurestate  1
set  CXC4011811   featurestate  1
set  CXC4011814   featurestate  1
set  CXC4011820   featurestate  1
set  CXC4011917   featurestate  1
set  CXC4011930   featurestate  1
set  CXC4011933   featurestate  1
set  CXC4011803   featurestate  1
set  CXC4011937   featurestate  1
set  CXC4011938   featurestate  1
set  CXC4011939   featurestate  1
set  CXC4011942   featurestate  1
set  CXC4011951   featurestate  1
set  CXC4011958   featurestate  0
set  CXC4011967   featurestate  1
set  CXC4011973   featurestate  1
set  CXC4011975   featurestate  1
set  CXC4011982   featurestate  1
set  CXC4011991   featurestate  1
set  CXC4012022   featurestate  1
set  CXC4040004   featurestate  1
set  CXC4040005   featurestate  1
set  CXC4040006   featurestate  1
set  CXC4040008   featurestate  1
set  CXC4040009   featurestate  1
set  CXC4040010   featurestate  1
set  CXC4040014   featurestate  1
set  CXC4011155   featurestate  1
set  CXC4012261   featurestate  1




## 20Q2Features

set CXC4012271 featurestate 1

## additional Feature

set CXC4012344 featurestate 1
set . ul256qamEnabled TRUE


set CXC4012316 featurestate 1
set . eUlFssSwitchThresh 30
set . noOfEnhAdptReTxCand -1


set ENodeBFunction=1 measuringEcgiWithAgActive false
set ENodeBFunction=1,AnrFunction=1 pciConflictDetectionEcgiMeas         false
set ENodeBFunction=1,AnrFunction=1 pciConflictMobilityEcgiMeas          false



set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThrQci1RsrqOffset -240

set EUtranCell prsPowerBoosting 3
set ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1 anrStateUtran 0
set ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1 hoAllowedUtranPolicy 0


##New Addition

set QciTable=default,QciProfilePredefined=qci1 measReportConfigParams a1ThresholdRsrpPrimOffset=2
set QciTable=default,QciProfilePredefined=qci1 measReportConfigParams a2ThresholdRsrpPrimOffset=2
set QciTable=default,QciProfilePredefined=qci1 measReportConfigParams a5Threshold1RsrpOffset=2
set QciTable=default,QciProfilePredefined=qci1 measReportConfigParams a5Threshold2RsrpOffset=2
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigEUtraBadCovPrim=1 a2ThresholdRsrpPrim -140
set EUtranCellFDD=.*,UeMeasControl=1                  filterCoefficientEUtraRsrq 11
set SectorCarrier radioTransmitPerfMode 2
set EUtranCellFDD=.*,UeMeasControl=1 ueMeasurementsActiveUTRAN False
set EUtranCellFDD=.*,UeMeasControl=1 ueMeasurementsActiveGERAN True
set ReportConfigCsfbUtra=1 hysteresis 10
set EUTRANCELL dlInternalChannelBandwidth 0
set EUTRANCELL UlInternalChannelBandwidth 0
set ReportConfigSCellA6=1 timeToTriggerA6   40
set EUtranCell  systemInformationBlock3 sNonIntraSearchP=10
set ReportConfigSearch=1 hysteresisA2CriticalRsrq 10
set ReportConfigElcA1A2=1 a1a2ThresholdRsrp -134
set ReportConfigSCellA1A2=1 a1a2ThresholdRsrp -126
set ReportConfigSCellA1A2=1 a1a2ThresholdRsrpBidir -140
set ReportConfigSCellA1A2=1 a1a2ThresholdRsrq -165
set GeranCellRelation=.* coverageIndicator 1
set EUtranCell.*DD=.*,UeMeasControl=1,ReportConfigB2GeranUlTrig=1 reportIntervalB2 4
set ReportConfigB2Geran=1 timeToTriggerB2   1280

set CXC4012238 featurestate 1

###Feature activation only
set CXC4012326 featurestate 1
set CXC4012260 featurestate 1
set CXC4012374 featurestate 1
set CXC4012019 featurestate 1

###ASGH BLER Target
set CXC4012199 featurestate 1
set ENodeBFunction=1,EUtranCell.*DD= dlBlerTargetEnabled TRUE
cr ENodeBFunction=1,SubscriberGroupProfile=1
set ENodeBFunction=1,SubscriberGroupProfile=1 bearerTriggerList qci=1
set ENodeBFunction=1,SubscriberGroupProfile=1 dlHarqBlerTarget 5
set ENodeBFunction=1,SubscriberGroupProfile=1 ulHarqBlerTarget 3



wait 2
lt all

$date = `date +%y%m%d_%H%M`
cvms GPL_$date
confbd-


lt all
rbs
rbs

confbd+

$date = `date +%y%m%d_%H%M`
cvms Pre_LMS_Config_$date

st cell


##FDD L850


ma L850 EUtranCellFDD earfcn 2545
wait 1
if $nr_of_mos != 0
for $mo in L850
$mordn = rdn($mo)
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2SearchRsrp 20
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrp -58
set $mordn,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a1a2ThrRsrqQciOffset=0,a1a2ThrRsrpQciOffset=-54
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2criticalthresholdRSRp -140
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThrQci1RsrpOffset -20
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThrQci1RsrqOffset -240
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrp -58
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp -114
set $mordn,UeMeasControl=1,ReportConfigA5=1 hysteresisA5 20
set $mordn,EUtranFreqRelation=39150 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39348 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39151 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39349 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=1526 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=365$ a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=2545 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39150 a5Thr2RsrpFreqOffset 2
set $mordn,EUtranFreqRelation=39348 a5Thr2RsrpFreqOffset 2
set $mordn,EUtranFreqRelation=39151 a5Thr2RsrpFreqOffset 2
set $mordn,EUtranFreqRelation=39349 a5Thr2RsrpFreqOffset 2
set $mordn,EUtranFreqRelation=1526 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=365$ a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=2545 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39150  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=-54,a5Thr2RsrpFreqQciOffset=66,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=39348  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=-54,a5Thr2RsrpFreqQciOffset=66,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=39151  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=-54,a5Thr2RsrpFreqQciOffset=66,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=39349  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=-54,a5Thr2RsrpFreqQciOffset=66,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=1526  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=-54,a5Thr2RsrpFreqQciOffset=8,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=365$  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=-54,a5Thr2RsrpFreqQciOffset=68,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=2545  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0,lbQciProfileHandling=1

set $mordn,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold1Rsrp -140
set $mordn,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold2Geran -95
set $mordn,EUtranFreqRelation=39150 cellReselectionPriority 6
set $mordn,EUtranFreqRelation=39348 cellReselectionPriority 6
set $mordn,EUtranFreqRelation=39151 cellReselectionPriority 6
set $mordn,EUtranFreqRelation=39349 cellReselectionPriority 6
set $mordn,EUtranFreqRelation=1526 cellReselectionPriority 4
set $mordn,EUtranFreqRelation=365$ cellReselectionPriority 3
set $mordn,EUtranFreqRelation=2545 cellReselectionPriority 2
set $mordn,GeranFreqGroupRelation=1         cellReselectionPriority 1

set $mordn,EUtranFreqRelation=39150 connectedmodemobilityprio 6
set $mordn,EUtranFreqRelation=39348 connectedmodemobilityprio 6
set $mordn,EUtranFreqRelation=39151 connectedmodemobilityprio 6
set $mordn,EUtranFreqRelation=39349 connectedmodemobilityprio 6
set $mordn,EUtranFreqRelation=1526 connectedmodemobilityprio 4
set $mordn,EUtranFreqRelation=365$ connectedmodemobilityprio 3
set $mordn,EUtranFreqRelation=2545 connectedmodemobilityprio 2
set $mordn,GeranFreqGroupRelation=1         connectedModeMobilityPrio -1
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA2CriticalRsrp 0
set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1 hysteresisA3 10
set $mordn,UeMeasControl=1,ReportConfigB2Geran=1 hysteresisB2 20
set $mordn,EUtranFreqRelation=.* qRxLevMin -124
set $mordn,GeranFreqGroupRelation=1         qRxLevMin         -95
set $mordn qRxLevMin -124
set $mordn SystemInformationBlock3 sintrasearch=44
set $mordn SystemInformationBlock3 snonintrasearch=0
set $mordn SystemInformationBlock3 qhyst=4
set $mordn threshServingLow 0
set $mordn,EUtranFreqRelation=39150 threshXHigh 14
set $mordn,EUtranFreqRelation=39348 threshXHigh 14
set $mordn,EUtranFreqRelation=39151 threshXHigh 14
set $mordn,EUtranFreqRelation=39349 threshXHigh 14
set $mordn,EUtranFreqRelation=1526 threshXHigh 12
set $mordn,EUtranFreqRelation=365$ threshXHigh 12
set $mordn,GeranFreqGroupRelation=1     threshXLow  62
set $mordn,EUtranFreqRelation=39150 voicePrio -1
set $mordn,EUtranFreqRelation=39348 voicePrio -1
set $mordn,EUtranFreqRelation=39151 voicePrio -1
set $mordn,EUtranFreqRelation=39349 voicePrio -1
set $mordn,EUtranFreqRelation=1526 voicePrio 4
set $mordn,EUtranFreqRelation=365$ voicePrio -1
set $mordn,EUtranFreqRelation=2545 voicePrio 2

set $mordn,GeranFreqGroupRelation=1         voicePrio     -1
set $mordn,EUtranFreqRelation  interFreqMeasType 0
set $mordn,UeMeasControl=1                  ueMeasurementsActiveGERAN True
set $mordn,EUtranFreqRelation=39150         lbA5Thr1RsrpFreqOffset 97
set $mordn,EUtranFreqRelation=39348         lbA5Thr1RsrpFreqOffset 97
set $mordn,EUtranFreqRelation=39151         lbA5Thr1RsrpFreqOffset 97
set $mordn,EUtranFreqRelation=39349         lbA5Thr1RsrpFreqOffset 97
set $mordn,EUtranFreqRelation=1526         lbA5Thr1RsrpFreqOffset 97
set $mordn,EUtranFreqRelation=365$         lbA5Thr1RsrpFreqOffset 97
set $mordn,EUtranFreqRelation=2545         lbA5Thr1RsrpFreqOffset 0

done
else
fi



#### IFLB Parameters

set EutrancellFDD=.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold1Rsrp  -140
set EutrancellFDD=.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold2Rsrp   -111


set EutrancellFDD=.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 hysteresisA5 10




lt all
rbs
rbs
$date = `date +%y%m%d_%H%M`
cvms BEFORE_QOS_$date
confb+
gs+

set ENodeBFunction=1                                        dscpLabel                       46
set ENodeBFunction=1                                        gtpuErrorIndicationDscp         46
set ENodeBFunction=1                                        interEnbCaTunnelDscp            26
set ENodeBFunction=1                                        interEnbUlCompTunnelDscp        26
set ENodeBFunction=1                                        s1GtpuEchoDscp                  46
set ENodeBFunction=1                                        x2GtpuEchoDscp                  46


cr Transport=1,QosProfiles=1,DscpPcpMap=1

set QciTable=default,QciProfilePredefined=qci1              dscp              34
set QciTable=default,QciProfilePredefined=qci2              dscp              34
set QciTable=default,QciProfilePredefined=qci3              dscp              26
set QciTable=default,QciProfilePredefined=qci4              dscp              26

set QciTable=default,QciProfilePredefined=qci5              dscp              46
set QciTable=default,QciProfilePredefined=qci6              dscp              26
set QciTable=default,QciProfilePredefined=qci7              dscp              26
set QciTable=default,QciProfilePredefined=qci8              dscp              26

set QciTable=default,QciProfilePredefined=qci9              dscp              26

set SysM=1,OamTrafficClass=1 dscp 28

set EthernetPort=TN_C                                       egressQosMarking  QosProfiles=1,DscpPcpMap=1


set SctpProfile= dscp 46
set Ntp=1,NtpFrequencySync= dscp 46



lt all


set QosProfiles=1,DscpPcpMap=1  pcp0
set QosProfiles=1,DscpPcpMap=1  pcp1
set QosProfiles=1,DscpPcpMap=1  pcp2
set QosProfiles=1,DscpPcpMap=1  pcp3
set QosProfiles=1,DscpPcpMap=1  pcp4
set QosProfiles=1,DscpPcpMap=1  pcp5
set QosProfiles=1,DscpPcpMap=1  pcp6
set QosProfiles=1,DscpPcpMap=1  pcp7


set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp0 0 1 2 3 4 5 6 7 8 9 10 11 19 20 21 27 29 30 31 32 33 35 36 37 38 39 40 41 42 43 44 45 47  48  49  50  51  52  53  54  55  56  57  58  59  60  61  62  63

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp3 12 13 14 15 16 17 18

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp4 22 23 24 25 26

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp5 28

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp6 34

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp7 46


set Router=OAM,DnsClient=1 dscp 28

set Router=.*,InterfaceIPv4= egressQosMarking               egressQosMarking  QosProfiles=1,DscpPcpMap=1
set Router=LTECP,InterfaceIPv4=TN_C_CP                      egressQosMarking  QosProfiles=1,DscpPcpMap=1
set Router=LTEUP,InterfaceIPv4=TN_C_UP                      egressQosMarking  QosProfiles=1,DscpPcpMap=1
set Router=OAM,InterfaceIPv4=TN_C_OAM                       egressQosMarking  QosProfiles=1,DscpPcpMap=1
set Router=ABIS,InterfaceIPv4=TN_A_ABIS                     egressQosMarking  QosProfiles=1,DscpPcpMap=1
set Router=ABIS,InterfaceIPv4=TN_B_ABIS                     egressQosMarking  QosProfiles=1,DscpPcpMap=1
set Router=ABIS,InterfaceIPv4=TN_C_ABIS                     egressQosMarking  QosProfiles=1,DscpPcpMap=1

set VlanPort=                                               egressQosMarking  QosProfiles=1,DscpPcpMap=1
set VlanPort=TN_C_CP                                        egressQosMarking  QosProfiles=1,DscpPcpMap=1
set VlanPort=TN_C_OAM                                       egressQosMarking  QosProfiles=1,DscpPcpMap=1
set VlanPort=TN_C_UP                                        egressQosMarking  QosProfiles=1,DscpPcpMap=1
set VlanPort=TN_A_ABIS                                      egressQosMarking  QosProfiles=1,DscpPcpMap=1
set VlanPort=TN_C_ABIS                                      egressQosMarking  QosProfiles=1,DscpPcpMap=1

cvms AFTER_QOS_$date

confb-
gs-

lt all
rbs
rbs
st cell
confb+
confd+
set Transport=1,SctpProfile=1 alphaIndex 3
set Transport=1,SctpProfile=1 assocMaxRtx 20
set Transport=1,SctpProfile=1 betaIndex 2
set Transport=1,SctpProfile=1 bundlingActivated TRUE
set Transport=1,SctpProfile=1 bundlingAdaptiveActivated TRUE
set Transport=1,SctpProfile=1 bundlingTimer 0
set Transport=1,SctpProfile=1 cookieLife 60
set Transport=1,SctpProfile=1 dscp 46
set Transport=1,SctpProfile=1 minRto 1000
set Transport=1,SctpProfile=1 hbMaxBurst 1
set Transport=1,SctpProfile=1 heartbeatActivated TRUE
set Transport=1,SctpProfile=1 heartbeatInterval 2000
set Transport=1,SctpProfile=1 incCookieLife 30
set Transport=1,SctpProfile=1 initARWnd 16384
set Transport=1,SctpProfile=1 initRto 2000
set Transport=1,SctpProfile=1 initialHeartbeatInterval 500
set Transport=1,SctpProfile=1 maxActivateThr 65535
set Transport=1,SctpProfile=1 maxBurst 4
set Transport=1,SctpProfile=1 maxInStreams 2
set Transport=1,SctpProfile=1 maxInitRt 5
set Transport=1,SctpProfile=1 maxOutStreams 2
set Transport=1,SctpProfile=1 maxRto 4000
set Transport=1,SctpProfile=1 maxSctpPduSize 1480
set Transport=1,SctpProfile=1 maxShutdownRt 5
set Transport=1,SctpProfile=1 minActivateThr 1
set Transport=1,SctpProfile=1 noSwitchback TRUE
set Transport=1,SctpProfile=1 pathMaxRtx 10
set Transport=1,SctpProfile=1 primaryPathAvoidance TRUE
set Transport=1,SctpProfile=1 primaryPathMaxRtx 0
set Transport=1,SctpProfile=1 sackTimer 100
set Transport=1,SctpProfile=1 thrTransmitBuffer 48
set Transport=1,SctpProfile=1 thrTransmitBufferCongCeased 85
set Transport=1,SctpProfile=1 transmitBufferSize 64
set Transport=1,SctpProfile=1 userLabel SCTP


set SignalingRadioBearer ulMaxRetxThreshold 16
set DataRadioBearer ulMaxRetxThreshold 16



set CXC4011973 featurestate 0
set CXC4011559 featurestate 0
set CXC4011922 featurestate 0
set CXC4011476 featurestate 0


#LMS
set EutrancellFDD=.*,EUtranFreqRelation=39150 a5Thr2RsrpFreqOffset 0
set EutrancellFDD=.*,EUtranFreqRelation=39348 a5Thr2RsrpFreqOffset 0
set EutrancellFDD=.*,EUtranFreqRelation=39151 a5Thr2RsrpFreqOffset 0
set EutrancellFDD=.*,EUtranFreqRelation=39348 a5Thr2RsrpFreqOffset 0
set EutrancellFDD=.*,EUtranFreqRelation=1526 a5Thr2RsrpFreqOffset -2
set EutrancellFDD=.*,EUtranFreqRelation=365$ a5Thr2RsrpFreqOffset -2
set EUtranCellFDD=.*,EUtranFreqRelation=1526  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=-54,a5Thr2RsrpFreqQciOffset=6,lbQciProfileHandling=1


##RSRQ
ma L900 EUtranCellFDD earfcn 2545
wait 1
if $nr_of_mos != 0 
for $mo in L900
$mordn = rdn($mo)
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2SearchRsrq 10
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrq -160
set $mordn,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a1a2ThrRsrqQciOffset=-40,a1a2ThrRsrpQciOffset=-54
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2criticalthresholdRSRq -195
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThrQci1RsrqOffset -100
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA2CriticalRsrq 100
set $mordn,UeMeasControl=1,ReportConfigSearch=1 InhibitA2SearchConfig 0
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA1SearchRsrq 1024
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2CriticalRsrq 1024
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2SearchRsrq 1024
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrq -150
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrq -190
set $mordn,UeMeasControl=1,ReportConfigA5=1 hysteresisA5 20
set $mordn,UeMeasControl=1,ReportConfigA5=1 hysteresisA5RsrqOffset 0
set $mordn,UeMeasControl=1,ReportConfigA5=1 timeToTriggerA5Rsrq 1024
set $mordn,EUtranFreqRelation=.* a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39150 a5Thr2RsrqFreqOffset -20
set $mordn,EUtranFreqRelation=39348 a5Thr2RsrqFreqOffset -20
set $mordn,EUtranFreqRelation=39151 a5Thr2RsrqFreqOffset -20
set $mordn,EUtranFreqRelation=39349 a5Thr2RsrqFreqOffset -20
set $mordn,EUtranFreqRelation=1526 a5Thr2RsrqFreqOffset  -20
set $mordn,EUtranFreqRelation=365$ a5Thr2RsrqFreqOffset  -20
set $mordn,EUtranFreqRelation=2545 a5Thr2RsrqFreqOffset 0
set $mordn,EUtranFreqRelation=39150  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=170,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=39348  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=170,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=39151  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=170,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=39349  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=170,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=1526  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=170,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=365$  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=170,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=2545  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrqFreqQciOffset=-0,a5Thr2RsrqFreqQciOffset=0,lbQciProfileHandling=1
set $mordn,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold2Rsrq -170
set $mordn,UeMeasControl=1 bothA5RsrpRsrqCheck True
done
else
fi


###ASGH
set CXC4012199  featurestate 1
set CXC4012374  featurestate 1
cr ENodeBFunction=1,SubscriberGroupProfile=1
set ENodeBFunction=1,SubscriberGroupProfile=1 bearerTriggerList qci=1
set ENodeBFunction=1,SubscriberGroupProfile=1 cellTriggerList 60 61 62
set ENodeBFunction=1,SubscriberGroupProfile=1 ulHarqBlerTarget 3
set ENodeBFunction=1,SubscriberGroupProfile=1 dlHarqBlerTarget 3
set ENodeBFunction=1,SubscriberGroupProfile=1 ulMcsUpperLimit 12 


#IFO

confbd+

set CXC4011557 featurestate 1
set CXC4011319 featurestate 1
set CXC4011373 featurestate 1
set CXC4010974 featurestate 1
set CXC4011443 featurestate 1

set EUtranCellFDD=.*,EUtranFreqRelation=39150 lbBnrPolicy 3
set EUtranCellFDD=.*,EUtranFreqRelation=39348 lbBnrPolicy 3
set EUtranCellFDD=.*,EUtranFreqRelation=39151 lbBnrPolicy 3
set EUtranCellFDD=.*,EUtranFreqRelation=39349 lbBnrPolicy 3
set EUtranCellFDD=.*,EUtranFreqRelation=1526 lbBnrPolicy 3
set EUtranCellFDD=.*,EUtranFreqRelation=365 lbBnrPolicy 3
set AnrFunction=1,AnrFunctionEUtran=1                       lbCellOffloadCapacityPolicy  24000
set LoadBalancingFunction=1                                 lbCauseCodeS1SourceTriggersOffload 0
set LoadBalancingFunction=1                                 lbCauseCodeS1TargetAcceptsOffload 0
set LoadBalancingFunction=1                                 lbCauseCodeX2SourceTriggersOffload 0
set LoadBalancingFunction=1                                 lbCauseCodeX2TargetAcceptsOffload 0
set LoadBalancingFunction=1                                 lbEUtranOffloadBackoffTime 30

set ,ExternalEUtranCellTDD=.* lbEUtranCellOffloadCapacity 24000
set ,ExternalEUtranCellFDD=.* lbEUtranCellOffloadCapacity 12000

set EUtranCellFDD=.* lbEUtranTriggerOffloadThreshold 10
set EUtranCellFDD=.* lbEUtranAcceptOffloadThreshold 1600


set EutrancellFDD=.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold1Rsrp  -140
set EutrancellFDD=.*,EUtranFreqRelation=39150         lbA5Thr1RsrpFreqOffset 97
set EutrancellFDD=.*,EUtranFreqRelation=39348         lbA5Thr1RsrpFreqOffset 97
set EutrancellFDD=.*,EUtranFreqRelation=39151         lbA5Thr1RsrpFreqOffset 97
set EutrancellFDD=.*,EUtranFreqRelation=39349         lbA5Thr1RsrpFreqOffset 97
set EutrancellFDD=.*,EUtranFreqRelation=1526         lbA5Thr1RsrpFreqOffset 97
set EutrancellFDD=.*,EUtranFreqRelation=365$         lbA5Thr1RsrpFreqOffset 97
set EutrancellFDD=.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 hysteresisA5 10

set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold2Rsrp -117
set LoadBalancingFunction=1 lbCeiling 500
set LoadBalancingFunction=1 lbRateOffsetCoefficient 320
set LoadBalancingFunction=1 lbRateOffsetLoadThreshold 1500
set LoadBalancingFunction=1 lbThreshold 5

set EutrancellFDD=.* cellCapMaxCellSubCap 60000
set EutrancellFDD=.* cellCapMinCellSubCap 9000
set AutoCellCapEstFunction=1 useEstimatedCellCap true

set EUtranCellFDD=.*,EUtranFreqRelation=39150, loadbalancing    2
set EUtranCellFDD=.*,EUtranFreqRelation=39150, lbBnrallowed True
set EUtranCellFDD=.*,EUtranFreqRelation=39151, loadbalancing    2
set EUtranCellFDD=.*,EUtranFreqRelation=39151, lbBnrallowed True
set EUtranCellFDD=.*,EUtranFreqRelation=39348, loadbalancing    2
set EUtranCellFDD=.*,EUtranFreqRelation=39348, lbBnrallowed True
set EUtranCellFDD=.*,EUtranFreqRelation=39349, loadbalancing    2
set EUtranCellFDD=.*,EUtranFreqRelation=39349, lbBnrallowed True
set EUtranCellFDD=.*,EUtranFreqRelation=1526, loadbalancing    2
set EUtranCellFDD=.*,EUtranFreqRelation=1526, lbBnrallowed True
set EUtranCellFDD=.*,EUtranFreqRelation=365, loadbalancing    2
set EUtranCellFDD=.*,EUtranFreqRelation=365, lbBnrallowed True

# Accelerated IFLB activation
set  CXC4012349   featurestate  1
set LoadBalancingFunction=1 lbCycle 5
set LoadBalancingFunction=1 lbSubCycle 30


set PmEventService=1 cellTraceFileSize 30000

set RadioBearerTable=default,DataRadioBearer=1 tPollRetransmitUl 60
set CXC4012344 featurestate 0
set . ul256qamEnabled FALSE

set EutrancellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a1a2ThrRsrqQciOffset=-50
set EutrancellFDD=.*,EUtranFreqRelation=1526  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrqFreqQciOffset=-50,a5Thr2RsrqFreqQciOffset=0,lbQciProfileHandling=1

set EUtranCellFDD=UW_E_F1.*,GeranFreqGroupRelation=1 csFallbackPrio 4

set EUtranCellFDD=UW_E_F5.*,GeranFreqGroupRelation=1 csFallbackPrio 1




lt all
rbs
rbs
confbd+

set ENodeBFunction=1 dscpLabel 46
set ENodeBFunction=1 gtpuErrorIndicationDscp 46
set ENodeBFunction=1 interEnbCaTunnelDscp 26
set ENodeBFunction=1 interEnbUlCompTunnelDscp 26
set ENodeBFunction=1 s1GtpuEchoDscp 46
set ENodeBFunction=1 x2GtpuEchoDscp 46

cr Transport=1,QosProfiles=1,DscpPcpMap=1
set QciTable=default,QciProfilePredefined=qci1$ dscp 34
set QciTable=default,QciProfilePredefined=qci2$ dscp 34
set QciTable=default,QciProfilePredefined=qci3$ dscp 26
set QciTable=default,QciProfilePredefined=qci4$ dscp 26
set QciTable=default,QciProfilePredefined=qci5$ dscp 46
set QciTable=default,QciProfilePredefined=qci6$ dscp 32
set QciTable=default,QciProfilePredefined=qci7$ dscp 40
set QciTable=default,QciProfilePredefined=qci8$ dscp 30
set QciTable=default,QciProfilePredefined=qci9$ dscp 26
set SysM=1,OamTrafficClass=1 dscp 28
set SctpProfile= dscp 46
set Ntp=1,NtpFrequencySync= dscp 46

set QosProfiles=1,DscpPcpMap=1 pcp0
set QosProfiles=1,DscpPcpMap=1 pcp1
set QosProfiles=1,DscpPcpMap=1 pcp2
set QosProfiles=1,DscpPcpMap=1 pcp3
set QosProfiles=1,DscpPcpMap=1 pcp4
set QosProfiles=1,DscpPcpMap=1 pcp5
set QosProfiles=1,DscpPcpMap=1 pcp6
set QosProfiles=1,DscpPcpMap=1 pcp7

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp0 0,1,2,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,36,37,38,39,41,43,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp2 22,24,26
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp3 6,8,10,30,32
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp4 12,14,40
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp5 4,28
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp6 16,18,34,42,44
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp7 20,46
set SctpProfile=Node_Internal_F1  dscp 46
set SctpProfile=1 dscp 46
cr Router=.*,DnsClient=1
set Router=OAM,DnsClient=1 dscp 28

set . egressQosMarking QosProfiles=1,DscpPcpMap=1



set Transport=1,SctpProfile=1 alphaIndex 3
set Transport=1,SctpProfile=1 assocMaxRtx 8
set Transport=1,SctpProfile=1 betaIndex 2
set Transport=1,SctpProfile=1 bundlingActivated TRUE
set Transport=1,SctpProfile=1 bundlingAdaptiveActivated TRUE
set Transport=1,SctpProfile=1 bundlingTimer 0
set Transport=1,SctpProfile=1 cookieLife 60
set Transport=1,SctpProfile=1 dscp 46
set Transport=1,SctpProfile=1 hbMaxBurst 1
set Transport=1,SctpProfile=1 heartbeatActivated TRUE
set Transport=1,SctpProfile=1 heartbeatInterval 2000
set Transport=1,SctpProfile=1 incCookieLife 30
set Transport=1,SctpProfile=1 initARWnd 16384
set Transport=1,SctpProfile=1 maxRto 4000
set Transport=1,SctpProfile=1 initRto 2000
set Transport=1,SctpProfile=1 minRto 1000
set Transport=1,SctpProfile=1 initialHeartbeatInterval 500
set Transport=1,SctpProfile=1 maxActivateThr 65535
set Transport=1,SctpProfile=1 maxBurst 4
set Transport=1,SctpProfile=1 maxInStreams 2
set Transport=1,SctpProfile=1 maxInitRt 5
set Transport=1,SctpProfile=1 maxOutStreams 2
set Transport=1,SctpProfile=1 maxSctpPduSize 1480
set Transport=1,SctpProfile=1 maxShutdownRt 5
set Transport=1,SctpProfile=1 minActivateThr 1
set Transport=1,SctpProfile=1 noSwitchback TRUE
set Transport=1,SctpProfile=1 pathMaxRtx 4
set Transport=1,SctpProfile=1 primaryPathAvoidance TRUE
set Transport=1,SctpProfile=1 primaryPathMaxRtx 0
set Transport=1,SctpProfile=1 sackTimer 100
set Transport=1,SctpProfile=1 thrTransmitBuffer 48
set Transport=1,SctpProfile=1 thrTransmitBufferCongCeased 85
set Transport=1,SctpProfile=1 transmitBufferSize 64
set Transport=1,SctpProfile=1 userLabel SCTP


set Transport=1,SctpProfile=Node_Internal_F1 pathMaxRtx 4
set Transport=1,SctpProfile=Node_Internal_F1 assocMaxRtx 8
set Transport=1,SctpProfile=1 pathMaxRtx 4
set Transport=1,SctpProfile=1 assocMaxRtx 8


confbd-



confb-
confbd-
st cell


lt all

$date = `date +%y%m%d_%H%M`
cvms Post_GPL_LMS_L850_$date

confbd-



lt all
rbs
rbs
cvms pregpl
set ENodeBFunction=1   x2retryTimerMaxAuto 1440
lbl nrcell
set NRCellDU=.* advancedDlSuMimoEnabled true
set nrcelldu=.* csiRsActivePortConfig 2 4
set nrcelldu=.* csiRsPeriodicity 40
set CXC4012273 featurestate 1
set CXC4012547 featurestate 1
set CXC4012325 featurestate 1
set CXC4012549 featurestate 1
set CXC4012493 featurestate 1
set CXC4012406 featurestate 1
set CXC4012510 featurestate 1
set CXC4012375 featurestate 1
set CXC4012330 featurestate 1
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 dlMaxRetxThreshold 32
set GNBDUFunction=1,UeCC=1,RadioLinkControl=1,DrbRlc=Default,DrbRlcUeCfg=Base dlMaxRetxThreshold 32
set GNBDUFunction=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base drxEnabled        true
set IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base endcActionEvalFail 1
set IntraFreqMC=1,IntraFreqMCCellProfile=Default,IntraFreqMCCellProfileUeCfg=Base endcActionEvalFail 1
set nrcelldu=.* endcUlNrLowQualThresh 12
set nrcelldu=.* endcUlNrQualHyst 6
set GNBCUUPFunction=1    endcUlNrRetProhibTimer 1000
set nrcelldu=.* maxNoOfAdvancedDlMuMimoLayers 8
set nrcellcu=.* mcpcPSCellEnabled true
set NRCellDU=.* pMax 26
set GNBDUFunction=1,UeCC=1,Prescheduling=1,PreschedulingUeCfg=Base preschedulingUeMode 1
set NRCellDU=.* pZeroNomPucch -114
set NRCellDU=.* pZeroNomPuschGrant 1000
set NRCellDU=.* pZeroNomSrs -110
set NRCellDU=.* rachPreambleRecTargetPower -110
set NRCellDU=.* rachPreambleTransMax 20
set GNBCUCPFunction=1,AnrFunction=1    removeNrelTime    7
set IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base rsrpBetterSpCell hysteresis=10
set NRCellDU=.* secondaryCellOnly false
set NRCellDU=.* ssbGscn 7811
set GNBDUFunction=1,Rrc=1 t304 2000
set GNBDUFunction=1,Rrc=1    t310   2000
set GNBDUFunction=1,Rrc=1    t311   3000
set GNBCUCPFunction=1,UeCC=1,InactivityProfile=Default,InactivityProfileUeCfg=Base tInactivityTimerEndcSn 5
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 tPollRetransmitDl 80
set GNBDUFunction=1,UeCC=1,RadioLinkControl=1,DrbRlc=Default,DrbRlcUeCfg=Base tPollRetransmitDl 80
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 tPollRetransmitUl 80
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 tPollRetransmitUl 80
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 ulMaxRetxThreshold 32
set GNBDUFunction=1,UeCC=1,RadioLinkControl=1,DrbRlc=Default,DrbRlcUeCfg=Base ulMaxRetxThreshold 32
set Mcpc=1,McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base rsrpCritical threshold=-118
set Mcpc=1,McpcPSCellProfile=Default_copy,McpcPSCellProfileUeCfg=Base rsrpCritical threshold=-118
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB1GUtra=1 timeToTriggerB1 480
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB1GUtra=1 b1ThresholdRsrp -113
set nrcelldu=.* cellrange 15000
set EUtranCellFDD=.*F3.*                      primaryUpperLayerInd 1
set EUtranCellFDD=.*F1.*                      primaryUpperLayerInd 1
set EUtranCellFDD=.*F8.*                      primaryUpperLayerInd 0
set EUtranCellTDD=.*T.*                      primaryUpperLayerInd 1
set EUtranCellFDD=.*F3.*                      additionalUpperLayerIndList 1 1 1 1 1
set EUtranCellFDD=.*F1.*                      additionalUpperLayerIndList 1 1 1 1 1
set EUtranCellFDD=.*F1.*                      additionalUpperLayerIndList 0 0 0 0 0
set EUtranCellTDD=.*T.*                      additionalUpperLayerIndList 1 1 1 1 1 
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB1GUtra=1 b1ThresholdRsrp   -110
set UePolicyOptimization=1                                  endcAwareImc      2
set EUtranCell.*=.*                      endcSetupDlPktVolThr 5
set EUtranCell.*=.*,UeMeasControl=1      endcMeasRestartTime 10000
set ENodeBFunction=1,AnrFunction=1,AnrFunctionGeran=1       anrStateGsm       1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          anrStateNR        1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1       anrStateUtran     0

deb nrcell
st cell
cvms postgpl
end

"""


UPW_TN_RN_GPS_MME_SCRIPT = """
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

set Transport=1,EthernetPort= egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1
set Transport=1,Router=.*,InterfaceIPv4= egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1
set Transport=1,VlanPort= egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=TWAMP                                                                                                     
dst 0.0.0.0/0                                                                                                                                               
end                                                                                                                                                               

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=TWAMP,NextHop=1                                                                                           
address {LTE_UP_GW}                                                                                                                                               
adminDistance 1                                                                                                                                                   
bfdMonitoring true                                                                                                                                              
discard false                                                                                                                                                     
reference                                                                                                                                                         
end

crn Transport=1,Router=LTEUP,TwampResponder=1
ipAddress Transport=1,Router=LTEUP,InterfaceIPv4={tnPortId}_UP,AddressIPv4={tnPortId}_UP
udpPort 4001
userLabel TWAMP1
end
#END Transport=1,Router=LTEUP,TwampResponder=1 --------------------


crn Transport=1,SctpProfile=1
alphaIndex 3
assocMaxRtx 20
betaIndex 2
bundlingActivated true
bundlingTimer 10
cookieLife 60
dscp 46
hbMaxBurst 1
heartbeatInterval 5000
incCookieLife 30
initARWnd 16384
initialHeartbeatInterval 500
initRto 2000
maxActivateThr 65535
maxBurst 4
maxInitRt 8
maxInStreams 2
maxOutStreams 2
maxRto 4000
maxSctpPduSize 1480
maxShutdownRt 5
minActivateThr 1
minRto 1000
pathMaxRtx 4
primaryPathMaxRtx 0
sackTimer 10
transmitBufferSize 64
userLabel SCTP
end

#END Transport=1,SctpProfile=1 --------------------

crn Transport=1,SctpEndpoint=1
localIpAddress Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP
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
encapsulation Equipment=1,FieldReplaceableUnit=4,SyncPort=1
end
#END Transport=1,Synchronization=1,TimeSyncIO=1 --------------------

crn Transport=1,Synchronization=1,RadioEquipmentClock=1,RadioEquipmentClockReference=1
adminQualityLevel qualityLevelValueOptionI=2,qualityLevelValueOptionII=2,qualityLevelValueOptionIII=1
administrativeState 1
encapsulation Transport=1,Synchronization=1,TimeSyncIO=1
priority 1
end
#END Transport=1,Synchronization=1,RadioEquipmentClock=1,RadioEquipmentClockReference=1 --------------------

crn Transport=1,Synchronization=1,RadioEquipmentClock=1,RadioEquipmentClockReference=2
adminQualityLevel qualityLevelValueOptionI=2,qualityLevelValueOptionII=2,qualityLevelValueOptionIII=1
administrativeState 1
encapsulation Transport=1,Ntp=1,NtpFrequencySync=NTP1
priority 2
end
#END Transport=1,Synchronization=1,RadioEquipmentClock=1,RadioEquipmentClockReference=2 --------------------

crn Transport=1,Synchronization=1,RadioEquipmentClock=1,RadioEquipmentClockReference=3
adminQualityLevel qualityLevelValueOptionI=2,qualityLevelValueOptionII=2,qualityLevelValueOptionIII=1
administrativeState 1
encapsulation Transport=1,Ntp=1,NtpFrequencySync=NTP2
priority 3
end


crn ENodeBFunction=1
eNodeBPlmnId mcc=404,mnc=97,mncLength=2
eNBId {eNBId}
sctpRef Transport=1,SctpEndpoint=1
timeAndPhaseSynchAlignment true
upIpAddressRef Transport=1,Router=LTEUP,InterfaceIPv4={tnPortId}_UP,AddressIPv4={tnPortId}_UP
x2GtpuEchoDscp 14
end
#END ENodeBFunction=1 --------------------

ld ENodeBFunction=1,Paging=1 #SystemCreated
lset ENodeBFunction=1,Paging=1$ maxNoOfPagingRecords 7

ld ENodeBFunction=1,AdmissionControl=1 #SystemCreated
lset ENodeBFunction=1,AdmissionControl=1$ dlAdmDifferentiationThr 750
lset ENodeBFunction=1,AdmissionControl=1$ ulAdmDifferentiationThr 750

ld ENodeBFunction=1,AnrFunction=1 #SystemCreated
lset ENodeBFunction=1,AnrFunction=1$ maxNoPciReportsEvent 30
lset ENodeBFunction=1,AnrFunction=1$ maxTimeEventBasedPciConf 30
lset ENodeBFunction=1,AnrFunction=1$ removeNrelTime 7

ld ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 #SystemCreated
lset ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1$ anrInterFreqState 1
lset ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1$ anrIntraFreqState 1
lset ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1$ anrUesEUtraIntraFMax 0
lset ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1$ anrUesEUtraIntraFMin 0
lset ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1$ anrUesThreshInterFMax 0
lset ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1$ anrUesThreshInterFMin 0
lset ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1$ cellAddRsrpThresholdEutran -1150

ld ENodeBFunction=1,AnrFunction=1,AnrFunctionGeran=1 #SystemCreated
lset ENodeBFunction=1,AnrFunction=1,AnrFunctionGeran=1$ anrStateGsm 1

ld ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1 #SystemCreated
lset ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1$ anrStateUtran 1
lset ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1$ cellAddEcNoThresholdUtranDelta 0
lset ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1$ cellAddRscpThresholdUtranDelta 0

ld ENodeBFunction=1,DrxProfile=1 #SystemCreated
lset ENodeBFunction=1,DrxProfile=1$ drxInactivityTimer 3
lset ENodeBFunction=1,DrxProfile=1$ drxRetransmissionTimer 2
lset ENodeBFunction=1,DrxProfile=1$ longDrxCycle 3
lset ENodeBFunction=1,DrxProfile=1$ longDrxCycleOnly 3
lset ENodeBFunction=1,DrxProfile=1$ onDurationTimer 6
lset ENodeBFunction=1,DrxProfile=1$ shortDrxCycle 7
lset ENodeBFunction=1,DrxProfile=1$ shortDrxCycleTimer 0

ld ENodeBFunction=1,DrxProfile=2 #SystemCreated
lset ENodeBFunction=1,DrxProfile=2$ drxInactivityTimer 6
lset ENodeBFunction=1,DrxProfile=2$ drxRetransmissionTimer 1
lset ENodeBFunction=1,DrxProfile=2$ longDrxCycle 3
lset ENodeBFunction=1,DrxProfile=2$ longDrxCycleOnly 3
lset ENodeBFunction=1,DrxProfile=2$ onDurationTimer 2
lset ENodeBFunction=1,DrxProfile=2$ shortDrxCycle 7
lset ENodeBFunction=1,DrxProfile=2$ shortDrxCycleTimer 0

ld ENodeBFunction=1,DrxProfile=0 #SystemCreated
lset ENodeBFunction=1,DrxProfile=0$ drxInactivityTimer 14
lset ENodeBFunction=1,DrxProfile=0$ drxRetransmissionTimer 4
lset ENodeBFunction=1,DrxProfile=0$ longDrxCycle 9
lset ENodeBFunction=1,DrxProfile=0$ longDrxCycleOnly 3
lset ENodeBFunction=1,DrxProfile=0$ onDurationTimer 7
lset ENodeBFunction=1,DrxProfile=0$ shortDrxCycle 9
lset ENodeBFunction=1,DrxProfile=0$ shortDrxCycleTimer 1

lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ dataFwdPerQciEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ dscp 34
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ schedulingAlgorithm 0

lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ dataFwdPerQciEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ dscp 34
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ schedulingAlgorithm 0

lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ dataFwdPerQciEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ dscp 26
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ schedulingAlgorithm 0

lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ dataFwdPerQciEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ dscp 26
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ schedulingAlgorithm 0

lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ dataFwdPerQciEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ dscp 46
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ schedulingAlgorithm 0

lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ dataFwdPerQciEnabled true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ dscp 26
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ schedulingAlgorithm 0


lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ dataFwdPerQciEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ dscp 26
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ schedulingAlgorithm 0


lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ dataFwdPerQciEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ dscp 26
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ schedulingAlgorithm 0


lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ dataFwdPerQciEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ dscp 26
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ schedulingAlgorithm 0

lset ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1$ dlMaxRetxThreshold 16
lset ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1$ ulMaxRetxThreshold 16

ld ENodeBFunction=1,Rcs=1 #SystemCreated
lset ENodeBFunction=1,Rcs=1$ tInactivityTimer 10

ld ENodeBFunction=1,Rrc=1 #SystemCreated
lset ENodeBFunction=1,Rrc=1$ t300 2000
lset ENodeBFunction=1,Rrc=1$ t301 1000
lset ENodeBFunction=1,Rrc=1$ t311 3000


crn ENodeBFunction=1,GeraNetwork=1
end
#END ENodeBFunction=1,GeraNetwork=1 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
frequencyGroupId 1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1 --------------------

crn ENodeBFunction=1,EUtraNetwork=1
end

set 0 Userlabel {Phy_SiteID_Userlabel}

confb-
gs-


##########################
## TermPointToMme ##
##########################


crn ENodeBFunction=1,TermPointToMme=MME2
ipAddress1 10.50.188.57
ipAddress2 0.0.0.0
administrativeState 1
ipv6Address1 ::
ipv6Address2 ::
mmeSupportLegacyLte true
mmeSupportNbIoT false
end

crn ENodeBFunction=1,TermPointToMme=MME3
ipAddress1 10.75.212.72
ipAddress2 0.0.0.0
administrativeState 1
ipv6Address1 ::
ipv6Address2 ::
mmeSupportLegacyLte true
mmeSupportNbIoT false
end


crn ENodeBFunction=1,TermPointToMme=MME4
ipAddress1 10.92.7.42
ipAddress2 0.0.0.0
administrativeState 1
ipv6Address1 ::
ipv6Address2 ::
mmeSupportLegacyLte true
mmeSupportNbIoT false
end


crn ENodeBFunction=1,TermPointToMme=MME5
ipAddress1 10.1.161.82
ipAddress2 0.0.0.0
administrativeState 1
ipv6Address1 ::
ipv6Address2 ::
mmeSupportLegacyLte true
mmeSupportNbIoT false
end



crn ENodeBFunction=1,TermPointToMme=MME6
ipAddress1 10.1.161.98
ipAddress2 0.0.0.0
administrativeState 1
ipv6Address1 ::
ipv6Address2 ::
mmeSupportLegacyLte true
mmeSupportNbIoT false
end


"""


################################################################################### 5G SCRIPS FOR INTEGRATION SCRIPTS ###################################################################################
UPW_5G_Cell_creation_Sctp_Endpoint_Creation = """
######################################################## IPV6 Interface for NR ####################################################################

cr Transport=1,Router=LTEUP,InterfaceIPv6=NR
VlanPort=TN_E_UP
false

crn Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
address {NR_IP}
configurationMode 0
duidType 0
primaryAddress true
userLabel
end


crn Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2
address {NR_ENDC_IP}
configurationMode 0
duidType 0
primaryAddress false
userLabel
end

gs+

crn Transport=1,Router=LTEUP,RouteTableIPv6Static=2                                                                                                              
end

crn Transport=1,Router=LTEUP,RouteTableIPv6Static=2,Dst=default                                                                                                   
dst ::/0                                                                                                                                                          
end



crn Transport=1,Router=LTEUP,RouteTableIPv6Static=2,Dst=default,NextHop=1
address {NR_GW}
adminDistance 1
bfdMonitoring true
discard false
reference
end


##################################################################################### TN SCRIPT #########################################################################

crn Transport=1,QosProfiles=1,DscpPcpMap=1
defaultPcp 0
pcp0 0 1 2 3 5 7 9 11 13 15 17 19 21 23 25 27 29 31 33 35 36 37 38 39 41 43 45 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
pcp1
pcp2 22 24 26
pcp3 6 8 10 30 32
pcp4 12 14 40
pcp5 4 28
pcp6 16 18 34 42 44
pcp7 20 46
userLabel Traffic
end


crn Transport=1,Router=LTEUP,TwampResponder=2
ipAddress Router=LTEUP,InterfaceIPv4={tnPortId}_UP,AddressIPv4={tnPortId}_UP
udpPort 4001
userLabel
end

crn Transport=1,Router=LTEUP,TwampResponder=3
ipAddress Router=LTEUP,InterfaceIPv4={tnPortId}_UP,AddressIPv4={tnPortId}_UP
udpPort 4002
userLabel
end

crn Transport=1,Router=LTEUP,TwampResponder=NR
ipAddress Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
udpPort 4001
userLabel
end

crn Transport=1,SctpProfile=1
alphaIndex 3
assocMaxRtx 8
betaIndex 2
bundlingActivated true
bundlingTimer 0
cookieLife 60
dscp 46
hbMaxBurst 1
heartbeatInterval 5000
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
pathMaxRtx 4
primaryPathMaxRtx 0
sackTimer 100
transmitBufferSize 64
userLabel SCTP
end

crn Transport=1,SctpEndpoint=1
localIpAddress Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP
portNumber 36422
sctpProfile Transport=1,SctpProfile=1
end

crn Transport=1,SctpEndpoint=X2_ENDC
localIpAddress Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2
portNumber 36422
sctpProfile Transport=1,SctpProfile=1
end

##########

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
end

cr Transport=1,Router=Node_Internal_F1

crn Transport=1,Router=Node_Internal_F1,InterfaceIPv4=NR_CUCP
aclEgress
aclIngress
arpTimeout 300
bfdProfile
bfdStaticRoutes 0
egressQosMarking
encapsulation
ingressQosMarking
ipOptionsDisabled false
loopback true
mtu 1500
pcpArp 6
routesHoldDownTimer
routingPolicyIngress
trackedInterface
userLabel
end

crn Transport=1,Router=Node_Internal_F1,InterfaceIPv4=NR_CUCP,AddressIPv4=1
address 10.0.0.1/32
configurationMode 0
dhcpClientIdentifier
dhcpClientIdentifierType 0
primaryAddress true
userLabel
end
gs-

crn Transport=1,SctpEndpoint=F1_NRCUCP
localIpAddress Transport=1,Router=Node_Internal_F1,InterfaceIPv4=NR_CUCP,AddressIPv4=1
portNumber 38472
sctpProfile Transport=1,SctpProfile=Node_Internal_F1
end

############

crn Transport=1,Router=Node_Internal_F1,InterfaceIPv4=NR_DU
aclEgress
aclIngress
arpTimeout 300
bfdProfile
bfdStaticRoutes 0
egressQosMarking
encapsulation
ingressQosMarking
ipOptionsDisabled false
loopback true
mtu 1500
pcpArp 6
routesHoldDownTimer
routingPolicyIngress
trackedInterface
userLabel
end

crn Transport=1,Router=Node_Internal_F1,InterfaceIPv4=NR_DU,AddressIPv4=1
address 10.0.0.2/32
configurationMode 0
dhcpClientIdentifier
dhcpClientIdentifierType 0
primaryAddress true
userLabel
end
gs-

crn Transport=1,SctpEndpoint=F1_NRDU
localIpAddress Transport=1,Router=Node_Internal_F1,InterfaceIPv4=NR_DU,AddressIPv4=1
portNumber 38472
sctpProfile Transport=1,SctpProfile=Node_Internal_F1
end

###########

crn Transport=1,SctpEndpoint=NG
localIpAddress Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
portNumber 38412
sctpProfile Transport=1,SctpProfile=1
end

crn Transport=1,SctpEndpoint=X2
localIpAddress Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
portNumber 36422
sctpProfile Transport=1,SctpProfile=1
end

crn Transport=1,SctpEndpoint=F1
dtls
dtlsNodeCredential
dtlsSctpSecurityMode 0
dtlsTrustCategory
localIpAddress Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
portNumber 38472
sctpProfile SctpProfile=1
userLabel
end


###########################################GNBCUUPFunction=1#############################################################################

crn GNBCUUPFunction=1
gNBId {gNBId}
gNBIdLength 26
pLMNIdList mcc=404,mnc=97
sNSSAIList
userLabel
end

crn GNBCUUPFunction=1,EndpointResource=1
end

crn GNBCUUPFunction=1,EndpointResource=1,LocalIpEndpoint=1
addressRef Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
interfaceList 4 5 7 6
end


ld GNBCUUPFunction=1
lset GNBCUUPFunction=1$ endpointResourceRef GNBCUUPFunction=1,EndpointResource=1



crn GNBCUUPFunction=1,CardinalityLimits=1
maxNgUPath 600
maxS1UPath 600
end

crn GNBCUUPFunction=1,GtpuSupervision=1
gtpuErrorIndDscp 40
end

crn GNBCUUPFunction=1,GtpuSupervision=1,GtpuSupervisionProfile=S1
endpointResourceRef
gtpuEchoDscp 32
gtpuEchoEnabled true
interfaceList 5
userLabel
end

crn GNBCUUPFunction=1,GtpuSupervision=1,GtpuSupervisionProfile=X2
endpointResourceRef
gtpuEchoDscp 32
gtpuEchoEnabled true
interfaceList 7
userLabel
end


####################################GNBDUFunction=1###################################

crn GNBDUFunction=1
gNBDUId 1
gNBDUName
gNBId {gNBId}
gNBIdLength 26
end

crn GNBDUFunction=1,EndpointResource=1
end

crn GNBDUFunction=1,EndpointResource=1,LocalSctpEndpoint=1
interfaceUsed 3
sctpEndpointRef Transport=1,SctpEndpoint=F1_NRDU
end

crn GNBDUFunction=1,TermPointToGNBCUCP=1
administrativeState 1
ipv4Address 10.0.0.1
ipv6Address ::
end

ld GNBDUFunction=1
lset GNBDUFunction=1$ endpointResourceRef GNBDUFunction=1,EndpointResource=1


crn GNBDUFunction=1,MassiveMimoSleep=1                                                                                                                                                                             
end 

crn GNBDUFunction=1,MassiveMimoSleep=1,MMimoSleepProfile=1                                                                                                                                                         
sleepMode 0                                                                                                                                                                                                        
switchDownMonitorDurTimer 60                                                                                                                                                                                       
switchDownMonitorDurTimerEco 300                                                                                                                                                                                   
switchDownPrbThreshDl 10                                                                                                                                                                                           
switchDownPrbThreshDlEco 15                                                                                                                                                                                        
switchDownPrbThreshUlEco 10                                                                                                                                                                                        
switchDownRrcConnThresh 10                                                                                                                                                                                         
switchDownRrcConnThreshEco 30                                                                                                                                                                                      
switchUpMonitorDurTimer 30                                                                                                                                                                                         
switchUpMonitorDurTimerEco 120                                                                                                                                                                                     
switchUpPrbThreshDl 20                                                                                                                                                                                             
switchUpPrbThreshDlEco 30                                                                                                                                                                                          
switchUpPrbThreshUlEco 15                                                                                                                                                                                          
switchUpRrcConnThresh 20                                                                                                                                                                                           
switchUpRrcConnThreshEco 50                                                                                                                                                                                        
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBDUFunction=1,MassiveMimoSleep=1,MMimoSleepTimeGroup=1                                                                                                                                                       
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBDUFunction=1,MassiveMimoSleep=1,MMimoSleepTimeGroup=1,MMimoSleepTimeWindow=1                                                                                                                                
dayOfWeek 0                                                                                                                                                                                                        
mMimoSleepProfileRef MassiveMimoSleep=1,MMimoSleepProfile=1                                                                                                                                                        
startTime 20:30                                                                                                                                                                                                    
stopTime 23:30                                                                                                                                                                                                     
end    


{UPW_CGSWITCH_SCRIPT}

############################GNBCUCPFunction=1####################################################


crn GNBCUCPFunction=1
gNBId {gNBId}
gNBIdLength 26
pLMNId mcc=404,mnc=97
end

crn GNBCUCPFunction=1,EndpointResource=1
end

ld GNBCUCPFunction=1
lset GNBCUCPFunction=1$ endpointResourceRef GNBCUCPFunction=1,EndpointResource=1

crn GNBCUCPFunction=1,EndpointResource=1,LocalSctpEndpoint=1
interfaceUsed 4
sctpEndpointRef SctpEndpoint=NG
end

crn GNBCUCPFunction=1,EndpointResource=1,LocalSctpEndpoint=2
interfaceUsed 7
sctpEndpointRef SctpEndpoint=X2
end

crn GNBCUCPFunction=1,EndpointResource=1,LocalSctpEndpoint=3
interfaceUsed 3
sctpEndpointRef SctpEndpoint=F1_NRCUCP
end

                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,AnrFunction=1                                                                                                                                                                                
demoteCellRelMobAttThresh                                                                                                                                                                                          
promoteCellRelMobAttThresh                                                                                                                                                                                         
removeEUtranFreqRelTime 10000                                                                                                                                                                                      
removeEnbTime 7                                                                                                                                                                                                    
removeFreqRelTime 15                                                                                                                                                                                               
removeGnbTime 7                                                                                                                                                                                                    
removeNrelTime 7                                                                                                                                                                                                   
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,AnrFunction=1,AnrFunctionNR=1                                                                                                                                                                
anrAutoCreateXnForEndc false                                                                                                                                                                                       
anrCgiMeasInterFreqMode 0                                                                                                                                                                                          
anrCgiMeasIntraFreqEnabled true                                                                                                                                                                                    
anrEndcX2Enabled true                                                                                                                                                                                              
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,AnrFunction=1,AnrFunctionNR=1,AnrFunctionNRUeCfg=Base                                                                                                                                        
anrRsrpThreshold -156                                                                                                                                                                                              
anrRsrqThreshold -435                                                                                                                                                                                              
anrSinrThreshold -230                                                                                                                                                                                              
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   

crn GNBCUCPFunction=1,CarrierAggregation=1                                                                                                                                                                         
end                                                                                                                                                                                                                
                                       
crn GNBCUCPFunction=1,CarrierAggregation=1,CaCellMeasProfile=1                                                                                                                                                     
ueConfGroupType 0                                                                                                                                                                                                  
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,CarrierAggregation=1,CaCellMeasProfile=1,CaCellMeasProfileUeCfg=Base                                                                                                                         
betterSCellReportConfigMode 0                                                                                                                                                                                      
prefUeGroupList                                                                                                                                                                                                    
rsrpBetterSCell hysteresis=10,offset=30,timeToTrigger=160                                                                                                                                                          
rsrpSCellCoverage hysteresis=10,threshold=-117,timeToTrigger=160,timeToTriggerA1=-1                                                                                                                                
rsrqSCellCoverage hysteresis=10,threshold=-435,timeToTrigger=160,timeToTriggerA1=-1                                                                                                                                
sCellCoverageTriggerQuantity 0                                                                                                                                                                                     
ueConfGroupList                                                                                                                                                                                                    
ueGroupList                                                                                                                                                                                                        
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                            

crn GNBCUCPFunction=1,IntraFreqMC=1                                                                                                                                                                                
sCellDepHEnabled true                                                                                                                                                                                              
end                                                                                                                                                                                                                
                                                   
crn GNBCUCPFunction=1,IntraFreqMC=1,IntraFreqMCCellProfile=1                                                                                                                                                       
ueConfGroupType 0                                                                                                                                                                                                  
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base                                                                                                                      
betterSpCellTriggerQuantity 0                                                                                                                                                                                      
endcActionEvalFail 1                                                                                                                                                                                               
prefUeGroupList                                                                                                                                                                                                    
rsrpBetterSpCell hysteresis=10,offset=30,timeToTrigger=640                                                                                                                                                         
rsrqBetterSpCell hysteresis=10,offset=30,timeToTrigger=640                                                                                                                                                         
sinrBetterSpCell hysteresis=10,offset=30,timeToTrigger=640                                                                                                                                                         
ueConfGroupList                                                                                                                                                                                                    
ueGroupList                                                                                                                                                                                                        
useT312BetterPCellCandidateA3 false                                                                                                                                                                                
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                


crn GNBCUCPFunction=1,NRNetwork=1
end

crn GNBCUCPFunction=1,NRNetwork=1,NRFrequency=629952-30
arfcnValueNRDl 629952
bandListManual
smtcDuration 1
smtcOffset 0
smtcPeriodicity 20
smtcScs 30
ssRssiMeasIdle
ssbToMeasureIdle
end

crn GNBCUCPFunction=1,NRNetwork=1,NRFrequency=629952-30,NRFrequencyUeCfg=Base
prefUeGroupList
ssRssiMeasConnected
ssbToMeasureConnected
ueConfGroupList
ueGroupList
userLabel
end

crn GNBCUCPFunction=1,UeGroupSelection=1                                                                                                                                                                           
validityTimeEmergencyCause 6                                                                                                                                                                                       
validityTimeHighPrioAccCause 6                                                                                                                                                                                     
validityTimeMcsPrioAccCause 6                                                                                                                                                                                      
validityTimeMoDataCause 6                                                                                                                                                                                          
validityTimeMoSignallingCause 6                                                                                                                                                                                    
validityTimeMoSmsCause 6                                                                                                                                                                                           
validityTimeMoVideoCallCause 6                                                                                                                                                                                     
validityTimeMoVoiceCallCause 6                                                                                                                                                                                     
validityTimeMpsPrioAccCause 6                                                                                                                                                                                      
validityTimeMtAccessCause 6                                                                                                                                                                                        
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,UeGroupSelection=1,ImeiSvGroups=1                                                                                                                                                            
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,UeGroupSelection=1,PrefUeGroupSelectionProfile=QCI6                                                                                                                                          
chipsetRef                                                                                                                                                                                                         
imeiSvRef                                                                                                                                                                                                          
prefUeGroupId 6                                                                                                                                                                                                    
prefUeGroupPriority 65534                                                                                                                                                                                          
selectionCriteria qci==6                                                                                                                                                                                           
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,UeGroupSelection=1,PrefUeGroupSelectionProfile=QCI7                                                                                                                                          
chipsetRef                                                                                                                                                                                                         
imeiSvRef                                                                                                                                                                                                          
prefUeGroupId 7                                                                                                                                                                                                    
prefUeGroupPriority 1000                                                                                                                                                                                           
selectionCriteria qci==7                                                                                                                                                                                           
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,UeGroupSelection=1,UeGroupSelectionProfile=QCI6                                                                                                                                              
chipsetRef                                                                                                                                                                                                         
imeiSvRef                                                                                                                                                                                                          
selectionCriteria qci==6                                                                                                                                                                                           
selectionProbability 100                                                                                                                                                                                           
ueGroupId 6                                                                                                                                                                                                        
ueGroupPriority 65534                                                                                                                                                                                              
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,UeGroupSelection=1,UeGroupSelectionProfile=QCI7                                                                                                                                              
chipsetRef                                                                                                                                                                                                         
imeiSvRef                                                                                                                                                                                                          
selectionCriteria qci==7                                                                                                                                                                                           
selectionProbability 100                                                                                                                                                                                           
ueGroupId 7                                                                                                                                                                                                        
ueGroupPriority 1000                                                                                                                                                                                               
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,UeGroupSelection=1,UeMobilityGroupDefinition=QCI6                                                                                                                                            
chipsetRef                                                                                                                                                                                                         
imeiSvRef                                                                                                                                                                                                          
selectionCriteria qci==6                                                                                                                                                                                           
ueMobilityGroupId 6                                                                                                                                                                                                
ueMobilityGroupPriority 65534                                                                                                                                                                                      
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,UeGroupSelection=1,UeMobilityGroupDefinition=QCI7                                                                                                                                            
chipsetRef                                                                                                                                                                                                         
imeiSvRef                                                                                                                                                                                                          
selectionCriteria qci==7                                                                                                                                                                                           
ueMobilityGroupId 7                                                                                                                                                                                                
ueMobilityGroupPriority 1000                                                                                                                                                                                       
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,UeGroupSelection=1,UeServiceGroupDefinition=QCI6                                                                                                                                             
chipsetRef                                                                                                                                                                                                         
imeiSvRef                                                                                                                                                                                                          
selectionCriteria qci==6                                                                                                                                                                                           
ueServiceGroupId 6                                                                                                                                                                                                 
ueServiceGroupPriority 65534                                                                                                                                                                                       
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,UeGroupSelection=1,UeServiceGroupDefinition=QCI7                                                                                                                                             
chipsetRef                                                                                                                                                                                                         
imeiSvRef                                                                                                                                                                                                          
selectionCriteria qci==7                                                                                                                                                                                           
ueServiceGroupId 7                                                                                                                                                                                                 
ueServiceGroupPriority 1000                                                                                                                                                                                        
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                

{UPW_GNBCUCPFunction}

crn GNBCUCPFunction=1,EUtraNetwork=1
userLabel
end
crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=1511
arfcnValueEUtranDl 1511
userLabel
end
crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=1526
arfcnValueEUtranDl 1526
userLabel
end
crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=240
arfcnValueEUtranDl 240
userLabel
end
crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=265
arfcnValueEUtranDl 265
userLabel
end
crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=3663
arfcnValueEUtranDl 3663
userLabel
end
crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=39150
arfcnValueEUtranDl 39150
userLabel
end
crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=39294
arfcnValueEUtranDl 39294
userLabel
end
crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=39348
arfcnValueEUtranDl 39348
userLabel
end

{UPW_GNBDUFunction}

"""

UPW_Termpoint_GUtranFreqRelation_script = """



###########################Termpoint & FreqRelation################################



cvms bfranchor

#####1. Transport=1,Router=LTEUP,InterfaceIPv6=NR--Change TN Port as per configured in BBU

get Router=LTEUP,InterfaceIPv4=TN_._UP                      encapsulation  > $encapsulation

$reqipX2 = readinput( ipv6 IP for X2 ENDC )
$reqhopadd = readinput( ipv6 nexthop )

get Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR usedAddress > $reqipNR                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
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


#####2. Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2/NR ---- Change IP address as per planning


crn Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2
address $reqipX2 ###need to change ENDC IP according to plan in AD column###
configurationMode 0
duidType 0
primaryAddress true
userLabel
end	
gs-

#######3. Transport=1,Router=LTEUP,RouteTableIPv6Static=1,Dst=default,NextHop=1/NR--Change Nexthop address as per planning

gs+

crn Transport=1,Router=LTEUP,RouteTableIPv6Static=1                                                                                                               
end

crn Transport=1,Router=LTEUP,RouteTableIPv6Static=1,Dst=default                                                                                                   
dst ::/0                                                                                                                                                          
end


crn Transport=1,Router=LTEUP,RouteTableIPv6Static=1,Dst=default,NextHop=1
address $reqhopadd ###need to change ENDC gateway according to plan in AA column###
adminDistance 1
bfdMonitoring true
discard false
reference
end
gs-

#########4. Transport=1,SctpEndpoint=X2_ENDC/NR 


gs+

crn Transport=1,SctpEndpoint=X2_ENDC
dtls
dtlsNodeCredential
dtlsSctpSecurityMode 0
dtlsTrustCategory
localIpAddress Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2
portNumber 36422
sctpProfile SctpProfile=1
userLabel
end

set ENodeBFunction=1$  endcAllowed  true                                                                                                                 
set ENodeBFunction=1$  sctpEndcX2Ref Transport=1,SctpEndpoint=X2_ENDC                                                                                        
set ENodeBFunction=1$  upEndcX2IpAddressRef Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2                                                                     
set ENodeBFunction=1$  intraRanIpAddressRef Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2                                                                  
set ^EUtranCell.DD= endcAllowedPlmnList mcc=404,mnc=97,mnclength=2                                                                                                

crn ENodeBFunction=1,EndcProfile=1                                                                                                                                
end

set ENodeBFunction=1,EndcProfile=1 meNbS1TermReqArpLev 0                                                                                                          
set ENodeBFunction=1,EndcProfile=1 splitNotAllowedUeArpLev 0 
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci[6789]$ endcProfileRef ENodeBFunction=1,EndcProfile=1

cr ENodeBFunction=1,UePolicyOptimization=1                                                                                                                        
set ENodeBFunction=1,UePolicyOptimization=1 ueCapPrioList 0                                                                                                       
set ENodeBFunction=1,UePolicyOptimization=1 coverageAwareImc true                                                                                                 
set ENodeBFunction=1  endcX2IpAddrViaS1Active  true
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR= gNodebIdLength 26                                                                                               
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1 anrStateNR 1 



################*Parameter Setting Required:

set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1  anrStateNR        1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1  anrFunctionNRId   1
set ENodeBFunction=1$   endcAllowed       true
set ENodeBFunction=1$  intraRanIpAddressRef Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2
set ENodeBFunction=1$  upEndcX2IpAddressRef Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2

set  CXC4012095   featureState 1
set  CXC4012504   featurestate 1
set  CXC4012381   featurestate 1
set  CXC4012385   featurestate 1 
set  CXC4040006   featurestate 1                                                                                                                                   

set EUtranCellFDD=UW_.*,EUtranFreqRelation=240 endcHoFreqPriority 6
set EUtranCellFDD=UW_.*,EUtranFreqRelation=1511 endcHoFreqPriority 7
set EUtranCellFDD=UW_.*,EUtranFreqRelation=3663 endcAwareIdleModePriority 3
set EUtranCellTDD=UW_.*,EUtranFreqRelation=39150 endcAwareIdleModePriority 5
set EUtranCellTDD=UW_.*,EUtranFreqRelation=39151 endcAwareIdleModePriority 7
set EUtranCellTDD=UW_.*,EUtranFreqRelation=39348 endcAwareIdleModePriority 5
set EUtranCellTDD=UW_.*,EUtranFreqRelation=39349 endcAwareIdleModePriority 7             

get Router=*.*,RouteTableIPv6Static=.*,Dst=default,NextHop= address > $gwip                                                                                          
mcc Router=*.*,InterfaceIPv6=NR,AddressIPv6=X2 ping6 $gwip -c 4



#############################################5. ENodeBFunction=1,GUtraNetwork=1###########################################

gs+

cr ENodeBFunction=1,GUtraNetwork=1


#############################################6. ENodeBFunction=1,GUtraNetwork=1###########################################

gs+                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
crn ENodeBFunction=1,GUtraNetwork=1,ExternalGNodeBFunction=40497-$gnbid                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
dirDataPathAvail true                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
eNBVlanPortRef                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
gNodeBId $gnbid                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
gNodeBIdLength 26                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
gNodeBPlmnId mcc=404,mnc=97,mncLength=2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
userLabel                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
end   

crn ENodeBFunction=1,GUtraNetwork=1,ExternalGNodeBFunction=40497-$gnbid,TermPointToGNB=40497-$gnbid                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
additionalCnRef                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
administrativeState 1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
domainName                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
ipAddress 0.0.0.0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
ipAddress2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
ipsecEpAddress ::                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
ipv6Address $reqipNR                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
ipv6Address2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
upIpAddress ::                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
end    

########################7. ENodeBFunction=1,GUtraNetwork=1,GUtranSyncSignalFrequency=######################################

crn ENodeBFunction=1,GUtraNetwork=1,GUtranSyncSignalFrequency=627936-30
arfcn 627936
smtcScs 30
userLabel
end
gs-



lt all


get GNBDUFunction=1,NRCellDU= celllocalid > $CLID

mr CWA_CRP_2
ma CWA_CRP_2 EUtranCell.DD=.*,EUtranFreqRelation= cellReselectionPriority 2
lpr CWA_CRP_2

set CWA_CRP_2 cellReselectionPriority 4


ma L21_12_21 ^EUtranCell.DD                                                                                                                                       

for $mo in L21_12_21                                                                                                                                              
$mordn = rdn($mo)                                                                                                                                                 
pr ENodeBFunction=1,$mordn,GUtranFreqRelation=627936                                                                                                              
if $nr_of_mos = 0                                                                                                                                                 
cr ENodeBFunction=1,$mordn,GUtranFreqRelation=627936                                                                                                              
GUtraNetwork=1,GUtranSyncSignalFrequency=627936-30                                                                                                       
fi                                                                                                                                                                
done                                                                                                                                                              


func Relation_121L21                                                                                                                                              
for $j = 1 to 5                                                                                                                                                   
pr GUtraNetwork=1,ExternalGNodeBFunction=40497-$gnbid,ExternalGUtranCell=40497-000000$gnbid-31$j                                                                  
if $nr_of_mos = 1                                                                                                                                                 
crn ENodeBFunction=1,$mordn,GUtranFreqRelation=627936,GUtranCellRelation=40497-000000$gnbid-31$j                                                                  
essEnabled false                                                                                                                                                  
isRemoveAllowed false                                                                                                                                             
neighborCellRef GUtraNetwork=1,ExternalGNodeBFunction=40497-$gnbid,ExternalGUtranCell=40497-000000$gnbid-31$j                                                     
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


set EUtranCell.DD=.*,GUtranFreqRelation=627936 cellReselectionPriority 5
set CWA_CRP_2 cellReselectionPriority 2

set ENodeBFunction=1$  endcAllowed  true                                                                                                                 
set ENodeBFunction=1$  sctpEndcX2Ref Transport=1,SctpEndpoint=X2_ENDC                                                                                        
set ENodeBFunction=1$  upEndcX2IpAddressRef Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2                                                                     
set ENodeBFunction=1$  intraRanIpAddressRef Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2                                                                  
set ^EUtranCell.DD= endcAllowedPlmnList mcc=404,mnc=97,mnclength=2                                                                                                


"""


UPW_NR_GPL_LMS_SCRIPT = """




lt all
rbs
rbs


confbd+

$date = `date +%y%m%d_%H%M`
cvms Pre_GPL_LMS_NR_PA_15_$date

lbl NRCellDU
lbl NRSectorCarrier=

set CXC4012500 FeatureState 1
set CXC4011803 featurestate 1
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
set CXC4012347 featurestate 1
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
set CXC4012272 featureState 1
set CXC4012273 featureState 1
set CXC4012316 featureState 1
set CXC4012324 featureState 1
set CXC4012325 featureState 1
set CXC4012326 featureState 1
set CXC4012347 featureState 1
set CXC4012349 featureState 1
set CXC4012356 featureState 1
set CXC4012371 featureState 1
set CXC4012374 featureState 1
set CXC4012375 featureState 1
set CXC4012381 featureState 1
set CXC4012385 featureState 1
set CXC4012480 featureState 1
set CXC4012485 featureState 1
set CXC4012492 featureState 1
set CXC4012493 featureState 1
set CXC4012500 featureState 1
set CXC4012502 featureState 1
set CXC4012503 featureState 1
set CXC4012504 featureState 1
set CXC4012505 featureState 1
set CXC4012510 featureState 1
set CXC4012534 featureState 1
set CXC4012549 featureState 1
set CXC4012558 featureState 1
set CXC4012578 featureState 1
set CXC4012587 featureState 1
set CXC4040004 featureState 1
set CXC4040005 featureState 1
set CXC4040006 featureState 1
set CXC4040008 featureState 1
set CXC4040009 featureState 1
set CXC4040010 featureState 1
set CXC4040014 featureState 1
set CXC4012590 FeatureState 1
set CXC4012480 FeatureState 0



///common_Parameters_32t_8t
set NRSectorCarrier=GNBDU,CommonBeamforming=1               cbfMacroTaperType 0
set CUUP5qi=6$  estimatedE2ERTT 50
set CUUP5qi=8$  estimatedE2ERTT 50
set GNBDUFunction=1,RadioBearerTable=1,DataRadioBearer=1  tPollRetransmitUl 40
set GNBDUFunction=1,RadioBearerTable=1,DataRadioBearer=1 tStatusProhibitUl 10
set GNBDUFunction=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base drxInactivityTimer 15
set GNBDUFunction=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base drxLongCycle      10
set GNBDUFunction=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base  drxOnDurationTimer  39
set GNBCUUPFunction=1          dcDlPdcpInitialScgRate 100

set NRCellDU tddSpecialSlotPattern 3
set NRCellDU tddUlDlPattern 1
set NRCellDU rachPreambleFormat 0
set NRCellDU cellRange 5000
set NRCellDU csiRsShiftingPrimary 1
set NRCellDU csiRsShiftingSecondary 1
set NRCellDU dl256QamEnabled true
set NRCellDU drxProfileEnabled true
set NRCellDU maxUeSpeed 2
set NRCellDU pdschStartPrbStrategy 3
set NRCellDU puschStartPrbStrategy 3
set NRCellDU pZeroNomPucch -114
set NRCellDU secondaryCellOnly False
set NRCellDU ssbDuration 1
set NRCellDU ssbOffset 0
set NRCellDU ssbPeriodicity 20
set NRCellDU ssbSubCarrierSpacing 30
set NRCellDU subCarrierSpacing 30
set NRCellDU trsPeriodicity 20
set NRCellDU trsPowerBoosting 0
set NRCellDU ul256QamEnabled true
set NRCellDU rachPreambleRecTargetPower -110
set NRCellDU rachPreambleTransMax 10
Set NRCellDU maxUsersRachSchedPusch 100
set NRCellDU pZeroNomPuschGrant -102
set NRCellDU csiRsPeriodicity 40
set NRCellDU additionalPucchForCaEnabled FALSE
set NRSectorCarrier=GNBDU configuredMaxTxPower    200000
set NRCellDU  maxNoOfAdvancedDlMuMimoLayers 8

#lkf required with dmrs feature for bm
set NRCellDU pdschAllowedInDmrsSym TRUE
set NRCellDU puschAllowedInDmrsSym TRUE

set QciProfileEndcConfigExt=1   initialUplinkConf 1
set GNBCUCPFunction=1,UeCC=1,InactivityProfile=Default,InactivityProfileUeCfg=Base tInactivityTimerEndcSn 5
set NRSectorCarrier= nRMicroSleepTxEnabled true
set NRSectorCarrier=.*,CommonBeamforming=1  coverageShape 1
set GNBDUFunction=1,RadioBearerTable=1,DataRadioBearer=1    tPollRetransmitDl 40
set AnrFunctionNR anrCgiMeasInterFreqMode 1
set AnrFunctionNR anrCgiMeasIntraFreqEnabled TRUE
set AnrFunctionNR anrEndcX2Enabled TRUE
set AnrFunction removeGnbTime 7

set GNBCUCPFunction=1,AnrFunction=1 removeNrelTime 7

set  GNBDUFunction=1,Rrc=1 n310 20
set  GNBDUFunction=1,Rrc=1 n311 1
set  GNBDUFunction=1,Rrc=1 t300 1500
set  GNBDUFunction=1,Rrc=1 t301 600
set  GNBDUFunction=1,Rrc=1 t304 1000
set  GNBDUFunction=1,Rrc=1 t310 2000
set  GNBDUFunction=1,Rrc=1 t311 3000
set  GNBDUFunction=1,Rrc=1 t319 400

set GNBCUUPFunction=1    endcDataUsageReportEnabled true
set GNBDUFunction=1,UeCC=1,Prescheduling=1,PreschedulingUeCfg=Base preschedulingUeMode 1
set . anrstateNR 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          gNodebIdLength 26
set . endcX2IpAddrViaS1Active 1

set NRCellDU csiRsConfig4P csiRsControl4Ports=0,i11Restriction=
set NRCellDU csiRsConfig8P  csiRsControl8Ports=1,i11Restriction=FFFF,i12Restriction=
set NRCellDU csiRsConfig32P csiRsControl32Ports=EIGHT_TWO_N1AZ,i11Restriction=FFFFFFFF,i12Restriction=FF
set NRCellDU ssbPowerBoost 6
set NRCellDU advancedDlSuMimoEnabled TRUE
set NRCellDU pZeroNomSrs -110
set NRCellDU srsPeriodicity 40
set NRCellDU dlMaxMuMimoLayers 8
set NRCellDU ulMaxMuMimoLayers 4
set NRCellDU pZeroUePuschOffset256Qam 4
set .  cbfMacroTaperType 0
set GNBCUCPFunction=1,AnrFunction=1,AnrFunctionNR=1         anrAutoCreateXnForEndc True

set . endcDlNrRetProhibTimer 400
set . endcDlNrQualHyst 3
set . initialUplinkConf SCG
set . endcUlNrRetProhibTimer 1000
set . dcDlAggActTime 1
set . dcDlAggExpiryTimer 100
set . ulDataSplitThreshold

set NRCellRelation= isHoAllowed true
set NRCellDU endcDlLegSwitchEnabled true
set NRCellDU endcDlNrLowQualThresh 0
set NRCellDU endcUlLegSwitchEnabled true
set NRCellDU endcUlNrLowQualThresh 5
set NRCellDU endcUlNrQualHyst 6
set NRCellCU=GNBDU mcpcPSCellEnabled true
set NRSectorCarrier=.*,CommonBeamforming=1 digitalTilt 30

cr GNBCUCPFunction=1,IntraFreqMC=1
cr GNBCUCPFunction=1,IntraFreqMC=1,IntraFreqMCCellProfile=1

set IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base betterSpCellTriggerQuantity 0
set IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base rsrpBetterSpCell hysteresis=10,offset=30,timeToTrigger=640


set IntraFreqMC=1,IntraFreqMCCellProfile=1 rsrpSCellCoverage hysteresis=10,threshold=-117
set IntraFreqMC=1,IntraFreqMCCellProfile=1 rsrpBetterSCell offset=30,hysteresis=10
set Mcpc=1,McpcPSCellProfile=GNBDU,McpcPSCellProfileUeCfg=Base  rsrpCriticalEnabled true
set Mcpc=1,McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base rsrpSearchZone threshold=-112,hysteresis=10,timeToTriggerA1=160
set Mcpc=1,McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base rsrpCandidateA5 threshold1=-118,threshold2=-112,hysteresis=10,timeToTrigger=640
set Mcpc=1,McpcPSCellNrFreqRelProfile=Default,McpcPSCellNrFreqRelProfileUeCfg=Base rsrpCandidateA5Offsets threshold1Offset=0,threshold2Offset=0
set Mcpc=1,McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base rsrpCritical threshold=-119,timeToTrigger=160,hysteresis=10
set FeatureState=CXC4012375 featurestate 1
set FeatureState=CXC4012273 featurestate 1
set FeatureState=CXC4012590 FeatureState 1
set FeatureState=CXC4012549 FeatureState 1
set FeatureState=CXC4012534 FeatureState 1

set NRCellDU  maxNoOfAdvancedDlMuMimoLayers 8



lt all

set CXC4012500 FeatureState 1
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
set CXC4012347 featurestate 1
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
set CXC4012272 featureState 1
set CXC4012273 featureState 1
set CXC4012316 featureState 1
set CXC4012324 featureState 1
set CXC4012325 featureState 1
set CXC4012326 featureState 1
set CXC4012347 featureState 1
set CXC4012349 featureState 1
set CXC4012356 featureState 1
set CXC4012371 featureState 1
set CXC4012374 featureState 1
set CXC4012375 featureState 1
set CXC4012381 featureState 1
set CXC4012385 featureState 1
set CXC4012480 featureState 1
set CXC4012485 featureState 1
set CXC4012492 featureState 1
set CXC4012493 featureState 1
set CXC4012500 featureState 1
set CXC4012502 featureState 1
set CXC4012503 featureState 1
set CXC4012504 featureState 1
set CXC4012505 featureState 1
set CXC4012510 featureState 1
set CXC4012534 featureState 1
set CXC4012549 featureState 1
set CXC4012558 featureState 1
set CXC4012578 featureState 1
set CXC4012587 featureState 1
set CXC4040004 featureState 1
set CXC4040005 featureState 1
set CXC4040006 featureState 1
set CXC4040008 featureState 1
set CXC4040009 featureState 1
set CXC4040010 featureState 1
set CXC4040014 featureState 1
set CXC4012590 FeatureState 1
set CXC4012480 FeatureState 0


set  NRCellDU=UW_5_EE advancedDlSuMimoEnabled  true
set  NRCellDU=UW_5_EE cellRange  5000
set  NRCellDU=UW_5_EE csiRsActivePortConfig  2 4
set  NRCellDU=UW_5_EE csiRsShiftingPrimary  1
set  NRCellDU=UW_5_EE csiRsShiftingSecondary  1
set  NRCellDU=UW_5_EE dlMaxMuMimoLayers  8
set  NRCellDU=UW_5_EE drxProfileEnabled  true
set  NRCellDU=UW_5_EE endcDlNrLowQualThresh  -8
set  NRCellDU=UW_5_EE endcDlNrQualHyst  3
set  NRCellDU=UW_5_EE endcUlNrLowQualThresh  0
set  NRCellDU=UW_5_EE maxNoOfAdvancedDlMuMimoLayers  8
set  NRCellDU=UW_5_EE pZeroNomPucch  -114
set  NRCellDU=UW_5_EE pZeroUePuschOffset256Qam  4
set  NRCellDU=UW_5_EE pdschAllowedInDmrsSym  true
set  NRCellDU=UW_5_EE puschAllowedInDmrsSym  true
set  NRCellDU=UW_5_EE ssbPowerBoost  6
set  NRCellDU=UW_5_EE tddSpecialSlotPattern  3
set  NRCellDU=UW_5_EE trsPeriodicity  20
set  NRCellDU=UW_5_EE ulMaxMuMimoLayers  4
set  NRCellDU=UW_5_EE csiRsConfig32P.csiRsControl32Ports  1
set  NRCellDU=UW_5_EE csiRsConfig32P.i11Restriction  FFFFFFFF
set  NRCellDU=UW_5_EE csiRsConfig32P.i12Restriction  FF
set  NRCellDU=UW_5_EE csiRsConfig4P.csiRsControl4Ports  0
set  NRCellCU=UW_5_EE mcpcPSCellEnabled  true
set  . rsrpCriticalEnabled  true

set GNBCUUPFunction=1    endcDataUsageReportEnabled true
set GNBDUFunction=1,RadioBearerTable=1,DataRadioBearer=1    tPollRetransmitDl 40
set GNBDUFunction=1,UeCC=1,Prescheduling=1,PreschedulingUeCfg=Base preschedulingUeMode 1

set . mcpcPSCellProfileRef GNBCUCPFunction=1,Mcpc=1,McpcPSCellProfile=Default

set Mcpc=1,McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base rsrpCritical threshold=-109

set  NRCellDU=UW_5_EE endcUlNrLowQualThresh  5
set  NRCellDU=UW_5_EE endcDlNrLowQualThresh  0

set QciProfileEndcConfigExt=1 ulDataSplitThresholdMcg -1


set Lm=1,FeatureState=CXC4011476 featurestate  0
set Lm=1,FeatureState=CXC4011559 featurestate  0
set Lm=1,FeatureState=CXC4011666 featurestate  0
set Lm=1,FeatureState=CXC4011922 featurestate  0
set Lm=1,FeatureState=CXC4011983 featurestate  0
set Lm=1,FeatureState=CXC4012111 featurestate  0
set Lm=1,FeatureState=CXC4012123 featurestate  0
set Lm=1,FeatureState=CXC4011973 featurestate  0
set Lm=1,FeatureState=CXC4012097 featurestate  0


gs+
crn Transport=1,Router=LTEUP,TwampResponder=NR
ipAddress Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
udpPort 4001
userLabel
end

gs-


lt all
rbs
rbs
confbd+

set ENodeBFunction=1 dscpLabel 46
set ENodeBFunction=1 gtpuErrorIndicationDscp 46
set ENodeBFunction=1 interEnbCaTunnelDscp 26
set ENodeBFunction=1 interEnbUlCompTunnelDscp 26
set ENodeBFunction=1 s1GtpuEchoDscp 46
set ENodeBFunction=1 x2GtpuEchoDscp 46

cr Transport=1,QosProfiles=1,DscpPcpMap=1
set QciTable=default,QciProfilePredefined=qci1$ dscp 34
set QciTable=default,QciProfilePredefined=qci2$ dscp 34
set QciTable=default,QciProfilePredefined=qci3$ dscp 26
set QciTable=default,QciProfilePredefined=qci4$ dscp 26
set QciTable=default,QciProfilePredefined=qci5$ dscp 46
set QciTable=default,QciProfilePredefined=qci6$ dscp 32
set QciTable=default,QciProfilePredefined=qci7$ dscp 40
set QciTable=default,QciProfilePredefined=qci8$ dscp 30
set QciTable=default,QciProfilePredefined=qci9$ dscp 26
set SysM=1,OamTrafficClass=1 dscp 28
set SctpProfile= dscp 46
set Ntp=1,NtpFrequencySync= dscp 46

set QosProfiles=1,DscpPcpMap=1 pcp0
set QosProfiles=1,DscpPcpMap=1 pcp1
set QosProfiles=1,DscpPcpMap=1 pcp2
set QosProfiles=1,DscpPcpMap=1 pcp3
set QosProfiles=1,DscpPcpMap=1 pcp4
set QosProfiles=1,DscpPcpMap=1 pcp5
set QosProfiles=1,DscpPcpMap=1 pcp6
set QosProfiles=1,DscpPcpMap=1 pcp7

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp0 0,1,2,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,36,37,38,39,41,43,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp2 22,24,26
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp3 6,8,10,30,32
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp4 12,14,40
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp5 4,28
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp6 16,18,34,42,44
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp7 20,46
set SctpProfile=Node_Internal_F1  dscp 46
set SctpProfile=1 dscp 46
cr Router=.*,DnsClient=1
set Router=.*,DnsClient=1 dscp 28

set . egressQosMarking QosProfiles=1,DscpPcpMap=1

lt all
rbs
rbs
st cell
set Transport=1,SctpProfile=Node_Internal_F1 alphaIndex 3
set Transport=1,SctpProfile=Node_Internal_F1 assocMaxRtx 8
set Transport=1,SctpProfile=Node_Internal_F1 betaIndex 2
set Transport=1,SctpProfile=Node_Internal_F1 bundlingActivated TRUE
set Transport=1,SctpProfile=Node_Internal_F1 bundlingAdaptiveActivated TRUE
set Transport=1,SctpProfile=Node_Internal_F1 bundlingTimer 0
set Transport=1,SctpProfile=Node_Internal_F1 cookieLife 60
set Transport=1,SctpProfile=Node_Internal_F1 dscp 46
set Transport=1,SctpProfile=Node_Internal_F1 hbMaxBurst 1
set Transport=1,SctpProfile=Node_Internal_F1 heartbeatActivated TRUE
set Transport=1,SctpProfile=Node_Internal_F1 heartbeatInterval 2000
set Transport=1,SctpProfile=Node_Internal_F1 incCookieLife 30
set Transport=1,SctpProfile=Node_Internal_F1 initARWnd 16384
set Transport=1,SctpProfile=Node_Internal_F1 maxRto 4000
set Transport=1,SctpProfile=Node_Internal_F1 initRto 2000
set Transport=1,SctpProfile=Node_Internal_F1 minRto 1000
set Transport=1,SctpProfile=Node_Internal_F1 initialHeartbeatInterval 500
set Transport=1,SctpProfile=Node_Internal_F1 maxActivateThr 65535
set Transport=1,SctpProfile=Node_Internal_F1 maxBurst 4
set Transport=1,SctpProfile=Node_Internal_F1 maxInStreams 2
set Transport=1,SctpProfile=Node_Internal_F1 maxInitRt 5
set Transport=1,SctpProfile=Node_Internal_F1 maxOutStreams 2
set Transport=1,SctpProfile=Node_Internal_F1 maxSctpPduSize 1480
set Transport=1,SctpProfile=Node_Internal_F1 maxShutdownRt 5
set Transport=1,SctpProfile=Node_Internal_F1 minActivateThr 1
set Transport=1,SctpProfile=Node_Internal_F1 noSwitchback TRUE
set Transport=1,SctpProfile=Node_Internal_F1 pathMaxRtx 4
set Transport=1,SctpProfile=Node_Internal_F1 primaryPathAvoidance TRUE
set Transport=1,SctpProfile=Node_Internal_F1 primaryPathMaxRtx 0
set Transport=1,SctpProfile=Node_Internal_F1 sackTimer 100
set Transport=1,SctpProfile=Node_Internal_F1 thrTransmitBuffer 48
set Transport=1,SctpProfile=Node_Internal_F1 thrTransmitBufferCongCeased 85
set Transport=1,SctpProfile=Node_Internal_F1 transmitBufferSize 64
set Transport=1,SctpProfile=Node_Internal_F1 userLabel SCTP
set Transport=1,SctpProfile=1 alphaIndex 3
set Transport=1,SctpProfile=1 assocMaxRtx 8
set Transport=1,SctpProfile=1 betaIndex 2
set Transport=1,SctpProfile=1 bundlingActivated TRUE
set Transport=1,SctpProfile=1 bundlingAdaptiveActivated TRUE
set Transport=1,SctpProfile=1 bundlingTimer 0
set Transport=1,SctpProfile=1 cookieLife 60
set Transport=1,SctpProfile=1 dscp 46
set Transport=1,SctpProfile=1 hbMaxBurst 1
set Transport=1,SctpProfile=1 heartbeatActivated TRUE
set Transport=1,SctpProfile=1 heartbeatInterval 2000
set Transport=1,SctpProfile=1 incCookieLife 30
set Transport=1,SctpProfile=1 initARWnd 16384
set Transport=1,SctpProfile=1 maxRto 4000
set Transport=1,SctpProfile=1 initRto 2000
set Transport=1,SctpProfile=1 minRto 1000
set Transport=1,SctpProfile=1 initialHeartbeatInterval 500
set Transport=1,SctpProfile=1 maxActivateThr 65535
set Transport=1,SctpProfile=1 maxBurst 4
set Transport=1,SctpProfile=1 maxInStreams 2
set Transport=1,SctpProfile=1 maxInitRt 5
set Transport=1,SctpProfile=1 maxOutStreams 2
set Transport=1,SctpProfile=1 maxSctpPduSize 1480
set Transport=1,SctpProfile=1 maxShutdownRt 5
set Transport=1,SctpProfile=1 minActivateThr 1
set Transport=1,SctpProfile=1 noSwitchback TRUE
set Transport=1,SctpProfile=1 pathMaxRtx 4
set Transport=1,SctpProfile=1 primaryPathAvoidance TRUE
set Transport=1,SctpProfile=1 primaryPathMaxRtx 0
set Transport=1,SctpProfile=1 sackTimer 100
set Transport=1,SctpProfile=1 thrTransmitBuffer 48
set Transport=1,SctpProfile=1 thrTransmitBufferCongCeased 85
set Transport=1,SctpProfile=1 transmitBufferSize 64
set Transport=1,SctpProfile=1 userLabel SCTP
st cell

set Transport=1,SctpProfile=Node_Internal_F1 pathMaxRtx 4
set Transport=1,SctpProfile=Node_Internal_F1 assocMaxRtx 8
set Transport=1,SctpProfile=1 pathMaxRtx 4
set Transport=1,SctpProfile=1 assocMaxRtx 8






set ENodeBFunction=1                                        dlBbCapacityTarget 300


rdel ENodeBFunction=1,SubscriberGroupProfile=ENDC

set CXC4012562 featurestate 1



lt all
rbs
rbs

confb+

get . longitude
get . latitude

get EUtranCellFDD=UW.* latitude > $lat
get EUtranCellFDD=UW.* longitude > $long

set EUtranCellFDD=UW.* latitude  $lat
set EUtranCellFDD=UW.* longitude  $long

set NRSectorCarrier=S.* longitude $long
set NRSectorCarrier=S.* latitude $lat

get . longitude
get . latitude


set CXC4012330 featurestate 1
set CXC4012373 featurestate 1
set CXC4012406 featurestate 1
set CXC4012562 featurestate 1
set CXC4012589 featurestate 1
set CXC4012587 featurestate 1
set CXC4012510 featurestate 1
set CXC4012547 featurestate 1

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

set GNBDUFunction=1,RadioBearerTable=1,DataRadioBearer=1 dlMaxRetxThreshold 32
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 dlMaxRetxThreshold 32
set GNBDUFunction=1,RadioBearerTable=1,DataRadioBearer=1 ulMaxRetxThreshold 32
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 ulMaxRetxThreshold 32

#### DFTS OFDM

set CXC4012373 featurestate 1
set NRCellDU dftSOfdmMsg3Enabled TRUE
set NRCellDU dftSOfdmPuschEnabled TRUE

#####endcActionEvalFail

set IntraFreqMCCellProfileUeCfg endcActionEvalFail 1

### GTP-U Supervision

set GtpuSupervision=1,GtpuSupervisionProfile=S1 gtpuEchoEnabled True
set GtpuSupervision=1,GtpuSupervisionProfile=X2 gtpuEchoEnabled True
set GtpuSupervision=1,GtpuSupervisionProfile=S1 gtpuEchoDscp 32
set GtpuSupervision=1,GtpuSupervisionProfile=X2 gtpuEchoDscp 32

### advanced DL SUMIMO

set CXC4012510 featurestate 1
set NRCellDU advancedDlSuMimoEnabled TRUE
set NRCellDU nrSrsDlBufferVolThr 100
set NRCellDU nrSrsDlPacketAgeThr 0
set NRCellDU pZeroNomSrs -110
set NRCellDU srsPeriodicity 40
set NRCellDU srsHoppingBandwidth 0

### endcUlNrRetProhibTimer



###  tDcOverall

set GNBCUCPFunction tDcOverall 11

###  uldatasplitthreshold

set QciProfileEndcConfigExt uldatasplitthresholdmcg -1
set QciProfileEndcConfigExt uldatasplitthreshold 102400

set GNBDUFunction=1,RadioBearerTable=1,DataRadioBearer=1  tPollRetransmitUl 80
set NRCellDU nrSrsDlBufferVolThr 100
set GNBDUFunction=1,RadioBearerTable=1,DataRadioBearer=1    tPollRetransmitDl 80
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1  tPollRetransmitUl 80
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1  tPollRetransmitDl 80
set GNBCUUPFunction endcUlNrRetProhibTimer 1000
set NRCellDU=UW_5_EE drxProfileRef GNBDUFunction=1,UeCC=1,DrxProfile=Default
set  GNBDUFunction=1,Rrc=1 t304 2000
set Mcpc=1,McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base rsrpCritical timeToTrigger=256



cvms Pre_RET_Defn

get NRSectorCarrier=S1_N11,CommonBeamforming=1  ^digitalTilt > $1st-sec-tilt
get NRSectorCarrier=S2_N11,CommonBeamforming=1  ^digitalTilt > $2nd-sec-tilt
get NRSectorCarrier=S3_N11,CommonBeamforming=1  ^digitalTilt > $3rd-sec-tilt

hget field prod@name 3219
for $mo in hget_group
$mordn = rdn($mo)
cr Equipment=1,$mordn,AntennaNearUnit=1
cr Equipment=1,$mordn,AntennaNearUnit=1,RetSubUnit=1
set Equipment=1,$mordn,Transceiver=1 retSubUnitRef $mordn,AntennaNearUnit=1,RetSubUnit=1
set FieldReplaceableUnit=AAS-S1_N1,AntennaNearUnit=1,RetSubUnit=1 electricalAntennaTilt $1st-sec-tilt
set FieldReplaceableUnit=AAS-S2_N1,AntennaNearUnit=1,RetSubUnit=1 electricalAntennaTilt $2nd-sec-tilt
set FieldReplaceableUnit=AAS-S3_N1,AntennaNearUnit=1,RetSubUnit=1 electricalAntennaTilt $3rd-sec-tilt
done

wait 3
lt all

confb-

cvms Post_RET_Defn

ldeb  NRSectorCarrier=
ldeb  NRCellDU



confb-

confbd-


lt all

gs+

confbd+

###added SubscriberGroupProfile=ENDC(PA13)
crn ENodeBFunction=1,SubscriberGroupProfile=ENDC
customTriggerType 2
customTriggerList 2
qciOffsetForQCI6 24
qciOffsetForQCI9 22
end


###added Qci30=Qci6 and Qci31=Qci9//set eutranFreqToQciProfileRelation values (PA13)

crn ENodeBFunction=1,QciTable=default,QciProfileOperatordefined=qci30
absPrioOverride                      0
aqmMode                              1
bitRateRecommendationEnabled         false
caOffloadingEnabled                  false
counterActiveMode                    false
dataFwdPerQciEnabled                 true
dlMaxHARQTxQci                       5
dlMaxWaitingTime                     0
dlMinBitRate                         2000
dlResourceAllocationStrategy         1
drxPriority                          0
drxProfileRef                        ENodeBFunction=1,DrxProfile=0
dscp                                 26
endcProfileRef                       EndcProfile=1
harqPriority                         0
inactivityTimerOffset                0
laaSupported                         true
lessMaxDelayThreshold                0
logicalChannelGroupRef               QciTable=default,LogicalChannelGroup=3
paPartitionOverride                  false
pdb                                  300
pdbOffset                            0
pdcpSNLength                         12
priority                             6
priorityFraction                     0
qci                                  30
qciACTuning                          1000
qciSubscriptionQuanta                200
relativePriority                     2
resourceAllocationStrategy           1
resourceType                         0
rlcMode                              0
rlcSNLength                          10
rlfPriority                          0
rlfProfileRef                        RlfProfile=0
rohcEnabled                          false
rohcForUlDataEnabled                 false
schedulingAlgorithm                  4
serviceType                          0
srsAllocationStrategy                0
tReorderingDl                        35
tReorderingUl                        60
timerPriority                        0
timerProfileRef
ulMaxHARQTxQci                       5
ulMaxWaitingTime                     0
ulMinBitRate                         300
zzzTemporary1
zzzTemporary2
zzzTemporary3                        -2000000000
zzzTemporary4                        -2000000000
zzzTemporary5                        -2000000000
end

crn ENodeBFunction=1,QciTable=default,QciProfileOperatordefined=qci31
absPrioOverride                      0
aqmMode                              1
bitRateRecommendationEnabled         false
caOffloadingEnabled                  false
counterActiveMode                    false
dataFwdPerQciEnabled                 true
dlMaxHARQTxQci                       5
dlMaxWaitingTime                     0
dlMinBitRate                         0
dlResourceAllocationStrategy         1
drxPriority                          0
drxProfileRef                        ENodeBFunction=1,DrxProfile=0
dscp                                 26
endcProfileRef                       EndcProfile=1
harqPriority                         0
inactivityTimerOffset                0
laaSupported                         true
lessMaxDelayThreshold                0
logicalChannelGroupRef               QciTable=default,LogicalChannelGroup=3
paPartitionOverride                  false
pdb                                  300
pdbOffset                            0
pdcpSNLength                         12
priority                             9
priorityFraction                     0
qci                                  31
qciACTuning                          1000
qciSubscriptionQuanta                200
relativePriority                     1
resourceAllocationStrategy           1
resourceType                         0
rlcMode                              0
rlcSNLength                          10
rlfPriority                          0
rlfProfileRef                        RlfProfile=0
rohcEnabled                          false
rohcForUlDataEnabled                 false
schedulingAlgorithm                  4
serviceType                          0
srsAllocationStrategy                0
tReorderingDl                        35
tReorderingUl                        35
timerPriority                        0
timerProfileRef
ulMaxHARQTxQci                       5
ulMaxWaitingTime                     0
ulMinBitRate                         0
zzzTemporary1
zzzTemporary2
zzzTemporary3                        -2000000000
zzzTemporary4                        -2000000000
zzzTemporary5                        -2000000000
end

mr TABTAB21
ma TABTAB21 ^eutrancell arfcn ^2545
pr TABTAB21
if $nr_of_mos >= 1
for $mo in TABTAB21
$mordn = rdn($mo)



set $mordn,UeMeasControl=1,ReportConfigSearch qciA1A2ThrOffsets     qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffset=0,a1a2ThrRsrQQciOffset=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci30;a1a2ThrRsrpQciOffset=0,a1a2ThrRsrQQciOffset=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci31



done
fi



mr TABTAB85
ma TABTAB85 ^eutrancell arfcn ^365$
pr TABTAB85
if $nr_of_mos >= 1
for $mo in TABTAB85
$mordn = rdn($mo)



set $mordn,UeMeasControl=1,ReportConfigSearch qciA1A2ThrOffsets     qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffset=0,a1a2ThrRsrQQciOffset=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci30;a1a2ThrRsrpQciOffset=0,a1a2ThrRsrQQciOffset=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci31


done
fi

gs-
confbd-

gs+
confb+
set EUtranFreqRelation=365      endcHoFreqPriority 7
set EUtranFreqRelation=2545      endcHoFreqPriority 6
set EUtranFreqRelation=1526     endcHoFreqPriority -1
set EUtranFreqRelation=39348     endcHoFreqPriority -1
set EUtranFreqRelation=39150      endcHoFreqPriority -1
set EUtranFreqRelation=39349      endcHoFreqPriority -1
set EUtranFreqRelation=39151      endcHoFreqPriority -1


set EUtranFreqRelation=365      endcAwareIdleModePriority 6
set EUtranFreqRelation=2545      endcAwareIdleModePriority 5
set EUtranFreqRelation=1526     endcAwareIdleModePriority 3
set EUtranFreqRelation=39348     endcAwareIdleModePriority 4
set EUtranFreqRelation=39150      endcAwareIdleModePriority 4
set EUtranFreqRelation=39349      endcAwareIdleModePriority 6
set EUtranFreqRelation=39151      endcAwareIdleModePriority 6



confb+

get ManagedElement= swVersion    > $sw

if $sw = 23.Q2

scw RP1993:1
scw RP1994:28
scw RP1954:2
set ENodeBFunction=1 measuringEcgiWithAgActive TRUE
set ENodeBFunction=1,AnrFunction=1 pciConflictMobilityEcgiMeas true
set ENodeBFunction=1,AnrFunction=1 pciConflictDetectionEcgiMeas False
cr EnodeBfunction=1,PmFlexCounterFilter=QCI1
set EnodeBfunction=1,PmFlexCounterFilter=QCI1 qciFilterEnabled true
set EnodeBFunction=1,PmFlexCounterFilter=QCI1 qciFilterMin 1
set EnodeBFunction=1,PmFlexCounterFilter=QCI1 qciFilterMax 1
else
get ManagedElement= swVersion
fi

confb-

confb+

lbl NRCellDU
lbl NRSectorCarrier=


set  NRCellDU=UW_5_EE endcUlNrLowQualThresh  10

set Mcpc=1,McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base rsrpCritical threshold=-110,timeToTrigger=256,hysteresis=20
set Mcpc=1,McpcPSCellProfile=Default_copy,McpcPSCellProfileUeCfg=Base rsrpCritical threshold=-119,timeToTrigger=160,hysteresis=10
set GNBDUFunction=1,UeCC=1,RadioLinkControl=1,DrbRlc=Default,DrbRlcUeCfg=Base dlMaxRetxThreshold 32

set GNBDUFunction=1,UeCC=1,RadioLinkControl=1,DrbRlc=Default,DrbRlcUeCfg=Base tPollRetransmitDl 80

set GNBDUFunction=1,UeCC=1,RadioLinkControl=1,DrbRlc=Default,DrbRlcUeCfg=Base tPollRetransmitUl 80

set IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base rsrpSCellCoverage hysteresis=10,threshold=-117

gs+
crn GNBCUUPFunction=1,GtpuSupervision=1
gtpuErrorIndDscp 40
end

crn GNBCUUPFunction=1,GtpuSupervision=1,GtpuSupervisionProfile=S1
endpointResourceRef
gtpuEchoDscp 32
gtpuEchoEnabled true
interfaceList 5
userLabel
end

crn GNBCUUPFunction=1,GtpuSupervision=1,GtpuSupervisionProfile=X2
endpointResourceRef
gtpuEchoDscp 32
gtpuEchoEnabled true
interfaceList 7
userLabel
end
gs-



set NRCellDU pZeroNomPuschGrant 1000

cr GNBDUFunction=1,MassiveMimoSleep=1,MMimoSleepProfile=1
cr GNBDUFunction=1,MassiveMimoSleep=1,MMimoSleepTimeGroup=1

cr GNBDUFunction=1,MassiveMimoSleep=1,MMimoSleepTimeGroup=1,MMimoSleepTimeWindow=1
MassiveMimoSleep=1,MMimoSleepProfile=1

set GNBDUFunction=1,MassiveMimoSleep=1,MMimoSleepTimeGroup=1,MMimoSleepTimeWindow=1 stopTime 23:30
set GNBDUFunction=1,MassiveMimoSleep=1,MMimoSleepTimeGroup=1,MMimoSleepTimeWindow=1 startTime 20:30
set GNBDUFunction=1,MassiveMimoSleep=1,MMimoSleepTimeGroup=1,MMimoSleepTimeWindow=1 dayOfWeek ALL
set GNBDUFunction=1,MassiveMimoSleep=1,MMimoSleepTimeGroup=1,MMimoSleepTimeWindow=1 mMimoSleepProfileRef  MassiveMimoSleep=1,MMimoSleepProfile=1


set NRSectorCarrier=S.*_N11  mMimoSleepTimeGroupRef  MassiveMimoSleep=1,MMimoSleepTimeGroup=1
set NRSectorCarrier=S.*_N11  massiveMimoSleepEnabled 1


set MassiveMimoSleep=1,MMimoSleepProfile=1                  switchDownPrbThreshDl 10
set MassiveMimoSleep=1,MMimoSleepProfile=1                  switchDownRrcConnThresh 10
set MassiveMimoSleep=1,MMimoSleepProfile=1                  switchUpRrcConnThresh 20

set NRCellDU  ssbPowerBoostMMimoSleep 3
set NRCellDU autoSelectedModeOffset 6
cr GNBDUFunction=1,UeCC=1,PowerControl=1,PowerControlUeCfg=clpc
set GNBDUFunction=1,UeCC=1,UeBb=1,UeBbProfile=Default,UeBbProfileUeCfg=Base powerControlUeCfgRef GNBDUFunction=1,UeCC=1,PowerControl=1,PowerControlUeCfg=clpc

set GNBDUFunction=1,UeCC=1,PowerControl=1,PowerControlUeCfg=clpc puschPowerControlModeFr1 1
set  NRSectorCarrier=S.*_N11  mMimoSleepTimeGroupRef GNBDUFunction=1,MassiveMimoSleep=1,MMimoSleepTimeGroup=1
set MassiveMimoSleep=1,MMimoSleepProfile=1  sleepMode 0
set MassiveMimoSleep=1,MMimoSleepProfile=1                  switchDownMonitorDurTimer  60
set MassiveMimoSleep=1,MMimoSleepProfile=1                  switchUpMonitorDurTimer 30
set MassiveMimoSleep=1,MMimoSleepProfile=1                  switchUpPrbThreshDl 20

set  NRCellDU  ssbTimeShiftEnabled true
set NRCellDU= tddBorderVersion  0
set GNBDUFunction=1,UeCC=1,RadioLinkControl=1,UeAdaptiveRlc=1,UeAdaptiveRlcUeCfg=Base ueAdaptiveRlcRetxMode 0
set GNBCUUPFunction=1,CardinalityLimits=1                   maxS1UPath        1800
set GNBCUCPFunction=1,AnrFunction=1,AnrFunctionNR=1,AnrFunctionNRUeCfg=Base anrRsrpThreshold  -112



set CXC4012536 featurestate 0
set CXC4012590 featurestate 1
set CXC4012673 featurestate 1
set CXC4012634 featurestate 1
set CXC4012638 featurestate 1
set CXC4012677 featurestate 0
set CXC4012690 featurestate 0


ldeb  NRSectorCarrier=
ldeb  NRCellDU




gs-
confb-
$date = `date +%y%m%d_%H%M`
cvms Post_GPL_LMS_NR_PA_15_$date

lt all
rbs
rbs
 
$date = `date +%y%m%d_%H%M`
cvms Pre_GPL_LMS_NR_PA_15_$date
 
confb+
 
lt all
 
get CXC4012273|CXC4012375|CXC4012549|CXC4012492|CXC4012534|CXC4012347|CXC4012500|CXC4012325|CXC4012493|CXC4012558 featurestate$
 
set CXC4012273|CXC4012375|CXC4012549|CXC4012492|CXC4012534|CXC4012347|CXC4012500|CXC4012325|CXC4012493|CXC4012558 featurestate 1
 
 
lbl NRCellDU=
lbl NRSectorCarrier=
 
 
///common_Parameters_32t_8t
set NRSectorCarrier=,CommonBeamforming=1               cbfMacroTaperType 0
set CUUP5qi=6$  estimatedE2ERTT 50
set CUUP5qi=8$  estimatedE2ERTT 50
set Function=1,RadioBearerTable=1,DataRadioBearer=1  tPollRetransmitUl 40
set Function=1,RadioBearerTable=1,DataRadioBearer=1 tStatusProhibitUl 10
set Function=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base drxInactivityTimer 15
set Function=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base drxLongCycle      10
set Function=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base  drxOnDurationTimer  39
set GNBCUUPFunction=1          dcDlPdcpInitialScgRate 100
 
set NRCellDU= tddSpecialSlotPattern 3
set NRCellDU= tddUlDlPattern 1
set NRCellDU= rachPreambleFormat 0
set NRCellDU= cellRange 5000
set NRCellDU= csiRsShiftingPrimary 1
set NRCellDU= csiRsShiftingSecondary 1
set NRCellDU= dl256QamEnabled true
set NRCellDU= drxProfileEnabled true
set NRCellDU= maxUeSpeed 2
set NRCellDU= pdschStartPrbStrategy 3
set NRCellDU= puschStartPrbStrategy 3
set NRCellDU= pZeroNomPucch -114
set NRCellDU= secondaryCellOnly False
set NRCellDU= ssbDuration 1
set NRCellDU= ssbOffset 0
set NRCellDU= ssbPeriodicity 20
set NRCellDU= ssbSubCarrierSpacing 30
set NRCellDU= subCarrierSpacing 30
set NRCellDU= trsPeriodicity 20
set NRCellDU= trsPowerBoosting 0
set NRCellDU= ul256QamEnabled true
set NRCellDU= rachPreambleRecTargetPower -110
set NRCellDU= rachPreambleTransMax 10
Set NRCellDU= maxUsersRachSchedPusch 100
set NRCellDU= pZeroNomPuschGrant -102
set NRCellDU= csiRsPeriodicity 40
set NRCellDU= additionalPucchForCaEnabled FALSE
set NRSectorCarrier= configuredMaxTxPower    200000
set NRCellDU=  maxNoOfAdvancedDlMuMimoLayers 8
 
#lkf required with dmrs feature for bm
set NRCellDU= pdschAllowedInDmrsSym TRUE
set NRCellDU= puschAllowedInDmrsSym TRUE
 
set QciProfileEndcConfigExt=1   initialUplinkConf 1
set GNBCUCPFunction=1,UeCC=1,InactivityProfile=Default,InactivityProfileUeCfg=Base tInactivityTimerEndcSn 5
set NRSectorCarrier= nRMicroSleepTxEnabled true
set NRSectorCarrier=,CommonBeamforming=1  coverageShape 1
set Function=1,RadioBearerTable=1,DataRadioBearer=1    tPollRetransmitDl 40
set AnrFunctionNR anrCgiMeasInterFreqMode 1
set AnrFunctionNR anrCgiMeasIntraFreqEnabled TRUE
set AnrFunctionNR anrEndcX2Enabled TRUE
set AnrFunction removeGnbTime 7
set AnrFunction removeNrelTime 7
set  Function=1,Rrc=1 n310 20
set  Function=1,Rrc=1 n311 1
set  Function=1,Rrc=1 t300 1500
set  Function=1,Rrc=1 301 600
set  Function=1,Rrc=1 304 1000
set  Function=1,Rrc=1 t310 2000
set  Function=1,Rrc=1 t311 3000
set  Function=1,Rrc=1 t319 400
 
set GNBCUUPFunction=1    endcDataUsageReportEnabled true
set Function=1,UeCC=1,Prescheduling=1,PreschedulingUeCfg=Base preschedulingUeMode 1
set . anrstateNR 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          gNodebIdLength 26
set . endcX2IpAddrViaS1Active 1
 
set NRCellDU= csiRsConfig4P csiRsControl4Ports=0,i11Restriction=
set NRCellDU= csiRsConfig8P  csiRsControl8Ports=1,i11Restriction=FFFF,i12Restriction=
set NRCellDU= csiRsConfig32P csiRsControl32Ports=EIGHT_TWO_N1AZ,i11Restriction=FFFFFFFF,i12Restriction=FF
set NRCellDU= ssbPowerBoost 6
set NRCellDU= advancedDlSuMimoEnabled TRUE
set NRCellDU= pZeroNomSrs -110
set NRCellDU= srsPeriodicity 40
set NRCellDU= dlMaxMuMimoLayers 8
set NRCellDU= ulMaxMuMimoLayers 4
set NRCellDU= pZeroUePuschOffset256Qam 4
set .  cbfMacroTaperType 0
set GNBCUCPFunction=1,AnrFunction=1,AnrFunctionNR=1         anrAutoCreateXnForEndc True
 
set . endcDlNrRetProhibTimer 400
set . endcDlNrQualHyst 3
set . initialUplinkConf SCG
set . endcUlNrRetProhibTimer 1000
set . dcDlAggActTime 1
set . dcDlAggExpiryTimer 100
set . ulDataSplitThreshold
 
set NRCellRelation= isHoAllowed true
set NRCellDU= endcDlLegSwitchEnabled true
set NRCellDU= endcDlNrLowQualThresh -8
set NRCellDU= endcUlLegSwitchEnabled true
set NRCellDU= endcUlNrLowQualThresh 0
set NRCellDU= endcUlNrQualHyst 6
set NRCellCU= mcpcPSCellEnabled true
set NRSectorCarrier=,CommonBeamforming=1 digitalTilt 30
 
cr GNBCUCPFunction=1,IntraFreqMC=1
cr GNBCUCPFunction=1,IntraFreqMC=1,IntraFreqMCCellProfile=1
 
set IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base betterSpCellTriggerQuantity 0
set IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base rsrpBetterSpCell hysteresis=10,offset=30,timeToTrigger=640
 
 
set IntraFreqMC=1,IntraFreqMCCellProfile=1 rsrpSCellCoverage hysteresis=10,threshold=-117
set IntraFreqMC=1,IntraFreqMCCellProfile=1 rsrpBetterSCell offset=30,hysteresis=10
set Mcpc=1,McpcPSCellProfile=.*,McpcPSCellProfileUeCfg=Base  rsrpCriticalEnabled true
set Mcpc=1,McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base rsrpSearchZone threshold=-112,hysteresis=10,timeToTriggerA1=160
set Mcpc=1,McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base rsrpCandidateA5 threshold1=-118,threshold2=-112,hysteresis=10,timeToTrigger=640
set Mcpc=1,McpcPSCellNrFreqRelProfile=Default,McpcPSCellNrFreqRelProfileUeCfg=Base rsrpCandidateA5Offsets threshold1Offset=0,threshold2Offset=0
set Mcpc=1,McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base rsrpCritical threshold=-119,timeToTrigger=160,hysteresis=10
set FeatureState=CXC4012375 featurestate 1
set FeatureState=CXC4012273 featurestate 1
set FeatureState=CXC4012590 FeatureState 1
set FeatureState=CXC4012549 FeatureState 1
set FeatureState=CXC4012534 FeatureState 1
set FeatureState=CXC4012480 FeatureState 0
 
set NRCellDU=  maxNoOfAdvancedDlMuMimoLayers 8
 
ldeb  NRSectorCarrier=
ldeb  NRCellDU=
 
 
lt all
rbs
rbs
 
 
confbd+
 
set IntraFreqMC=1,IntraFreqMCCellProfile=1 rsrpSCellCoverage hysteresis=10,threshold=-117
 
set Mcpc=1,McpcPSCellProfile=.*,McpcPSCellProfileUeCfg=Base  rsrpCriticalEnabled true
 
confbd-
 
confbd+
 
lbl NRCell
 
lbl NRSectorCarrier=
 
set NRCellDU= dlMaxMuMimoLayers 0
set NRCellDU= csiRsConfig32P csiRsControl32Ports=0,i11Restriction=,i12Restriction=
set NRCellDU= csiRsConfig8P   csiRsControl8Ports=0,i11Restriction=,i12Restriction=
set NRCellDU= csiRsConfig4P csiRsControl4Ports=1,i11Restriction=FF
set NRCellDU= pZeroUePuschOffset256Qam 8
set NRCellDU= ssbPowerBoost 3
set NRCellDU= dlMaxMuMimoLayers 0
set NRSectorCarrier= configuredMaxTxPower    10000
set NRCellDU= maxNoOfAdvancedDlMuMimoLayers 0
set NRCellDU= advancedDlSuMimoEnabled false
set RfPort= vswrSupervisionActive  false
bl rfport=r
 
ldeb NRCellDU=
 
ldeb NRSectorCarrier=
 
 
$date = `date +%y%m%d_%H%M`
cvms Post_GPL_LMS_NR_PA_15_$date


"""


UPW_GNBCUCPFunction=""" 
########################################################################### Cell Specific Started -- NRCellCU={gUtranCell}##################################################

crn GNBCUCPFunction=1,NRCellCU={gUtranCell}
admissionLimitRef GNBCUCPFunction=1,AdmissionControl=1,AdmissionLimit=Default
admissionPriorityRef GNBCUCPFunction=1,AdmissionControl=1,AdmissionPriority=Default
advUePosMode 0
caCellMeasProfileRef CarrierAggregation=1,CaCellMeasProfile=Default
caCellProfileRef CarrierAggregation=1,CaCellProfile=Default
cellLocalId {cellLocalId}
checkUeGrpAtCellOffload false
hiPrioDetEnabled false
interfaceSupervision 0
intraFreqMCCellProfileRef IntraFreqMC=1,IntraFreqMCCellProfile=Default
mcfbCellProfileRef Mcfb=1,McfbCellProfile=Default
mcpcNrdcPSCellEnabled false
mcpcNrdcPSCellProfileRef
mcpcPCellEnabled false
mcpcPCellProfileRef Mcpc=1,McpcPCellProfile=Default
mcpcPSCellEnabled false
mcpcPSCellProfileRef Mcpc=1,McpcPSCellProfile=Default
mdtCellProfileRef Mdt=1,MdtCellProfile=Default
mdtEnabled false
nCellChangeHigh
nCellChangeMedium
nRFrequencyRef NRNetwork=1,NRFrequency=629952-30
noOfPeriodicUeMeasPerRop 900
nrdcMnCellProfileRef NrdcControl=1,NrdcMnCellProfile=Default
offloadCellProfileRef TrafficOffload=1,OffloadCellProfile=Default
periodicCellProfileRef
pmUeIntraFreqCellProfileRef
pmUeIntraFreqEnabled false
primaryPLMNId mcc=404,mnc=97
pwsEmergencyAreaIdList
qHyst 4
qHystSfHigh
qHystSfMedium
resourceStatusMaxConnUe -2
sNonIntraSearchP 0
sNonIntraSearchQ
tEvaluation
tHystNormal
threshServingLowP 0
threshServingLowQ
trStPSCellProfileRef TrafficSteering=1,TrStPSCellProfile=Default
trStSaCellProfileRef TrafficSteering=1,TrStSaCellProfile=Default
transmitSib2 false
transmitSib4 false
transmitSib5 false
transmitSib9 false
uacProfileRef GNBCUCPFunction=1,AdmissionControl=1,Uac=1,UacProfile=Default
ucmCellProfileRef UeCovMeas=1,UcmCellProfile=Default
ueMCCellProfileRef UeMC=1,UeMCCellProfile=Default
userLabel {gUtranCell}
end

crn GNBCUCPFunction=1,NRCellCU={gUtranCell},DESManagementFunction=1
desSwitch false
esNotAllowedTimePeriod
intraRatEsActivationOriginalCellLoadParameters threshold=10,timeDuration=900
periodicEsDuration 120
requiredWakeUpTime 180
end

crn GNBCUCPFunction=1,NRCellCU={gUtranCell},NRFreqRelation=629952
anrMeasOn true
caFreqRelMeasProfileRef CarrierAggregation=1,CaFreqRelMeasProfile=Default
cellReselectionPriority 7
cellReselectionSubPriority
mcpcPCellNrFreqRelProfileRef Mcpc=1,McpcPCellNrFreqRelProfile=Default
mcpcPSCellNrFreqRelProfileRef Mcpc=1,McpcPSCellNrFreqRelProfile=Default
mdtMeasOn true
nRFrequencyRef NRNetwork=1,NRFrequency=629952-30
nrdcA4ThrRsrpFreqOffset 0
offloadNrFreqRelProfileRef TrafficOffload=1,OffloadNrFreqRelProfile=Default
pMax 23
plmnIdList
plmnRestriction false
qOffsetFreq 0
qQualMin
qRxLevMin -140
redCapEnabled false
sIntraSearchP 62
sIntraSearchQ
tReselectionNR 2
tReselectionNrSfHigh
tReselectionNrSfMedium
threshXHighP 4
threshXHighQ
threshXLowP 0
threshXLowQ
trStSaNrFreqRelProfileRef TrafficSteering=1,TrStSaNrFreqRelProfile=Default
ucmNrFreqRelProfileRef UeCovMeas=1,UcmNrFreqRelProfile=Default
ueMCNrFreqRelProfileRef UeMC=1,UeMCNrFreqRelProfile=Default
end


##################################Cell Specific Ended-- NRCellCU={gUtranCell}############################


"""

UPW_GNBDUFunction = """
###############################Cell Specific Started -- NRCellDU={gUtranCell}############################


crn GNBDUFunction=1,NRSectorCarrier={nRSectorCarrierId}
administrativeState 1
arfcnDL {arfcnDL}
arfcnUL {arfcnUL}
bSChannelBwDL {bSChannelBwDL_UL}
bSChannelBwUL {bSChannelBwDL_UL}
configuredMaxTxPower {configuredMaxTxPower}
latitude {Latitude}
longitude {Longitude}
sectorEquipmentFunctionRef NodeSupport=1,SectorEquipmentFunction={sectorEquipmentFunctionId}
txDirection 0
txPowerChangeRate 1
txPowerPersistentLock false
txPowerRatio 100
end

crn GNBDUFunction=1,NRSectorCarrier={nRSectorCarrierId},CommonBeamforming=1
cbfMacroTaperType 0
coverageShape 1
digitalTilt 30
end

crn GNBDUFunction=1,NRCellDU={gUtranCell}
csiRsConfig16P csiRsControl16Ports=0
csiRsConfig2P aRestriction=3F,csiRsControl2Ports=1
csiRsConfig32P csiRsControl32Ports=0
csiRsConfig4P csiRsControl4Ports=1,i11Restriction=FF
csiRsConfig8P csiRsControl8Ports=1,i11Restriction=FFFF
pLMNIdList mcc=404,mnc=97
sibType2 siBroadcastStatus=0,siPeriodicity=64
sibType4 siBroadcastStatus=0,siPeriodicity=64
sibType5 siBroadcastStatus=0,siPeriodicity=64
sibType6 siBroadcastStatus=0,siPeriodicity=16
sibType7 siBroadcastStatus=0,siPeriodicity=64
sibType8 siBroadcastStatus=0,siPeriodicity=64
administrativeState 0
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
rachRootSequence {rachRootSequence}
secondaryCellOnly false
siWindowLength 20
ssbDuration 1
ssbFrequency 629952
ssbOffset 0
ssbPeriodicity 20
ssbSubCarrierSpacing 30
subCarrierSpacing 30
tddSpecialSlotPattern 3
tddUlDlPattern 1
trsPeriodicity 40
trsPowerBoosting 0
ul256QamEnabled true
ulMaxMuMimoLayers 0
ulStartCrb 0
userLabel {gUtranCell}
end

############################################################################ Cell Specific Ended -- NRCellDU={gUtranCell}##########################################

"""


UPW_CGSWITCH_SCRIPT = """
############Cell Specific Started -- CgSwitch={gUtranCell}################

crn GNBDUFunction=1,UeCC=1,CgSwitch={gUtranCell}
ueConfGroupType 1
userLabel
end

crn GNBDUFunction=1,UeCC=1,CgSwitchCfg={gUtranCell}
dlCgSwitchMode 1
dlScgCritQualHyst 100
dlScgCritQualThresh
dlScgLowQualHyst 50
dlScgLowQualThresh 50
dlScgNoDataAcsiPeriodicity 300
ulCgSwitchMode 1
ulScgCritQualHyst 100
ulScgCritQualThresh
ulScgLowQualHyst 60
ulScgLowQualThresh 170
userLabel
end

crn GNBDUFunction=1,UeCC=1,CgSwitch={gUtranCell},CgSwitchUeCfg=Base
cgSwitchCfgRef GNBDUFunction=1,UeCC=1,CgSwitchCfg={gUtranCell}
prefUeGroupList
ueConfGroupList
ueGroupList
userLabel
end

############Cell Specific Ended -- CgSwitch={gUtranCell}################

"""

