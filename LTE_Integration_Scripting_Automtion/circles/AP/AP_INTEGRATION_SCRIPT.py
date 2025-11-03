"""
    This script is used to automate the integration of AP (Radio Jockey) systems with LTE (Long Term Evolution) networks. 
    It handles the configuration, testing, and deployment of AP systems in an LTE environment.

"""


import os




#####################--------------------------------------------------4G LTE INTEGRATION SCRIPT--------------------------------------------------#####################

AP_Route_4G_GPL_LMS = """


$date = `date +%y%m%d_%H%M`
cvms PRE_GPL_$date

lrdel UtranFreqRelation=10757
lrdel UtranFreqRelation=10657
lrdel UtranFrequency=10757
lrdel UtranFrequency=10657

ma olt1 eutrancelltdd earfcn 39050|39025|39250
ma olt2 eutrancelltdd earfcn 39175|39200|39100
ma olf1800 eutrancellfdd earfcn 1373

for $mo in olt1
$mordn = rdn($mo)
accn $mordn changeFrequency 39150
done

for $mo in olt2
$mordn = rdn($mo)
accn $mordn changeFrequency 39294
done

for $mo in olf1800
$mordn = rdn($mo)
accn $mordn changeFrequency 1415
done

#creating EUTRAN Freq rel
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39294
39294
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39150
39150
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1415
1415
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3690
3690

################ Gearn freq ##############################

cr ENodeBFunction=1,GeraNetwork=1
cr ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
1 #frequencyGroupId

######################################

################################################

cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=48
48
0
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=48 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1

cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=49
49
0
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=49 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1

cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=50
50
0
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=50 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1

cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=51
51
0
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=51 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1

cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=52
52
0
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=52 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1

cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=53
53
0
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=53 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1

cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=54
54
0
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=54 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1

cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=55
55
0
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=55 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1

###################################################

cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=562
562
0
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=562 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1

cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=563
563
0
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=563 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1

cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=564
564
0
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=564 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1

cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=565
565
0
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=565 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1

cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=566
566
0
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=566 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1

cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=567
567
0
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=567 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1

cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=568
568
0
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=568 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1

unset all
$Tab[1] = BAN_F3
$Tab[2] = BAN_F8
$Tab[3] = BAN_T2
$Tab[4] = BAN_T1

mr BAN_F8
mr BAN_F3
mr BAN_T2
mr BAN_T1

ma BAN_F3 EUtranCellFDD earfcndl 1415
ma BAN_F8 EUtranCellFDD earfcndl 3690
ma BAN_T1 EUtranCellTDD earfcn 39150
ma BAN_T2 EUtranCellTDD earfcn 39294

func Gran_Rel
for $mo in $Tab[$i]
$mordn = rdn($mo)
pr $mordn,GeranFreqGroupRelation=1
cr ENodeBFunction=1,$mordn,GeranFreqGroupRelation=1
ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
1
done
endfunc

for $i = 1 to 4
Gran_Rel
done

set ENodeBFunction=1,EUtranCell.*,GeranFreqGroupRelation=1 cellReselectionPriority 0

set ENodeBFunction=1,AnrFunction=1,AnrFunctionGeran=1 anrStateGsm 1
set Lm=1,FeatureState=CXC4010620 featureState 1


#######################################################################

unset all
$Tab[1] = BAN_F3
$Tab[2] = BAN_F8
$Tab[3] = BAN_T2
$Tab[4] = BAN_T1

mr BAN_F8
mr BAN_F3
mr BAN_T2
mr BAN_T1

ma BAN_F3 EUtranCellFDD earfcndl 1415
ma BAN_F8 EUtranCellFDD earfcndl 3690
ma BAN_T1 EUtranCellTDD earfcn 39150
ma BAN_T2 EUtranCellTDD earfcn 39294

func EURel_3690
for $mo in $Tab[$i]
$mordn = rdn($mo)
pr $mordn,EUtranFreqRelation=3690
cr ENodeBFunction=1,$mordn,EUtranFreqRelation=3690
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3690
3
done
endfunc

func EURel_1415
for $mo in $Tab[$i]
$mordn = rdn($mo)
pr $mordn,EUtranFreqRelation=1415
cr ENodeBFunction=1,$mordn,EUtranFreqRelation=1415
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1415
5
done
endfunc

func EURel_39294
for $mo in $Tab[$i]
$mordn = rdn($mo)
pr $mordn,EUtranFreqRelation=39294
cr ENodeBFunction=1,$mordn,EUtranFreqRelation=39294
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39294
6
done
endfunc

func EURel_39150
for $mo in $Tab[$i]
$mordn = rdn($mo)
pr $mordn,EUtranFreqRelation=39150
cr ENodeBFunction=1,$mordn,EUtranFreqRelation=39150
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39150
7
done
endfunc

for $i = 1 to 4
EURel_3690
EURel_1415
EURel_39294
EURel_39150
done

######################A3###################A3##############LM###################################################
set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1 a3offset 30
set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1 hysteresisA3 10
set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1 timeToTriggerA3 480
set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1 triggerQuantityA3 0

######################A1A2################A1A2##########LM#####################A1A2#############################
for $mo in BAN_F3
$mordn = rdn($mo)
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrp -106
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrq -170
done

for $mo in BAN_F8
$mordn = rdn($mo)
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrp -98
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrq -150
done


set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThresholdRsrp -140
set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThresholdRsrq -195
set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2SearchRsrp 20
set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2SearchRsrq 10
set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 hysteresisA2CriticalRsrp 0
set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 hysteresisA2CriticalRsrq 100
set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA1Search 480
set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2Critical 480
set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2Search 480

#########################A5##########LM#############A5#####################A5#####################################


set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrq -160
set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5=1 hysteresisA5 20
set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5=1 timeToTriggerA5 480
set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5=1 triggerQuantityA5 0

######################B2###########################B2##############################B2#############################
set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold1Rsrq -195
set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold2EcNoUtra -160
set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold2RscpUtra -110
set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1,ReportConfigB2Utra=1 hysteresisB2 20
set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1,ReportConfigB2Utra=1 timeToTriggerB2 1280
set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1,ReportConfigB2Utra=1 triggerQuantityB2 0
set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1 sMeasure 0
set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1 a5B2MobilityTimer 0
set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1 ueMeasurementsActive true

############SIB3######################SIB3#########################SIB3########################SIB3###############
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=39150 allowedMeasBandwidth 100
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=39150 anrMeasOn true
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=39150 caTriggeredRedirectionActive false
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=39150 mobilityAction 1
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=39150 pMax 1000
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=39150 qOffsetFreq 0
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=39150 tReselectionEutra 2
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=39150 tReselectionEutraSfHigh 100
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=39150 tReselectionEutraSfMedium 100
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=39150 threshXHighQ 0
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=39150 threshXLow 16
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=39150 threshXLowQ 2
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=39150 userLabel SIB3

for $mo in BAN_F3
$mordn = rdn($mo)
set $mordn systemInformationBlock3 sNonIntraSearchP=10
done

for $mo in BAN_F8
$mordn = rdn($mo)
set $mordn systemInformationBlock3 sNonIntraSearchP=0
done

set ENodeBFunction=1,EUtranCellFDD=.* systemInformationBlock3 sIntraSearch=44
set ENodeBFunction=1,EUtranCellFDD=.* systemInformationBlock3 sIntraSearchP=44
set ENodeBFunction=1,EUtranCellFDD=.* systemInformationBlock3 sNonIntraSearchQ=0
set ENodeBFunction=1,EUtranCellFDD=.* systemInformationBlock3 qHyst=4
set ENodeBFunction=1,EUtranCellFDD=.* systemInformationBlock3 threshServingLowQ=1000


set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=1415 allowedMeasBandwidth 100
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=1415 anrMeasOn true
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=1415 caTriggeredRedirectionActive false
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=1415 interFreqMeasType 0
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=1415 mobilityAction 1
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=1415 nonPlannedPhysCellId 1000
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=1415 pMax 1000
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=1415 qOffsetFreq 0
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=1415 qQualMin -34
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=1415 tReselectionEutra 2
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=1415 tReselectionEutraSfHigh 100
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=1415 tReselectionEutraSfMedium 100
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=1415 threshXHigh 14
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=1415 threshXHighQ 0
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=1415 threshXLow 16
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=1415 threshXLowQ 2
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=1415 userLabel SIB5
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=1415 presenceAntennaPort1 true

set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=3690 allowedMeasBandwidth 50
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=3690 anrMeasOn true
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=3690 caTriggeredRedirectionActive false
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=3690 interFreqMeasType 0
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=3690 mobilityAction 1
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=3690 nonPlannedPhysCellId 1000
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=3690 pMax 1000
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=3690 qOffsetFreq 0
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=3690 qQualMin -34
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=3690 tReselectionEutra 2
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=3690 tReselectionEutraSfHigh 100
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=3690 tReselectionEutraSfMedium 100
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=3690 threshXHigh 14
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=3690 threshXHighQ 0
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=3690 threshXLow 16
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=3690 threshXLowQ 2
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=3690 userLabel SIB5
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=3690 presenceAntennaPort1 true

############SIB4######################SIB4#########################SIB4########################SIB4#################
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=39294 allowedMeasBandwidth 50
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=39294 anrMeasOn true
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=39294 caTriggeredRedirectionActive false
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=39294 mobilityAction 1
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=39294 pMax 1000
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=39294 qOffsetFreq 0
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=39294 qQualMin -34
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=39294 tReselectionEutra 2
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=39294 tReselectionEutraSfHigh 100
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=39294 tReselectionEutraSfMedium 100

for $mo in BAN_F3
$mordn = rdn($mo)
set $mordn,EUtranFreqRelation=39294 threshXHigh 14
done

for $mo in BAN_F8
$mordn = rdn($mo)
set $mordn,EUtranFreqRelation=39294 threshXHigh 14
done

set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=39294 threshXHighQ 0
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=39294 threshXLow 16
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=39294 threshXLowQ 0
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=39294 userLabel SIB3
set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold2Rsrp -114

##LM#############TDD#############TDD##################TDD######LM#########TDD##########TDD#########################
######################A3###################A3##############LM######################################################
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1 a3offset 30
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1 hysteresisA3 10
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1 timeToTriggerA3 480
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1 triggerQuantityA3 0

######################A1A2################A1A2##########LM#####################A1A2#################################
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrp -114
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThresholdRsrp -140
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThresholdRsrq -195
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2SearchRsrp 20
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2SearchRsrq 10
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 hysteresisA2CriticalRsrp 0
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 hysteresisA2CriticalRsrq 100
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA1Search 480
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2Critical 480
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2Search 480

#########################A5##########LM#############A5#####################A5########################################
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrp -124
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrq -160
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp -112
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrq -160
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5=1 hysteresisA5 20
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5=1 timeToTriggerA5 480
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5=1 triggerQuantityA5 0

######################B2###########################B2##############################B2################################
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold1Rsrp -140
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold1Rsrq -195
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold2EcNoUtra -160
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold2RscpUtra -110
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigB2Utra=1 hysteresisB2 20
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigB2Utra=1 timeToTriggerB2 1280
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigB2Utra=1 triggerQuantityB2 0
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1 sMeasure 0
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1 a5B2MobilityTimer 0
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1 ueMeasurementsActive true

############SIB3######################SIB3#########################SIB3########################SIB3###################
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=39150 allowedMeasBandwidth 100
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=39150 anrMeasOn true
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=39150 caTriggeredRedirectionActive false
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=39150 mobilityAction 1
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=39150 pMax 1000
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=39150 qOffsetFreq 0
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=39150 tReselectionEutra 2
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=39150 tReselectionEutraSfHigh 100
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=39150 tReselectionEutraSfMedium 100
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=39150 threshXHigh 14
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=39150 threshXHighQ 0
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=39150 threshXLow 16
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=39150 threshXLowQ 2
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=39150 userLabel SIB3
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=39150 presenceAntennaPort1 true

for $mo in BAN_T1
    $mordn = rdn($mo)
        set $mordn systemInformationBlock3 sNonIntraSearchP=12
        set $mordn,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrq -170
done

for $mo in BAN_T2
    $mordn = rdn($mo)
        set $mordn systemInformationBlock3 sNonIntraSearchP=16
        set $mordn,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrq -170
done

set ENodeBFunction=1,EUtranCellTDD=.* systemInformationBlock3 sIntraSearch=44
set ENodeBFunction=1,EUtranCellTDD=.* systemInformationBlock3 sIntraSearchP=44
set ENodeBFunction=1,EUtranCellTDD=.* systemInformationBlock3 qHyst=4
set ENodeBFunction=1,EUtranCellTDD=.* systemInformationBlock3 threshServingLowQ=1000

############SIB4######################SIB4#########################SIB4########################SIB4###################
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=39294 allowedMeasBandwidth 50
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=39294 anrMeasOn true
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=39294 caTriggeredRedirectionActive      false
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=39294 mobilityAction 1
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=39294 pMax 1000
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=39294 qOffsetFreq 0
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=39294 qQualMin -34
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=39294 tReselectionEutra 2
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=39294 tReselectionEutraSfHigh 100
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=39294 tReselectionEutraSfMedium 100
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=39294 threshXHigh 12
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=39294 threshXHighQ 0
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=39294 threshXLow 16
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=39294 threshXLowQ 0
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=39294 userLabel SIB3

##########SIB5#######################SIB5########################LM###############SIB5##################################
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=1415 allowedMeasBandwidth 100
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=1415 anrMeasOn true
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=1415 caTriggeredRedirectionActive false
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=1415 interFreqMeasType 0
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=1415 mobilityAction 1
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=1415 nonPlannedPhysCellId 1000
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=1415 pMax 1000
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=1415 qOffsetFreq 0
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=1415 qQualMin -34
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=1415 tReselectionEutra 2
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=1415 tReselectionEutraSfHigh 100
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=1415 tReselectionEutraSfMedium 100
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=1415 threshXHigh 12
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=1415 threshXHighQ 0
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=1415 threshXLow 14
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=1415 threshXLowQ 2
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=1415 userLabel SIB5

set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=3690 allowedMeasBandwidth 50
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=3690 anrMeasOn true
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=3690 caTriggeredRedirectionActive false
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=3690 mobilityAction 1
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=3690 nonPlannedPhysCellId 1000
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=3690 pMax 1000
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=3690 qOffsetFreq 0
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=3690 qQualMin -34
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=3690 tReselectionEutra 2
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=3690 tReselectionEutraSfHigh 100
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=3690 tReselectionEutraSfMedium 100
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=3690 threshXHigh 14
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=3690 threshXHighQ 0
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=3690 threshXLowQ 2
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=3690 userLabel SIB5
#########FEATURES-L18Q1-TDDFDDLM###############FEATURES-L18Q1-TDDFDDLM#################FEATURES-L18Q1-TDDFDDLM##############
########Non-Licensed Features#######LM#######Non-Licensed Features##############Non-Licensed Features#######LM##############
Set Lm=1,FeatureState=CXC4011242 featureState 0
Set Lm=1,FeatureState=CXC4011365 featureState 0
Set Lm=1,FeatureState=CXC4011555 featureState 0
Set Lm=1,FeatureState=CXC4011558 featureState 0
Set Lm=1,FeatureState=CXC4011613 featureState 0
Set Lm=1,FeatureState=CXC4011665 featureState 0
Set Lm=1,FeatureState=CXC4011712 featureState 0
Set Lm=1,FeatureState=CXC4011812 featureState 0
Set Lm=1,FeatureState=CXC4011838 featureState 0
Set Lm=1,FeatureState=CXC4011842 featureState 0
Set Lm=1,FeatureState=CXC4011931 featureState 0
Set Lm=1,FeatureState=CXC4011932 featureState 0
Set Lm=1,FeatureState=CXC4011968 featureState 0
Set Lm=1,FeatureState=CXC4012002 featureState 0
Set Lm=1,FeatureState=CXC4012012 featureState 0
Set Lm=1,FeatureState=CXC4012013 featureState 0
Set Lm=1,FeatureState=CXC4012014 featureState 0
Set Lm=1,FeatureState=CXC4012019 featureState 0
Set Lm=1,FeatureState=CXC4012034 featureState 0
Set Lm=1,FeatureState=CXC4012043 featureState 0
Set Lm=1,FeatureState=CXC4012050 featureState 0
Set Lm=1,FeatureState=CXC4012053 featureState 0
Set Lm=1,FeatureState=CXC4012079 featureState 0
Set Lm=1,FeatureState=CXC4012081 featureState 0
Set Lm=1,FeatureState=CXC4012082 featureState 0
Set Lm=1,FeatureState=CXC4012096 featureState 0
Set Lm=1,FeatureState=CXC4012102 featureState 0
Set Lm=1,FeatureState=CXC4012119 featureState 0
Set Lm=1,FeatureState=CXC4012157 featureState 0
Set Lm=1,FeatureState=CXC4012162 featureState 0
Set Lm=1,FeatureState=CXC4012163 featureState 0
Set Lm=1,FeatureState=CXC4012182 featureState 0
Set Lm=1,FeatureState=CXC4012188 featureState 0
Set Lm=1,FeatureState=CXC4012198 featureState 0
Set Lm=1,FeatureState=CXC4012201 featureState 0
Set Lm=1,FeatureState=CXC4012212 featureState 0
Set Lm=1,FeatureState=CXC4012213 featureState 0
Set Lm=1,FeatureState=CXC4012218 featureState 0
Set Lm=1,FeatureState=CXC4040002 featureState 0
Set Lm=1,FeatureState=CXC4040015 featureState 0
Set Lm=1,FeatureState=CXC4040017 featureState 0
Set Lm=1,FeatureState=CXC4010511 featureState 0
Set Lm=1,FeatureState=CXC4012022 featureState 0

#########LM########Licensed but not featured##################LM##############Licensed but not featured#####################
Set Lm=1,FeatureState=CXC4010512 featureState 0
Set Lm=1,FeatureState=CXC4010614 featureState 0
Set Lm=1,FeatureState=CXC4010955 featureState 0
Set Lm=1,FeatureState=CXC4010960 featureState 0
Set Lm=1,FeatureState=CXC4011055 featureState 0
Set Lm=1,FeatureState=CXC4011254 featureState 0
Set Lm=1,FeatureState=CXC4011262 featureState 0
Set Lm=1,FeatureState=CXC4011264 featureState 0
Set Lm=1,FeatureState=CXC4011326 featureState 0
Set Lm=1,FeatureState=CXC4011368 featureState 0
Set Lm=1,FeatureState=CXC4011377 featureState 0
Set Lm=1,FeatureState=CXC4011478 featureState 0
Set Lm=1,FeatureState=CXC4011513 featureState 0
Set Lm=1,FeatureState=CXC4011567 featureState 0
Set Lm=1,FeatureState=CXC4011649 featureState 0
Set Lm=1,FeatureState=CXC4011700 featureState 0
Set Lm=1,FeatureState=CXC4011736 featureState 0
Set Lm=1,FeatureState=CXC4011802 featureState 0
Set Lm=1,FeatureState=CXC4011810 featureState 0
Set Lm=1,FeatureState=CXC4011840 featureState 0
Set Lm=1,FeatureState=CXC4011929 featureState 0
Set Lm=1,FeatureState=CXC4011943 featureState 0
Set Lm=1,FeatureState=CXC4011944 featureState 0
Set Lm=1,FeatureState=CXC4011958 featureState 0
Set Lm=1,FeatureState=CXC4011980 featureState 0
Set Lm=1,FeatureState=CXC4011981 featureState 0
Set Lm=1,FeatureState=CXC4011983 featureState 1
Set Lm=1,FeatureState=CXC4011996 featureState 0
Set Lm=1,FeatureState=CXC4012020 featureState 0
Set Lm=1,FeatureState=CXC4012051 featureState 0
Set Lm=1,FeatureState=CXC4012052 featureState 0
Set Lm=1,FeatureState=CXC4012095 featureState 0
Set Lm=1,FeatureState=CXC4012101 featureState 0
Set Lm=1,FeatureState=CXC4012104 featureState 0
Set Lm=1,FeatureState=CXC4012110 featureState 0
Set Lm=1,FeatureState=CXC4012120 featureState 0
Set Lm=1,FeatureState=CXC4012131 featureState 0
Set Lm=1,FeatureState=CXC4012200 featureState 0
Set Lm=1,FeatureState=CXC4040018 featureState 0
Set Lm=1,FeatureState=CXC4011715 featureState 0
Set Lm=1,FeatureState=CXC4011714 featureState 0
Set Lm=1,FeatureState=CXC4011370 featureState 1
#####Licensed Features#############LM####################Licensed Features###############LM##############L18Q1################
Set Lm=1,FeatureState=CXC4012240 featureState 1
Set Lm=1,FeatureState=CXC4010973 featureState 1
Set Lm=1,FeatureState=CXC4010319 featureState 1
Set Lm=1,FeatureState=CXC4010320 featureState 1
Set Lm=1,FeatureState=CXC4010609 featureState 1
Set Lm=1,FeatureState=CXC4010613 featureState 1
Set Lm=1,FeatureState=CXC4010616 featureState 1
Set Lm=1,FeatureState=CXC4010618 featureState 1
Set Lm=1,FeatureState=CXC4010620 featureState 1
Set Lm=1,FeatureState=CXC4010717 featureState 1
Set Lm=1,FeatureState=CXC4010723 featureState 1
Set Lm=1,FeatureState=CXC4010770 featureState 1
Set Lm=1,FeatureState=CXC4010841 featureState 1
Set Lm=1,FeatureState=CXC4010856 featureState 1
Set Lm=1,FeatureState=CXC4010912 featureState 1
Set Lm=1,FeatureState=CXC4010949 featureState 1
Set Lm=1,FeatureState=CXC4010956 featureState 1
Set Lm=1,FeatureState=CXC4010959 featureState 1
Set Lm=1,FeatureState=CXC4010961 featureState 1
Set Lm=1,FeatureState=CXC4010962 featureState 1
Set Lm=1,FeatureState=CXC4010963 featureState 1
Set Lm=1,FeatureState=CXC4010964 featureState 1
Set Lm=1,FeatureState=CXC4010967 featureState 1
Set Lm=1,FeatureState=CXC4010974 featureState 1
Set Lm=1,FeatureState=CXC4010980 featureState 1
Set Lm=1,FeatureState=CXC4010990 featureState 1
Set Lm=1,FeatureState=CXC4011011 featureState 1
Set Lm=1,FeatureState=CXC4011018 featureState 1
Set Lm=1,FeatureState=CXC4011033 featureState 1
Set Lm=1,FeatureState=CXC4011034 featureState 1
Set Lm=1,FeatureState=CXC4011050 featureState 1
Set Lm=1,FeatureState=CXC4011056 featureState 1
Set Lm=1,FeatureState=CXC4011057 featureState 1
Set Lm=1,FeatureState=CXC4011059 featureState 1
Set Lm=1,FeatureState=CXC4011060 featureState 1
Set Lm=1,FeatureState=CXC4011061 featureState 1
Set Lm=1,FeatureState=CXC4011062 featureState 1
Set Lm=1,FeatureState=CXC4011063 featureState 1
Set Lm=1,FeatureState=CXC4011064 featureState 1
Set Lm=1,FeatureState=CXC4011065 featureState 1
Set Lm=1,FeatureState=CXC4011067 featureState 1
Set Lm=1,FeatureState=CXC4011068 featureState 1
Set Lm=1,FeatureState=CXC4011069 featureState 1
Set Lm=1,FeatureState=CXC4011072 featureState 1
Set Lm=1,FeatureState=CXC4011075 featureState 1
Set Lm=1,FeatureState=CXC4011155 featureState 1
Set Lm=1,FeatureState=CXC4011157 featureState 1
Set Lm=1,FeatureState=CXC4011163 featureState 1
Set Lm=1,FeatureState=CXC4011183 featureState 1
Set Lm=1,FeatureState=CXC4011245 featureState 1
Set Lm=1,FeatureState=CXC4011246 featureState 0
Set Lm=1,FeatureState=CXC4011247 featureState 1
Set Lm=1,FeatureState=CXC4011323 featureState 1
Set Lm=1,FeatureState=CXC4011252 featureState 1
Set Lm=1,FeatureState=CXC4011253 featureState 1
Set Lm=1,FeatureState=CXC4011255 featureState 1
Set Lm=1,FeatureState=CXC4011256 featureState 1
Set Lm=1,FeatureState=CXC4011258 featureState 1
Set Lm=1,FeatureState=CXC4011266 featureState 1
Set Lm=1,FeatureState=CXC4011317 featureState 1
Set Lm=1,FeatureState=CXC4011319 featureState 1
Set Lm=1,FeatureState=CXC4011327 featureState 1
Set Lm=1,FeatureState=CXC4011345 featureState 1
Set Lm=1,FeatureState=CXC4011346 featureState 1
Set Lm=1,FeatureState=CXC4011356 featureState 1
Set Lm=1,FeatureState=CXC4011366 featureState 1
Set Lm=1,FeatureState=CXC4011372 featureState 1
Set Lm=1,FeatureState=CXC4011376 featureState 1
Set Lm=1,FeatureState=CXC4011378 featureState 1
Set Lm=1,FeatureState=CXC4011422 featureState 1
Set Lm=1,FeatureState=CXC4011427 featureState 1
Set Lm=1,FeatureState=CXC4011443 featureState 1
Set Lm=1,FeatureState=CXC4011444 featureState 1
Set Lm=1,FeatureState=CXC4011476 featureState 1
Set Lm=1,FeatureState=CXC4011477 featureState 1
Set Lm=1,FeatureState=CXC4011479 featureState 1
Set Lm=1,FeatureState=CXC4011481 featureState 1
Set Lm=1,FeatureState=CXC4011482 featureState 1
Set Lm=1,FeatureState=CXC4011485 featureState 1
Set Lm=1,FeatureState=CXC4011512 featureState 1
Set Lm=1,FeatureState=CXC4011554 featureState 1
Set Lm=1,FeatureState=CXC4011557 featureState 1
Set Lm=1,FeatureState=CXC4011559 featureState 1
Set Lm=1,FeatureState=CXC4011618 featureState 1
Set Lm=1,FeatureState=CXC4011667 featureState 1
Set Lm=1,FeatureState=CXC4011698 featureState 1
Set Lm=1,FeatureState=CXC4011699 featureState 1
Set Lm=1,FeatureState=CXC4011707 featureState 1
Set Lm=1,FeatureState=CXC4011710 featureState 1
Set Lm=1,FeatureState=CXC4011711 featureState 1
Set Lm=1,FeatureState=CXC4011713 featureState 1
Set Lm=1,FeatureState=CXC4011716 featureState 1
Set Lm=1,FeatureState=CXC4011803 featureState 1
Set Lm=1,FeatureState=CXC4011804 featureState 1
Set Lm=1,FeatureState=CXC4011807 featureState 1
Set Lm=1,FeatureState=CXC4011808 featureState 1
Set Lm=1,FeatureState=CXC4011809 featureState 1
Set Lm=1,FeatureState=CXC4011811 featureState 1
Set Lm=1,FeatureState=CXC4011813 featureState 1
Set Lm=1,FeatureState=CXC4011814 featureState 1
Set Lm=1,FeatureState=CXC4011815 featureState 1
Set Lm=1,FeatureState=CXC4011820 featureState 1
Set Lm=1,FeatureState=CXC4011823 featureState 1
Set Lm=1,FeatureState=CXC4011910 featureState 1
Set Lm=1,FeatureState=CXC4011911 featureState 1
Set Lm=1,FeatureState=CXC4011914 featureState 1
Set Lm=1,FeatureState=CXC4011917 featureState 1
Set Lm=1,FeatureState=CXC4011918 featureState 1
Set Lm=1,FeatureState=CXC4011922 featureState 1
Set Lm=1,FeatureState=CXC4011930 featureState 1
Set Lm=1,FeatureState=CXC4011933 featureState 1
Set Lm=1,FeatureState=CXC4011937 featureState 1
Set Lm=1,FeatureState=CXC4011938 featureState 1
Set Lm=1,FeatureState=CXC4011939 featureState 1
Set Lm=1,FeatureState=CXC4012097 featureState 1
Set Lm=1,FeatureState=CXC4011515 featureState 1
Set Lm=1,FeatureState=CXC4012129 featureState 1
Set Lm=1,FeatureState=CXC4012036 featureState 1
Set Lm=1,FeatureState=CXC4011251 featureState 1
Set Lm=1,FeatureState=CXC4011940 featureState 1
Set Lm=1,FeatureState=CXC4011941 featureState 1
Set Lm=1,FeatureState=CXC4011942 featureState 1
Set Lm=1,FeatureState=CXC4011946 featureState 1
Set Lm=1,FeatureState=CXC4011951 featureState 1
Set Lm=1,FeatureState=CXC4011955 featureState 1
Set Lm=1,FeatureState=CXC4011966 featureState 1
Set Lm=1,FeatureState=CXC4011967 featureState 1
Set Lm=1,FeatureState=CXC4011969 featureState 1
Set Lm=1,FeatureState=CXC4011973 featureState 1
Set Lm=1,FeatureState=CXC4011974 featureState 0
Set Lm=1,FeatureState=CXC4011975 featureState 0
Set Lm=1,FeatureState=CXC4011982 featureState 1
Set Lm=1,FeatureState=CXC4011991 featureState 0
Set Lm=1,FeatureState=CXC4011999 featureState 1
Set Lm=1,FeatureState=CXC4012003 featureState 1
Set Lm=1,FeatureState=CXC4012015 featureState 1
Set Lm=1,FeatureState=CXC4012018 featureState 1
Set Lm=1,FeatureState=CXC4012023 featureState 1
Set Lm=1,FeatureState=CXC4012089 featureState 1
Set Lm=1,FeatureState=CXC4040004 featureState 1
Set Lm=1,FeatureState=CXC4040005 featureState 1
Set Lm=1,FeatureState=CXC4040006 featureState 1
Set Lm=1,FeatureState=CXC4040007 featureState 1
Set Lm=1,FeatureState=CXC4040008 featureState 1
Set Lm=1,FeatureState=CXC4040009 featureState 1
Set Lm=1,FeatureState=CXC4040010 featureState 1
Set Lm=1,FeatureState=CXC4040011 featureState 1
Set Lm=1,FeatureState=CXC4040013 featureState 0
Set Lm=1,FeatureState=CXC4040014 featureState 1
Set Lm=1,FeatureState=CXC4040016 featureState 1
Set Lm=1,FeatureState=CXC4010619 featureState 1
Set Lm=1,FeatureState=CXC4010621 featureState 1
Set Lm=1,FeatureState=CXC4010622 featureState 1
Set Lm=1,FeatureState=CXC4010798 featureState 1
Set Lm=1,FeatureState=CXC4010799 featureState 1
Set Lm=1,FeatureState=CXC4010830 featureState 1
Set Lm=1,FeatureState=CXC4011036 featureState 1
Set Lm=1,FeatureState=CXC4011077 featureState 1
Set Lm=1,FeatureState=CXC4011156 featureState 1
Set Lm=1,FeatureState=CXC4011817 featureState 1
Set Lm=1,FeatureState=CXC4011663 featureState 1
Set Lm=1,FeatureState=CXC4011664 featureState 1
Set Lm=1,FeatureState=CXC4012017 featureState 1
Set Lm=1,FeatureState=CXC4012026 featureState 1
Set Lm=1,FeatureState=CXC4011415 featureState 1
Set Lm=1,FeatureState=CXC4012070 featureState 1

########FDD-TDD######################TDD-FDD#############LM#############FDD########TDD#######################################
set ENodeBFunction=1,EUtranCell.*,GeranFreqGroupRelation=1 altCsfbTargetPrio 7
set EUtranCell.*,UeMeasControl=1                  csfbHoTargetSearchTimer 1200
set ENodeBFunction=1,EUtranCell.*,GeranFreqGroupRelation=1 csFallbackPrio 5
set ENodeBFunction=1,EUtranCell.*,GeranFreqGroupRelation=1 csFallbackPrioEC 5
set ENodeBFunction=1 measuringEcgiWithAgActive false
set ENodeBFunction=1 tRelocOverall 20
set ENodeBFunction=1 tS1HoCancelTimer 3
set ENodeBFunction=1 rrcConnReestActive true
set AnrFunction=1 removeNrelTime 3
set AnrFunction=1 maxNoPciReportsEvent 30
set AnrFunction=1 maxTimeEventBasedPciConf 30
set AnrFunction=1,AnrFunctionEUtran=1 anrUesEUtraIntraFMax 0
set AnrFunction=1,AnrFunctionEUtran=1 anrUesThreshInterFMax 0
set AnrFunction=1,AnrFunctionEUtran=1 cellAddRsrpThresholdEutran -1240
set AnrFunction=1,AnrFunctionEUtran=1 cellAddRsrqThresholdEutran -1530
set AnrFunction=1,AnrFunctionUtran=1 cellAddEcNoThresholdUtranDelta -10
set AnrFunction=1,AnrFunctionUtran=1 cellAddRscpThresholdUtranDelta -1
set AdmissionControl=1 admNrRrcDifferentiationThr 750
set AdmissionControl=1 admNrRbDifferentiationThr 750
set PowerDistribution=1 controlDomainRef Cabinet=1
set PowerSupply=1 controlDomainRef Cabinet=1
set Rcs=1 tInactivityTimer 10
deb RfPort=[A,B,C,D]
set RfPort=[ABCD] vswrSupervisionSensitivity 100
bl Equipment=1,AntennaUnitGroup=.*,AntennaNearUnit=2
set EUtranCell systemInformationBlock6 tReselectionUtra=4
set EUtranCell covTriggerdBlindHoAllowed false
set EUtranCell mobCtrlAtPoorCovActive true
set EUtranCell tTimeAlignmentTimer 0
set EUtranCell drxActive true
set EUtranCell cfraEnable true
set EUtranCell pdcchCfiMode 5
set EutranCell alpha 8
set EUtranCell pdschTypeBGain 1
set EUtranCell advCellSupAction 2
set EUtranCell pdcchPowerBoostMax 0
set EUtranCell pMaxServingCell 1000
set EUtranCell qRxLevMinOffset 1000
set EUtranCell qRxLevMin -124
set EUtranCellFDD pZeroNominalPusch -83
set EUtranCellFDD pZeroNominalPucch -110
set EUtranCellTDD pZeroNominalPusch -86
set EUtranCellTDD pZeroNominalPucch -110
set EUtranCell advCellSupSensitivity 25
set EUtranCell mappingInfo mappingInfoSIB10=0
set EUtranCell mappingInfo mappingInfoSIB3=1
set EUtranCell mappingInfo mappingInfoSIB5=3
set EUtranCell mappingInfo mappingInfoSIB6=4
set . qciSubscriptionQuanta 100
set LoadBalancingFunction=1 lbCeiling 500
set LoadBalancingFunction=1 lbRateOffsetCoefficient 320
set LoadBalancingFunction=1 lbThreshold 20
set LoadBalancingFunction=1 lbCaThreshold 2000
set LoadBalancingFunction=1 lbDiffCaOffset 100
set LoadBalancingFunction=1 lbCaCapHysteresis 20
set . caTriggeredRedirectionActive false
set . interFreqMeasType 0
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold2Rsrp -106
set ^UtranCellRelation coverageIndicator 1

########SCTP##############QOS_BBU###################QOS_BBU###################SCTP################L########M####################
set Transport=1,SctpProfile=1 alphaIndex 3
set Transport=1,SctpProfile=1 assocMaxRtx 20
set Transport=1,SctpProfile=1 betaIndex 2
set Transport=1,SctpProfile=1 bundlingActivated TRUE
set Transport=1,SctpProfile=1 bundlingAdaptiveActivated TRUE
set Transport=1,SctpProfile=1 bundlingTimer 0
set Transport=1,SctpProfile=1 cookieLife 60
set Transport=1,SctpProfile=1 dscp 46
set Transport=1,SctpProfile=1 initRto 2000
set Transport=1,SctpProfile=1 minRto 1000
set Transport=1,SctpProfile=1 hbMaxBurst 1
set Transport=1,SctpProfile=1 heartbeatActivated TRUE
set Transport=1,SctpProfile=1 heartbeatInterval 2000
set Transport=1,SctpProfile=1 incCookieLife 30
set Transport=1,SctpProfile=1 initARWnd 16384
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

########QOS_BBU###################QOS_BBU##################LM###########QOS_BBU############################QOS_BBU#################

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
set Router=.*,DnsClient=1 dscp 28

set . egressQosMarking QosProfiles=1,DscpPcpMap=1

#######Volte######################LM##########################Volte16.0########################################L###M############
set AdmissionControl=1 dlAdmDifferentiationThr 750
set AdmissionControl=1 ulAdmDifferentiationThr 750
set RadioBearerTable=default,dataradiobearer=1 ulMaxRetxThreshold 16
set RadioBearerTable=default,dataradiobearer=1 dlMaxRetxThreshold 16
set RadioBearerTable=default,MACConfiguration=1 ulMaxHARQTx 5
set RadioBearerTable=default,MACConfiguration=1 dlMaxHARQTx 4
set RadioBearerTable=default,DataRadioBearer=1 tPollRetransmitUl 60
set RadioBearerTable=default,DataRadioBearer=1 tPollRetransmitDl 80
set RadioBearerTable=default,SignalingRadioBearer=1 tReorderingUl 60
set RadioBearerTable=default,SignalingRadioBearer=1 tPollRetransmitUl 80
set RadioBearerTable=default,SignalingRadioBearer=1 tPollRetransmitDl 80
set RadioBearerTable=default,SignalingRadioBearer=1 ulMaxRetxThreshold 16
set RadioBearerTable=default,SignalingRadioBearer=1 dlMaxRetxThreshold 16
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 absPrioOverride 0
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 aqmMode 2
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 counterActiveMode false
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 dlResourceAllocationStrategy 1
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 drxPriority 99
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 drxProfileRef DrxProfile=1
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 dscp 34
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 inactivityTimerOffset 30
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=1
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 pdb 80
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 pdbOffset 100
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 pdcpSNLength 12
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 priority 1
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 rlcSNLength 10
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 rlcMode 1
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 rohcEnabled true
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 serviceType 1
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 tReorderingUl 60
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 rlfPriority 10
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 schedulingAlgorithm 6
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 measReportConfigParams a1ThresholdRsrpPrimOffset=2
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 measReportConfigParams a2ThresholdRsrpPrimOffset=2
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 measReportConfigParams a5Threshold1RsrpOffset=2
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 measReportConfigParams a5Threshold2RsrpOffset=2
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 measReportConfigParams b2Threshold1RsrpUtraOffset=2
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 measReportConfigParams b2Threshold2EcNoUtraOffset=20
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 rlfProfileRef RlfProfile=1
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 tReorderingDl 120
set QciTable=default,QciProfilePredefined=qci1              resourceType      1
set QciTable=default,QciProfilePredefined=qci2              resourceType      1
set QciTable=default,QciProfilePredefined=qci5              resourceType      0
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 absPrioOverride 0
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 aqmMode 2
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 counterActiveMode false
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 dlResourceAllocationStrategy 1
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 drxPriority 100
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 drxProfileRef DrxProfile=2
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 dscp 34
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 inactivityTimerOffset 30
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=2
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 pdb 150
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 pdbOffset 50
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 pdcpSNLength 12
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 priority 4
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 rlcSNLength 10
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 rlcMode 1
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 rohcEnabled false
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 serviceType 0
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 schedulingAlgorithm 3
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 dlMinBitRate 384
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 ulMinBitRate 384
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 absPrioOverride 1
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 aqmMode 0
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 counterActiveMode false
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 dlResourceAllocationStrategy 0
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 drxPriority 1
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 drxProfileRef DrxProfile=0
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 dscp 46
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 inactivityTimerOffset 0
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=1
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 pdb 100
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 pdbOffset 0
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 pdcpSNLength 12
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 priority 2
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 rlcSNLength 10
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 rlcMode 0
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 rohcEnabled false
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 serviceType 2
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 schedulingAlgorithm 0
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 tReorderingUl 35
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 tReorderingUl 35
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6 counterActiveMode false
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6 tReorderingUl 60
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8 counterActiveMode false
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9 counterActiveMode false
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci[1,2,5,6,7,8,9] dataFwdPerQciEnabled true
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci[1,3,4,5] dlMinBitRate 0
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci[6,7,8,9] dlMinBitRate 200
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci[1,3,4,5] ulMinBitRate 0
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci[6,7,8,9] ulMinBitRate 100
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci[6,7,8,9] schedulingAlgorithm 4
set ENodeBFunction=1 alignTtiBundWUlTrigSinr 1
set ENodeBFunction=1,DrxProfile=0 drxInactivityTimer 14
set ENodeBFunction=1,DrxProfile=0 drxRetransmissionTimer 4
set ENodeBFunction=1,DrxProfile=0 longDrxCycle 9
set ENodeBFunction=1,DrxProfile=0 longDrxCycleOnly 9
set ENodeBFunction=1,DrxProfile=0 onDurationTimer 7
set ENodeBFunction=1,DrxProfile=0 shortDrxCycle 9
set ENodeBFunction=1,DrxProfile=0 shortDrxCycleTimer 1
set ENodeBFunction=1,DrxProfile=1 drxInactivityTimer 6
set ENodeBFunction=1,DrxProfile=1 drxRetransmissionTimer 2
set ENodeBFunction=1,DrxProfile=1 longDrxCycle 3
set ENodeBFunction=1,DrxProfile=1 longDrxCycleOnly 3
set ENodeBFunction=1,DrxProfile=1 onDurationTimer 7
set ENodeBFunction=1,DrxProfile=1 shortDrxCycle 7
set ENodeBFunction=1,DrxProfile=1 shortDrxCycleTimer 0
set DrxProfile=1$                                            drxState          0
set ENodeBFunction=1,DrxProfile=2 drxInactivityTimer 6
set ENodeBFunction=1,DrxProfile=2 drxRetransmissionTimer 1
set ENodeBFunction=1,DrxProfile=2 longDrxCycle 3
set ENodeBFunction=1,DrxProfile=2 longDrxCycleOnly 3
set ENodeBFunction=1,DrxProfile=2 onDurationTimer 6
set ENodeBFunction=1,DrxProfile=2 shortDrxCycle 7
set ENodeBFunction=1,DrxProfile=2 shortDrxCycleTimer 0
set EUtranCell acBarringSkipForSms true
set EUtranCell acBarringSkipForMmtelVoice true
set EUtranCell acBarringSkipForMmtelVideo true
set EUtranCell pdschTypeBGain 1
set EUtranCell pdcchTargetBler 24
set EUtranCell pdcchTargetBlerPCell 22
set EUtranCell pdcchTargetBleremun 22
set EUtranCellFDD pdcchOuterLoopInitialAdj -70
set EUtranCellFDD pdcchOuterLoopInitialAdjPCell -70
set EUtranCell pdcchOuterLoopInitialAdjVolte -70
set EUtranCellFDD pdcchOuterLoopUpStep 8
set EUtranCellFDD pdcchOuterLoopUpStepPCell 6
set EUtranCell pdcchOuterLoopUpStepVolte 9
set EUtranCellFDD ttiBundlingAfterHO 1
set EUtranCellFDD ttiBundlingAfterReest 1
set EUtranCellFDD ttiBundlingSwitchThres 150
set EUtranCellFDD ttiBundlingSwitchThresHyst 30
set EUtranCell.*,UeMeasControl=1 measQuantityUtraFDD 1
set EUtranCell.*,UeMeasControl=1 ueMeasurementsActive true
set EUtranCell.*,UeMeasControl=1 ueMeasurementsActiveIF true
set EUtranCell.*,UeMeasControl=1 ueMeasurementsActiveUTRAN true
set EUtranCellFDD.*,UeMeasControl=1 ueMeasurementsActiveGERAN true
set EUtranCellTDD.*,UeMeasControl=1 ueMeasurementsActiveGERAN false
set EUtranCell.*,UeMeasControl=1,ReportConfigSearch=1 inhibitA2SearchConfig 0
set EUtranCell.*,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThrQci1RsrpOffset -20
set EUtranCell.*,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThrQci1RsrqOffset -100
set EUtranCell drxActive true
set EUtranCell ulBlerTargetEnabled true
set EUtranCell allocThrPucchFormat1 50
set EUtranCell allocTimerPucchFormat1 50
set EUtranCell deallocThrPucchFormat1 100
set EUtranCell deallocTimerPucchFormat1 6000
set EUtranCell pdcchCovImproveQci1 true
set EUtranCell pdcchCovImproveDtx true
set EUtranCell pdcchCovImproveSrb false
set EUtranCellTDD dlBlerTargetEnabled 1
set EUtranCellFDD dlBlerTargetEnabled 1
set . srvccCapability 1
set . dlInterferenceManagementActive true
set ENodeBFunction=1,RlfProfile n311 1
set ENodeBFunction=1,RlfProfile n310 10
set RlfProfile=0$ t301 1000
set RlfProfile=1$ t301 1000
set RlfProfile=1$ t310 500
set RlfProfile=0$ t311 10000
set RlfProfile=1$ t311 5000
set ENodeBFunction=1,Rrc=1 t301 1000
set ENodeBFunction=1,Rrc=1 t304 2000
set ENodeBFunction=1,Rrc=1 t311 5000
set ENodeBFunction=1,Rrc=1 tRrcConnReest 2
set ENodeBFunction=1,Rrc=1 tWaitForRrcConnReest 9
set ENodeBFunction=1,Rrc=1 tRrcConnectionReconfiguration 10
set ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1 anrStateUtran 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionGeran=1 anrStateGsm 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 anrIntraFreqState 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 anrInterFreqState 1
set Eutrancell adaptiveCfiHoProhibit 0
set Rcs=1 rlcDlDeliveryFailureAction 2
set EUtranCellFDD=  enableServiceSpecificHARQ true
set EUtranCellTDD=  enableServiceSpecificHARQ true
set EUtranCellFDD=  ulHarqVolteBlerTarget 3
set EUtranCellTDD=  ulHarqVolteBlerTarget 3
set QciTable=default,QciProfilePredefined=qci1 harqPriority 1
set QciTable=default,QciProfilePredefined=qci1 dlMaxHARQTxQci 7
set QciTable=default,QciProfilePredefined=qci1 ulMaxHARQTxQci 7
set RadioBearerTable=default,MACConfiguration=1 ulMaxHARQTx 5
set RadioBearerTable=default,MACConfiguration=1 ulTtiBundlingMaxHARQTx 7


lt all

unset all
$Tab[1] = BAN_F3
$Tab[2] = BAN_F8
$Tab[3] = BAN_T2
$Tab[4] = BAN_T1

mr BAN_F8
mr BAN_F3
mr BAN_T2
mr BAN_T1

ma BAN_F3 EUtranCellFDD earfcndl 1415
ma BAN_F8 EUtranCellFDD earfcndl 3690
ma BAN_T1 EUtranCellTDD earfcn 39150
ma BAN_T2 EUtranCellTDD earfcn 39294
ma S_F3 BAN_F3 sectorCarrierRef
ma S_F8 BAN_F8 sectorCarrierRef
ma S_T1 BAN_T1 sectorCarrierRef
ma S_T2 BAN_T2 sectorCarrierRef

bl UlCompGroup
rdel UlCompGroup

get ENodeBFunction=1 enbid > $temp
l touch $temp.txt
for $mo in S_F3
$mordn = rdn($mo)
! echo ' $mordn' >> $temp.txt
done

! cat $temp.txt |tr '\n' ' ' >file2.txt

$sector3 = `$gawk  '{$n= substr ($n,1,length($n)-0); print $n}' file2.txt

cr ENodeBFunction=1,UlCompGroup=1
$sector3

l rm file2.txt
l rm $temp.txt

l touch $temp.txt
for $mo in S_F8
$mordn = rdn($mo)
! echo ' $mordn' >> $temp.txt
done

! cat $temp.txt |tr '\n' ' ' >file2.txt

$sector8 = `$gawk  '{$n= substr ($n,1,length($n)-0); print $n}' file2.txt


cr ENodeBFunction=1,UlCompGroup=3
$sector8

l rm $temp.txt
l rm file2.txt

l touch $temp.txt
for $mo in S_T1
$mordn = rdn($mo)
! echo ' $mordn' >> $temp.txt
done

! cat $temp.txt |tr '\n' ' ' >file2.txt

$sectorT1 = `$gawk  '{$n= substr ($n,1,length($n)-0); print $n}' file2.txt

cr ENodeBFunction=1,UlCompGroup=4
$sectorT1

l rm $temp.txt
l rm file2.txt

l touch $temp.txt
for $mo in S_T2
$mordn = rdn($mo)
! echo ' $mordn' >> $temp.txt
done

! cat $temp.txt |tr '\n' ' ' >file2.txt

$sectorT2 = `$gawk  '{$n= substr ($n,1,length($n)-0); print $n}' file2.txt

cr ENodeBFunction=1,UlCompGroup=5
$sectorT2

l rm $temp.txt
l rm file2.txt

deb UlCompGroup

for $mo in BAN_F8
$mordn = rdn($mo)
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrp -44
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrq -140
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp -116
set $mordn,EUtranFreqRelation=3690 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=1415 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39294 a5Thr1RsrpFreqOffset 16
set $mordn,EUtranFreqRelation=39150 a5Thr1RsrpFreqOffset 16
set $mordn,EUtranFreqRelation=1415 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39150 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39294 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=1415 eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=-64,a5Thr2RsrpFreqQciOffset=10,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets a1a2ThrRsrpQciOffset=-10,a1a2ThrRsrqQciOffset=0,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=39150 eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=66,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=39294 eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=66,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
done

for $mo in BAN_F3
$mordn = rdn($mo)
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrp -116
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp -114
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrq -160
set $mordn,EUtranFreqRelation=3690 a5Thr1RsrpFreqOffset 2
set $mordn,EUtranFreqRelation=39294 a5Thr1RsrpFreqOffset 10
set $mordn,EUtranFreqRelation=39150 a5Thr1RsrpFreqOffset 10
set $mordn,EUtranFreqRelation=3690 a5Thr2RsrpFreqOffset 6
set $mordn,EUtranFreqRelation=39150 a5Thr2RsrpFreqOffset -2
set $mordn,EUtranFreqRelation=39294 a5Thr2RsrpFreqOffset 2
set $mordn,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets a1a2ThrRsrpQciOffset=2,a1a2ThrRsrqQciOffset=0,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=3690 eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=10,a5Thr2RsrpFreqQciOffset=0,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=39150 eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=-2,a5Thr2RsrpFreqQciOffset=66,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=39294 eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=-2,a5Thr2RsrpFreqQciOffset=66,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
done

for $mo in BAN_T1
$mordn = rdn($mo)
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrp -124
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp -112
set $mordn,EUtranFreqRelation=39294 a5Thr1RsrpFreqOffset 10
set $mordn,EUtranFreqRelation=39150 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=1415 a5Thr1RsrpFreqOffset 10
set $mordn,EUtranFreqRelation=3690 a5Thr1RsrpFreqOffset 10
set $mordn,EUtranFreqRelation=3690 a5Thr2RsrpFreqOffset 66
set $mordn,EUtranFreqRelation=39150 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39294 a5Thr2RsrpFreqOffset 4
set $mordn,EUtranFreqRelation=1415 a5Thr2RsrpFreqOffset 4
set $mordn,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets a1a2ThrRsrpQciOffset=76,a1a2ThrRsrqQciOffset=0,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=1415 eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=76,a5Thr2RsrpFreqQciOffset=-4,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=39294 eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=62,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=3690 eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=76,a5Thr2RsrpFreqQciOffset=0,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
done


for $mo in BAN_T2
$mordn = rdn($mo)
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrp -124
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp -112
set $mordn,EUtranFreqRelation=39294 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39150 a5Thr1RsrpFreqOffset 10
set $mordn,EUtranFreqRelation=1415 a5Thr1RsrpFreqOffset 10
set $mordn,EUtranFreqRelation=3690 a5Thr1RsrpFreqOffset 10
set $mordn,EUtranFreqRelation=3690 a5Thr2RsrpFreqOffset 66
set $mordn,EUtranFreqRelation=39150 a5Thr2RsrpFreqOffset -2
set $mordn,EUtranFreqRelation=39294 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=1415 a5Thr2RsrpFreqOffset 4
set $mordn,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets a1a2ThrRsrpQciOffset=76,a1a2ThrRsrqQciOffset=0,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=1415 eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=76,a5Thr2RsrpFreqQciOffset=-4,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=3690 eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=76,a5Thr2RsrpFreqQciOffset=0,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=39150 eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=68,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
done

#################### new parameters############################################
set EUtranCell.*,UeMeasControl=1                  inhibitB2RsrqConfig true
set EUtranCell tReorderingAutoConfiguration true
set EUtranCell.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2OutSearch 40
set EUtranCell.*,UeMeasControl=1                  bothA5RsrpRsrqCheck false
set EUtranCellTDD=.*                                  cceDynUeAdmCtrlRetDiffThr 300
set EUtranCellFDD=.*                                  cceDynUeAdmCtrlRetDiffThr 400
set EUtranCell.*                                  cceDynUeAdmCtrlOverloadThr 900
set EUtranCell.*                                  dlDynUeAdmCtrlOverloadThr 950
set EUtranCell.*                                  dlDynUeAdmCtrlRetDiffThr 400
set EUtranCell.*                                  dynUeAdmCtrlFilterConst 2000
set EUtranCell.*                                  ulDynUeAdmCtrlOverloadThr 950
set EUtranCell.*                                  ulDynUeAdmCtrlRetDiffThr 400
set EUtranCell.*                                  dynUeAdmCtrlEnabled false
set ENodeBFunction=1                                        dlMaxWaitingTimeGlobal 500
set EUtranCell.*                                  prescheduling false
set EUtranCell.*                                  cellCapMinMaxWriProt true
set EUtranCell.*                                  cellCapMinCellSubCap 1000
set EUtranCell.*                                  cellCapMaxCellSubCap 60000
set EUtranCell enableSinrUplinkClpc 1
set CarrierAggregationFunction=1                            dynamicSCellSelectionMethod 3
set EUtranCellFDD lbEUtranAcceptOffloadThreshold 10
set EUtranCellFDD lbEUtranTriggerOffloadThreshold 30
set EUtranCell.*,UeMeasControl=1,ReportConfigEUtraBadCovPrim=1 a2ThresholdRsrpPrim -140
set EUtranCell.*,UeMeasControl=1,ReportConfigEUtraBestCell=1,ReportConfigEUtraBestCellAnr=1 a3offsetAnrDelta 0
set AnrFunction=1                                           cellRelHoAttRateThreshold 15
set EUtranCellFDD cellDownlinkCaCapacity 0
set EUtranCell changeNotification changeNotificationSIB15=true
set EUtranCell changeNotification changeNotificationSIB16=true
set EUtranCell changeNotification changeNotificationSIB8=true
set . ulTrafficDelay -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1
set . dlTrafficDelay -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1
set EUtraNetwork=1,ExternalENodeBFunction=.*,ExternalEUtranCellTDD=.* lbEUtranCellOffloadCapacity 1000
set EUtranCell.*,UeMeasControl=1                  filterCoefficientEUtraRsrp 4
set EUtranCell.*,UeMeasControl=1                  filterCoefficientEUtraRsrq 11
set EUtranCell hoOptAdjThresholdAbs 5
set EUtranCell hoOptAdjThresholdPerc 50
set EUtranCellTDD hoOptStatTime 24
set EUtranCell.*,UeMeasControl=1,ReportConfigSCellA1A2=1 hysteresisA1A2RsrpBidirectional 10
set AnrFunction=1,AnrFunctionEUtran=1                       lbCellOffloadCapacityPolicy 30000
set EUtranCellFDD mappingInfo mappingInfoSIB12=7
set EUtranCellFDD mappingInfo mappingInfoSIB4=2
set EUtranCellFDD mappingInfo mappingInfoSIB6=4
set EUtranCellTDD mappingInfo mappingInfoSIB7=5
set Paging=1                                                pagingDiscardTimerDrxNb 3
set AnrFunction=1                                           probCellDetectLowHoSuccTime 4
set AnrFunction=1                                           probCellDetectMedHoSuccTime 2
set AnrFunction=1                                           problematicCellPolicy 1
set EUtranCell prsPowerBoosting 0
set . radioTransmitPerformanceMode 0
set AnrFunction=1                                           removeNcellTime   3
set AnrFunction=1                                           removeNenbTime    3
set EUtranCell.*,MimoSleepFunction=1              switchUpMonitorDurTimer 5
set EUtranCell transmissionMode 4
set ENodeBFunction=1                                        zzzTemporary52    1
set ENodeBFunction=1                                        zzzTemporary55    -2000000000
set EUtranCell ns05FullBandSchedEnabled false
set EUtrancell ns05FullBandUsersInCellThres 1
set ENodeBFunction=1                                        enabledUlTrigMeas True
set AutoCellCapEstFunction=1                                useEstimatedCellCap true
set EUtranCell.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 hysteresisA5 10
set LoadBalancingFunction=1 lbRateOffsetLoadThreshold 1000
set LoadBalancingFunction=1 lbHitRateEUtranAddThreshold 5
set LoadBalancingFunction=1 lbHitRateEUtranMeasUeIntensity 10
set LoadBalancingFunction=1 lbHitRateEUtranMeasUeThreshold 10
set LoadBalancingFunction=1 lbHitRateEUtranRemoveThreshold 0
set LoadBalancingFunction=1 lbMeasScalingLimit 30
set QciTable=default,QciProfilePredefined=qci1              qciSubscriptionQuanta 60
set QciTable=default,QciProfilePredefined=qci2              qciSubscriptionQuanta 384
set QciTable=default,QciProfilePredefined=qci5              qciSubscriptionQuanta 1
set QciTable=default,QciProfilePredefined=qci[6,7,8,9]              qciSubscriptionQuanta 200
set EUtranCellTDD=.*,EUtranFreqRelation=3690          lbA5Thr1RsrpFreqOffset 0
set EUtranCellFDD=.*,EUtranFreqRelation=.*         lbBnrPolicy 2
set EUtranCellTDD=.*,EUtranFreqRelation=.*         lbBnrPolicy 2

for $mo in BAN_F8
$mordn = rdn($mo)
set $mordn,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold1Rsrp -44
set $mordn,EUtranFreqRelation=3690          lbA5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=1415          lbA5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39150          lbA5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39294          lbA5Thr1RsrpFreqOffset 0
set $mordn$ cellSubscriptionCapacity 5000
set $mordn$ systemInformationBlock3 sNonIntraSearch=0
set $mordn,EUtranFreqRelation=39150 threshXHigh 12
set $mordn,EUtranFreqRelation=39294 threshXHigh 14
set $mordn,EUtranFreqRelation=1415 threshXHigh 14
set $mordn$ threshServingLow 0
set $mordn,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold1Rsrp -140
set $mordn,EUtranFreqRelation=1415 voicePrio 7
set $mordn,EUtranFreqRelation=39150 voicePrio -1
set $mordn,EUtranFreqRelation=39294 voicePrio -1
set $mordn,EUtranFreqRelation=3690 voicePrio 6
set $mordn,GeranFreqGroupRelation=1 voicePrio -1
set $mordn,EUtranFreqRelation=1415 voicePrioBr 7
set $mordn,EUtranFreqRelation=39150 voicePrioBr -1
set $mordn,EUtranFreqRelation=39294 voicePrioBr -1
set $mordn,EUtranFreqRelation=3690 voicePrioBr 6
set $mordn,GeranFreqGroupRelation=1 voicePrioBr -1
set $mordn,EUtranFreqRelation=3690 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=3690 eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,lbQciProfileHandling=1
setm $mordn noOfPucchSrUsers 240 noOfPucchCqiUsers 120
set $mordn qRxLevMin??-124
set $mordn systemInformationBlock3 sNonIntraSearch=0
set $mordn$ threshServingLow 0
set $mordn,GeranFreqGroupRelation=1 qRxLevMin -111
set $mordn,GeranFreqGroupRelation=1 threshXLow 16
done

for $mo in BAN_F3
$mordn = rdn($mo)
set $mordn,EUtranFreqRelation=3690 a5Thr2rsrqFreqOffset  10
set $mordn,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold1Rsrp -140
set $mordn,EUtranFreqRelation=1415          lbA5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=3690          lbA5Thr1RsrpFreqOffset 97
set $mordn,EUtranFreqRelation=39150          lbA5Thr1RsrpFreqOffset 97
set $mordn,EUtranFreqRelation=39294          lbA5Thr1RsrpFreqOffset 97
set $mordn$ cellSubscriptionCapacity 20000
set $mordn$ systemInformationBlock3 sNonIntraSearch=8
set $mordn,EUtranFreqRelation=39150 threshXHigh 12
set $mordn,EUtranFreqRelation=39294 threshXHigh 14
set $mordn$ threshServingLow 6
set $mordn,EUtranFreqRelation=3690 threshXLow 16
set $mordn,EUtranFreqRelation=1415 voicePrio 7
set $mordn,EUtranFreqRelation=39150 voicePrio -1
set $mordn,EUtranFreqRelation=39294 voicePrio -1
set $mordn,EUtranFreqRelation=3690 voicePrio 6
set $mordn,GeranFreqGroupRelation=1 voicePrio 1
set $mordn,EUtranFreqRelation=1415 voicePrioBr 7
set $mordn,EUtranFreqRelation=39150 voicePrioBr -1
set $mordn,EUtranFreqRelation=39294 voicePrioBr -1
set $mordn,EUtranFreqRelation=3690 voicePrioBr 6
set $mordn,GeranFreqGroupRelation=1 voicePrioBr 1
set $mordn,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold1Rsrp -118
set $mordn,EUtranFreqRelation=1415 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=1415 eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,lbQciProfileHandling=1
setm $mordn ulChannelBandwidth 20000 dlChannelBandwidth 20000
setm $mordn noOfPucchSrUsers 420 noOfPucchCqiUsers 210
set $mordn qRxLevMin??-124
set $mordn systemInformationBlock3 sNonIntraSearch=4
set $mordn$ threshServingLow 4
set $mordn,GeranFreqGroupRelation=1 qRxLevMin -111
set $mordn,GeranFreqGroupRelation=1 threshXLow 62
done


for $mo in BAN_T1
$mordn = rdn($mo)
set $mordn,EUtranFreqRelation=1415          lbA5Thr1RsrpFreqOffset 61
set $mordn,EUtranFreqRelation=39294          lbA5Thr1RsrpFreqOffset 61
set $mordn,EUtranFreqRelation=39150          lbA5Thr1RsrpFreqOffset 0
set $mordn$ cellSubscriptionCapacity 20000
set $mordn$ systemInformationBlock3 sNonIntraSearch=8
set $mordn$ threshServingLow 8
set $mordn,EUtranFreqRelation=39294 threshXLow 16
set $mordn,EUtranFreqRelation=1415 threshXLow 14
set $mordn,EUtranFreqRelation=39150 connectedModeMobilityPrio 7
set $mordn,EUtranFreqRelation=39294 connectedModeMobilityPrio 6
set $mordn,EUtranFreqRelation=39150 connectedModeMobilityPrioBr 7
set $mordn,EUtranFreqRelation=39294 connectedModeMobilityPrioBr 6
set $mordn,EUtranFreqRelation=1415 voicePrio 7
set $mordn,EUtranFreqRelation=39150 voicePrio 6
set $mordn,EUtranFreqRelation=39294 voicePrio -1
set $mordn,EUtranFreqRelation=3690 voicePrio -1
set $mordn,GeranFreqGroupRelation=1 voicePrio -1
set $mordn,EUtranFreqRelation=1415 voicePrioBr 7
set $mordn,EUtranFreqRelation=39150 voicePrioBr 6
set $mordn,EUtranFreqRelation=39294 voicePrioBr -1
set $mordn,EUtranFreqRelation=3690 voicePrioBr -1
set $mordn,GeranFreqGroupRelation=1 voicePrioBr -1
set $mordn,EUtranFreqRelation=39150 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39150 eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,lbQciProfileHandling=1
set $mordn$ ChannelBandwidth 20000
setm $mordn$ noOfPucchSrUsers 300 noOfPucchCqiUsers 160
set $mordn,EUtranFreqRelation=39294 a5Thr2RsrqFreqOffset 12
set $mordn qRxLevMin??-124
set $mordn systemInformationBlock3 sNonIntraSearch=8
set $mordn$ threshServingLow 8
set $mordn,GeranFreqGroupRelation=1 qRxLevMin -111
set $mordn,GeranFreqGroupRelation=1 threshXLow 62
done

for $mo in BAN_T2
$mordn = rdn($mo)
set $mordn,EUtranFreqRelation=39150 a5Thr2RsrqFreqOffset 12
set $mordn,EUtranFreqRelation=1415          lbA5Thr1RsrpFreqOffset 61
set $mordn,EUtranFreqRelation=39150          lbA5Thr1RsrpFreqOffset 61
set $mordn,EUtranFreqRelation=39294          lbA5Thr1RsrpFreqOffset 0
set $mordn$ cellSubscriptionCapacity 10000
set $mordn$ systemInformationBlock3 sNonIntraSearch=8
set $mordn$ threshServingLow 12
set $mordn,EUtranFreqRelation=39150 threshXHigh 12
set $mordn,EUtranFreqRelation=39150 threshXLow 0
set $mordn,EUtranFreqRelation=1415 threshXLow 14
set $mordn,EUtranFreqRelation=39150 connectedModeMobilityPrio 7
set $mordn,EUtranFreqRelation=39294 connectedModeMobilityPrio 6
set $mordn,EUtranFreqRelation=39150 connectedModeMobilityPrioBr 7
set $mordn,EUtranFreqRelation=39294 connectedModeMobilityPrioBr 6
set $mordn,EUtranFreqRelation=1415 voicePrio 7
set $mordn,EUtranFreqRelation=39150 voicePrio -1
set $mordn,EUtranFreqRelation=39294 voicePrio 6
set $mordn,EUtranFreqRelation=3690 voicePrio -1
set $mordn,GeranFreqGroupRelation=1 voicePrio -1
set $mordn,EUtranFreqRelation=1415 voicePrioBr 7
set $mordn,EUtranFreqRelation=39150 voicePrioBr -1
set $mordn,EUtranFreqRelation=39294 voicePrioBr 6
set $mordn,EUtranFreqRelation=3690 voicePrioBr -1
set $mordn,GeranFreqGroupRelation=1 voicePrioBr -1
set $mordn,EUtranFreqRelation=39294 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39294 eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,lbQciProfileHandling=1
set $mordn$ ChannelBandwidth 10000
setm $mordn$ noOfPucchSrUsers 300 noOfPucchCqiUsers 160
set $mordn qRxLevMin??-124
set $mordn systemInformationBlock3 sNonIntraSearch=8
set $mordn$ threshServingLow 8
set $mordn,GeranFreqGroupRelation=1 qRxLevMin -111
set $mordn,GeranFreqGroupRelation=1 threshXLow 62
done

set EUtranCell crsGain 300
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=3690 threshXLow 62

set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=39150 qQualMin -34
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=39150 qQualMin -34
set . enableUeAssistedAdaptiveDrx false
set . enableueassistedsigreduction false
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold1Rsrp -140

###############LM###################Repeated#################################Repeated#######################L##########M#####################
set ENodeBFunction=1,EUtranCell.*,EUtranFreqRelation=1415 qOffsetFreq 0
set ENodeBFunction=1,EUtranCell.*,EUtranFreqRelation=39150 qOffsetFreq 0
set ENodeBFunction=1,EUtranCell.*,EUtranFreqRelation=39294 qOffsetFreq 0
set ENodeBFunction=1,EUtranCell.*,EUtranFreqRelation=3690 qOffsetFreq 0
set ENodeBFunction=1,EUtranCell.*,EUtranFreqRelation=39150 qRxLevMin -124
set ENodeBFunction=1,EUtranCell.*,EUtranFreqRelation=39294 qRxLevMin -124
set ENodeBFunction=1,EUtranCell.*,EUtranFreqRelation=1415 qRxLevMin -124
set ENodeBFunction=1,EUtranCell.*,EUtranFreqRelation=3690 qRxLevMin -124
set ENodeBFunction=1,EUtranCell.*,EUtranFreqRelation=1415 interFreqMeasType 0
set ENodeBFunction=1,EUtranCell.*,EUtranFreqRelation=3690 interFreqMeasType 0
set ENodeBFunction=1,EUtranCell.*,EUtranFreqRelation=39150 interFreqMeasType 0
set ENodeBFunction=1,EUtranCell.*,EUtranFreqRelation=39294 interFreqMeasType 0
set EUtranCellFDD                                 servOrPrioTriggeredErabAction 3
set ENodeBFunction=1,EUtranCell.*,GeranFreqGroupRelation=1 cellReselectionPriority 0
set ENodeBFunction=1,EUtranCell.*,EUtranFreqRelation=3690 cellReselectionPriority 3
set ENodeBFunction=1,EUtranCell.*,EUtranFreqRelation=1415 cellReselectionPriority 5
set ENodeBFunction=1,EUtranCell.*,EUtranFreqRelation=39150 cellReselectionPriority 7
set ENodeBFunction=1,EUtranCell.*,EUtranFreqRelation=39294 cellReselectionPriority 6
set ENodeBFunction=1,EUtranCell.*,UtranFreqRelation=2490 cellReselectionPriority 2
set ENodeBFunction=1,EUtranCell.*,EUtranFreqRelation=1415 connectedModeMobilityPrio 5
set ENodeBFunction=1,EUtranCell.*,EUtranFreqRelation=39150 connectedModeMobilityPrio 7
set ENodeBFunction=1,EUtranCell.*,EUtranFreqRelation=39294 connectedModeMobilityPrio 6
set ENodeBFunction=1,EUtranCell.*,EUtranFreqRelation=3690 connectedModeMobilityPrio 3
set ENodeBFunction=1,EUtranCell.*,GeranFreqGroupRelation=1 connectedModeMobilityPrio -1
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=3690 connectedModeMobilityPrio -1
set ENodeBFunction=1,EUtranCell.*,EUtranFreqRelation=1415 connectedModeMobilityPrioBr 5
set ENodeBFunction=1,EUtranCell.*,EUtranFreqRelation=39150 connectedModeMobilityPrioBr 7
set ENodeBFunction=1,EUtranCell.*,EUtranFreqRelation=39294 connectedModeMobilityPrioBr 6
set ENodeBFunction=1,EUtranCell.*,EUtranFreqRelation=3690 connectedModeMobilityPrioBr 3
set ENodeBFunction=1,EUtranCell.*,GeranFreqGroupRelation=1 connectedModeMobilityPrioBr -1
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=3690 connectedModeMobilityPrioBr -1
set . timeAndPhaseSynchAlignment true
set . timeAndPhaseSynchCritical false
set ENodeBFunction=1,EUtranCell.*,EUtranFreqRelation=.* eutranFreqToQciProfileRelation lbQciProfileHandling=1

################ GPLV20 New parameters Start##################################################
set AnrFunction=1,AnrFunctionEUtran=1 anrUesEUtraIntraFMin 0
set AnrFunction=1,AnrFunctionEUtran=1 anrUesThreshInterFMin 0
set AdmissionControl=1 arpBasedPreEmptionState 0
set AdmissionControl=1 ulAdmOverloadThr 950
set AdmissionControl=1 ulTransNwBandwidth 1000
set AnrFunction=1 probCellDetectMedHoSuccThres 50
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 hoAllowedEutranPolicy 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 x2SetupPolicy 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1 hoAllowedUtranPolicy 1
set AnrPciConflictDrxProfile=1                              anrPciConflictDrxInactivityTimer 8
set AnrPciConflictDrxProfile=1                              anrPciConflictOnDurationTimer 4
set CarrierAggregationFunction=1                            fourLayerMimoPreferred false
set CarrierAggregationFunction=1                            enhancedSelectionOfMimoAndCa false
set CarrierAggregationFunction=1                            waitForAdditionalSCellOpportunity 10000
set CarrierAggregationFunction=1                            sCellActProhibitTimer 10
set CarrierAggregationFunction=1                            selectionPolicyUlWeighting -1
set CarrierAggregationFunction=1                            waitForBlindSelSCellRepLessTtt 600
set CarrierAggregationFunction=1                            laaSCellDeactProhibitTimer 200
set ENodeBFunction=1                                        csfbMeasFromIdleMode 1
set ENodeBFunction=1                                        x2SetupTwoWayRelations true
set ENodeBFunction=1                                        dnsLookupOnTai 1
set ENodeBFunction=1                                        zzzTemporary13    -2000000000
set ENodeBFunction=1                                        caAwareMfbiIntraCellHo false
set ENodeBFunction=1                                        mfbiSupportPolicy false
set ENodeBFunction=1                                        s1HODirDataPathAvail True
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
set EUtranCell                                  useBandPrioritiesInSib1 false
set ENodeBFunction=1                                        x2GtpuEchoEnable  0
set ENodeBFunction=1                                        x2IpAddrViaS1Active true
set ENodeBFunction=1                                        x2retryTimerMaxAuto 1440
set ENodeBFunction=1                                        forcedSiTunnelingActive false
set EUtranCellFDD  dlInternalChannelBandwidth 0
set EUtranCellFDD  ulInternalChannelBandwidth 0
set EUtranCellFDD  beamWeightSet16Tr 0
set EUtranCellTDD  dlMaxMuMimoLayers 0
set EUtranCellTDD  ulMaxMuMimoLayers 0
set EUtranCellTDD  subframeAssignment 2
set EUtranCellTDD  timePhaseMaxDeviationTddIndex 0
set EUtranCell.*,EUtranFreqRelation=.*,EUtranCellRelation=40449-.*-.* isHoAllowed       true
set EUtranCell.*,EUtranFreqRelation=1415          qRxLevMinCe       -140
set EUtranCell.*,EUtranFreqRelation=3690          qRxLevMinCe       -140
set EUtranCell.*,EUtranFreqRelation=39150          qRxLevMinCe       -140
set EUtranCell.*,EUtranFreqRelation=39294         qRxLevMinCe       -140
set LoadBalancingFunction=1                                 txPwrForOverlaidCellDetect 370
set Paging=1                                                maxNoOfPagingRecordsNb 3
set Paging=1                                                noOfDefPagCyclPrim 8
set EUtranCell.*,UeMeasControl=1,ReportConfigCsfbUtra=1 hysteresis        10
set EUtranCell.*,UeMeasControl=1,ReportConfigSCellA6=1 triggerQuantityA6 0
set SecurityHandling=1                                      cipheringAlgoPrio 1 2 0
set EUtranCell.*,UeMeasControl=1                  zzzTemporary13    -2000000000
set EUtranCell.*,UeMeasControl=1                  lowPrioMeasThresh 0
set EUtranCell.*,UeMeasControl=1                  maxUtranCellsToMeasure 32
set EUtranCell.*,UeMeasControl=1                  allowReleaseQci1 false
set EUtranCell.*,UeMeasControl=1                  ulSinrOffset 30
set EUtranCell  puschNcpChannelEstWindowSize 1
set EUtranCell  servOrPrioTriggeredIFHo 0
set EUtranCell  ul64qamEnabled    true
set EUtranCell  dl256QamStatus    2
set EUtranCell  dl256QamEnabled   true
set EUtranCell  dlFrequencyAllocationProportion 100
set EUtranCellFDD  commonSrPeriodicity 10
set EUtranCellTDD  commonSrPeriodicity 20
set EUtranCell changeNotification changeNotificationSIB7=true
set EUtranCell changeNotification changeNotificationSIB2=true
set EUtranCell changeNotification changeNotificationSIB3=true
set EUtranCell changeNotification changeNotificationSIB4=true
set EUtranCell changeNotification changeNotificationSIB1=true
set EUtranCell changeNotification changeNotificationSIB6=true
set EUtranCell changeNotification changeNotificationSIB5=true
set EUtranCell changeNotification changeNotificationSIB13=true
set EUtranCell ulInterferenceManagementActive true
set EUtranCell  qRxLevMinCe       -140
set EUtranCell  pdcchLaGinrMargin 40
set EUtranCell  acBarringPresence acBarringForMmtelVideoPresence=0
set EUtranCell  acBarringPresence acBarringForMmtelVoicePresence=0
set EUtranCell  acBarringPresence acBarringPriorityMmtelVideo=0
set EUtranCell  acBarringPresence acBarringPriorityMmtelVoice=0
set EUtranCell  acBarringPresence acBarringForMoDataPresence=0
set EUtranCell  noOfEnhAdptReTxCand -1
set EUtranCell  dynUlResourceAllocEnabled false
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
set EUtranCell  systemInformationBlock7 tReselectionGeran=2
set EUtranCell  systemInformationBlock7 tReselectionGeranSfHigh=100
set EUtranCell  systemInformationBlock7 tReselectionGeranSfMedium=100
set EUtranCell  tUeBlockingTimer  200
set EUtranCell  ulConfigurableFrequencyStart 0
set EUtranCell  ulFrequencyAllocationProportion 100
set EUtranCell  ulImprovedUeSchedLastEnabled true
set EUtranCell  ulPsdLoadThresholdSinrClpc 2
set EUtranCell  ulSCellPriority   5
set EUtranCell  ulSchedCtrlForOocUesEnabled true
set EUtranCell  ulSrsEnable       false
set EUtranCellFDD  ulTrigActive      False
set EUtranCellTDD  ulTrigActive      True
set EUtranCell  ulTxPsdDistrThr   40
set EUtranCell  uncertAltitude    0
set EUtranCell  uncertSemiMajor   0
set EUtranCell  uncertSemiMinor   0
set EUtranCell pdcchTargetBlervolte 4
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci[6,7,8,9] absPrioOverride 0
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold1Rsrp  -140
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigB2Geran=1 hysteresisB2      20
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold2Geran -110
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold2Geran -110
set EUtranCell.*,UeMeasControl=1,ReportConfigB2Geran=1 timeToTriggerB2 1280
set EutrancellFDD=.*,EutranCellRelation=.* lbBnrAllowed true
set EutrancellTDD=.*,EutranCellRelation=.* lbBnrAllowed true
set EUtranCell.*,EUtranFreqRelation=.*         tReselectionEutraCe 2
set EUtranCell.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA1SearchRsrq 1024
set EUtranCell.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2CriticalRsrq 1024
set EUtranCell.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2SearchRsrq 1024
set EUtranCell.*,UeMeasControl=1,ReportConfigA5=1 hysteresisA5RsrqOffset 0
set EUtranCell.*,UeMeasControl=1,ReportConfigA5=1 timeToTriggerA5Rsrq 1024
set EUtranCell.*,EUtranFreqRelation=39150 a5Thr1RsrqFreqOffset 0
set EUtranCell.*,EUtranFreqRelation=39294 a5Thr1RsrqFreqOffset 0
set EUtranCell.*,EUtranFreqRelation=1415 a5Thr1RsrqFreqOffset 0
set EUtranCell.*,EUtranFreqRelation=3690 a5Thr1RsrqFreqOffset 0
set EUtranCell.*,EUtranFreqRelation=39150 a5Thr2rsrqFreqOffset 0
set EUtranCell.*,EUtranFreqRelation=39294 a5Thr2rsrqFreqOffset 0
set EUtranCell.*,EUtranFreqRelation=1415 a5Thr2rsrqFreqOffset 0
set EUtranCell.*,EUtranFreqRelation=3690 a5Thr2rsrqFreqOffset 0
set EUtranCell.*,EUtranFreqRelation=39150 eutranFreqToQciProfileRelation  a5Thr1rsrqFreqQciOffset=0,a5Thr2rsrqFreqQciOffset=240,lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set EUtranCell.*,EUtranFreqRelation=39294 eutranFreqToQciProfileRelation  a5Thr1rsrqFreqQciOffset=0,a5Thr2rsrqFreqQciOffset=240,lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set EUtranCell.*,EUtranFreqRelation=1415 eutranFreqToQciProfileRelation  a5Thr1rsrqFreqQciOffset=0,a5Thr2rsrqFreqQciOffset=240,lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set EUtranCell.*,EUtranFreqRelation=3690 eutranFreqToQciProfileRelation  a5Thr1rsrqFreqQciOffset=0,a5Thr2rsrqFreqQciOffset=240,lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set EUtranCell.*,UeMeasControl=1,ReportConfigB2Geran=1  hysteresisB2RsrqOffset 100
set EUtranCell.*,UeMeasControl=1,ReportConfigB2Geran=1  b2Threshold1Rsrq -195
set EUtranCell.*,UeMeasControl=1,ReportConfigB2Utra=1  hysteresisB2RsrqOffset 100
set EUtranCell.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold2Rsrq  -170
Set Lm=1,FeatureState=CXC4011666 featureState 0
set Lm=1,FeatureState=CXC4011074 featureState 1
set Lm=1,FeatureState=CXC4012316 featureState 1
set Lm=1,FeatureState=CXC4012261 featureState 1
set Lm=1,FeatureState=CXC4011373 featureState 1

set QciTable=default,QciProfilePredefined=.* resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=.* srsAllocationStrategy 1
lset EUtranCellFDD.*,UeMeasControl PrioOffsetPerQci qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,offsetPerQciPrio=7
lset EUtranCellTDD.*,UeMeasControl PrioOffsetPerQci qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,offsetPerQciPrio=7
set EUtranCellTDD excludeInterFreqAtCritical true
set EUtranCellFDD excludeInterFreqAtCritical False
set EUtranCell.* srvccDelayTimer 3000
set EUtranCellTDD.* qQualMin -34
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA1UlSearch 480
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2UlCritical 480

crn ENodeBFunction=1,TimerProfile=0
tWaitForRrcConnReest 6
tRrcConnectionReconfiguration 8
tRrcConnReest 3
tRelocOverall 10
end

set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 timerProfileRef ENodeBFunction=1,TimerProfile=0
EUtranCellTDD=.*                      interferenceThresholdSinrClpc -100
set EUtranCellFDD=.*,EUtranFreqRelation=1415 caFreqPriority    5
set EUtranCellTDD=.*,EUtranFreqRelation=1415 caFreqPriority    5
set EUtranCellFDD=.*,EUtranFreqRelation=39294 caFreqPriority    6
set EUtranCellTDD=.*,EUtranFreqRelation=39294 caFreqPriority    6
set EUtranCellFDD=.*,EUtranFreqRelation=39150 caFreqPriority    7
set EUtranCellTDD=.*,EUtranFreqRelation=39150 caFreqPriority    7
set CarrierAggregationFunction=1                            a6TriggerSCellDeconfig false
set CarrierAggregationFunction=1                            sCellSelectionMode 2
set CarrierAggregationFunction=1                            waitForAdditionalSCellOpportunity 3000

set SystemFunctions=1,Lm=1,FeatureState=CXC4012485 featureState 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4012199 featureState 1
set SystemFunctions=1,Lm=1,FeatureState=ASGHPerfPkg featureState 1
set SystemFunctions=1,Lm=1,FeatureState=OptimizedRRCConnectionReleaseControl featureState 1

cr ENodeBFunction=1,SubscriberGroupProfile=1
set ENodeBFunction=1,SubscriberGroupProfile=1 bearerTriggerList qci=1
set ENodeBFunction=1,SubscriberGroupProfile=1 fastACqiReportEnabled true

set EUtranCell.*DD=.*                                  dlMaxRetxRrcReleaseThr 8
set EUtranCell.*DD=.*                                  tPollRetxRrcReleaseDl 80

set SystemFunctions=1,Lm=1,FeatureState=CXC4012356 featureState 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4011913 featureState 0
set SystemFunctions=1,Lm=1,FeatureState=CXC4011984 featureState 0
set SystemFunctions=1,Lm=1,FeatureState=CXC4012505 featureState 1


set DynamicBlerTarget=1 dlActivitySubscrDelay 1



cr ENodeBFunction=1,SubscriberGroupProfile=1
set ENodeBFunction=1,SubscriberGroupProfile=1 bearerTriggerList qci=1
set SubscriberGroupProfile=1 profilePriority 10
set SubscriberGroupProfile=1 dlDynBlerTargetMax -1



cr ENodeBFunction=1,SubscriberGroupProfile=2
set ENodeBFunction=1,SubscriberGroupProfile=2 bearerTriggerList qci=6
set SubscriberGroupProfile=2 profilePriority 1
set SubscriberGroupProfile=2 dlDynBlerTargetMin 10
set SubscriberGroupProfile=2 dlDynBlerTargetMax 60
set SubscriberGroupProfile=2 dlDynBlerTargetAlg 1



cr ENodeBFunction=1,SubscriberGroupProfile=3
set ENodeBFunction=1,SubscriberGroupProfile=3 bearerTriggerList qci=7
set SubscriberGroupProfile=3 profilePriority 1
set SubscriberGroupProfile=3 dlDynBlerTargetMin 10
set SubscriberGroupProfile=3 dlDynBlerTargetMax 60
set SubscriberGroupProfile=3 dlDynBlerTargetAlg 1



cr ENodeBFunction=1,SubscriberGroupProfile=4
set ENodeBFunction=1,SubscriberGroupProfile=4 bearerTriggerList qci=8
set SubscriberGroupProfile=4 profilePriority 1
set SubscriberGroupProfile=4 dlDynBlerTargetMin 10
set SubscriberGroupProfile=4 dlDynBlerTargetMax 60
set SubscriberGroupProfile=4 dlDynBlerTargetAlg 1



cr ENodeBFunction=1,SubscriberGroupProfile=5
set ENodeBFunction=1,SubscriberGroupProfile=5 bearerTriggerList qci=9
set SubscriberGroupProfile=5 profilePriority 1
set SubscriberGroupProfile=5 dlDynBlerTargetMin 10
set SubscriberGroupProfile=5 dlDynBlerTargetMax 60
set SubscriberGroupProfile=5 dlDynBlerTargetAlg 1

confb+
set QciTable=default,QciProfilePredefined=qci[6-9]$ dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci1 dlResourceAllocationStrategy 1
confb-

set EUtranCell.* eUlFssSwitchThresh 30

set . ductIntOpMode 3
set . DuctIntPerfTuning ductIntBgNoiseThr=-100,ductIntCharSeqCorrPeakThr=50,ductIntCharSeqPwrDiff=5,ductIntRedRecovThr=10,ductIntRedTriggerThr=20
set ENodeBFunction=1 ductIntCharInfoScheme 0
scw 4292:10
scw 1225:50
scw 4285:5

get =1 ^fingerprint$ > $fp
get ^ENodeBFunction=1 eNBId > $enbid
l echo $fp > $fp.txt
$Nodename = `$gawk  '{ print substr ($NR,2,6) }' $fp.txt
l rm $fp.txt

confbd+

confbd+
ma unlockedcells ^eutrancell administrativestate 1
bl unlockedcells
wait 10

set AtmosphericDuctInterferenceReduction Featurestate 1
set CarrierAggregation Featurestate 1
set CarrierAggregation FDD-TDD Featurestate 1
set CarrierAggregation-AwareIFLB Featurestate 1
set DynamicSCellSelectionForCarrierAggregation Featurestate 1
set FDDandTDDonSameeNodeB Featurestate 1
set ThreeDlCarrierAggregation Featurestate 0
set FourDlCarrierAggregation Featurestate 0
set Dl256Qam Featurestate 1
set EnhancedPdcchLa Featurestate 1
set VoLTEOptimizedCA Featurestate 1

set CXC4012256 featurestate 1
set CXC4011666 featurestate 1
set CXC4012259 featurestate 1
set CXC4012111 featureState 1

set EUtranCell.*DD=.*,EUtranFreqRelation=.*          caTriggeredRedirectionActive true
set CarrierAggregationFunction=1                            pdcchEnhancedLaForVolte true
set EUtranCellFDD=.*                                  sCellHandlingAtVolteCall 0
set EUtranCellTDD=.*                                  sCellHandlingAtVolteCall 1

get =1 ^fingerprint$ > $fp
get ^ENodeBFunction=1 eNBId > $enbid
l echo $fp > $fp.txt
$Nodename = `$gawk  '{ print substr ($NR,2,6) }' $fp.txt
l rm $fp.txt

confbd+

set EUtranCellTDD=.*,EUtranFreqRelation=39150,EUtranCellRelation=.* sCellCandidate    1
set EUtranCellTDD=.*,EUtranFreqRelation=39294,EUtranCellRelation=.* sCellCandidate    1
set EUtranCellTDD=.*,EUtranFreqRelation=1415,EUtranCellRelation=.* sCellCandidate    0
set EUtranCellTDD=.*,EUtranFreqRelation=3690,EUtranCellRelation=.* sCellCandidate    0
set EUtranCellTDD=.*,EUtranFreqRelation=215,EUtranCellRelation=.* sCellCandidate    0

set EUtranCellFDD=.*[K-P],EUtranFreqRelation=39150,EUtranCellRelation=.* sCellCandidate    1
set EUtranCellFDD=.*[K-P],EUtranFreqRelation=39294,EUtranCellRelation=.* sCellCandidate    1
set EUtranCellFDD=.*[K-P]1,EUtranFreqRelation=39150,EUtranCellRelation=.* sCellCandidate    1
set EUtranCellFDD=.*[K-P]1,EUtranFreqRelation=39294,EUtranCellRelation=.* sCellCandidate    1
set EUtranCellFDD=.*[K-P],EUtranFreqRelation=1415,EUtranCellRelation=.* sCellCandidate    1
set EUtranCellFDD=.*[K-P]1,EUtranFreqRelation=1415,EUtranCellRelation=.* sCellCandidate    1
set EUtranCellFDD=.*[K-P],EUtranFreqRelation=3690,EUtranCellRelation=.* sCellCandidate    0
set EUtranCellFDD=.*[K-P]1,EUtranFreqRelation=3690,EUtranCellRelation=.* sCellCandidate    1
set EUtranCellFDD=.*[K-P],EUtranFreqRelation=215,EUtranCellRelation=.* sCellCandidate    0
set EUtranCellFDD=.*[K-P]1,EUtranFreqRelation=215,EUtranCellRelation=.* sCellCandidate    0

set ENodeBFunction=1,EUtranCellFDD=AP_E_F3_OM_$Nodename[A-D]_[A-D],EUtranFreqRelation=39150,EUtranCellRelation=.* sCellCandidate    1
set ENodeBFunction=1,EUtranCellFDD=AP_E_F3_OM_$Nodename[A-D]_[A-D],EUtranFreqRelation=39294,EUtranCellRelation=.* sCellCandidate    1
set ENodeBFunction=1,EUtranCellFDD=AP_E_F3_OM_$Nodename[A-D]_[A-D],EUtranFreqRelation=3690,EUtranCellRelation=.* sCellCandidate    0
set ENodeBFunction=1,EUtranCellFDD=AP_E_F3_OM_$Nodename[A-D]_[A-D],EUtranFreqRelation=1415,EUtranCellRelation=.* sCellCandidate    1
set ENodeBFunction=1,EUtranCellFDD=AP_E_F3_OM_$Nodename[A-D]_[A-D],EUtranFreqRelation=215,EUtranCellRelation=.* sCellCandidate    0

set EUtranCellFDD=.*[G-J],EUtranFreqRelation=39150,EUtranCellRelation=.* sCellCandidate    0
set EUtranCellFDD=.*[G-J],EUtranFreqRelation=39294,EUtranCellRelation=.* sCellCandidate    0
set EUtranCellFDD=.*[G-J],EUtranFreqRelation=1415,EUtranCellRelation=.* sCellCandidate    0
set EUtranCellFDD=.*[G-J],EUtranFreqRelation=215,EUtranCellRelation=.* sCellCandidate    0
set EUtranCellFDD=.*[G-J],EUtranFreqRelation=3690,EUtranCellRelation=.* sCellCandidate    1
set ENodeBFunction=1,EUtranCellFDD=AP_E_F8_OM_$Nodename[A-D]_[A-D],EUtranFreqRelation=39150,EUtranCellRelation=.* sCellCandidate    0
set ENodeBFunction=1,EUtranCellFDD=AP_E_F8_OM_$Nodename[A-D]_[A-D],EUtranFreqRelation=39294,EUtranCellRelation=.* sCellCandidate    0
set ENodeBFunction=1,EUtranCellFDD=AP_E_F8_OM_$Nodename[A-D]_[A-D],EUtranFreqRelation=1415,EUtranCellRelation=.* sCellCandidate    0
set ENodeBFunction=1,EUtranCellFDD=AP_E_F8_OM_$Nodename[A-D]_[A-D],EUtranFreqRelation=3690,EUtranCellRelation=.* sCellCandidate    0
set ENodeBFunction=1,EUtranCellFDD=AP_E_F8_OM_$Nodename[A-D]_[A-D],EUtranFreqRelation=215,EUtranCellRelation=.* sCellCandidate    0

confbd+

set EUtranCellTDD=.*                                  specialSubframePattern 7
set ENodeBFunction=1                                        ductIntFlexibleDetectionEnabled false

set InterENBCarrierAggregation Featurestate 1
set AutoSCellMgmFunction Featurestate 1
set CXC4012123 featurestate 1

Set EUtranCellFDD=.*,EUtranFreqRelation=.*,EUtranCellRelation=.* sCellCandidate 2
Set EUtranCellTDD=.*,EUtranFreqRelation=.*,EUtranCellRelation=.* sCellCandidate 2
Set EUtranCell.*=.* sCellHandlingAtVolteCall 1
Set CarrierAggregationFunction=1,AutoSCellMgmFunction=1     asmInterFMeasReportDecr 1
set CarrierAggregationFunction=1,AutoSCellMgmFunction=1     asmInterFMeasReportIncr  10
set CarrierAggregationFunction=1,AutoSCellMgmFunction=1     asmInterFMeasReportMax 100
set CarrierAggregationFunction=1,AutoSCellMgmFunction=1     asmInterFMeasReportMin 20
set CarrierAggregationFunction=1,AutoSCellMgmFunction=1     sCellCandidateLimit 50
set EUtranCellFDD=.*,EUtranFreqRelation=.* asmSCellDetection 0
set EUtranCellTDD=.*,EUtranFreqRelation=.* asmSCellDetection 0
set EUtranCellTDD=.*,EUtranFreqRelation=39150 asmSCellDetection 3
set EUtranCellTDD=.*,EUtranFreqRelation=39294 asmSCellDetection 3
set EUtranCellFDD=.*[K-P],EUtranFreqRelation=39150 asmSCellDetection 3
set EUtranCellFDD=.*[K-P],EUtranFreqRelation=39294 asmSCellDetection 3
set EUtranCellFDD=.*[K-P]1,EUtranFreqRelation=39150 asmSCellDetection 3
set EUtranCellFDD=.*[K-P]1,EUtranFreqRelation=39294 asmSCellDetection 3
set EUtranCellTDD=.*,EUtranFreqRelation=39150 asmHitRateAddThreshold 15
set EUtranCellTDD=.*,EUtranFreqRelation=39294 asmHitRateAddThreshold 15
set EUtranCellFDD=.*[K-P],EUtranFreqRelation=39150 asmHitRateAddThreshold 15
set EUtranCellFDD=.*[K-P],EUtranFreqRelation=39294 asmHitRateAddThreshold 15
set EUtranCellFDD=.*[K-P]1,EUtranFreqRelation=39150 asmHitRateAddThreshold 15
set EUtranCellFDD=.*[K-P]1,EUtranFreqRelation=39294 asmHitRateAddThreshold 15
set EUtranCellTDD=.*,EUtranFreqRelation=39150 asmHitRateRemoveThreshold 5
set EUtranCellTDD=.*,EUtranFreqRelation=39294 asmHitRateRemoveThreshold 5
set EUtranCellFDD=.*[K-P],EUtranFreqRelation=39150 asmHitRateRemoveThreshold 5
set EUtranCellFDD=.*[K-P],EUtranFreqRelation=39294 asmHitRateRemoveThreshold 5
set EUtranCellFDD=.*[K-P]1,EUtranFreqRelation=39150 asmHitRateRemoveThreshold 5
set EUtranCellFDD=.*[K-P]1,EUtranFreqRelation=39294 asmHitRateRemoveThreshold 5

Set EUtranCellFDD=.*,EUtranFreqRelation=.*,EUtranCellRelation=.* sCellCandidate 2
Set EUtranCellTDD=.*,EUtranFreqRelation=.*,EUtranCellRelation=.* sCellCandidate 2
Set EUtranCell.*=.* sCellHandlingAtVolteCall 1
Set CarrierAggregationFunction=1,AutoSCellMgmFunction=1     asmInterFMeasReportDecr 1
set CarrierAggregationFunction=1,AutoSCellMgmFunction=1     asmInterFMeasReportIncr  10
set CarrierAggregationFunction=1,AutoSCellMgmFunction=1     asmInterFMeasReportMax 100
set CarrierAggregationFunction=1,AutoSCellMgmFunction=1     asmInterFMeasReportMin 20
set CarrierAggregationFunction=1,AutoSCellMgmFunction=1     sCellCandidateLimit 50
set EUtranCellFDD=.*,EUtranFreqRelation=.* asmSCellDetection 0
set EUtranCellTDD=.*,EUtranFreqRelation=.* asmSCellDetection 0
set EUtranCellTDD=.*,EUtranFreqRelation=39150 asmSCellDetection 3
set EUtranCellTDD=.*,EUtranFreqRelation=39294 asmSCellDetection 3
set EUtranCellFDD=.*AP_E_F3_OM_$Nodename[A-D]_[A-D],EUtranFreqRelation=39150 asmSCellDetection 3
set EUtranCellFDD=.*AP_E_F3_OM_$Nodename[A-D]_[L-O],EUtranFreqRelation=39150 asmSCellDetection 3
set EUtranCellFDD=.*AP_E_F3_OM_$Nodename[A-D]_[A-D],EUtranFreqRelation=39294 asmSCellDetection 3
set EUtranCellFDD=.*AP_E_F3_OM_$Nodename[A-D]_[L-O],EUtranFreqRelation=39294 asmSCellDetection 3
set EUtranCellTDD=.*,EUtranFreqRelation=39150 asmHitRateAddThreshold 15
set EUtranCellTDD=.*,EUtranFreqRelation=39294 asmHitRateAddThreshold 15
set EUtranCellFDD=.*AP_E_F3_OM_$Nodename[A-D]_[A-D],EUtranFreqRelation=39150 asmHitRateAddThreshold 15
set EUtranCellFDD=.*AP_E_F3_OM_$Nodename[A-D]_[L-O],EUtranFreqRelation=39150 asmHitRateAddThreshold 15
set EUtranCellFDD=.*AP_E_F3_OM_$Nodename[A-D]_[A-D],EUtranFreqRelation=39294 asmHitRateAddThreshold 15
set EUtranCellFDD=.*AP_E_F3_OM_$Nodename[A-D]_[L-O],EUtranFreqRelation=39294 asmHitRateAddThreshold 15
set EUtranCellTDD=.*,EUtranFreqRelation=39150 asmHitRateRemoveThreshold 5
set EUtranCellTDD=.*,EUtranFreqRelation=39294 asmHitRateRemoveThreshold 5
set EUtranCellFDD=.*AP_E_F3_OM_$Nodename[A-D]_[A-D],EUtranFreqRelation=39150 asmHitRateRemoveThreshold 5
set EUtranCellFDD=.*AP_E_F3_OM_$Nodename[A-D]_[L-O],EUtranFreqRelation=39150 asmHitRateRemoveThreshold 5
set EUtranCellFDD=.*AP_E_F3_OM_$Nodename[A-D]_[A-D],EUtranFreqRelation=39294 asmHitRateRemoveThreshold 5
set EUtranCellFDD=.*AP_E_F3_OM_$Nodename[A-D]_[L-O],EUtranFreqRelation=39294 asmHitRateRemoveThreshold 5
set EUtranCell.DD=.*                      outOfCoverageSparseGrantingBsr 8
EUtranCellTDD=.*                      rxSinrTargetClpc  20
set GeraNetwork=1,ExternalGeranCell       rimCapable        0
set GeraNetwork=1,ExternalGeranCell       rimAssociationStatus 0
set EUtranCell.DD=.*,GeranFreqGroupRelation=1 mobilityAction    0
set EUtranCell.DD=.*,GeranFreqGroupRelation=1 mobilityActionCsfb 1

#################################################################################

set EUtranCell.*DD=.*,GeranFreqGroupRelation=1    voicePrio         -1
set EUtranCell.*DD=.*,GeranFreqGroupRelation=1    voicePrioBr       -1

################ GPLV20 New parameters END##################################################
################ GPLV23 New LMS END##################################################

confbd+

get 0 networkManagedElementId > $Nodename

ma TAFDQOS ^eutrancell arfcn ^1415

for $mo in TAFDQOS
$mordn = rdn($mo)
set $mordn,EUtranFreqRelation=1415 threshXHigh 14
set $mordn,EUtranFreqRelation=3690 threshXHigh 14
set $mordn,EUtranFreqRelation=39150 threshXHigh 12
set $mordn,EUtranFreqRelation=39294 threshXHigh 12
set $mordn,EUtranFreqRelation=1415 threshXLow 14
set $mordn,EUtranFreqRelation=3690 threshXLow 12
set $mordn,EUtranFreqRelation=39150 threshXLow 14
set $mordn,EUtranFreqRelation=39294 threshXLow 14
set $mordn systemInformationBlock3 Struct{16},sNonIntraSearch=8
set $mordn threshServingLow 6
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrp  -106
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2SearchRsrp  20
set $mordn,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets a1a2ThrRsrpQciOffset=2,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=1415 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=3690 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39150 a5Thr1RsrpFreqOffset 10
set $mordn,EUtranFreqRelation=39294 a5Thr1RsrpFreqOffset 10
set $mordn,EUtranFreqRelation=1415 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=3690 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39150 a5Thr2RsrpFreqOffset -2
set $mordn,EUtranFreqRelation=39294 a5Thr2RsrpFreqOffset 0
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrp -116
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp -114
set $mordn,EUtranFreqRelation=1415 EutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=0,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=3690 EutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=12,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=39150 EutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=-2,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=39294 EutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=-2,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=1415 EutranFreqToQciProfileRelation a5Thr2RsrpFreqQciOffset=0,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=3690 EutranFreqToQciProfileRelation a5Thr2RsrpFreqQciOffset=6,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=39150 EutranFreqToQciProfileRelation a5Thr2RsrpFreqQciOffset=66,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=39294 EutranFreqToQciProfileRelation a5Thr2RsrpFreqQciOffset=64,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
done


ma TAL90QOS ^eutrancell arfcn ^3690

for $mo in TAL90QOS
$mordn = rdn($mo)
set $mordn,EUtranFreqRelation=1415 threshXHigh 10
set $mordn,EUtranFreqRelation=3690 threshXHigh 14
set $mordn,EUtranFreqRelation=39150 threshXHigh 12
set $mordn,EUtranFreqRelation=39294 threshXHigh 12
set $mordn,EUtranFreqRelation=1415 threshXLow 16
set $mordn,EUtranFreqRelation=3690 threshXLow 16
set $mordn,EUtranFreqRelation=39150 threshXLow 16
set $mordn,EUtranFreqRelation=39294 threshXLow 16
set $mordn systemInformationBlock3 Struct{16},sNonIntraSearch=0
set $mordn threshServingLow 0
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrp  -94
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2SearchRsrp  20
set $mordn,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets a1a2ThrRsrpQciOffset=-14,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=1415 a5Thr1RsrpFreqOffset -54
set $mordn,EUtranFreqRelation=3690 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39150 a5Thr1RsrpFreqOffset -54
set $mordn,EUtranFreqRelation=39294 a5Thr1RsrpFreqOffset -54
set $mordn,EUtranFreqRelation=1415 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=3690 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39150 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39294 a5Thr2RsrpFreqOffset 2
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrp -44
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp -116
set $mordn,EUtranFreqRelation=1415 EutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=54,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=3690 EutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=0,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=39150 EutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=70,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=39294 EutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=70,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=1415 EutranFreqToQciProfileRelation a5Thr2RsrpFreqQciOffset=10,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=3690 EutranFreqToQciProfileRelation a5Thr2RsrpFreqQciOffset=0,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=39150 EutranFreqToQciProfileRelation a5Thr2RsrpFreqQciOffset=66,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=39294 EutranFreqToQciProfileRelation a5Thr2RsrpFreqQciOffset=64,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
done



ma TATD20QOS ^eutrancell arfcn ^39150

for $mo in TATD20QOS
$mordn = rdn($mo)
set $mordn,EUtranFreqRelation=1415 threshXHigh 14
set $mordn,EUtranFreqRelation=3690 threshXHigh 14
set $mordn,EUtranFreqRelation=39150 threshXHigh 14
set $mordn,EUtranFreqRelation=39294 threshXHigh 12
set $mordn,EUtranFreqRelation=1415 threshXLow 14
set $mordn,EUtranFreqRelation=3690 threshXLow 62
set $mordn,EUtranFreqRelation=39150 threshXLow 0
set $mordn,EUtranFreqRelation=39294 threshXLow 14
set $mordn systemInformationBlock3 Struct{16},sNonIntraSearch=8
set $mordn threshServingLow 8
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrp  -114
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2SearchRsrp  20
set $mordn,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets a1a2ThrRsrpQciOffset=76,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=1415 a5Thr1RsrpFreqOffset 10
set $mordn,EUtranFreqRelation=3690 a5Thr1RsrpFreqOffset 10
set $mordn,EUtranFreqRelation=39150 a5Thr1RsrpFreqOffset 10
set $mordn,EUtranFreqRelation=39294 a5Thr1RsrpFreqOffset 10
set $mordn,EUtranFreqRelation=1415 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=3690 a5Thr2RsrpFreqOffset 66
set $mordn,EUtranFreqRelation=39150 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39294 a5Thr2RsrpFreqOffset 0
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrp -124
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp -112
set $mordn,EUtranFreqRelation=1415 EutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=76,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=3690 EutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=76,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=39150 EutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=6,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=39294 EutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=6,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=1415 EutranFreqToQciProfileRelation a5Thr2RsrpFreqQciOffset=0,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=3690 EutranFreqToQciProfileRelation a5Thr2RsrpFreqQciOffset=-4,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=39150 EutranFreqToQciProfileRelation a5Thr2RsrpFreqQciOffset=58,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=39294 EutranFreqToQciProfileRelation a5Thr2RsrpFreqQciOffset=62,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
done


ma TATD10QOS ^eutrancell arfcn ^39294
for $mo in TATD10QOS
$mordn = rdn($mo)
set $mordn,EUtranFreqRelation=1415 threshXHigh 14
set $mordn,EUtranFreqRelation=3690 threshXHigh 14
set $mordn,EUtranFreqRelation=39150 threshXHigh 12
set $mordn,EUtranFreqRelation=39294 threshXHigh 12
set $mordn,EUtranFreqRelation=1415 threshXLow 14
set $mordn,EUtranFreqRelation=3690 threshXLow 62
set $mordn,EUtranFreqRelation=39150 threshXLow 0
set $mordn,EUtranFreqRelation=39294 threshXLow 0
set $mordn systemInformationBlock3 Struct{16},sNonIntraSearch=8
set $mordn threshServingLow 8
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrp  -114
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2SearchRsrp  20
set $mordn,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets a1a2ThrRsrpQciOffset=76,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=1415 a5Thr1RsrpFreqOffset 10
set $mordn,EUtranFreqRelation=3690 a5Thr1RsrpFreqOffset 10
set $mordn,EUtranFreqRelation=39150 a5Thr1RsrpFreqOffset 10
set $mordn,EUtranFreqRelation=39294 a5Thr1RsrpFreqOffset 10
set $mordn,EUtranFreqRelation=1415 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=3690 a5Thr2RsrpFreqOffset 66
set $mordn,EUtranFreqRelation=39150 a5Thr2RsrpFreqOffset -2
set $mordn,EUtranFreqRelation=39294 a5Thr2RsrpFreqOffset 0
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrp -124
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp -112
set $mordn,EUtranFreqRelation=1415 EutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=76,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=3690 EutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=76,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=39150 EutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=6,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=39294 EutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=6,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=1415 EutranFreqToQciProfileRelation a5Thr2RsrpFreqQciOffset=0,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=3690 EutranFreqToQciProfileRelation a5Thr2RsrpFreqQciOffset=-4,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=39150 EutranFreqToQciProfileRelation a5Thr2RsrpFreqQciOffset=64,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set $mordn,EUtranFreqRelation=39294 EutranFreqToQciProfileRelation a5Thr2RsrpFreqQciOffset=-4,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
done

####################################################################

set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5=1 hysteresisA5 20
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5=1 hysteresisA5 20

####################################################################

#####################  S1U alarm report  ###########################################

confb+

set SystemFunctions=1,Lm=1,FeatureState=CXC4012022 featureState 1
set SystemFunctions=1,Licensing=1,OptionalFeatureLicense=TransportPathCharMonitoring featureState 1
set ENodeBFunction=1                                        s1GtpuEchoEnable  1

##################################################################################

bl cell
lt all
wait 10

deb unlockedcells
$date = `date +%y%m%d_%H%M`
cvms LMS_$date
confbd-
###################################################################################





confbd

get ^ENodeBFunction=1 eNBId > $enbid

ma B31 ^eutrancell ^cellid$ 11
ma B32 ^eutrancell ^cellid$ 12
ma B33 ^eutrancell ^cellid$ 13
ma B34 ^eutrancell ^cellid$ 14
ma B81 ^eutrancell ^cellid$ 41
ma B82 ^eutrancell ^cellid$ 42
ma B83 ^eutrancell ^cellid$ 43
ma B84 ^eutrancell ^cellid$ 44
ma B11 ^eutrancell ^cellid$ 21
ma B12 ^eutrancell ^cellid$ 22
ma B13 ^eutrancell ^cellid$ 23
ma B14 ^eutrancell ^cellid$ 24
ma B21 ^eutrancell ^cellid$ 31
ma B22 ^eutrancell ^cellid$ 32
ma B23 ^eutrancell ^cellid$ 33
ma B24 ^eutrancell ^cellid$ 34
ma B51 ^eutrancell ^cellid$ 51
ma B52 ^eutrancell ^cellid$ 52
ma B53 ^eutrancell ^cellid$ 53
ma B54 ^eutrancell ^cellid$ 54
ma B61 ^eutrancell ^cellid$ 61
ma B62 ^eutrancell ^cellid$ 62
ma B63 ^eutrancell ^cellid$ 63
ma B64 ^eutrancell ^cellid$ 64
ma B71 ^eutrancell ^cellid$ 71
ma B72 ^eutrancell ^cellid$ 72
ma B73 ^eutrancell ^cellid$ 73
ma B74 ^eutrancell ^cellid$ 74



get B31 eutrancellfddid > $fdd3a
get B32 eutrancellfddid > $fdd3b
get B33 eutrancellfddid > $fdd3c
get B34 eutrancellfddid > $fdd3d
get B81 eutrancellfddid > $fdd8a
get B82 eutrancellfddid > $fdd8b
get B83 eutrancellfddid > $fdd8c
get B84 eutrancellfddid > $fdd8d
get B11 eutrancelltddid > $tdd1a
get B12 eutrancelltddid > $tdd1b
get B13 eutrancelltddid > $tdd1c
get B14 eutrancelltddid > $tdd1d
get B21 eutrancelltddid > $tdd2a
get B22 eutrancelltddid > $tdd2b
get B23 eutrancelltddid > $tdd2c
get B24 eutrancelltddid > $tdd2d
get B51 eutrancellfddid > $fdd5a
get B52 eutrancellfddid > $fdd5b
get B53 eutrancellfddid > $fdd5c
get B54 eutrancellfddid > $fdd5d
get B61 eutrancelltddid > $tdd6a
get B62 eutrancelltddid > $tdd6b
get B63 eutrancelltddid > $tdd6c
get B64 eutrancelltddid > $tdd6d
get B71 eutrancelltddid > $tdd7a
get B72 eutrancelltddid > $tdd7b
get B73 eutrancelltddid > $tdd7c
get B74 eutrancelltddid > $tdd7d


cr EUtranCellFDD=$fdd8a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-21
EUtranCellTDD=$tdd1a
cr EUtranCellFDD=$fdd8a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-22
EUtranCellTDD=$tdd1b
cr EUtranCellFDD=$fdd8a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-23
EUtranCellTDD=$tdd1c
cr EUtranCellFDD=$fdd8a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-24
EUtranCellTDD=$tdd1d
cr EUtranCellFDD=$fdd8a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-31
EUtranCellTDD=$tdd2a
cr EUtranCellFDD=$fdd8a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-32
EUtranCellTDD=$tdd2b
cr EUtranCellFDD=$fdd8a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-33
EUtranCellTDD=$tdd2c
cr EUtranCellFDD=$fdd8a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-34
EUtranCellTDD=$tdd2d
cr EUtranCellFDD=$fdd8a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-11
EUtranCellFDD=$fdd3a
cr EUtranCellFDD=$fdd8a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-12
EUtranCellFDD=$fdd3b
cr EUtranCellFDD=$fdd8a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-13
EUtranCellFDD=$fdd3c
cr EUtranCellFDD=$fdd8a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-14
EUtranCellFDD=$fdd3d
cr EUtranCellFDD=$fdd8a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-51
EUtranCellFDD=$fdd5a
cr EUtranCellFDD=$fdd8a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-52
EUtranCellFDD=$fdd5b
cr EUtranCellFDD=$fdd8a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-53
EUtranCellFDD=$fdd5c
cr EUtranCellFDD=$fdd8a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-54
EUtranCellFDD=$fdd5d
cr EUtranCellFDD=$fdd8a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-61
EUtranCellTDD=$tdd6a
cr EUtranCellFDD=$fdd8a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-62
EUtranCellTDD=$tdd6b
cr EUtranCellFDD=$fdd8a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-63
EUtranCellTDD=$tdd6c
cr EUtranCellFDD=$fdd8a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-64
EUtranCellTDD=$tdd6d
cr EUtranCellFDD=$fdd8a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-71
EUtranCellTDD=$tdd7a
cr EUtranCellFDD=$fdd8a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-72
EUtranCellTDD=$tdd7b
cr EUtranCellFDD=$fdd8a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-73
EUtranCellTDD=$tdd7c
cr EUtranCellFDD=$fdd8a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-74
EUtranCellTDD=$tdd7d


cr EUtranCellFDD=$fdd8b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-21
EUtranCellTDD=$tdd1a
cr EUtranCellFDD=$fdd8b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-22
EUtranCellTDD=$tdd1b
cr EUtranCellFDD=$fdd8b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-23
EUtranCellTDD=$tdd1c
cr EUtranCellFDD=$fdd8b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-24
EUtranCellTDD=$tdd1d
cr EUtranCellFDD=$fdd8b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-31
EUtranCellTDD=$tdd2a
cr EUtranCellFDD=$fdd8b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-32
EUtranCellTDD=$tdd2b
cr EUtranCellFDD=$fdd8b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-33
EUtranCellTDD=$tdd2c
cr EUtranCellFDD=$fdd8b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-34
EUtranCellTDD=$tdd2d
cr EUtranCellFDD=$fdd8b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-11
EUtranCellFDD=$fdd3a
cr EUtranCellFDD=$fdd8b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-12
EUtranCellFDD=$fdd3b
cr EUtranCellFDD=$fdd8b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-13
EUtranCellFDD=$fdd3c
cr EUtranCellFDD=$fdd8b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-14
EUtranCellFDD=$fdd3d
cr EUtranCellFDD=$fdd8b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-51
EUtranCellFDD=$fdd5a
cr EUtranCellFDD=$fdd8b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-52
EUtranCellFDD=$fdd5b
cr EUtranCellFDD=$fdd8b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-53
EUtranCellFDD=$fdd5c
cr EUtranCellFDD=$fdd8b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-54
EUtranCellFDD=$fdd5d
cr EUtranCellFDD=$fdd8b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-61
EUtranCellTDD=$tdd6a
cr EUtranCellFDD=$fdd8b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-62
EUtranCellTDD=$tdd6b
cr EUtranCellFDD=$fdd8b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-63
EUtranCellTDD=$tdd6c
cr EUtranCellFDD=$fdd8b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-64
EUtranCellTDD=$tdd6d
cr EUtranCellFDD=$fdd8b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-71
EUtranCellTDD=$tdd7a
cr EUtranCellFDD=$fdd8b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-72
EUtranCellTDD=$tdd7b
cr EUtranCellFDD=$fdd8b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-73
EUtranCellTDD=$tdd7c
cr EUtranCellFDD=$fdd8b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-74
EUtranCellTDD=$tdd7d


cr EUtranCellFDD=$fdd8c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-21
EUtranCellTDD=$tdd1a
cr EUtranCellFDD=$fdd8c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-22
EUtranCellTDD=$tdd1b
cr EUtranCellFDD=$fdd8c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-23
EUtranCellTDD=$tdd1c
cr EUtranCellFDD=$fdd8c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-24
EUtranCellTDD=$tdd1d
cr EUtranCellFDD=$fdd8c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-31
EUtranCellTDD=$tdd2a
cr EUtranCellFDD=$fdd8c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-32
EUtranCellTDD=$tdd2b
cr EUtranCellFDD=$fdd8c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-33
EUtranCellTDD=$tdd2c
cr EUtranCellFDD=$fdd8c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-34
EUtranCellTDD=$tdd2d
cr EUtranCellFDD=$fdd8c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-11
EUtranCellFDD=$fdd3a
cr EUtranCellFDD=$fdd8c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-12
EUtranCellFDD=$fdd3b
cr EUtranCellFDD=$fdd8c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-13
EUtranCellFDD=$fdd3c
cr EUtranCellFDD=$fdd8c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-14
EUtranCellFDD=$fdd3d
cr EUtranCellFDD=$fdd8c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-51
EUtranCellFDD=$fdd5a
cr EUtranCellFDD=$fdd8c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-52
EUtranCellFDD=$fdd5b
cr EUtranCellFDD=$fdd8c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-53
EUtranCellFDD=$fdd5c
cr EUtranCellFDD=$fdd8c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-54
EUtranCellFDD=$fdd5d
cr EUtranCellFDD=$fdd8c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-61
EUtranCellTDD=$tdd6a
cr EUtranCellFDD=$fdd8c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-62
EUtranCellTDD=$tdd6b
cr EUtranCellFDD=$fdd8c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-63
EUtranCellTDD=$tdd6c
cr EUtranCellFDD=$fdd8c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-64
EUtranCellTDD=$tdd6d
cr EUtranCellFDD=$fdd8c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-71
EUtranCellTDD=$tdd7a
cr EUtranCellFDD=$fdd8c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-72
EUtranCellTDD=$tdd7b
cr EUtranCellFDD=$fdd8c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-73
EUtranCellTDD=$tdd7c
cr EUtranCellFDD=$fdd8c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-74
EUtranCellTDD=$tdd7d


cr EUtranCellFDD=$fdd8d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-21
EUtranCellTDD=$tdd1a
cr EUtranCellFDD=$fdd8d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-22
EUtranCellTDD=$tdd1b
cr EUtranCellFDD=$fdd8d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-23
EUtranCellTDD=$tdd1c
cr EUtranCellFDD=$fdd8d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-24
EUtranCellTDD=$tdd1d
cr EUtranCellFDD=$fdd8d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-31
EUtranCellTDD=$tdd2a
cr EUtranCellFDD=$fdd8d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-32
EUtranCellTDD=$tdd2b
cr EUtranCellFDD=$fdd8d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-33
EUtranCellTDD=$tdd2c
cr EUtranCellFDD=$fdd8d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-34
EUtranCellTDD=$tdd2d
cr EUtranCellFDD=$fdd8d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-11
EUtranCellFDD=$fdd3a
cr EUtranCellFDD=$fdd8d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-12
EUtranCellFDD=$fdd3b
cr EUtranCellFDD=$fdd8d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-13
EUtranCellFDD=$fdd3c
cr EUtranCellFDD=$fdd8d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-14
EUtranCellFDD=$fdd3d
cr EUtranCellFDD=$fdd8d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-51
EUtranCellFDD=$fdd5a
cr EUtranCellFDD=$fdd8d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-52
EUtranCellFDD=$fdd5b
cr EUtranCellFDD=$fdd8d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-53
EUtranCellFDD=$fdd5c
cr EUtranCellFDD=$fdd8d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-54
EUtranCellFDD=$fdd5d
cr EUtranCellFDD=$fdd8d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-61
EUtranCellTDD=$tdd6a
cr EUtranCellFDD=$fdd8d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-62
EUtranCellTDD=$tdd6b
cr EUtranCellFDD=$fdd8d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-63
EUtranCellTDD=$tdd6c
cr EUtranCellFDD=$fdd8d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-64
EUtranCellTDD=$tdd6d
cr EUtranCellFDD=$fdd8d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-71
EUtranCellTDD=$tdd7a
cr EUtranCellFDD=$fdd8d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-72
EUtranCellTDD=$tdd7b
cr EUtranCellFDD=$fdd8d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-73
EUtranCellTDD=$tdd7c
cr EUtranCellFDD=$fdd8d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-74
EUtranCellTDD=$tdd7d




cr EUtranCellFDD=$fdd3a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-21
EUtranCellTDD=$tdd1a
cr EUtranCellFDD=$fdd3a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-22
EUtranCellTDD=$tdd1b
cr EUtranCellFDD=$fdd3a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-23
EUtranCellTDD=$tdd1c
cr EUtranCellFDD=$fdd3a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-24
EUtranCellTDD=$tdd1d
cr EUtranCellFDD=$fdd3a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-31
EUtranCellTDD=$tdd2a
cr EUtranCellFDD=$fdd3a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-32
EUtranCellTDD=$tdd2b
cr EUtranCellFDD=$fdd3a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-33
EUtranCellTDD=$tdd2c
cr EUtranCellFDD=$fdd3a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-34
EUtranCellTDD=$tdd2d
cr EUtranCellFDD=$fdd3a,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-41
EUtranCellFDD=$fdd8a
cr EUtranCellFDD=$fdd3a,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-42
EUtranCellFDD=$fdd8b
cr EUtranCellFDD=$fdd3a,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-43
EUtranCellFDD=$fdd8c
cr EUtranCellFDD=$fdd3a,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-44
EUtranCellFDD=$fdd8d
cr EUtranCellFDD=$fdd3a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-51
EUtranCellFDD=$fdd5a
cr EUtranCellFDD=$fdd3a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-52
EUtranCellFDD=$fdd5b
cr EUtranCellFDD=$fdd3a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-53
EUtranCellFDD=$fdd5c
cr EUtranCellFDD=$fdd3a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-54
EUtranCellFDD=$fdd5d
cr EUtranCellFDD=$fdd3a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-61
EUtranCellTDD=$tdd6a
cr EUtranCellFDD=$fdd3a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-62
EUtranCellTDD=$tdd6b
cr EUtranCellFDD=$fdd3a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-63
EUtranCellTDD=$tdd6c
cr EUtranCellFDD=$fdd3a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-64
EUtranCellTDD=$tdd6d
cr EUtranCellFDD=$fdd3a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-71
EUtranCellTDD=$tdd7a
cr EUtranCellFDD=$fdd3a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-72
EUtranCellTDD=$tdd7b
cr EUtranCellFDD=$fdd3a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-73
EUtranCellTDD=$tdd7c
cr EUtranCellFDD=$fdd3a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-74
EUtranCellTDD=$tdd7d



cr EUtranCellFDD=$fdd3b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-21
EUtranCellTDD=$tdd1a
cr EUtranCellFDD=$fdd3b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-22
EUtranCellTDD=$tdd1b
cr EUtranCellFDD=$fdd3b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-23
EUtranCellTDD=$tdd1c
cr EUtranCellFDD=$fdd3b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-24
EUtranCellTDD=$tdd1d
cr EUtranCellFDD=$fdd3b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-31
EUtranCellTDD=$tdd2a
cr EUtranCellFDD=$fdd3b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-32
EUtranCellTDD=$tdd2b
cr EUtranCellFDD=$fdd3b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-33
EUtranCellTDD=$tdd2c
cr EUtranCellFDD=$fdd3b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-34
EUtranCellTDD=$tdd2d
cr EUtranCellFDD=$fdd3b,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-41
EUtranCellFDD=$fdd8a
cr EUtranCellFDD=$fdd3b,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-42
EUtranCellFDD=$fdd8b
cr EUtranCellFDD=$fdd3b,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-43
EUtranCellFDD=$fdd8c
cr EUtranCellFDD=$fdd3b,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-44
EUtranCellFDD=$fdd8d
cr EUtranCellFDD=$fdd3b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-51
EUtranCellFDD=$fdd5a
cr EUtranCellFDD=$fdd3b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-52
EUtranCellFDD=$fdd5b
cr EUtranCellFDD=$fdd3b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-53
EUtranCellFDD=$fdd5c
cr EUtranCellFDD=$fdd3b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-54
EUtranCellFDD=$fdd5d
cr EUtranCellFDD=$fdd3b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-61
EUtranCellTDD=$tdd6a
cr EUtranCellFDD=$fdd3b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-62
EUtranCellTDD=$tdd6b
cr EUtranCellFDD=$fdd3b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-63
EUtranCellTDD=$tdd6c
cr EUtranCellFDD=$fdd3b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-64
EUtranCellTDD=$tdd6d
cr EUtranCellFDD=$fdd3b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-71
EUtranCellTDD=$tdd7a
cr EUtranCellFDD=$fdd3b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-72
EUtranCellTDD=$tdd7b
cr EUtranCellFDD=$fdd3b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-73
EUtranCellTDD=$tdd7c
cr EUtranCellFDD=$fdd3b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-74
EUtranCellTDD=$tdd7d



cr EUtranCellFDD=$fdd3c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-21
EUtranCellTDD=$tdd1a
cr EUtranCellFDD=$fdd3c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-22
EUtranCellTDD=$tdd1b
cr EUtranCellFDD=$fdd3c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-23
EUtranCellTDD=$tdd1c
cr EUtranCellFDD=$fdd3c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-24
EUtranCellTDD=$tdd1d
cr EUtranCellFDD=$fdd3c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-31
EUtranCellTDD=$tdd2a
cr EUtranCellFDD=$fdd3c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-32
EUtranCellTDD=$tdd2b
cr EUtranCellFDD=$fdd3c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-33
EUtranCellTDD=$tdd2c
cr EUtranCellFDD=$fdd3c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-34
EUtranCellTDD=$tdd2d
cr EUtranCellFDD=$fdd3c,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-41
EUtranCellFDD=$fdd8a
cr EUtranCellFDD=$fdd3c,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-42
EUtranCellFDD=$fdd8b
cr EUtranCellFDD=$fdd3c,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-43
EUtranCellFDD=$fdd8c
cr EUtranCellFDD=$fdd3c,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-44
EUtranCellFDD=$fdd8d
cr EUtranCellFDD=$fdd3c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-51
EUtranCellFDD=$fdd5a
cr EUtranCellFDD=$fdd3c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-52
EUtranCellFDD=$fdd5b
cr EUtranCellFDD=$fdd3c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-53
EUtranCellFDD=$fdd5c
cr EUtranCellFDD=$fdd3c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-54
EUtranCellFDD=$fdd5d
cr EUtranCellFDD=$fdd3c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-61
EUtranCellTDD=$tdd6a
cr EUtranCellFDD=$fdd3c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-62
EUtranCellTDD=$tdd6b
cr EUtranCellFDD=$fdd3c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-63
EUtranCellTDD=$tdd6c
cr EUtranCellFDD=$fdd3c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-64
EUtranCellTDD=$tdd6d
cr EUtranCellFDD=$fdd3c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-71
EUtranCellTDD=$tdd7a
cr EUtranCellFDD=$fdd3c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-72
EUtranCellTDD=$tdd7b
cr EUtranCellFDD=$fdd3c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-73
EUtranCellTDD=$tdd7c
cr EUtranCellFDD=$fdd3c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-74
EUtranCellTDD=$tdd7d



cr EUtranCellFDD=$fdd3d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-21
EUtranCellTDD=$tdd1a
cr EUtranCellFDD=$fdd3d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-22
EUtranCellTDD=$tdd1b
cr EUtranCellFDD=$fdd3d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-23
EUtranCellTDD=$tdd1c
cr EUtranCellFDD=$fdd3d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-24
EUtranCellTDD=$tdd1d
cr EUtranCellFDD=$fdd3d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-31
EUtranCellTDD=$tdd2a
cr EUtranCellFDD=$fdd3d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-32
EUtranCellTDD=$tdd2b
cr EUtranCellFDD=$fdd3d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-33
EUtranCellTDD=$tdd2c
cr EUtranCellFDD=$fdd3d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-34
EUtranCellTDD=$tdd2d
cr EUtranCellFDD=$fdd3d,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-41
EUtranCellFDD=$fdd8a
cr EUtranCellFDD=$fdd3d,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-42
EUtranCellFDD=$fdd8b
cr EUtranCellFDD=$fdd3d,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-43
EUtranCellFDD=$fdd8c
cr EUtranCellFDD=$fdd3d,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-44
EUtranCellFDD=$fdd8d
cr EUtranCellFDD=$fdd3d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-51
EUtranCellFDD=$fdd5a
cr EUtranCellFDD=$fdd3d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-52
EUtranCellFDD=$fdd5b
cr EUtranCellFDD=$fdd3d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-53
EUtranCellFDD=$fdd5c
cr EUtranCellFDD=$fdd3d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-54
EUtranCellFDD=$fdd5d
cr EUtranCellFDD=$fdd3d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-61
EUtranCellTDD=$tdd6a
cr EUtranCellFDD=$fdd3d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-62
EUtranCellTDD=$tdd6b
cr EUtranCellFDD=$fdd3d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-63
EUtranCellTDD=$tdd6c
cr EUtranCellFDD=$fdd3d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-64
EUtranCellTDD=$tdd6d
cr EUtranCellFDD=$fdd3d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-71
EUtranCellTDD=$tdd7a
cr EUtranCellFDD=$fdd3d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-72
EUtranCellTDD=$tdd7b
cr EUtranCellFDD=$fdd3d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-73
EUtranCellTDD=$tdd7c
cr EUtranCellFDD=$fdd3d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-74
EUtranCellTDD=$tdd7d


cr EUtranCellTDD=$tdd1a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-11
EUtranCellFDD=$fdd3a
cr EUtranCellTDD=$tdd1a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-12
EUtranCellFDD=$fdd3b
cr EUtranCellTDD=$tdd1a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-13
EUtranCellFDD=$fdd3c
cr EUtranCellTDD=$tdd1a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-14
EUtranCellFDD=$fdd3d
cr EUtranCellTDD=$tdd1a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-31
EUtranCellTDD=$tdd2a
cr EUtranCellTDD=$tdd1a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-32
EUtranCellTDD=$tdd2b
cr EUtranCellTDD=$tdd1a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-33
EUtranCellTDD=$tdd2c
cr EUtranCellTDD=$tdd1a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-34
EUtranCellTDD=$tdd2d
cr EUtranCellTDD=$tdd1a,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-41
EUtranCellFDD=$fdd8a
cr EUtranCellTDD=$tdd1a,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-42
EUtranCellFDD=$fdd8b
cr EUtranCellTDD=$tdd1a,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-43
EUtranCellFDD=$fdd8c
cr EUtranCellTDD=$tdd1a,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-44
EUtranCellFDD=$fdd8d
cr EUtranCellTDD=$tdd1a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-51
EUtranCellFDD=$fdd5a
cr EUtranCellTDD=$tdd1a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-52
EUtranCellFDD=$fdd5b
cr EUtranCellTDD=$tdd1a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-53
EUtranCellFDD=$fdd5c
cr EUtranCellTDD=$tdd1a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-54
EUtranCellFDD=$fdd5d
cr EUtranCellTDD=$tdd1a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-61
EUtranCellTDD=$tdd6a
cr EUtranCellTDD=$tdd1a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-62
EUtranCellTDD=$tdd6b
cr EUtranCellTDD=$tdd1a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-63
EUtranCellTDD=$tdd6c
cr EUtranCellTDD=$tdd1a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-64
EUtranCellTDD=$tdd6d
cr EUtranCellTDD=$tdd1a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-71
EUtranCellTDD=$tdd7a
cr EUtranCellTDD=$tdd1a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-72
EUtranCellTDD=$tdd7b
cr EUtranCellTDD=$tdd1a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-73
EUtranCellTDD=$tdd7c
cr EUtranCellTDD=$tdd1a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-74
EUtranCellTDD=$tdd7d

cr EUtranCellTDD=$tdd1b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-11
EUtranCellFDD=$fdd3a
cr EUtranCellTDD=$tdd1b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-12
EUtranCellFDD=$fdd3b
cr EUtranCellTDD=$tdd1b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-13
EUtranCellFDD=$fdd3c
cr EUtranCellTDD=$tdd1b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-14
EUtranCellFDD=$fdd3d
cr EUtranCellTDD=$tdd1b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-31
EUtranCellTDD=$tdd2a
cr EUtranCellTDD=$tdd1b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-32
EUtranCellTDD=$tdd2b
cr EUtranCellTDD=$tdd1b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-33
EUtranCellTDD=$tdd2c
cr EUtranCellTDD=$tdd1b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-34
EUtranCellTDD=$tdd2d
cr EUtranCellTDD=$tdd1b,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-41
EUtranCellFDD=$fdd8a
cr EUtranCellTDD=$tdd1b,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-42
EUtranCellFDD=$fdd8b
cr EUtranCellTDD=$tdd1b,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-43
EUtranCellFDD=$fdd8c
cr EUtranCellTDD=$tdd1b,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-44
EUtranCellFDD=$fdd8d
cr EUtranCellTDD=$tdd1b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-51
EUtranCellFDD=$fdd5a
cr EUtranCellTDD=$tdd1b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-52
EUtranCellFDD=$fdd5b
cr EUtranCellTDD=$tdd1b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-53
EUtranCellFDD=$fdd5c
cr EUtranCellTDD=$tdd1b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-54
EUtranCellFDD=$fdd5d
cr EUtranCellTDD=$tdd1b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-61
EUtranCellTDD=$tdd6a
cr EUtranCellTDD=$tdd1b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-62
EUtranCellTDD=$tdd6b
cr EUtranCellTDD=$tdd1b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-63
EUtranCellTDD=$tdd6c
cr EUtranCellTDD=$tdd1b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-64
EUtranCellTDD=$tdd6d
cr EUtranCellTDD=$tdd1b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-71
EUtranCellTDD=$tdd7a
cr EUtranCellTDD=$tdd1b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-72
EUtranCellTDD=$tdd7b
cr EUtranCellTDD=$tdd1b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-73
EUtranCellTDD=$tdd7c
cr EUtranCellTDD=$tdd1b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-74
EUtranCellTDD=$tdd7d

cr EUtranCellTDD=$tdd1c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-11
EUtranCellFDD=$fdd3a
cr EUtranCellTDD=$tdd1c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-12
EUtranCellFDD=$fdd3b
cr EUtranCellTDD=$tdd1c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-13
EUtranCellFDD=$fdd3c
cr EUtranCellTDD=$tdd1c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-14
EUtranCellFDD=$fdd3d
cr EUtranCellTDD=$tdd1c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-31
EUtranCellTDD=$tdd2a
cr EUtranCellTDD=$tdd1c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-32
EUtranCellTDD=$tdd2b
cr EUtranCellTDD=$tdd1c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-33
EUtranCellTDD=$tdd2c
cr EUtranCellTDD=$tdd1c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-34
EUtranCellTDD=$tdd2d
cr EUtranCellTDD=$tdd1c,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-41
EUtranCellFDD=$fdd8a
cr EUtranCellTDD=$tdd1c,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-42
EUtranCellFDD=$fdd8b
cr EUtranCellTDD=$tdd1c,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-43
EUtranCellFDD=$fdd8c
cr EUtranCellTDD=$tdd1c,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-44
EUtranCellFDD=$fdd8d
cr EUtranCellTDD=$tdd1c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-51
EUtranCellFDD=$fdd5a
cr EUtranCellTDD=$tdd1c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-52
EUtranCellFDD=$fdd5b
cr EUtranCellTDD=$tdd1c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-53
EUtranCellFDD=$fdd5c
cr EUtranCellTDD=$tdd1c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-54
EUtranCellFDD=$fdd5d
cr EUtranCellTDD=$tdd1c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-61
EUtranCellTDD=$tdd6a
cr EUtranCellTDD=$tdd1c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-62
EUtranCellTDD=$tdd6b
cr EUtranCellTDD=$tdd1c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-63
EUtranCellTDD=$tdd6c
cr EUtranCellTDD=$tdd1c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-64
EUtranCellTDD=$tdd6d
cr EUtranCellTDD=$tdd1c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-71
EUtranCellTDD=$tdd7a
cr EUtranCellTDD=$tdd1c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-72
EUtranCellTDD=$tdd7b
cr EUtranCellTDD=$tdd1c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-73
EUtranCellTDD=$tdd7c
cr EUtranCellTDD=$tdd1c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-74
EUtranCellTDD=$tdd7d



cr EUtranCellTDD=$tdd1d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-11
EUtranCellFDD=$fdd3a
cr EUtranCellTDD=$tdd1d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-12
EUtranCellFDD=$fdd3b
cr EUtranCellTDD=$tdd1d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-13
EUtranCellFDD=$fdd3c
cr EUtranCellTDD=$tdd1d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-14
EUtranCellFDD=$fdd3d
cr EUtranCellTDD=$tdd1d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-31
EUtranCellTDD=$tdd2a
cr EUtranCellTDD=$tdd1d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-32
EUtranCellTDD=$tdd2b
cr EUtranCellTDD=$tdd1d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-33
EUtranCellTDD=$tdd2c
cr EUtranCellTDD=$tdd1d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-34
EUtranCellTDD=$tdd2d
cr EUtranCellTDD=$tdd1d,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-41
EUtranCellFDD=$fdd8a
cr EUtranCellTDD=$tdd1d,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-42
EUtranCellFDD=$fdd8b
cr EUtranCellTDD=$tdd1d,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-43
EUtranCellFDD=$fdd8c
cr EUtranCellTDD=$tdd1d,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-44
EUtranCellFDD=$fdd8d
cr EUtranCellTDD=$tdd1d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-51
EUtranCellFDD=$fdd5a
cr EUtranCellTDD=$tdd1d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-52
EUtranCellFDD=$fdd5b
cr EUtranCellTDD=$tdd1d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-53
EUtranCellFDD=$fdd5c
cr EUtranCellTDD=$tdd1d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-54
EUtranCellFDD=$fdd5d
cr EUtranCellTDD=$tdd1d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-61
EUtranCellTDD=$tdd6a
cr EUtranCellTDD=$tdd1d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-62
EUtranCellTDD=$tdd6b
cr EUtranCellTDD=$tdd1d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-63
EUtranCellTDD=$tdd6c
cr EUtranCellTDD=$tdd1d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-64
EUtranCellTDD=$tdd6d
cr EUtranCellTDD=$tdd1d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-71
EUtranCellTDD=$tdd7a
cr EUtranCellTDD=$tdd1d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-72
EUtranCellTDD=$tdd7b
cr EUtranCellTDD=$tdd1d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-73
EUtranCellTDD=$tdd7c
cr EUtranCellTDD=$tdd1d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-74
EUtranCellTDD=$tdd7d


cr EUtranCellTDD=$tdd2a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-11
EUtranCellFDD=$fdd3a
cr EUtranCellTDD=$tdd2a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-12
EUtranCellFDD=$fdd3b
cr EUtranCellTDD=$tdd2a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-13
EUtranCellFDD=$fdd3c
cr EUtranCellTDD=$tdd2a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-14
EUtranCellFDD=$fdd3d
cr EUtranCellTDD=$tdd2a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-21
EUtranCellTDD=$tdd1a
cr EUtranCellTDD=$tdd2a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-22
EUtranCellTDD=$tdd1b
cr EUtranCellTDD=$tdd2a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-23
EUtranCellTDD=$tdd1c
cr EUtranCellTDD=$tdd2a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-24
EUtranCellTDD=$tdd1d
cr EUtranCellTDD=$tdd2a,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-41
EUtranCellFDD=$fdd8a
cr EUtranCellTDD=$tdd2a,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-42
EUtranCellFDD=$fdd8b
cr EUtranCellTDD=$tdd2a,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-43
EUtranCellFDD=$fdd8c
cr EUtranCellTDD=$tdd2a,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-44
EUtranCellFDD=$fdd8d
cr EUtranCellTDD=$tdd2a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-51
EUtranCellFDD=$fdd5a
cr EUtranCellTDD=$tdd2a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-52
EUtranCellFDD=$fdd5b
cr EUtranCellTDD=$tdd2a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-53
EUtranCellFDD=$fdd5c
cr EUtranCellTDD=$tdd2a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-54
EUtranCellFDD=$fdd5d
cr EUtranCellTDD=$tdd2a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-61
EUtranCellTDD=$tdd6a
cr EUtranCellTDD=$tdd2a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-62
EUtranCellTDD=$tdd6b
cr EUtranCellTDD=$tdd2a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-63
EUtranCellTDD=$tdd6c
cr EUtranCellTDD=$tdd2a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-64
EUtranCellTDD=$tdd6d
cr EUtranCellTDD=$tdd2a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-71
EUtranCellTDD=$tdd7a
cr EUtranCellTDD=$tdd2a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-72
EUtranCellTDD=$tdd7b
cr EUtranCellTDD=$tdd2a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-73
EUtranCellTDD=$tdd7c
cr EUtranCellTDD=$tdd2a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-74
EUtranCellTDD=$tdd7d

cr EUtranCellTDD=$tdd2b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-11
EUtranCellFDD=$fdd3a
cr EUtranCellTDD=$tdd2b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-12
EUtranCellFDD=$fdd3b
cr EUtranCellTDD=$tdd2b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-13
EUtranCellFDD=$fdd3c
cr EUtranCellTDD=$tdd2b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-14
EUtranCellFDD=$fdd3d
cr EUtranCellTDD=$tdd2b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-21
EUtranCellTDD=$tdd1a
cr EUtranCellTDD=$tdd2b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-22
EUtranCellTDD=$tdd1b
cr EUtranCellTDD=$tdd2b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-23
EUtranCellTDD=$tdd1c
cr EUtranCellTDD=$tdd2b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-24
EUtranCellTDD=$tdd1d
cr EUtranCellTDD=$tdd2b,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-41
EUtranCellFDD=$fdd8a
cr EUtranCellTDD=$tdd2b,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-42
EUtranCellFDD=$fdd8b
cr EUtranCellTDD=$tdd2b,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-43
EUtranCellFDD=$fdd8c
cr EUtranCellTDD=$tdd2b,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-44
EUtranCellFDD=$fdd8d
cr EUtranCellTDD=$tdd2b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-51
EUtranCellFDD=$fdd5a
cr EUtranCellTDD=$tdd2b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-52
EUtranCellFDD=$fdd5b
cr EUtranCellTDD=$tdd2b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-53
EUtranCellFDD=$fdd5c
cr EUtranCellTDD=$tdd2b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-54
EUtranCellFDD=$fdd5d
cr EUtranCellTDD=$tdd2b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-61
EUtranCellTDD=$tdd6a
cr EUtranCellTDD=$tdd2b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-62
EUtranCellTDD=$tdd6b
cr EUtranCellTDD=$tdd2b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-63
EUtranCellTDD=$tdd6c
cr EUtranCellTDD=$tdd2b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-64
EUtranCellTDD=$tdd6d
cr EUtranCellTDD=$tdd2b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-71
EUtranCellTDD=$tdd7a
cr EUtranCellTDD=$tdd2b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-72
EUtranCellTDD=$tdd7b
cr EUtranCellTDD=$tdd2b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-73
EUtranCellTDD=$tdd7c
cr EUtranCellTDD=$tdd2b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-74
EUtranCellTDD=$tdd7d


cr EUtranCellTDD=$tdd2c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-11
EUtranCellFDD=$fdd3a
cr EUtranCellTDD=$tdd2c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-12
EUtranCellFDD=$fdd3b
cr EUtranCellTDD=$tdd2c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-13
EUtranCellFDD=$fdd3c
cr EUtranCellTDD=$tdd2c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-14
EUtranCellFDD=$fdd3d
cr EUtranCellTDD=$tdd2c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-21
EUtranCellTDD=$tdd1a
cr EUtranCellTDD=$tdd2c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-22
EUtranCellTDD=$tdd1b
cr EUtranCellTDD=$tdd2c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-23
EUtranCellTDD=$tdd1c
cr EUtranCellTDD=$tdd2c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-24
EUtranCellTDD=$tdd1d
cr EUtranCellTDD=$tdd2c,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-41
EUtranCellFDD=$fdd8a
cr EUtranCellTDD=$tdd2c,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-42
EUtranCellFDD=$fdd8b
cr EUtranCellTDD=$tdd2c,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-43
EUtranCellFDD=$fdd8c
cr EUtranCellTDD=$tdd2c,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-44
EUtranCellFDD=$fdd8d
cr EUtranCellTDD=$tdd2c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-51
EUtranCellFDD=$fdd5a
cr EUtranCellTDD=$tdd2c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-52
EUtranCellFDD=$fdd5b
cr EUtranCellTDD=$tdd2c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-53
EUtranCellFDD=$fdd5c
cr EUtranCellTDD=$tdd2c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-54
EUtranCellFDD=$fdd5d
cr EUtranCellTDD=$tdd2c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-61
EUtranCellTDD=$tdd6a
cr EUtranCellTDD=$tdd2c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-62
EUtranCellTDD=$tdd6b
cr EUtranCellTDD=$tdd2c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-63
EUtranCellTDD=$tdd6c
cr EUtranCellTDD=$tdd2c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-64
EUtranCellTDD=$tdd6d
cr EUtranCellTDD=$tdd2c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-71
EUtranCellTDD=$tdd7a
cr EUtranCellTDD=$tdd2c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-72
EUtranCellTDD=$tdd7b
cr EUtranCellTDD=$tdd2c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-73
EUtranCellTDD=$tdd7c
cr EUtranCellTDD=$tdd2c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-74
EUtranCellTDD=$tdd7d


cr EUtranCellTDD=$tdd2d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-11
EUtranCellFDD=$fdd3a
cr EUtranCellTDD=$tdd2d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-12
EUtranCellFDD=$fdd3b
cr EUtranCellTDD=$tdd2d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-13
EUtranCellFDD=$fdd3c
cr EUtranCellTDD=$tdd2d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-14
EUtranCellFDD=$fdd3d
cr EUtranCellTDD=$tdd2d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-21
EUtranCellTDD=$tdd1a
cr EUtranCellTDD=$tdd2d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-22
EUtranCellTDD=$tdd1b
cr EUtranCellTDD=$tdd2d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-23
EUtranCellTDD=$tdd1c
cr EUtranCellTDD=$tdd2d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-24
EUtranCellTDD=$tdd1d
cr EUtranCellTDD=$tdd2d,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-41
EUtranCellFDD=$fdd8a
cr EUtranCellTDD=$tdd2d,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-42
EUtranCellFDD=$fdd8b
cr EUtranCellTDD=$tdd2d,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-43
EUtranCellFDD=$fdd8c
cr EUtranCellTDD=$tdd2d,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-44
EUtranCellFDD=$fdd8d
cr EUtranCellTDD=$tdd2d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-51
EUtranCellFDD=$fdd5a
cr EUtranCellTDD=$tdd2d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-52
EUtranCellFDD=$fdd5b
cr EUtranCellTDD=$tdd2d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-53
EUtranCellFDD=$fdd5c
cr EUtranCellTDD=$tdd2d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-54
EUtranCellFDD=$fdd5d
cr EUtranCellTDD=$tdd2d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-61
EUtranCellTDD=$tdd6a
cr EUtranCellTDD=$tdd2d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-62
EUtranCellTDD=$tdd6b
cr EUtranCellTDD=$tdd2d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-63
EUtranCellTDD=$tdd6c
cr EUtranCellTDD=$tdd2d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-64
EUtranCellTDD=$tdd6d
cr EUtranCellTDD=$tdd2d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-71
EUtranCellTDD=$tdd7a
cr EUtranCellTDD=$tdd2d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-72
EUtranCellTDD=$tdd7b
cr EUtranCellTDD=$tdd2d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-73
EUtranCellTDD=$tdd7c
cr EUtranCellTDD=$tdd2d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-74
EUtranCellTDD=$tdd7d

cr EUtranCellFDD=$fdd5a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-21
EUtranCellTDD=$tdd1a
cr EUtranCellFDD=$fdd5a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-22
EUtranCellTDD=$tdd1b
cr EUtranCellFDD=$fdd5a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-23
EUtranCellTDD=$tdd1c
cr EUtranCellFDD=$fdd5a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-24
EUtranCellTDD=$tdd1d
cr EUtranCellFDD=$fdd5a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-31
EUtranCellTDD=$tdd2a
cr EUtranCellFDD=$fdd5a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-32
EUtranCellTDD=$tdd2b
cr EUtranCellFDD=$fdd5a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-33
EUtranCellTDD=$tdd2c
cr EUtranCellFDD=$fdd5a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-34
EUtranCellTDD=$tdd2d
cr EUtranCellFDD=$fdd5a,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-41
EUtranCellFDD=$fdd8a
cr EUtranCellFDD=$fdd5a,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-42
EUtranCellFDD=$fdd8b
cr EUtranCellFDD=$fdd5a,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-43
EUtranCellFDD=$fdd8c
cr EUtranCellFDD=$fdd5a,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-44
EUtranCellFDD=$fdd8d
cr EUtranCellFDD=$fdd5a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-11
EUtranCellFDD=$fdd3a
cr EUtranCellFDD=$fdd5a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-12
EUtranCellFDD=$fdd3b
cr EUtranCellFDD=$fdd5a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-13
EUtranCellFDD=$fdd3c
cr EUtranCellFDD=$fdd5a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-14
EUtranCellFDD=$fdd3d
cr EUtranCellFDD=$fdd5a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-61
EUtranCellTDD=$tdd6a
cr EUtranCellFDD=$fdd5a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-62
EUtranCellTDD=$tdd6b
cr EUtranCellFDD=$fdd5a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-63
EUtranCellTDD=$tdd6c
cr EUtranCellFDD=$fdd5a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-64
EUtranCellTDD=$tdd6d
cr EUtranCellFDD=$fdd5a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-71
EUtranCellTDD=$tdd7a
cr EUtranCellFDD=$fdd5a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-72
EUtranCellTDD=$tdd7b
cr EUtranCellFDD=$fdd5a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-73
EUtranCellTDD=$tdd7c
cr EUtranCellFDD=$fdd5a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-74
EUtranCellTDD=$tdd7d


cr EUtranCellFDD=$fdd5b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-21
EUtranCellTDD=$tdd1a
cr EUtranCellFDD=$fdd5b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-22
EUtranCellTDD=$tdd1b
cr EUtranCellFDD=$fdd5b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-23
EUtranCellTDD=$tdd1c
cr EUtranCellFDD=$fdd5b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-24
EUtranCellTDD=$tdd1d
cr EUtranCellFDD=$fdd5b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-31
EUtranCellTDD=$tdd2a
cr EUtranCellFDD=$fdd5b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-32
EUtranCellTDD=$tdd2b
cr EUtranCellFDD=$fdd5b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-33
EUtranCellTDD=$tdd2c
cr EUtranCellFDD=$fdd5b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-34
EUtranCellTDD=$tdd2d
cr EUtranCellFDD=$fdd5b,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-41
EUtranCellFDD=$fdd8a
cr EUtranCellFDD=$fdd5b,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-42
EUtranCellFDD=$fdd8b
cr EUtranCellFDD=$fdd5b,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-43
EUtranCellFDD=$fdd8c
cr EUtranCellFDD=$fdd5b,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-44
EUtranCellFDD=$fdd8d
cr EUtranCellFDD=$fdd5b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-11
EUtranCellFDD=$fdd3a
cr EUtranCellFDD=$fdd5b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-12
EUtranCellFDD=$fdd3b
cr EUtranCellFDD=$fdd5b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-13
EUtranCellFDD=$fdd3c
cr EUtranCellFDD=$fdd5b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-14
EUtranCellFDD=$fdd3d
cr EUtranCellFDD=$fdd5b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-61
EUtranCellTDD=$tdd6a
cr EUtranCellFDD=$fdd5b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-62
EUtranCellTDD=$tdd6b
cr EUtranCellFDD=$fdd5b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-63
EUtranCellTDD=$tdd6c
cr EUtranCellFDD=$fdd5b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-64
EUtranCellTDD=$tdd6d
cr EUtranCellFDD=$fdd5b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-71
EUtranCellTDD=$tdd7a
cr EUtranCellFDD=$fdd5b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-72
EUtranCellTDD=$tdd7b
cr EUtranCellFDD=$fdd5b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-73
EUtranCellTDD=$tdd7c
cr EUtranCellFDD=$fdd5b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-74
EUtranCellTDD=$tdd7d


cr EUtranCellFDD=$fdd5c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-21
EUtranCellTDD=$tdd1a
cr EUtranCellFDD=$fdd5c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-22
EUtranCellTDD=$tdd1b
cr EUtranCellFDD=$fdd5c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-23
EUtranCellTDD=$tdd1c
cr EUtranCellFDD=$fdd5c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-24
EUtranCellTDD=$tdd1d
cr EUtranCellFDD=$fdd5c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-31
EUtranCellTDD=$tdd2a
cr EUtranCellFDD=$fdd5c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-32
EUtranCellTDD=$tdd2b
cr EUtranCellFDD=$fdd5c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-33
EUtranCellTDD=$tdd2c
cr EUtranCellFDD=$fdd5c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-34
EUtranCellTDD=$tdd2d
cr EUtranCellFDD=$fdd5c,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-41
EUtranCellFDD=$fdd8a
cr EUtranCellFDD=$fdd5c,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-42
EUtranCellFDD=$fdd8b
cr EUtranCellFDD=$fdd5c,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-43
EUtranCellFDD=$fdd8c
cr EUtranCellFDD=$fdd5c,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-44
EUtranCellFDD=$fdd8d
cr EUtranCellFDD=$fdd5c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-11
EUtranCellFDD=$fdd3a
cr EUtranCellFDD=$fdd5c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-12
EUtranCellFDD=$fdd3b
cr EUtranCellFDD=$fdd5c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-13
EUtranCellFDD=$fdd3c
cr EUtranCellFDD=$fdd5c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-14
EUtranCellFDD=$fdd3d
cr EUtranCellFDD=$fdd5c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-61
EUtranCellTDD=$tdd6a
cr EUtranCellFDD=$fdd5c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-62
EUtranCellTDD=$tdd6b
cr EUtranCellFDD=$fdd5c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-63
EUtranCellTDD=$tdd6c
cr EUtranCellFDD=$fdd5c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-64
EUtranCellTDD=$tdd6d
cr EUtranCellFDD=$fdd5c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-71
EUtranCellTDD=$tdd7a
cr EUtranCellFDD=$fdd5c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-72
EUtranCellTDD=$tdd7b
cr EUtranCellFDD=$fdd5c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-73
EUtranCellTDD=$tdd7c
cr EUtranCellFDD=$fdd5c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-74
EUtranCellTDD=$tdd7d

cr EUtranCellFDD=$fdd5d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-21
EUtranCellTDD=$tdd1a
cr EUtranCellFDD=$fdd5d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-22
EUtranCellTDD=$tdd1b
cr EUtranCellFDD=$fdd5d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-23
EUtranCellTDD=$tdd1c
cr EUtranCellFDD=$fdd5d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-24
EUtranCellTDD=$tdd1d
cr EUtranCellFDD=$fdd5d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-31
EUtranCellTDD=$tdd2a
cr EUtranCellFDD=$fdd5d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-32
EUtranCellTDD=$tdd2b
cr EUtranCellFDD=$fdd5d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-33
EUtranCellTDD=$tdd2c
cr EUtranCellFDD=$fdd5d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-34
EUtranCellTDD=$tdd2d
cr EUtranCellFDD=$fdd5d,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-41
EUtranCellFDD=$fdd8a
cr EUtranCellFDD=$fdd5d,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-42
EUtranCellFDD=$fdd8b
cr EUtranCellFDD=$fdd5d,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-43
EUtranCellFDD=$fdd8c
cr EUtranCellFDD=$fdd5d,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-44
EUtranCellFDD=$fdd8d
cr EUtranCellFDD=$fdd5d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-11
EUtranCellFDD=$fdd3a
cr EUtranCellFDD=$fdd5d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-12
EUtranCellFDD=$fdd3b
cr EUtranCellFDD=$fdd5d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-13
EUtranCellFDD=$fdd3c
cr EUtranCellFDD=$fdd5d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-14
EUtranCellFDD=$fdd3d
cr EUtranCellFDD=$fdd5d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-61
EUtranCellTDD=$tdd6a
cr EUtranCellFDD=$fdd5d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-62
EUtranCellTDD=$tdd6b
cr EUtranCellFDD=$fdd5d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-63
EUtranCellTDD=$tdd6c
cr EUtranCellFDD=$fdd5d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-64
EUtranCellTDD=$tdd6d
cr EUtranCellFDD=$fdd5d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-71
EUtranCellTDD=$tdd7a
cr EUtranCellFDD=$fdd5d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-72
EUtranCellTDD=$tdd7b
cr EUtranCellFDD=$fdd5d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-73
EUtranCellTDD=$tdd7c
cr EUtranCellFDD=$fdd5d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-74
EUtranCellTDD=$tdd7d

cr EUtranCellTDD=$tdd6a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-21
EUtranCellTDD=$tdd1a
cr EUtranCellTDD=$tdd6a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-22
EUtranCellTDD=$tdd1b
cr EUtranCellTDD=$tdd6a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-23
EUtranCellTDD=$tdd1c
cr EUtranCellTDD=$tdd6a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-24
EUtranCellTDD=$tdd1d
cr EUtranCellTDD=$tdd6a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-31
EUtranCellTDD=$tdd2a
cr EUtranCellTDD=$tdd6a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-32
EUtranCellTDD=$tdd2b
cr EUtranCellTDD=$tdd6a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-33
EUtranCellTDD=$tdd2c
cr EUtranCellTDD=$tdd6a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-34
EUtranCellTDD=$tdd2d
cr EUtranCellTDD=$tdd6a,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-41
EUtranCellFDD=$fdd8a
cr EUtranCellTDD=$tdd6a,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-42
EUtranCellFDD=$fdd8b
cr EUtranCellTDD=$tdd6a,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-43
EUtranCellFDD=$fdd8c
cr EUtranCellTDD=$tdd6a,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-44
EUtranCellFDD=$fdd8d
cr EUtranCellTDD=$tdd6a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-11
EUtranCellFDD=$fdd3a
cr EUtranCellTDD=$tdd6a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-12
EUtranCellFDD=$fdd3b
cr EUtranCellTDD=$tdd6a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-13
EUtranCellFDD=$fdd3c
cr EUtranCellTDD=$tdd6a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-14
EUtranCellFDD=$fdd3d
cr EUtranCellTDD=$tdd6a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-71
EUtranCellTDD=$tdd7a
cr EUtranCellTDD=$tdd6a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-72
EUtranCellTDD=$tdd7b
cr EUtranCellTDD=$tdd6a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-73
EUtranCellTDD=$tdd7c
cr EUtranCellTDD=$tdd6a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-74
EUtranCellTDD=$tdd7d
cr EUtranCellTDD=$tdd6a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-51
EUtranCellFDD=$fdd5a
cr EUtranCellTDD=$tdd6a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-52
EUtranCellFDD=$fdd5b
cr EUtranCellTDD=$tdd6a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-53
EUtranCellFDD=$fdd5c
cr EUtranCellTDD=$tdd6a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-54
EUtranCellFDD=$fdd5d

cr EUtranCellTDD=$tdd6b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-21
EUtranCellTDD=$tdd1a
cr EUtranCellTDD=$tdd6b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-22
EUtranCellTDD=$tdd1b
cr EUtranCellTDD=$tdd6b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-23
EUtranCellTDD=$tdd1c
cr EUtranCellTDD=$tdd6b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-24
EUtranCellTDD=$tdd1d
cr EUtranCellTDD=$tdd6b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-31
EUtranCellTDD=$tdd2a
cr EUtranCellTDD=$tdd6b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-32
EUtranCellTDD=$tdd2b
cr EUtranCellTDD=$tdd6b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-33
EUtranCellTDD=$tdd2c
cr EUtranCellTDD=$tdd6b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-34
EUtranCellTDD=$tdd2d
cr EUtranCellTDD=$tdd6b,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-41
EUtranCellFDD=$fdd8a
cr EUtranCellTDD=$tdd6b,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-42
EUtranCellFDD=$fdd8b
cr EUtranCellTDD=$tdd6b,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-43
EUtranCellFDD=$fdd8c
cr EUtranCellTDD=$tdd6b,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-44
EUtranCellFDD=$fdd8d
cr EUtranCellTDD=$tdd6b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-11
EUtranCellFDD=$fdd3a
cr EUtranCellTDD=$tdd6b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-12
EUtranCellFDD=$fdd3b
cr EUtranCellTDD=$tdd6b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-13
EUtranCellFDD=$fdd3c
cr EUtranCellTDD=$tdd6b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-14
EUtranCellFDD=$fdd3d
cr EUtranCellTDD=$tdd6b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-71
EUtranCellTDD=$tdd7a
cr EUtranCellTDD=$tdd6b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-72
EUtranCellTDD=$tdd7b
cr EUtranCellTDD=$tdd6b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-73
EUtranCellTDD=$tdd7c
cr EUtranCellTDD=$tdd6b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-74
EUtranCellTDD=$tdd7d
cr EUtranCellTDD=$tdd6b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-51
EUtranCellFDD=$fdd5a
cr EUtranCellTDD=$tdd6b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-52
EUtranCellFDD=$fdd5b
cr EUtranCellTDD=$tdd6b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-53
EUtranCellFDD=$fdd5c
cr EUtranCellTDD=$tdd6b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-54
EUtranCellFDD=$fdd5d

cr EUtranCellTDD=$tdd6c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-21
EUtranCellTDD=$tdd1a
cr EUtranCellTDD=$tdd6c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-22
EUtranCellTDD=$tdd1b
cr EUtranCellTDD=$tdd6c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-23
EUtranCellTDD=$tdd1c
cr EUtranCellTDD=$tdd6c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-24
EUtranCellTDD=$tdd1d
cr EUtranCellTDD=$tdd6c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-31
EUtranCellTDD=$tdd2a
cr EUtranCellTDD=$tdd6c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-32
EUtranCellTDD=$tdd2b
cr EUtranCellTDD=$tdd6c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-33
EUtranCellTDD=$tdd2c
cr EUtranCellTDD=$tdd6c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-34
EUtranCellTDD=$tdd2d
cr EUtranCellTDD=$tdd6c,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-41
EUtranCellFDD=$fdd8a
cr EUtranCellTDD=$tdd6c,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-42
EUtranCellFDD=$fdd8b
cr EUtranCellTDD=$tdd6c,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-43
EUtranCellFDD=$fdd8c
cr EUtranCellTDD=$tdd6c,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-44
EUtranCellFDD=$fdd8d
cr EUtranCellTDD=$tdd6c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-11
EUtranCellFDD=$fdd3a
cr EUtranCellTDD=$tdd6c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-12
EUtranCellFDD=$fdd3b
cr EUtranCellTDD=$tdd6c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-13
EUtranCellFDD=$fdd3c
cr EUtranCellTDD=$tdd6c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-14
EUtranCellFDD=$fdd3d
cr EUtranCellTDD=$tdd6c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-71
EUtranCellTDD=$tdd7a
cr EUtranCellTDD=$tdd6c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-72
EUtranCellTDD=$tdd7b
cr EUtranCellTDD=$tdd6c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-73
EUtranCellTDD=$tdd7c
cr EUtranCellTDD=$tdd6c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-74
EUtranCellTDD=$tdd7d
cr EUtranCellTDD=$tdd6c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-51
EUtranCellFDD=$fdd5a
cr EUtranCellTDD=$tdd6c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-52
EUtranCellFDD=$fdd5b
cr EUtranCellTDD=$tdd6c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-53
EUtranCellFDD=$fdd5c
cr EUtranCellTDD=$tdd6c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-54
EUtranCellFDD=$fdd5d

cr EUtranCellTDD=$tdd6d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-21
EUtranCellTDD=$tdd1a
cr EUtranCellTDD=$tdd6d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-22
EUtranCellTDD=$tdd1b
cr EUtranCellTDD=$tdd6d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-23
EUtranCellTDD=$tdd1c
cr EUtranCellTDD=$tdd6d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-24
EUtranCellTDD=$tdd1d
cr EUtranCellTDD=$tdd6d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-31
EUtranCellTDD=$tdd2a
cr EUtranCellTDD=$tdd6d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-32
EUtranCellTDD=$tdd2b
cr EUtranCellTDD=$tdd6d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-33
EUtranCellTDD=$tdd2c
cr EUtranCellTDD=$tdd6d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-34
EUtranCellTDD=$tdd2d
cr EUtranCellTDD=$tdd6d,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-41
EUtranCellFDD=$fdd8a
cr EUtranCellTDD=$tdd6d,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-42
EUtranCellFDD=$fdd8b
cr EUtranCellTDD=$tdd6d,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-43
EUtranCellFDD=$fdd8c
cr EUtranCellTDD=$tdd6d,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-44
EUtranCellFDD=$fdd8d
cr EUtranCellTDD=$tdd6d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-11
EUtranCellFDD=$fdd3a
cr EUtranCellTDD=$tdd6d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-12
EUtranCellFDD=$fdd3b
cr EUtranCellTDD=$tdd6d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-13
EUtranCellFDD=$fdd3c
cr EUtranCellTDD=$tdd6d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-14
EUtranCellFDD=$fdd3d
cr EUtranCellTDD=$tdd6d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-71
EUtranCellTDD=$tdd7a
cr EUtranCellTDD=$tdd6d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-72
EUtranCellTDD=$tdd7b
cr EUtranCellTDD=$tdd6d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-73
EUtranCellTDD=$tdd7c
cr EUtranCellTDD=$tdd6d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-74
EUtranCellTDD=$tdd7d
cr EUtranCellTDD=$tdd6d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-51
EUtranCellFDD=$fdd5a
cr EUtranCellTDD=$tdd6d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-52
EUtranCellFDD=$fdd5b
cr EUtranCellTDD=$tdd6d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-53
EUtranCellFDD=$fdd5c
cr EUtranCellTDD=$tdd6d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-54
EUtranCellFDD=$fdd5d


cr EUtranCellTDD=$tdd7a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-21
EUtranCellTDD=$tdd1a
cr EUtranCellTDD=$tdd7a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-22
EUtranCellTDD=$tdd1b
cr EUtranCellTDD=$tdd7a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-23
EUtranCellTDD=$tdd1c
cr EUtranCellTDD=$tdd7a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-24
EUtranCellTDD=$tdd1d
cr EUtranCellTDD=$tdd7a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-31
EUtranCellTDD=$tdd2a
cr EUtranCellTDD=$tdd7a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-32
EUtranCellTDD=$tdd2b
cr EUtranCellTDD=$tdd7a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-33
EUtranCellTDD=$tdd2c
cr EUtranCellTDD=$tdd7a,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-34
EUtranCellTDD=$tdd2d
cr EUtranCellTDD=$tdd7a,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-41
EUtranCellFDD=$fdd8a
cr EUtranCellTDD=$tdd7a,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-42
EUtranCellFDD=$fdd8b
cr EUtranCellTDD=$tdd7a,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-43
EUtranCellFDD=$fdd8c
cr EUtranCellTDD=$tdd7a,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-44
EUtranCellFDD=$fdd8d
cr EUtranCellTDD=$tdd7a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-11
EUtranCellFDD=$fdd3a
cr EUtranCellTDD=$tdd7a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-12
EUtranCellFDD=$fdd3b
cr EUtranCellTDD=$tdd7a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-13
EUtranCellFDD=$fdd3c
cr EUtranCellTDD=$tdd7a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-14
EUtranCellFDD=$fdd3d
cr EUtranCellTDD=$tdd7a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-61
EUtranCellTDD=$tdd6a
cr EUtranCellTDD=$tdd7a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-62
EUtranCellTDD=$tdd6b
cr EUtranCellTDD=$tdd7a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-63
EUtranCellTDD=$tdd6c
cr EUtranCellTDD=$tdd7a,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-64
EUtranCellTDD=$tdd6d
cr EUtranCellTDD=$tdd7a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-51
EUtranCellFDD=$fdd5a
cr EUtranCellTDD=$tdd7a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-52
EUtranCellFDD=$fdd5b
cr EUtranCellTDD=$tdd7a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-53
EUtranCellFDD=$fdd5c
cr EUtranCellTDD=$tdd7a,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-54
EUtranCellFDD=$fdd5d


cr EUtranCellTDD=$tdd7b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-21
EUtranCellTDD=$tdd1a
cr EUtranCellTDD=$tdd7b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-22
EUtranCellTDD=$tdd1b
cr EUtranCellTDD=$tdd7b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-23
EUtranCellTDD=$tdd1c
cr EUtranCellTDD=$tdd7b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-24
EUtranCellTDD=$tdd1d
cr EUtranCellTDD=$tdd7b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-31
EUtranCellTDD=$tdd2a
cr EUtranCellTDD=$tdd7b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-32
EUtranCellTDD=$tdd2b
cr EUtranCellTDD=$tdd7b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-33
EUtranCellTDD=$tdd2c
cr EUtranCellTDD=$tdd7b,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-34
EUtranCellTDD=$tdd2d
cr EUtranCellTDD=$tdd7b,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-41
EUtranCellFDD=$fdd8a
cr EUtranCellTDD=$tdd7b,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-42
EUtranCellFDD=$fdd8b
cr EUtranCellTDD=$tdd7b,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-43
EUtranCellFDD=$fdd8c
cr EUtranCellTDD=$tdd7b,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-44
EUtranCellFDD=$fdd8d
cr EUtranCellTDD=$tdd7b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-11
EUtranCellFDD=$fdd3a
cr EUtranCellTDD=$tdd7b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-12
EUtranCellFDD=$fdd3b
cr EUtranCellTDD=$tdd7b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-13
EUtranCellFDD=$fdd3c
cr EUtranCellTDD=$tdd7b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-14
EUtranCellFDD=$fdd3d
cr EUtranCellTDD=$tdd7b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-61
EUtranCellTDD=$tdd6a
cr EUtranCellTDD=$tdd7b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-62
EUtranCellTDD=$tdd6b
cr EUtranCellTDD=$tdd7b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-63
EUtranCellTDD=$tdd6c
cr EUtranCellTDD=$tdd7b,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-64
EUtranCellTDD=$tdd6d
cr EUtranCellTDD=$tdd7b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-51
EUtranCellFDD=$fdd5a
cr EUtranCellTDD=$tdd7b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-52
EUtranCellFDD=$fdd5b
cr EUtranCellTDD=$tdd7b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-53
EUtranCellFDD=$fdd5c
cr EUtranCellTDD=$tdd7b,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-54
EUtranCellFDD=$fdd5d

cr EUtranCellTDD=$tdd7c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-21
EUtranCellTDD=$tdd1a
cr EUtranCellTDD=$tdd7c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-22
EUtranCellTDD=$tdd1b
cr EUtranCellTDD=$tdd7c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-23
EUtranCellTDD=$tdd1c
cr EUtranCellTDD=$tdd7c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-24
EUtranCellTDD=$tdd1d
cr EUtranCellTDD=$tdd7c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-31
EUtranCellTDD=$tdd2a
cr EUtranCellTDD=$tdd7c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-32
EUtranCellTDD=$tdd2b
cr EUtranCellTDD=$tdd7c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-33
EUtranCellTDD=$tdd2c
cr EUtranCellTDD=$tdd7c,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-34
EUtranCellTDD=$tdd2d
cr EUtranCellTDD=$tdd7c,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-41
EUtranCellFDD=$fdd8a
cr EUtranCellTDD=$tdd7c,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-42
EUtranCellFDD=$fdd8b
cr EUtranCellTDD=$tdd7c,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-43
EUtranCellFDD=$fdd8c
cr EUtranCellTDD=$tdd7c,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-44
EUtranCellFDD=$fdd8d
cr EUtranCellTDD=$tdd7c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-11
EUtranCellFDD=$fdd3a
cr EUtranCellTDD=$tdd7c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-12
EUtranCellFDD=$fdd3b
cr EUtranCellTDD=$tdd7c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-13
EUtranCellFDD=$fdd3c
cr EUtranCellTDD=$tdd7c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-14
EUtranCellFDD=$fdd3d
cr EUtranCellTDD=$tdd7c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-61
EUtranCellTDD=$tdd6a
cr EUtranCellTDD=$tdd7c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-62
EUtranCellTDD=$tdd6b
cr EUtranCellTDD=$tdd7c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-63
EUtranCellTDD=$tdd6c
cr EUtranCellTDD=$tdd7c,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-64
EUtranCellTDD=$tdd6d
cr EUtranCellTDD=$tdd7c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-51
EUtranCellFDD=$fdd5a
cr EUtranCellTDD=$tdd7c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-52
EUtranCellFDD=$fdd5b
cr EUtranCellTDD=$tdd7c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-53
EUtranCellFDD=$fdd5c
cr EUtranCellTDD=$tdd7c,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-54
EUtranCellFDD=$fdd5d


cr EUtranCellTDD=$tdd7d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-21
EUtranCellTDD=$tdd1a
cr EUtranCellTDD=$tdd7d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-22
EUtranCellTDD=$tdd1b
cr EUtranCellTDD=$tdd7d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-23
EUtranCellTDD=$tdd1c
cr EUtranCellTDD=$tdd7d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-24
EUtranCellTDD=$tdd1d
cr EUtranCellTDD=$tdd7d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-31
EUtranCellTDD=$tdd2a
cr EUtranCellTDD=$tdd7d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-32
EUtranCellTDD=$tdd2b
cr EUtranCellTDD=$tdd7d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-33
EUtranCellTDD=$tdd2c
cr EUtranCellTDD=$tdd7d,EUtranFreqRelation=39294,EUtranCellRelation=40449-$enbid-34
EUtranCellTDD=$tdd2d
cr EUtranCellTDD=$tdd7d,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-41
EUtranCellFDD=$fdd8a
cr EUtranCellTDD=$tdd7d,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-42
EUtranCellFDD=$fdd8b
cr EUtranCellTDD=$tdd7d,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-43
EUtranCellFDD=$fdd8c
cr EUtranCellTDD=$tdd7d,EUtranFreqRelation=3690,EUtranCellRelation=40449-$enbid-44
EUtranCellFDD=$fdd8d
cr EUtranCellTDD=$tdd7d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-11
EUtranCellFDD=$fdd3a
cr EUtranCellTDD=$tdd7d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-12
EUtranCellFDD=$fdd3b
cr EUtranCellTDD=$tdd7d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-13
EUtranCellFDD=$fdd3c
cr EUtranCellTDD=$tdd7d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-14
EUtranCellFDD=$fdd3d
cr EUtranCellTDD=$tdd7d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-61
EUtranCellTDD=$tdd6a
cr EUtranCellTDD=$tdd7d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-62
EUtranCellTDD=$tdd6b
cr EUtranCellTDD=$tdd7d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-63
EUtranCellTDD=$tdd6c
cr EUtranCellTDD=$tdd7d,EUtranFreqRelation=39150,EUtranCellRelation=40449-$enbid-64
EUtranCellTDD=$tdd6d
cr EUtranCellTDD=$tdd7d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-51
EUtranCellFDD=$fdd5a
cr EUtranCellTDD=$tdd7d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-52
EUtranCellFDD=$fdd5b
cr EUtranCellTDD=$tdd7d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-53
EUtranCellFDD=$fdd5c
cr EUtranCellTDD=$tdd7d,EUtranFreqRelation=1415,EUtranCellRelation=40449-$enbid-54
EUtranCellFDD=$fdd5d


set ENodeBFunction=1,EUtranCell.*,EUtranFreqRelation=.*,EUtranCellRelation=40449-$enbid-.* loadBalancing 1






l+
cvls
gsg+
confb+

###################PSF Mandatory Features#######################################
set SystemFunctions=1,Lm=1,FeatureState=CXC4011958 featureState 1
set SystemFunctions=1,Licensing=1,OptionalFeatureLicense=CellSleepMode featureState 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4011808 featureState 1
set SystemFunctions=1,Licensing=1,OptionalFeatureLicense=MIMOSleepMode Featurestate 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4011803 featureState 1
set SystemFunctions=1,Licensing=1,OptionalFeatureLicense=MicroSleepTx Featurestate 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4011378 featureState 1
set SystemFunctions=1,Licensing=1,OptionalFeatureLicense=CellSoftLock Featurestate 1
###################PSF Mandatory Features########################################


#####################Cell Sleep Function Parameters############################
set EUtranCellTDD=.*,CellSleepFunction=1 sleepMode 1
set EUtranCellFDD=.*,CellSleepFunction=1 sleepMode 0
set EUtranCellTDD=.*,CellSleepFunction=1 sleepStartTime 18:30
set EUtranCellTDD=.*,CellSleepFunction=1 sleepEndTime 00:30
set EUtranCellTDD=.*,CellSleepFunction=1 capCellSleepMonitorDurTimer 5
set EUtranCellTDD=.*,CellSleepFunction=1 capCellDlPrbSleepThreshold 40
set EUtranCellTDD=.*,CellSleepFunction=1 capCellRrcConnSleepThreshold 90
set EUtranCellTDD=.*,CellSleepFunction=1 covCellWakeUpMonitorDurTimer 15
set EUtranCellTDD=.*,CellSleepFunction=1 covCellDlPrbWakeUpThreshold 55
set EUtranCellTDD=.*,CellSleepFunction=1 covCellRrcConnWakeUpThreshold 100
set EUtranCellTDD=.*,CellSleepFunction=1 coverageCellDiscovery true
set EUtranCellTDD=.*,CellSleepFunction=1 capCellMobReasNotSleepThr -1
set EUtranCellTDD=.*,CellSleepFunction=1 capCellSleepProhibitInterval 0
set EUtranCellTDD=.*,CellSleepFunction=1 isCleanupHitRateTable TRUE
set EUtranCellTDD=.*,CellSleepFunction=1 covCellUeLostWakeUpThr 100
set EUtranCellTDD=.*,CellSleepFunction=1 covCellRrcReestWakeUpThr 100
set EUtranCellTDD=.*,CellSleepFunction=1 covCellUeCtxtRelMin 200
set EUtranCellTDD=.*,CellSleepFunction=1 covCellRrcConnEstAttMin 200
set EUtranCellTDD=.*,CellSleepFunction=1 covCellLatestStatsAdaRatio 60
set EUtranCellTDD=.*,CellSleepFunction=1 isAllowedMsmOnCovCell true
set EUtranCellTDD=.*,CellSleepFunction=1 wakeUpLastHoTime 2
set EUtranCellTDD=.*,CellSleepFunction=1 wakeUpWaitTimer 0
#####################Cell Sleep Function Parameters############################

###################MIMO Sleep function parameters #############################
set EUtranCellTDD=.*,MimoSleepFunction=1 sleepMode 4
set EUtranCellFDD=.*,MimoSleepFunction=1 sleepMode 0
set EUtranCellFDD=.*[G-J],MimoSleepFunction=1 sleepMode 0
set EUtranCellTDD=.*,MimoSleepFunction=1 sleepStartTime 18:30
set EUtranCellTDD=.*,MimoSleepFunction=1 sleepEndTime 02:30
set EUtranCellTDD=.*,MimoSleepFunction=1 sleepPowerControl 1
set EUtranCellTDD=.*,MimoSleepFunction=1 switchDownMonitorDurTimer 5
set EUtranCellTDD=.*,MimoSleepFunction=1 switchDownPrbThreshold 40
set EUtranCellTDD=.*,MimoSleepFunction=1 switchDownRrcConnThreshold 20
set EUtranCellTDD=.*,MimoSleepFunction=1 switchUpMonitorDurTimer 15
set EUtranCellTDD=.*,MimoSleepFunction=1 switchUpPrbThreshold 55
set EUtranCellTDD=.*,MimoSleepFunction=1 switchUpRrcConnThreshold 60
###################MIMO Sleep function parameters #######################################

###################Cellsleepnodefunction parameters######################################
set CellSleepNodeFunction=1 csmEutranInterFMeasReportDecr 1
set CellSleepNodeFunction=1  csmEutranInterFMeasReportIncr 10
set CellSleepNodeFunction=1  csmEutranInterFMeasReportMax 100
set CellSleepNodeFunction=1  csmEutranInterFMeasReportMin 5
set CellSleepNodeFunction=1  csmMinHitRateForCovCell 50
##################Cellsleepnodefunction parameters#########################################


#####################Hidden Paratmeters############################
seti ENodeBFunction=1    csmCovDiscoveryCycleTime  1
set ENodeBFunction=1  csmMinHighHitThreshold  50
#####################Hidden Paratmeters############################


#####################EUtranFreqrelation Parameters#####################################
set EUtranCellTDD=.*,EUtranFreqRelation=39150 cellSleepCovCellMeasOn false
set EUtranCellTDD=.*,EUtranFreqRelation=39294 cellSleepCovCellMeasOn false
set EUtranCellTDD=.*,EUtranFreqRelation=1415 cellSleepCovCellMeasOn true
set EUtranCellTDD=.*,EUtranFreqRelation=3690 cellSleepCovCellMeasOn ture
set EUtranCellTDD=.*,EUtranFreqRelation=.* csmUeCapMonitorEnabled false
set EUtrancellFDD=.*,EUtranFreqRelation=.* cellSleepCovCellMeasOn false
set EUtrancellFDD=.*,EUtranFreqRelation=.* csmUeCapMonitorEnabled false
set EUtranCellFDD=.*,EUtranFreqRelation=3690 cellSleepCovCellMeasOn true
set EUtrancellFDD=.*,EUtranFreqRelation=.* csmUeCapMonitorTime 60
#####################EUtranFreqrelation Parameters#####################################

#####################EUtranCell relation & UE Measure control&ENodeBFunction Parameters#####################################
set EUtranCellTDD=.*,EUtranFreqRelation=1415,EUtranCellRelation=.* sleepModeCovCellCandidate 2
set EUtranCellTDD=.*,EUtranFreqRelation=3690,EUtranCellRelation=.* sleepModeCovCellCandidate 2
set EUtranCell.*=.*,UeMeasControl=1   maxNoMeasReportsInact   1
set ENodeBFunction=1 csmMinHighHitThreshold 50
#####################EUtranCell relation & UE Measure control&ENodeBFunction Parameters#####################################

ma unlockedcells ^eutrancell administrativestate 1
bl unlockedcells
wait 10
deb unlockedcells
wait 10
ue print -admitted

wait 3

get router=.*OAM routerid > $routerOAM
get router=.*CP routerid > $routerCP
get router=.*UP routerid > $routerUP

get router=$routerOAM,.*,nexthop address > $nextOam
get router=$routerCP,.*,nexthop address > $nextCP
get router=$routerUP,.*,nexthop address > $nextUP

get Transport=1,Router=$routerOAM,RouteTableIPv4Static= routeTableIPv4StaticId > $OAMRouteTableid
get Transport=1,Router=$routerCP,RouteTableIPv4Static= routeTableIPv4StaticId > $CPRouteTableid
get Transport=1,Router=$routerUP,RouteTableIPv4Static= routeTableIPv4StaticId > $UPRouteTableid

get router=$routerOAM,.*,nexthop nextHopId > $OamNextHopID
get router=$routerCP,.*,nexthop nextHopId > $CPNextHopID
get router=$routerUP,.*,nexthop nextHopId > $UPNextHopID



cr Transport=1,Router=$routerOAM,RouteTableIPv4Static=$OAMRouteTableid,Dst=OSS
0.0.0.0/0

cr Transport=1,Router=$routerOAM,RouteTableIPv4Static=$OAMRouteTableid,Dst=OSS,NextHop=$OAMRouteTableid
$nextOam
false
d
d


cr Transport=1,Router=$routerUP,RouteTableIPv4Static=$UPRouteTableid,Dst=UP
0.0.0.0/0

cr Transport=1,Router=$routerUP,RouteTableIPv4Static=$UPRouteTableid,Dst=UP,NextHop=$UPRouteTableid
$nextUP
false
d
d
cr Transport=1,Router=$routerCP,RouteTableIPv4Static=$CPRouteTableid,Dst=CP
0.0.0.0/0

cr Transport=1,Router=$routerCP,RouteTableIPv4Static=$CPRouteTableid,Dst=CP,NextHop=$CPRouteTableid
$nextCP
false
d
d
rdel dst=sgw
rdel dst=x2-up
rdel dst=mme.*
rdel dst=rnc
rdel dst=x2-cp.*
rdel dst=oss[1-6]$
rdel dst=.*ENM
rdel dst=twamp





confb+
gsg+
cvls
scg
scw 1225:50
set EUtranCellTDD=.* DuctIntPerfTuning ductIntSlopePwrDiffThr=5,ductIntCharSeqTransThr=10
scw L4885:1
scw 99:12,109:12
scg
wait 5    



set SystemFunctions=1,Lm=1,FeatureState=CXC4040009 featureState 1
gs+
crn Transport=1,Router=LTEUP,TwampResponder=1
ipAddress Router=LTEUP,InterfaceIPv4=TN_A_UP,AddressIPv4=TN_A_UP
udpPort 4001
userLabel
end
crn Transport=1,Router=LTEUP,TwampResponder=1
ipAddress Router=LTEUP,InterfaceIPv4=TN_C_UP,AddressIPv4=TN_C_UP
udpPort 4001
userLabel
end
crn Transport=1,Router=LTEUP,TwampResponder=1
ipAddress Router=LTEUP,InterfaceIPv4=TN_B_UP,AddressIPv4=TN_B_UP
udpPort 4001
userLabel
end

crn Transport=1,Router=LTEUP,TwampResponder=1
ipAddress Router=LTEUP,InterfaceIPv4=TN_E_UP,AddressIPv4=TN_E_UP
udpPort 4001
userLabel
end

Confbd+
gs+

crn SystemFunctions=1,SysM=1,Snmp=1,SnmpTargetV3=1
address 2401:4900:00d4:1700:0000:0000:0000:039C
administrativeState 1
authKey cleartext=false,password=1:RkajtHw5NwfrzL/lRWBD86fXNaqB5UHHZff49WY=
authProtocol 0
informRetryCount 1
informTimeout 300
isMibWritable true
port 162
privKey cleartext=false,password=1:vvcwYuJv1d7wmpnxX88t8ybPjWu+YH9+z5sx56E=
privProtocol 0
snmpSecurityLevel 1
transportMethod 2
user ECIMUser
end

cvms PostGPL
gs-
confb-

"""


AP_TN_RN_GPS_MME = """
confb+
gs+

$script_nodename = {eNodeBName}
if $nodename != $script_nodename
   l echo "This node is called $nodename but the command file should be loaded in {eNodeBName}"
   return
fi

if $moshell_version ~ ^([7-9]|10)
   l echo "The moshell version is too old. 11.0a or higher is required for scripts containing the crn command."
   return
fi

###################################### TN SCRIPT ######################################

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

cr Transport=1,Router=LTEUP,TwampResponder=1
Transport=1,Router=LTEUP,InterfaceIPv4={tnPortId}_UP,AddressIPv4={tnPortId}_UP
4001

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
localIpAddress       Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP
portNumber 36422
sctpProfile          Transport=1,SctpProfile=1
end

###################################### RN SCRIPT ######################################

crn ENodeBFunction=1
eNodeBPlmnId mcc=404,mnc=70,mncLength=2
eNBId {eNBId}
sctpRef              Transport=1,SctpEndpoint=1
tRelocOverall 20
upIpAddressRef       Transport=1,Router=LTEUP,InterfaceIPv4={tnPortId}_UP,AddressIPv4={tnPortId}_UP
end



###################################### GPS SCRIPT ######################################

lbl RadioEquipmentClockReference=1
lbl RadioEquipmentClockReference=2

del RadioEquipmentClockReference=1
y
del RadioEquipmentClockReference=2
y
del Transport=1,Synchronization=1,FrequencySyncIO=1
y

crn Equipment=1,FieldReplaceableUnit=4,SyncPort=1
userLabel
end

ld Transport=1,Synchronization=1
lset Transport=1,Synchronization=1$ fixedPosition true
lset Transport=1,Synchronization=1$ telecomStandard 1

crn Transport=1,Synchronization=1,TimeSyncIO=1
encapsulation Equipment=1,FieldReplaceableUnit=4,SyncPort=1
end

cr Transport=1,Synchronization=1,TimeSyncIO=1,GnssInfo=1

crn Transport=1,Synchronization=1,RadioEquipmentClock=1
minQualityLevel qualityLevelValueOptionI=2,qualityLevelValueOptionII=2,qualityLevelValueOptionIII=1
end

crn Transport=1,Synchronization=1,RadioEquipmentClock=1,RadioEquipmentClockReference=1
adminQualityLevel qualityLevelValueOptionI=2,qualityLevelValueOptionII=2,qualityLevelValueOptionIII=1
administrativeState 0
encapsulation Transport=1,Synchronization=1,TimeSyncIO=1
priority 1
end

bl Transport=1,Synchronization=1,RadioEquipmentClock=1,NodeGroupSyncMember=1
set Transport=1,Synchronization=1,RadioEquipmentClock=1,NodeGroupSyncMember=1 syncNodePriority 3
deb Transport=1,Synchronization=1,RadioEquipmentClock=1,NodeGroupSyncMember=1

ldeb RadioEquipmentClockReference=1



"""


AP_Route_5G_GPL_LMS = """

lt all     	                                                                                                                                                       
rbs                                                                                                                                                        
rbs                                                                                                                                                               
confbd+                                                                                                                                                           
                                                                                                                                                                  
$date = `date +%y%m%d_%H%M`                                                                                                                                       
cvms Pre_5G_GPL_$date                                                                                                                                         
                                

                                                                        
confbd+
gs+

set GNBDUFunction=1                                         endpointResourceRef GNBDUFunction=1,EndpointResource=1
set GNBCUUPFunction=1                                         endpointResourceRef GNBCUUPFunction=1,EndpointResource=1
set GNBCUCPFunction=1                                         endpointResourceRef GNBCUCPFunction=1,EndpointResource=1

set GNBCUCPFunction=1,EndpointResource=1,LocalSctpEndpoint=3 sctpEndpointRef   SctpEndpoint=F1_NRCUCP
set GNBDUFunction=1,EndpointResource=1,LocalSctpEndpoint=1  sctpEndpointRef   SctpEndpoint=F1_NRDU
set GNBCUCPFunction=1,EndpointResource=1,LocalSctpEndpoint=1 sctpEndpointRef   SctpEndpoint=NG
set GNBCUCPFunction=1,EndpointResource=1,LocalSctpEndpoint=2 sctpEndpointRef   SctpEndpoint=X2



crn GNBCUUPFunction=1,EndpointResource=1,LocalIpEndpoint=1
addressRef                           Transport=1,Router=LTE_NR,InterfaceIPv6=NR,AddressIPv6=NR_S1U_OAM
interfaceList                        4 5 7 6
mode                                 0
end


crn GNBCUCPFunction=1,IntraFreqMC=1
end





crn GNBDUFunction=1,MassiveMimoSleep=1
end

crn GNBDUFunction=1,MassiveMimoSleep=1,MMimoSleepTimeGroup=1
end

crn GNBDUFunction=1,MassiveMimoSleep=1,MMimoSleepProfile=1
sleepMode                            0
switchDownMonitorDurTimer            60
switchDownMonitorDurTimerEco         300
switchDownPrbThreshDl                10
switchDownPrbThreshDlEco             15
switchDownPrbThreshUlEco             10
switchDownRrcConnThresh              10
switchDownRrcConnThreshEco           30
switchUpMonitorDurTimer              30
switchUpMonitorDurTimerEco           120
switchUpPrbThreshDl                  20
switchUpPrbThreshDlEco               30
switchUpPrbThreshUlEco               15
switchUpRrcConnThresh                20
switchUpRrcConnThreshEco             50
end

crn GNBDUFunction=1,MassiveMimoSleep=1,MMimoSleepTimeGroup=1,MMimoSleepTimeWindow=1
dayOfWeek                            0
mMimoSleepProfileRef                 MassiveMimoSleep=1,MMimoSleepProfile=1
startTime                            20:30
stopTime                             23:30
end


set GNBDUFunction=1,NRSectorCarrier=.* mMimoSleepTimeGroupRef               MassiveMimoSleep=1,MMimoSleepTimeGroup=1



crn GNBCUCPFunction=1,AnrFunction=1
removeEnbTime                        7
removeFreqRelTime                    15
removeGnbTime                        7
removeNrelTime                       7
end

crn GNBCUCPFunction=1,AnrFunction=1,AnrFunctionNR=1
anrAutoCreateXnForEndc               true
anrCgiMeasInterFreqMode              1
anrCgiMeasIntraFreqEnabled           true
anrEndcX2Enabled                     true
end


crn GNBCUCPFunction=1,Mcpc=1,McpcPSCellProfile=Default
ueConfGroupType                      0
userLabel
end

crn GNBCUCPFunction=1,IntraFreqMC=1,IntraFreqMCCellProfile=Default
ueConfGroupType                      0
userLabel
end


crn GNBCUCPFunction=1,UeMC=1,UeMCNrFreqRelProfile=Midband
ueConfGroupType                      0
userLabel
end


crn ENodeBFunction=1,EndcProfile=1
meNbS1TermReqArpLev                  0
splitNotAllowedUeArpLev              0
userLabel
end

crn ENodeBFunction=1,EndcProfile=2
meNbS1TermReqArpLev                  15
splitNotAllowedUeArpLev              0
userLabel
end

set QciTable=default,QciProfilePredefined=qci5              endcProfileRef    EndcProfile=2
set QciTable=default,QciProfilePredefined=qci6$             endcProfileRef    EndcProfile=1
set QciTable=default,QciProfilePredefined=qci7$             endcProfileRef    EndcProfile=1
set QciTable=default,QciProfilePredefined=qci8              endcProfileRef    EndcProfile=1
set QciTable=default,QciProfilePredefined=qci9              endcProfileRef    EndcProfile=1




crn ENodeBFunction=1,PmFlexCounterFilter=ENDC
arpFilterEnabled                     false
arpFilterMax                         0
arpFilterMin                         0
ceLevelFilterEnabled                 false
ceLevelFilterMax                     0
ceLevelFilterMin                     0
endcFilterEnabled                    true
lcgFilterEnabled                     false
pciFilterEnabled                     false
plmnFilterEnabled                    false
pviFilterEnabled                     false
qciFilterEnabled                     false
reportAppCounterOnly                 true
spidFilterEnabled                    false
spidFilterMax                        1
spidFilterMin                        1
subscriberGroupFilterEnabled         false
subscriberGroupFilterMax             0
subscriberGroupFilterMin             0
ueCatFilterEnabled                   false
ueCatFilterMax                       0
ueCatFilterMin                       0
uePowerClassFilterEnabled            false
uePowerClassFilterMax                1
uePowerClassFilterMin                1
end

crn ENodeBFunction=1,UePolicyOptimization=1
coverageAwareImc                     true
endcAwareImc                         2
t320                                 180
ueCapPrioList                        0
zzzTemporary1                        1
zzzTemporary2                        -2000000000
zzzTemporary3                        -2000000000
end


crn GNBCUUPFunction=1,GtpuSupervision=1
end


crn GNBCUUPFunction=1,GtpuSupervision=1,GtpuSupervisionProfile=S1
endpointResourceRef                  
gtpuEchoDscp                         32
gtpuEchoEnabled                      true
interfaceList                        5
userLabel
end


crn GNBCUUPFunction=1,GtpuSupervision=1,GtpuSupervisionProfile=X2
endpointResourceRef                  
gtpuEchoDscp                         32
gtpuEchoEnabled                      true
interfaceList                        7
userLabel
end


set QosProfiles=1,DscpPcpMap=1  pcp0
set QosProfiles=1,DscpPcpMap=1  pcp1
set QosProfiles=1,DscpPcpMap=1  pcp2
set QosProfiles=1,DscpPcpMap=1  pcp3
set QosProfiles=1,DscpPcpMap=1  pcp4
set QosProfiles=1,DscpPcpMap=1  pcp5
set QosProfiles=1,DscpPcpMap=1  pcp6
set QosProfiles=1,DscpPcpMap=1  pcp7
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp0 0,1,2,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,36,37,38,39,41,43,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp2 22 24 26
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp3 6 8 10 30 32
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp4 12 14 40
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp5 4 28
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp6 16 18 34 42 44
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp7 20 46

set QosProfiles=1,DscpPcpMap=1    pcp7   20 46                                                                       
set QosProfiles=1,DscpPcpMap=1    pcp6   16 18 34 42 44                                                              
set QosProfiles=1,DscpPcpMap=1    pcp5   4 28                                                                        
set QosProfiles=1,DscpPcpMap=1    pcp4   12 14 40                                                                    
set QosProfiles=1,DscpPcpMap=1    pcp3   6 8 10 30 32                                                                
set QosProfiles=1,DscpPcpMap=1    pcp2   22 24 26                                                                    
set QosProfiles=1,DscpPcpMap=1    pcp0   0 1 2 3 5 7 9 11 13 15 17 19 21 23 25 27 29 31 33 35 36 37 38 39 41 43 45 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63




set ENodeBFunction=1                                        zzzTemporary81    1                                                                                  
set UePolicyOptimization=1                                  zzzTemporary1     1                                                                                  
set EndcProfile=1                                           splitNotAllowedUeArpLev 0                                                                            
set EndcProfile=2                                           meNbS1TermReqArpLev 15                                                                               
set EUtranCellFDD=.*                      measGapPattEndc   1                                                                                  
set EUtranCellFDD=.*,UeMeasControl=1      maxMeasB1Endc     3                                                                                  
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          gNodebIdLength    26                                                                                 
set ENodeBFunction=1                                        endcS1OverlapMode true      
set EUtranCellFDD=.*,UeMeasControl=1      endcMeasTime      2000                                                                               
set EUtranCellFDD=.*,UeMeasControl=1      endcMeasRestartTime 10000                                                                            
set ENodeBFunction=1                                        endcDataUsageReportEnabled true                                                                      
set EUtranCellFDD=.*,UeMeasControl=1      endcB1MeasWindow  40                                                                                 
set QciTable=default,QciProfilePredefined=qci1              dscp              34                                                                                 
set QciTable=default,QciProfilePredefined=qci2              dscp              34                                                                                 
set QciTable=default,QciProfilePredefined=qci3              dscp              26                                                                                 
set QciTable=default,QciProfilePredefined=qci4              dscp              26                                                                                 
set QciTable=default,QciProfilePredefined=qci5              dscp              46                                                                                 
set QciTable=default,QciProfilePredefined=qci6$             dscp              32    
set QciTable=default,QciProfilePredefined=qci7$             dscp              40   
set QciTable=default,QciProfilePredefined=qci8              dscp              30                                                                                 
set QciTable=default,QciProfilePredefined=qci9              dscp              26                                                                                 
set CarrierAggregationFunction=1                            dcSCellDeactDelayTimer 200                                                                           
set CarrierAggregationFunction=1                            dcSCellActDeactDataThresHyst 30                                                                      
set CarrierAggregationFunction=1                            dcSCellActDeactDataThres 30                                                                          
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          anrStateNR        1                           
set EUtranCellFDD=.*,GUtranFreqRelation=627936 anrMeasOn         true                                                                          
set ENodeBFunction=1                                        x2retryTimerMaxAuto 1440                                                                             
set CarrierAggregationFunction=1                            endcCaPolicy      1                                                  


set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 ulMaxRetxThreshold 32                                                                              
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 ulMaxRetxThreshold 32                                                                              
set NRCellDU=.*                   ul256QamEnabled   true   
set GNBDUFunction=1,UeCC=1,RadioLinkControl=1,DrbRlc=Default,DrbRlcUeCfg=Base tStatusProhibitUl 10                                                               
set NRCellDU=.*                   trsPowerBoosting  0                                                                                  
set NRCellDU=.*                   trsPeriodicity    20                                                                                 
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 tPollRetransmitUl 80                                                                               
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 tPollRetransmitUl 80                                                                               
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 tPollRetransmitDl 80                                                                               
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 tPollRetransmitDl 80                                                                               
set GNBCUCPFunction=1,UeCC=1,InactivityProfile=Default,InactivityProfileUeCfg=Base tInactivityTimerEndcSn 5                                                      
set NRCellDU=.*                   tddUlDlPattern    1                                               
set NRCellDU=.*                   tddSpecialSlotPattern 3                                     
set GNBCUCPFunction=1                                       tDcOverall        11                                                                                 
set GNBDUFunction=1,Rrc=1                                   t319              400  
set GNBDUFunction=1,Rrc=1                                   t311              3000                                                                               
set GNBDUFunction=1,Rrc=1                                   t310              2000                                                                               
set GNBDUFunction=1,Rrc=1                                   t304              2000                                                                               
set GNBDUFunction=1,Rrc=1                                   t301              600                                                                                
set GNBDUFunction=1,Rrc=1                                   t300              1500                                                                               
set NRCellDU=.*                   subCarrierSpacing 30                                                                                 
set NRCellDU=.*                   ssbSubCarrierSpacing 30                                                                              
set NRCellDU=.*                   ssbPowerBoost     6                                                                                  
set NRCellDU=.*                   ssbPeriodicity    20                                                                                 
set NRCellDU=.*                   ssbOffset         0        
set NRCellDU=.*                   ssbDuration       1                                                                                  
set NRCellDU=.*                   srsPeriodicity    40                                                                                 
set NRCellDU=.*                   srsHoppingBandwidth 0                                                                         
set NRCellDU=.*                   secondaryCellOnly false                                                                              
set GNBCUCPFunction=1,AnrFunction=1                         removeNrelTime    7                                                                                                                           
set GNBCUCPFunction=1,AnrFunction=1                         removeGnbTime     7                                                                                  
set GNBCUCPFunction=1,AnrFunction=1                         removeEnbTime     7                                                                                  
set NRCellDU=.*                   rachPreambleTransMax 10                                                                              
set NRCellDU=.*                   rachPreambleRecTargetPower -110                                                                      
set NRCellDU=.*                   rachPreambleFormat 0                                        
set NRCellDU=.*                   pZeroUePuschOffset256Qam 4                                                                           
set NRCellDU=.*                   pZeroNomSrs       -110                                                                               
set NRCellDU=.*                   pZeroNomPuschGrant 1000                                                                              
set NRCellDU=.*                   pZeroNomPucch     -114                                                                               
set NRCellDU=.*                   puschStartPrbStrategy 3                                         
set NRCellDU=.*                   puschAllowedInDmrsSym true                                                                           
set GNBDUFunction=1,UeCC=1,Prescheduling=1,PreschedulingUeCfg=Base preschedulingUeMode 1                                                    
set GNBDUFunction=1,UeCC=1,Prescheduling=1,PreschedulingUeCfg=Base preschedulingDuration 100                                                                     
set NRCellDU=.*                   pMax              26                                                                                 
set NRCellDU=.*                   pdschStartPrbStrategy 3                                         
set NRCellDU=.*                   pdcchSymbConfig   0                                                                     
set NRCellDU=.*                   nrSrsDlPacketAgeThr 0                                                                                
set GNBDUFunction=1,Rrc=1                                   n311              1                                                                                  
set GNBDUFunction=1,Rrc=1                                   n310              20                                                                                 
set NRCellDU=.*                   maxUeSpeed        2                                                   
set NRCellDU=.*                   maxNoOfAdvancedDlMuMimoLayers 8                                                                      
set QciProfileEndcConfigExt=1                               initialUplinkConf 1   




                                                        
set GtpuSupervision=1,GtpuSupervisionProfile=S1             gtpuEchoEnabled   true                                                                               
set GtpuSupervision=1,GtpuSupervisionProfile=X2             gtpuEchoEnabled   true                                                                               
set GtpuSupervision=1,GtpuSupervisionProfile=S1             gtpuEchoDscp      32                                                                                 
set GtpuSupervision=1,GtpuSupervisionProfile=X2             gtpuEchoDscp      32                                                                                 
set GNBCUUPFunction=1,UeCC=1,AqmCfg=           estimatedE2ERTT   50                                                                                                                                                           
set ENodeBFunction=1                                        endcDataUsageReportEnabled true                                                                      
set IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base endcActionEvalFail 1                                             
set GNBDUFunction=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base drxRetransmissionTimerUl 8  
set GNBDUFunction=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base drxRetransmissionTimerDl 8                                                                    
set NRCellDU=.*                   drxProfileEnabled true                                                                               
set GNBDUFunction=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base drxOnDurationTimer 39
set GNBDUFunction=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base drxLongCycle      10                                               
set GNBDUFunction=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base drxInactivityTimer 15
set GNBDUFunction=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base drxEnabled        true                                                                        
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 dlMaxRetxThreshold 32                                                                              
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 dlMaxRetxThreshold 32                                                                              
set NRCellDU=.*                   dlDmrsMuxSinrThresh -10                                                                              
set NRCellDU=.*                   dl256QamEnabled   true                                                                               
set NRCellDU=.*                   dftSOfdmPuschEnabled true                                                                            
set NRCellDU=.*                   dftSOfdmMsg3Enabled true                                                                             
set GNBCUUPFunction=1                                       dcDlPdcpInitialScgRate 100               
set NRCellDU=.*                   csiRsShiftingSecondary 1                                         
set NRCellDU=.*                   csiRsShiftingPrimary 1                                 
set NRCellDU=.*                   csiRsPeriodicity  40                                                                                 
set NRCellDU=.*                   csiRsConfig8P     csiRsControl8Ports=1,i11Restriction=FFFF,i12Restriction=                                                                         
set NRCellDU=.*                   csiRsConfig32P    csiRsControl32Ports=1,i11Restriction=FFFFFFFF,i12Restriction=FF                                                                        
set NRCellDU=.*                   csiRsActivePortConfig 2 4                   
set NRSectorCarrier=.*                                 configuredMaxTxPower 200000                                                                          
                                                                              
set NRSectorCarrier=.*,CommonBeamforming=1              cbfMacroTaperType 0
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          anrStateNR        1                           
set GNBCUCPFunction=1,AnrFunction=1,AnrFunctionNR=1         anrEndcX2Enabled  true                                                                               
set GNBCUCPFunction=1,AnrFunction=1,AnrFunctionNR=1         anrCgiMeasIntraFreqEnabled true                                                                      
set GNBCUCPFunction=1,AnrFunction=1,AnrFunctionNR=1         anrAutoCreateXnForEndc true                                                                          
set NRCellDU=.*                   advancedDlSuMimoEnabled true                                                                         
set NRCellDU=.*                   additionalPucchForCaEnabled false                                                                    
set NRCellDU=.*                   ulMaxMuMimoLayers 4                                                                                  
set GNBDUFunction=1,UeCC=1,Prescheduling=1,PreschedulingUeCfg=Base preschedulingDataSize 86                                                                      
set NRCellDU=.*                   pdschAllowedInDmrsSym true                                                                           
set NRSectorCarrier=.*                                  nRMicroSleepTxEnabled true                                                                           
set NRCellDU=.*                   maxUsersRachSchedPusch 100                                                                           
set NRCellDU=.*                   dlMaxMuMimoLayers 8                                                                                  
set NRCellDU=.*                   csiRsConfig4P     csiRsControl4Ports=OFF,i11Restriction=,i12Restriction=        
set NRSectorCarrier=.*,CommonBeamforming=1              coverageShape     1
set NRCellDU=.*                   nrSrsDlBufferVolThr 100                                                                              
set NRCellDU=.*                   pdcchLaSinrOffset -20      

                                                                          
set ENodeBFunction=1                                        s1GtpuEchoEnable  1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          anrStateNR        1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          gNodebIdLength    26
Set ENodeBFunction=1                                        endcX2IpAddrViaS1Active true
set ENodeBFunction=1                                        endcAllowed       true
set ENodeBFunction=1                                        endcAwareMfbiIntraCellHo false
set ENodeBFunction=1                                        endcDataUsageReportEnabled true
set ENodeBFunction=1                                        endcIntraBandBlocked true
set ENodeBFunction=1                                        endcPowerOffsetLte 3
set ENodeBFunction=1                                        endcS1OverlapMode true
set ENodeBFunction=1                                        endcSplitAllowedMoVoice false
set ENodeBFunction=1                                        endcSplitAllowedNonDynPwrShUe false

set ENodeBFunction=1                                        endcOverheatingAssistance true
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          endcRachFailThrPerUe 5
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          scgSessTimeForEndcRachFail 2500
set PmFlexCounterFilter=ENDC                                endcFilterMin     2



set ENodeBFunction=1,EndcProfile=1 meNbS1TermReqArpLev 0                                                                                                          
set ENodeBFunction=1,EndcProfile=1 splitNotAllowedUeArpLev 0 
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci[6789]$ endcProfileRef ENodeBFunction=1,EndcProfile=1


cr ENodeBFunction=1,UePolicyOptimization=1 
                                                                                                                       
set ENodeBFunction=1,UePolicyOptimization=1 ueCapPrioList 0                                                                                                       
set ENodeBFunction=1,UePolicyOptimization=1 coverageAwareImc true 
set UePolicyOptimization=1                                  endcAwareImc      2
set EUtranCellFDD=.*                    endcB1MeasGapEnabled true
set EUtranCellFDD=.*                      endcB1MeasGapConfig 0
set EUtranCellFDD=.*                      endcSetupUlBsVolThr 5000
set EUtranCellFDD=.*                      loopingEndcBackoffDuration 200
set EUtranCellFDD=.*                      loopingEndcProtectionEnabled true
set EUtranCellFDD=.*                      loopingEndcShortScgSessTime 3000

set EutrancellFDD additionalUpperLayerIndList          1 1 1 1 1                                                    
set EutrancellFDD endcSetupDlPktVolThr                 5                                                                                                                            
set EutrancellFDD primaryUpperLayerInd                 1

set EutrancellTDD additionalUpperLayerIndList          1 1 1 1 1                                                    
set EutrancellTDD endcSetupDlPktVolThr                 5                                                                                                                            
set EutrancellTDD primaryUpperLayerInd                 1



set CXC4040004 FeatureState  1
set CXC4040005 FeatureState  1
set CXC4040006 FeatureState  1
set CXC4040008 FeatureState  1
set CXC4040009 FeatureState  1
set CXC4040010 FeatureState  1
set CXC4040014 FeatureState  1
set CXC4012492 FeatureState  1
set CXC4012271 FeatureState  1
set CXC4011067 FeatureState  1
set CXC4010963 FeatureState  1
set CXC4012505 FeatureState  1
set CXC4012356 FeatureState  1
set CXC4012200 FeatureState  1
set CXC4012199 FeatureState  1
set CXC4012349 FeatureState  1
set CXC4012018 FeatureState  1
set CXC4011814 FeatureState  1
set CXC4010320 FeatureState  1
set CXC4012590 FeatureState  1
set CXC4012510 FeatureState  1
set CXC4011967 FeatureState  1
set CXC4010620 FeatureState  1
set CXC4011422 FeatureState  1
set CXC4012256 FeatureState  1
set CXC4011373 FeatureState  1
set CXC4012123 FeatureState  1
set CXC4012218 FeatureState  1
set CXC4011370 FeatureState  1
set CXC4012371 FeatureState  1
set CXC4011476 FeatureState  1
set CXC4011666 FeatureState  1
set CXC4011922 FeatureState  1
set CXC4012374 FeatureState  1
set CXC4011958 FeatureState  1
set CXC4011378 FeatureState  1
set CXC4012097 FeatureState  1
set CXC4011698 FeatureState  1
set CXC4012589 FeatureState  1
set CXC4011910 FeatureState  1
set CXC4010949 FeatureState  1
set CXC4010956 FeatureState  1
set CXC4012129 FeatureState  1
set CXC4011064 FeatureState  1
set CXC4012238 FeatureState  1
set CXC4012373 FeatureState  1
set CXC4012089 FeatureState  1
set CXC4011062 FeatureState  1
set CXC4011951 FeatureState  1
set CXC4011969 FeatureState  1
set CXC4012558 FeatureState  1
set CXC4011255 FeatureState  1
set CXC4012326 FeatureState  1
set CXC4012406 FeatureState  1
set CXC4010912 FeatureState  1
set CXC4010609 FeatureState  1
set CXC4011060 FeatureState  1
set CXC4011061 FeatureState  1
set CXC4011937 FeatureState  1
set CXC4011559 FeatureState  1
set CXC4011940 FeatureState  1
set CXC4011034 FeatureState  1
set CXC4012504 FeatureState  1
set CXC4012381 FeatureState  1
set CXC4011069 FeatureState  1
set CXC4010964 FeatureState  1
set CXC4011245 FeatureState  1
set CXC4011482 FeatureState  1
set CXC4012316 FeatureState  1
set CXC4011930 FeatureState  1
set CXC4012111 FeatureState  1
set CXC4010618 FeatureState  1
set CXC4011256 FeatureState  1
set CXC4011157 FeatureState  1
set CXC4011941 FeatureState  1
set CXC4012385 FeatureState  1
set CXC4011983 FeatureState  1
set CXC4010770 FeatureState  1
set CXC4011319 FeatureState  1
set CXC4010974 FeatureState  1
set CXC4011804 FeatureState  1
set CXC4011557 FeatureState  1
set CXC4011443 FeatureState  1
set CXC4010613 FeatureState  1
set CXC4010319 FeatureState  1
set CXC4012273 FeatureState  1
set CXC4012375 FeatureState  1
set CXC4011807 FeatureState  1
set CXC4011481 FeatureState  1
set CXC4011372 FeatureState  1
set CXC4012578 FeatureState  1
set CXC4011808 FeatureState  1
set CXC4012502 FeatureState  1
set CXC4012272 FeatureState  1
set CXC4010967 FeatureState  1
set CXC4012015 FeatureState  1
set CXC4011018 FeatureState  1
set CXC4011811 FeatureState  1
set CXC4011345 FeatureState  1
set CXC4011982 FeatureState  1
set CXC4010723 FeatureState  1
set CXC4011485 FeatureState  1
set CXC4011815 FeatureState  1
set CXC4011366 FeatureState  1
set CXC4012324 FeatureState  1
set CXC4012534 FeatureState  1
set CXC4012549 FeatureState  1
set CXC4012547 FeatureState  1
set CXC4012503 FeatureState  1
set CXC4011068 FeatureState  1
set CXC4011163 FeatureState  1
set CXC4012485 FeatureState  1
set CXC4012563 FeatureState  1
set CXC4011716 FeatureState  1
set CXC4010962 FeatureState  1
set CXC4011699 FeatureState  1
set CXC4011813 FeatureState  1
set CXC4011183 FeatureState  1
set CXC4011515 FeatureState  1
set CXC4011033 FeatureState  1
set CXC4010717 FeatureState  1
set CXC4012424 FeatureState  1
set CXC4012347 FeatureState  1
set CXC4011715 FeatureState  1
set CXC4011942 FeatureState  1
set CXC4011938 FeatureState  1
set CXC4011711 FeatureState  1
set CXC4010980 FeatureState  1
set CXC4011252 FeatureState  1
set CXC4010959 FeatureState  1
set CXC4011427 FeatureState  1
set CXC4011667 FeatureState  1
set CXC4011056 FeatureState  1
set CXC4011710 FeatureState  1
set CXC4011057 FeatureState  1
set CXC4010856 FeatureState  1
set CXC4010973 FeatureState  1
set CXC4011939 FeatureState  1
set CXC4012261 FeatureState  1
set CXC4012019 FeatureState  1
set CXC4010961 FeatureState  1
set CXC4010990 FeatureState  1
set CXC4011251 FeatureState  1
set CXC4011075 FeatureState  1
set CXC4011327 FeatureState  1
set CXC4012070 FeatureState  1
set CXC4011918 FeatureState  1
set CXC4011477 FeatureState  1
set CXC4011059 FeatureState  1
set CXC4011479 FeatureState  1
set CXC4012260 FeatureState  1
set CXC4011155 FeatureState  1
set CXC4011063 FeatureState  1
set CXC4012500 FeatureState  1
set CXC4012325 FeatureState  1
set CXC4011356 FeatureState  1
set CXC4011917 FeatureState  1
set CXC4011974 FeatureState  1
set CXC4011317 FeatureState  1
set CXC4011050 FeatureState  1
set CXC4011618 FeatureState  1
set CXC4012022 FeatureState  1
set CXC4011253 FeatureState  1
set CXC4011975 FeatureState  1
set CXC4011991 FeatureState  1
set CXC4011933 FeatureState  1
set CXC4012562 FeatureState  1
set CXC4010841 FeatureState  1
set CXC4011911 FeatureState  1
set CXC4011946 FeatureState  1
set CXC4011444 FeatureState  1
set CXC4012587 FeatureState  1
set CXC4012036 FeatureState  1
set CXC4011074 FeatureState  1
set CXC4011820 FeatureState  1
set CXC4012003 FeatureState  1
set CXC4011072 FeatureState  1
set CXC4012330 FeatureState  1
set CXC4012493 FeatureState  1
set CXC4011258 FeatureState  1
set CXC4011823 FeatureState  1
set CXC4012259 FeatureState  1
set CXC4011914 FeatureState  1
set CXC4012333 FeatureState  1
set CXC4011011 FeatureState  1
set CXC4010616 FeatureState  1
set CXC4011707 FeatureState  1
set CXC4011809 FeatureState  1


crn ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci30
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
dscpArpMap                           dscpArp1=-1,dscpArp10=-1,dscpArp11=-1,dscpArp12=-1,dscpArp13=-1,dscpArp14=-1,dscpArp15=-1,dscpArp2=-1,dscpArp3=-1,dscpArp4=-1,dscpArp5=-1,dscpArp6=-1,dscpArp7=-1,dscpArp8=-1,dscpArp9=-1
endcProfileRef                       EndcProfile=1
harqPriority                         0
inactivityTimerOffset                0
laaSupported                         true
lessMaxDelayThreshold                0
logicalChannelGroupRef               QciTable=default,LogicalChannelGroup=3
measReportConfigParams               a1ThresholdRsrpPrimOffset=0,a1ThresholdRsrpSecOffset=0,a1ThresholdRsrqPrimOffset=0,a1ThresholdRsrqSecOffset=0,a2ThresholdRsrpPrimOffset=0,a2ThresholdRsrpSecOffset=0,a2ThresholdRsrqPrimOffset=0,a2ThresholdRsrqSecOffset=0,a3InterOffsetAdjustmentRsrp=0,a3InterOffsetAdjustmentRsrq=0,a3IntraOffsetAdjustmentRsrp=0,a3IntraOffsetAdjustmentRsrq=0,a5Threshold1RsrpOffset=0,a5Threshold1RsrqOffset=0,a5Threshold2RsrpOffset=0,a5Threshold2RsrqOffset=0,b2Threshold1RsrpCdma2000Offset=0,b2Threshold1RsrpGeranOffset=0,b2Threshold1RsrpUtraOffset=0,b2Threshold1RsrqCdma2000Offset=0,b2Threshold1RsrqGeranOffset=0,b2Threshold1RsrqUtraOffset=0,b2Threshold2Cdma2000Offset=0,b2Threshold2EcNoUtraOffset=0,b2Threshold2GeranOffset=0,b2Threshold2RscpUtraOffset=0,offsetPerQciPrio=0,timeToTriggerInterA3=-1,timeToTriggerInterA3Rsrq=-1,timeToTriggerIntraA3=-1
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
ulMaxHARQTxQci                       5
ulMaxWaitingTime                     0
ulMinBitRate                         300
zzzTemporary3                        -2000000000
zzzTemporary4                        -2000000000
zzzTemporary5                        -2000000000
userLabel
end




crn ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci31
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
dscpArpMap                           dscpArp1=-1,dscpArp10=-1,dscpArp11=-1,dscpArp12=-1,dscpArp13=-1,dscpArp14=-1,dscpArp15=-1,dscpArp2=-1,dscpArp3=-1,dscpArp4=-1,dscpArp5=-1,dscpArp6=-1,dscpArp7=-1,dscpArp8=-1,dscpArp9=-1
endcProfileRef                       EndcProfile=1
harqPriority                         0
inactivityTimerOffset                0
laaSupported                         true
lessMaxDelayThreshold                0
logicalChannelGroupRef               QciTable=default,LogicalChannelGroup=3
measReportConfigParams               a1ThresholdRsrpPrimOffset=0,a1ThresholdRsrpSecOffset=0,a1ThresholdRsrqPrimOffset=0,a1ThresholdRsrqSecOffset=0,a2ThresholdRsrpPrimOffset=0,a2ThresholdRsrpSecOffset=0,a2ThresholdRsrqPrimOffset=0,a2ThresholdRsrqSecOffset=0,a3InterOffsetAdjustmentRsrp=0,a3InterOffsetAdjustmentRsrq=0,a3IntraOffsetAdjustmentRsrp=0,a3IntraOffsetAdjustmentRsrq=0,a5Threshold1RsrpOffset=0,a5Threshold1RsrqOffset=0,a5Threshold2RsrpOffset=0,a5Threshold2RsrqOffset=0,b2Threshold1RsrpCdma2000Offset=0,b2Threshold1RsrpGeranOffset=0,b2Threshold1RsrpUtraOffset=0,b2Threshold1RsrqCdma2000Offset=0,b2Threshold1RsrqGeranOffset=0,b2Threshold1RsrqUtraOffset=0,b2Threshold2Cdma2000Offset=0,b2Threshold2EcNoUtraOffset=0,b2Threshold2GeranOffset=0,b2Threshold2RscpUtraOffset=0,offsetPerQciPrio=0,timeToTriggerInterA3=-1,timeToTriggerInterA3Rsrq=-1,timeToTriggerIntraA3=-1
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
ulMaxHARQTxQci                       5
ulMaxWaitingTime                     0
ulMinBitRate                         0
userLabel
zzzTemporary3                        -2000000000
zzzTemporary4                        -2000000000
zzzTemporary5                        -2000000000
end






crn ENodeBFunction=1,SubscriberGroupProfile=ENDC
bearerTriggerList                    
caRateAdjustCoeff                    -1
cellTriggerList                      
customTriggerList                    0
customTriggerType                    2
dlAiLaDeltaSinrMax                   30
dlDynBlerTargetAlg                   0
dlDynBlerTargetMax                   -1
dlDynBlerTargetMin                   1
dlHarqBlerTarget                     10
drxMode                              0
endcUserProfileRef
fastACqiReportEnabled                false
featuresToDisableMeas                
groupExtendInactAfterVolteRel        0
higherPriorityEnabled                false
iuaMode                              0
iuaProfileRef
lastSchedLinkAdaptMode               0
pZeroNominalPucchOffset              0
pZeroNominalPuschOffset              0
pdcchFlexibleBlerMode                0
preschedProfileRef
preschedulingMode                    0
profilePriority                      5
qciOffsetForQCI6                     0
qciOffsetForQCI7                     0
qciOffsetForQCI8                     0
qciOffsetForQCI9                     0
sCellScheduleSinrThresOffset         0
selectionProbability                 100
spidTriggerList                      
subGroupConfiguration1               
subGroupConfiguration2               
subGroupConfiguration3               
subGroupConfiguration4               
subGroupConfiguration5               
subGroupConfiguration6               
subGroupConfiguration7               
ulCandidateToRegion                  false
ulHarqBlerTarget                     10
ulMcsLowerLimit                      -1
ulMcsUpperLimit                      -1
ulOuterloopStepSizeFactor            10
ulPlThresToRegion                    500
ulSinrThresToRegion                  400
userLabel
volteCodecRateForUlSinrEst           -1
end

confbd-
gs-
cvms Post_5G_GPL_$date


lt all     	                                                                                                                                                       
rbs                                                                                                                                                        
rbs                                                                                                                                                               
confbd+                                                                                                                                                           
                                                                                                                                                                  
$date = `date +%y%m%d_%H%M`                                                                                                                                       
cvms Pre_LMS_Settings_5G_$date                                                                                                                                         
                                  


confbd+
gs+
set NRCellDU=.*                   cellRange         10000 
set NRCellDU=.*                   ssbGscn           7790                                                                               
set NRCellDU=.*                   ssbFrequency      627936     

set EUtranCellFDD=.* endcAllowedPlmnList  mcc=404,mnc=70,mncLength=2
set EUtranCellTDD=.* endcAllowedPlmnList  mcc=404,mnc=70,mncLength=2


Set McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base rsrpCritical hysteresis=10,threshold=-118,timeToTrigger=160
Set EUtranCellFDD=.*,GUtranFreqRelation=627936 b1ThrRsrqFreqOffset 0
Set EUtranCellFDD=.*,GUtranFreqRelation=627936 b1ThrRsrpFreqOffset 0
Set EUtranCellFDD=.*,GUtranFreqRelation=627936 endcB1MeasPriority 7


confbd+
gs+
set EUtranCellFDD=.*,EUtranFreqRelation=3651 endcHoFreqPriority 6
set EUtranCellFDD=.*,EUtranFreqRelation=415 endcHoFreqPriority -1
set EUtranCellFDD=.*,EUtranFreqRelation=39150 endcHoFreqPriority -1
set EUtranCellFDD=.*,EUtranFreqRelation=39348 endcHoFreqPriority -1
set EUtranCellFDD=.*,EUtranFreqRelation=1301 endcHoFreqPriority 7

set EUtranCellFDD=.*,EUtranFreqRelation=3651 endcAwareIdleModePriority 5
set EUtranCellFDD=.*,EUtranFreqRelation=415 endcAwareIdleModePriority 6
set EUtranCellFDD=.*,EUtranFreqRelation=39150 endcAwareIdleModePriority 3
set EUtranCellFDD=.*,EUtranFreqRelation=39348 endcAwareIdleModePriority 3
set EUtranCellFDD=.*,EUtranFreqRelation=1301 endcAwareIdleModePriority 7

set EUtranCellFDD=.*,GUtranFreqRelation=627936 cellReselectionPriority 2
set EUtranCellFDD=.*,GUtranFreqRelation=627936 qRxLevMin         -124

#####TDD###
set EUtranCellTDD=.*,EUtranFreqRelation=3651 endcHoFreqPriority 6
set EUtranCellTDD=.*,EUtranFreqRelation=415 endcHoFreqPriority -1
set EUtranCellTDD=.*,EUtranFreqRelation=39150 endcHoFreqPriority -1
set EUtranCellTDD=.*,EUtranFreqRelation=39348 endcHoFreqPriority -1
set EUtranCellTDD=.*,EUtranFreqRelation=1301 endcHoFreqPriority 7

set EUtranCellTDD=.*,EUtranFreqRelation=3651 endcAwareIdleModePriority 5
set EUtranCellTDD=.*,EUtranFreqRelation=415 endcAwareIdleModePriority 6
set EUtranCellTDD=.*,EUtranFreqRelation=39150 endcAwareIdleModePriority 3
set EUtranCellTDD=.*,EUtranFreqRelation=39348 endcAwareIdleModePriority 3
set EUtranCellTDD=.*,EUtranFreqRelation=1301 endcAwareIdleModePriority 7

set EUtranCellTDD=.*,GUtranFreqRelation=627936 cellReselectionPriority 2
set EUtranCellTDD=.*,GUtranFreqRelation=627936 qRxLevMin         -124



crn GNBCUCPFunction=1,EUtraNetwork=1
end




crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=415
arfcnValueEUtranDl                   415
userLabel
end


crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=39150
arfcnValueEUtranDl                   39150
userLabel
end

crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=39348
arfcnValueEUtranDl                   39348
userLabel
end

crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=3651
arfcnValueEUtranDl                   3651
userLabel
end





Set GNBCUCPFunction=1,QciProfileEndcConfigExt=1  ulDataSplitThresholdMcg              -1
Set GNBCUCPFunction=1,QciProfileEndcConfigExt=1 ulDataSplitThreshold                 102400
Set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigB1GUtra= triggerQuantityB1    0
Set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1  triggerQuantityA5     0
Set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1 timeToTriggerB1   320
Set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1 timeToTriggerA5    100
Set McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base  rsrpSearchZone hysteresis=10,threshold=-112,timeToTrigger=160,timeToTriggerA1=-1
Set McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base  rsrpCandidateA5  hysteresis=10,threshold1=-118,threshold2=-112,timeToTrigger=640
Set McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base  rsrpCandidateA5  hysteresis=10,threshold1=-118,threshold2=-112,timeToTrigger=256
set McpcPSCellNrFreqRelProfileUeCfg=Base  rsrpCandidateA5Offset threshold1Offset=0,threshold2Offset=0
Set McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base  rsrpCandidateA5  hysteresis=10,threshold1=-118,threshold2=-112,timeToTrigger=640
set McpcPSCellNrFreqRelProfileUeCfg=Base  rsrpCandidateA5Offset threshold1Offset=0,threshold2Offset=0
Set McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base  rsrpCandidateA5  hysteresis=10,threshold1=-118,threshold2=-112,timeToTrigger=640
set McpcPSCellProfileUeCfg=Base  rsrpSearchZone threshold=-112
set IntraFreqMCCellProfileUeCfg=Base rsrpSCellCoverage threshold=-117
Set UePolicyOptimization=1        t320    180
Set UeCA=1,CaSCellHandling=Default,CaSCellHandlingUeCfg=Base sCellActDeactDataThresHyst 90
Set UeCA=1,CaSCellHandling=Default,CaSCellHandlingUeCfg=Base sCellActDeactDataThres -1
Set McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base rsrpCriticalEnabled true
Set IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base  rsrpBetterSpCell hysteresis=10,offset=30,timeToTrigger=640
Set IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base  rsrpBetterSpCell hysteresis=10,offset=30,timeToTrigger=640
Set IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base  rsrpBetterSpCell hysteresis=10,offset=30,timeToTrigger=640
Set EUtranCellFDD=.*,EUtranFreqRelation=.* qOffsetFreq       0
Set EUtranCellFDD=.*,EUtranFreqRelation=.* qOffsetFreq       0
SET ENodeBFunction=1,SubscriberGroupProfile=ENDC qciOffsetForQCI9                     0
SET ENodeBFunction=1,SubscriberGroupProfile=ENDC qciOffsetForQCI6                     0
Set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA1A2Endc=1 a2OuterSearchThrRsrqOffsetEndc       0
set ReportConfigA1A2Endc=1 qciA1A2ThrOffsetsEndc a1a2ThrRsrqQciOffsetEndc=0
Set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA1A2Endc=1 a2OuterSearchThrRsrpOffsetEndc       0
set ReportConfigA1A2Endc=1 qciA1A2ThrOffsetsEndc a1a2ThrRsrpQciOffsetEndc=0
set ReportConfigSearch=1 qciA1A2ThrOffsets a1a2ThrRsrpQciOffset=0,a1a2ThrRsrqQciOffset=0
Set EUtranCellFDD=.*                      primaryUpperLayerInd 1
Set GNBCUCPFunction=1,IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base rsrpBetterSpCell hysteresis=10,offset=30,timeToTrigger=640
Set NRCellCU=.*                   mcpcPSCellProfileRef Mcpc=1,McpcPSCellProfile=Default
Set NRCellCU=.*                   mcpcPSCellEnabled true
set EUtranCell.*DD=.*                      lbActionForEndcUe 0
Set EUtranCellFDD=.*,EUtranFreqRelation=.*,EUtranCellRelation=.*  isHoAllowed       true
Set QciProfileEndcConfigExt=1                               initialUplinkConf 1
Set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1 hysteresisA5      20
Set GNBCUCPFunction=1,IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base rsrpBetterSpCell hysteresis=10,offset=30,timeToTrigger=640
Set GNBCUCPFunction=1,IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base rsrpBetterSpCell hysteresis=10,offset=30,timeToTrigger=640
Set GNBCUCPFunction=1,IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base rsrpBetterSpCell hysteresis=10,offset=30,timeToTrigger=640
Set GNBCUCPFunction=1,IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base rsrpBetterSpCell hysteresis=10,offset=30,timeToTrigger=640
Set GNBCUUPFunction=1                                       endcUlNrRetProhibTimer 1000
Set NRCellDU=.*                   endcUlNrQualHyst  6
Set NRCellDU=.*                   endcUlNrLowQualThresh 10
Set NRCellDU=.*                   endcUlLegSwitchEnabled true
Set ENodeBFunction=1                                        endcSplitAllowedMoVoice false
Set EUtranCellFDD=.*                      endcSetupDlPktAgeThr 0
Set GNBCUUPFunction=1                                       endcDlNrRetProhibTimer 400 
Set UePolicyOptimization=1         endcAwareImc      2
Set ENodeBFunction=1                                        endcAllowed       true 
Set GNBCUUPFunction=1                                       dcDlAggExpiryTimer 100
Set GNBCUUPFunction=1                                       dcDlAggActTime    1
SET ENodeBFunction=1,SubscriberGroupProfile=ENDC customTriggerType                    2
SET ENodeBFunction=1,SubscriberGroupProfile=ENDC customTriggerList                    0
Set IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base betterSpCellTriggerQuantity 0

Set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigB1GUtra=1 b1ThresholdRsrq   -435
Set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigB1GUtra=1 b1ThresholdRsrp   -115 
Set EUtranCellFDD=.*                      additionalUpperLayerIndList  1 1 1 1 1
Set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1 a5Threshold2Rsrq  -195
Set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1 a5Threshold2Rsrp  -112
Set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1 a5Threshold1Rsrq  -195 
Set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1 a5Threshold1Rsrp  -44


Set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1  reportQuantityA5   0
Set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigB1GUtra=1  hysteresisB1     0
Set GNBCUCPFunction=1,IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base rsrpBetterSpCell hysteresis=20,offset=30,timeToTrigger=640
Set EUtranCellFDD=.*                      endcSetupDlPktVolThr 5






confbd-
gs-


cvms Post_LMS_Settings_5G_$date  
"""

AP_Termpoint_GUtranFreqRelation = """
lt all

get GNBCUUPFunction=1  gNBId$ > $gnbid                                                                                       

get Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR ^address$ > $reqip                                                                                             


crn ENodeBFunction=1,GUtraNetwork=1                                                                                                                               
userLabel                                                                                                                                                         
end                                                                                                                                                               


crn ENodeBFunction=1,GUtraNetwork=1,GUtranSyncSignalFrequency=627936-30                                                                                                                                                                
arfcn 627936                                                                                                                                                                                                                           
band 78                                                                                                                                                                                                                                
smtcDuration 1                                                                                                                                                                                                                         
smtcOffset 0                                                                                                                                                                                                                           
smtcPeriodicity 20                                                                                                                                                                                                                     
smtcScs 30                                                                                                                                                                                                                             
userLabel                                                                                                                                                                                                                              
end                                                                                                                                                                                                                                    


crn ENodeBFunction=1,GUtraNetwork=1,ExternalGNodeBFunction=40470-$gnbid                                                                                           
dirDataPathAvail true                                                                                                                                             
eNBVlanPortRef                                                                                                                                                    
gNodeBId $gnbid                                                                                                                                                   
gNodeBIdLength 26                                                                                                                                                 
gNodeBPlmnId mcc=404,mnc=70,mncLength=2                                                                                                                          
userLabel                                                                                                                                                         
end                                                                                                                                                               

crn ENodeBFunction=1,GUtraNetwork=1,ExternalGNodeBFunction=40470-$gnbid,TermPointToGNB=40470-$gnbid                                                               
additionalCnRef                                                                                                                                                   
administrativeState 0                                                                                                                                             
domainName                                                                                                                                                        
ipAddress 0.0.0.0                                                                                                                                                 
ipAddress2                                                                                                                                                        
ipsecEpAddress ::                                                                                                                                                 
ipv6Address   $reqip                                                                                                                                            
ipv6Address2                                                                                                                                                      
upIpAddress ::                                                                                                                                                    
end                                                                                                                                                               

deb TermPointToGNB                                                                                                                                                


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
pr GUtraNetwork=1,ExternalGNodeBFunction=40470-$gnbid,ExternalGUtranCell=40470-000000$gnbid-31$j                                                                  
if $nr_of_mos = 1                                                                                                                                                 
crn ENodeBFunction=1,$mordn,GUtranFreqRelation=627936,GUtranCellRelation=40470-000000$gnbid-31$j                                                                  
essEnabled false                                                                                                                                                  
isRemoveAllowed false                                                                                                                                             
neighborCellRef GUtraNetwork=1,ExternalGNodeBFunction=40470-$gnbid,ExternalGUtranCell=40470-000000$gnbid-31$j                                                     
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
set ^EUtranCell.DD= endcAllowedPlmnList mcc=404,mnc=70,mnclength=2                                                                                                
"""




AP_5G_Cell_creation_Sctp_Endpoint_Creation = """
confb+
gs+

$script_nodename = {gNodeBName}
if $nodename != $script_nodename
   l echo "This node is called $nodename but the command file should be loaded in {gNodeBName}"
   return
fi

if $moshell_version ~ ^([7-9]|10)
   l echo "The moshell version is too old. 11.0a or higher is required for scripts containing the crn command."
   return
fi

###################################### TN SCRIPT ######################################

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




get Router=LTEUP,InterfaceIPv4=TN_.*_UP                      encapsulation > $encapsulation

crn Transport=1,Router=LTEUP,InterfaceIPv6=NR                                                                                                                                                                      
aclEgress                                                                                                                                                                                                          
aclIngress                                                                                                                                                                                                         
bfdProfile                                                                                                                                                                                                         
bfdStaticRoutes 0                                                                                                                                                                                                  
dscpNdp 48                                                                                                                                                                                                         
egressQosMarking QosProfiles=1,DscpPcpMap=1                                                                                                                                                                        
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
  

crn Transport=1,Router=LTEUP,RouteTableIPv6Static=1                                                                                                                                                                
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn Transport=1,Router=LTEUP,RouteTableIPv6Static=1,Dst=default                                                                                                                                                    
dst ::/0                                                                                                                                                                                                           
end

        
crn Transport=1,Router=LTEUP,RouteTableIPv6Static=1,Dst=default,NextHop=1                                                                                                                                          
address {NR_GW}                                                                                                                                                                        
adminDistance 1                                                                                                                                                                                                    
bfdMonitoring true                                                                                                                                                                                                 
discard false
reference                                                                                                                                                                                                          
end




crn Transport=1,Router=Node_Internal_F1                                                                                                                                                                            
hopLimit 64                                                                                                                                                                                                        
pathMtuExpiresIPv6 86400                                                                                                                                                                                           
routingPolicyLocal                                                                                                                                                                                                 
routingPolicyLocalIPv6                                                                                                                                                                                             
ttl 64                                                                                                                                                                                                             
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn Transport=1,Router=Node_Internal_F1,InterfaceIPv4=NR_CUCP                                                                                                                                                      
aclEgress                                                                                                                                                                                                          
aclIngress                                                                                                                                                                                                         
arpTimeout 300                                                                                                                                                                                                     
bfdProfile                                                                                                                                                                                                         
bfdStaticRoutes 0                                                                                                                                                                                                  
egressQosMarking                                                                                                                                                                                                   
encapsulation                                                                                                                                                                                                      
ingressQosMarking                                                                                                                                                                                                  
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
                                                                                                                                                                                                                   
crn Transport=1,Router=Node_Internal_F1,InterfaceIPv4=NR_DU                                                                                                                                                        
aclEgress                                                                                                                                                                                                          
aclIngress                                                                                                                                                                                                         
arpTimeout 300                                                                                                                                                                                                     
bfdProfile                                                                                                                                                                                                         
bfdStaticRoutes 0                                                                                                                                                                                                  
egressQosMarking                                                                                                                                                                                                   
encapsulation                                                                                                                                                                                                      
ingressQosMarking                                                                                                                                                                                                  
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




crn Transport=1,Router=LTEUP,TwampResponder=1
ipAddress Transport=1,Router=LTEUP,InterfaceIPv4=TN_E_UP,AddressIPv4=TN_E_UP
udpPort 4001
userLabel
end

crn Transport=1,Router=LTEUP,TwampResponder=NR
ipAddress Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
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
localIpAddress Transport=1,Router=LTECP,InterfaceIPv4=TN_E_CP,AddressIPv4=TN_E_CP
portNumber 36422
sctpProfile Transport=1,SctpProfile=1
end



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

crn Transport=1,SctpEndpoint=F1_NRCUCP
localIpAddress Transport=1,Router=Node_Internal_F1,InterfaceIPv4=NR_CUCP,AddressIPv4=1
portNumber 38472
sctpProfile Transport=1,SctpProfile=Node_Internal_F1
end

crn Transport=1,SctpEndpoint=F1_NRDU
localIpAddress Transport=1,Router=Node_Internal_F1,InterfaceIPv4=NR_DU,AddressIPv4=1
portNumber 38472
sctpProfile Transport=1,SctpProfile=Node_Internal_F1
end

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


crn Transport=1,SctpEndpoint=X2_ENDC
localIpAddress Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2
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


######################################################### 5G SCRIPT #########################################################


$Correct_swVersion = 24.Q2
get 0 swVersion > $swVersion

if $swVersion != $Correct_swVersion 
   l echo "Old software version ($swVersion) found. Please update the software before 5G integration."
   return
fi


###################################### GNBCUUPFunction=1 SCRIPT ######################################

crn GNBCUUPFunction=1
altDepHServAdapUPProfEnabled false
dataFwdRateTo5Gs 5000
dataFwdRateToEps 200
dcDlAggActTime 1
dcDlAggExpiryTimer 100
dcDlPdcpInitialMcgRate 20
dcDlPdcpInitialScgRate 100
dlPdcpSpsTargetTimeLTE 25
dlPdcpSpsTargetTimeNR 25
endcDataUsageReportEnabled true
endcDlNrRetProhibTimer 400
endcUlNrRetProhibTimer 1000
estimatedUeL2Buffer
gNBId {gNBId}
gNBIdLength 26
pLMNIdList mcc=404,mnc=70
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



###################################### GNBDUFunction=1 SCRIPT ######################################

crn GNBDUFunction=1
altDepHMultCGPeriodEnabled false
altDepHServAdapUPProfEnabled false
autoLockDelay 0
caVlanPortRef
capacityAllocationPolicy 0
configuredGrantConfMode 0
dlBbCapacityTarget
dynTACConfigEnabled false
esiSuetEnabled false
gNBDUId 1
gNBDUName
gNBId {gNBId}
gNBIdLength 26
mixedSrsModeEnabled false
multiTddPatternSmEnabled false
pimCancAutoConfigEnabled false
pwsEtwsPrimaryInd 8
servAdapUPProfDepHEnabled true
userLabel
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

{AP_5g_CgSwitch_text}

###################################### GNBCUCPFunction=1 SCRIPT ######################################

crn GNBCUCPFunction=1
advUePosPeriodicityMode 0
caDepHEnabled true
cellRelationMOThresh 1500
dnsLookup5GsTaiPeriodicTimer 0
dnsLookupOn5GsTai false
extEnbRemoveTime 1440
extendedBandN77Supported false
extendedBandN77TwoSupported false
gNBCUName
gNBId {gNBId}
gNBIdLength 26
maxCommonProcTime 30
maxNgRetryTime 30
nasInactivityTime 5
networkIdInUeCapEnq false
ngcDedProcTime 5
nrNeedForGapsSupported true
pLMNId mcc=404,mnc=70
pimAutoDetectionEnabled false
prefInterGnbHo 0
ranNodeName
resourceStatusReportDefault -2
resourceStatusReportF1Enabled true
rfspSpidPairList
ribTmAutoMax 0
rrcReestSupportType 0
tDcOverall 7
tXnDcOverall 5
tXnDcPrep 5
userLabel
xnIpAddrViaNgActive true
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

crn GNBCUCPFunction=1,NRNetwork=1,NRFrequency=627936-30
arfcnValueNRDl 627936
bandListManual
smtcDuration 1
smtcOffset 0
smtcPeriodicity 20
smtcScs 30
ssRssiMeasIdle
ssbToMeasureIdle
end

crn GNBCUCPFunction=1,NRNetwork=1,NRFrequency=627936-30,NRFrequencyUeCfg=Base
prefUeGroupList
ssRssiMeasConnected
ssbToMeasureConnected
ueConfGroupList
ueGroupList
userLabel
end


ld GNBCUCPFunction=1,TermPointToGNBDU=1 #SystemCreated                                                                                                                                                             
 
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

{AP_GNBCUCPFunction_text}

{AP_GNBDUFunction_text}
"""

AP_GNBDUFunction_text = """
###################################### Cell Specific Started - NRCellDU={gUtranCell} ###################################### 

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
pLMNIdList mcc=404,mnc=70
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
rachRootSequence {rachRootSequence}
secondaryCellOnly false
siWindowLength 20
ssbDuration 1
ssbFrequency 627936
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
"""


AP_GNBCUCPFunction_text = """
###################################### Cell Specific Started - NRCellCU={gUtranCell} ###################################### 

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
nRFrequencyRef NRNetwork=1,NRFrequency=627936-30
noOfPeriodicUeMeasPerRop 900
nrdcMnCellProfileRef NrdcControl=1,NrdcMnCellProfile=Default
offloadCellProfileRef TrafficOffload=1,OffloadCellProfile=Default
periodicCellProfileRef
pmUeIntraFreqCellProfileRef
pmUeIntraFreqEnabled false
primaryPLMNId mcc=404,mnc=70
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

crn GNBCUCPFunction=1,NRCellCU={gUtranCell},NRFreqRelation=627936
anrMeasOn true
caFreqRelMeasProfileRef CarrierAggregation=1,CaFreqRelMeasProfile=Default
cellReselectionPriority 7
cellReselectionSubPriority
mcpcPCellNrFreqRelProfileRef Mcpc=1,McpcPCellNrFreqRelProfile=Default
mcpcPSCellNrFreqRelProfileRef Mcpc=1,McpcPSCellNrFreqRelProfile=Default
mdtMeasOn true
nRFrequencyRef NRNetwork=1,NRFrequency=627936-30
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


crn GNBCUCPFunction=1,EUtraNetwork=1
userLabel
end
crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=1576
arfcnValueEUtranDl 1576
userLabel
end
crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=365
arfcnValueEUtranDl 365
userLabel
end
crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=39150
arfcnValueEUtranDl 39150
userLabel
end
crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=39151
arfcnValueEUtranDl 39151
userLabel
end
crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=39348
arfcnValueEUtranDl 39348
userLabel
end
crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=39349
arfcnValueEUtranDl 39349
userLabel
end
crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=515
arfcnValueEUtranDl 515
userLabel
end

###################################### Cell Specific Ended - NRCellCU={gUtranCell} ###################################### 


"""

AP_5g_CgSwitch_text = """
###################################### Cell Specific Started - 5G CgSwitch={gUtranCell} ###################################### 

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

######################################Cell Specific Ended - 5G CgSwitch={gUtranCell} ###################################### 

"""






###################################### CISCO MME SCRIPT ####################################################################################################
CISCO_MME_AP = """



gs+

crn ENodeBFunction=1,TermPointToMme=APUPLRHCK01ERPCCMM06
additionalCnRef
administrativeState 1
dcnType 0
domainName
ipAddress1 10.103.10.1
ipAddress2 10.103.10.3
ipv6Address1 ::
ipv6Address2 ::
mmeSupportLegacyLte true
mmeSupportNbIoT false
end


crn ENodeBFunction=1,TermPointToMme=APVIJEMME04
additionalCnRef
administrativeState 1
dcnType 0
domainName
ipAddress1 10.103.45.34
ipAddress2 10.103.45.35
ipv6Address1 ::
ipv6Address2 ::
mmeSupportLegacyLte true
mmeSupportNbIoT false
end


crn ENodeBFunction=1,TermPointToMme=APVIJEMME05
additionalCnRef
administrativeState 1
dcnType 0
domainName
ipAddress1 10.103.45.45
ipAddress2 10.103.45.46
ipv6Address1 ::
ipv6Address2 ::
mmeSupportLegacyLte true
mmeSupportNbIoT false
end

crn ENodeBFunction=1,TermPointToMme=APVIJRHCK01ERPCCMM07
additionalCnRef
administrativeState 1
dcnType 0
domainName
ipAddress1 10.103.152.179
ipAddress2 10.103.152.181
ipv6Address1 ::
ipv6Address2 ::
mmeSupportLegacyLte true
mmeSupportNbIoT false
end

crn ENodeBFunction=1,TermPointToMme=MME3_Uppal
additionalCnRef 
administrativeState 1
dcnType 0
domainName 
ipAddress1 10.1.162.80
ipAddress2 10.1.162.81
ipv6Address1 ::
ipv6Address2 ::
mmeSupportLegacyLte true
mmeSupportNbIoT false
end

cr ENodeBFunction=1,TermPointToMme=MME_Vijayawada
set ENodeBFunction=1,TermPointToMme=MME_Vijayawada ipAddress1 10.1.98.89
set ENodeBFunction=1,TermPointToMme=MME_Vijayawada ipAddress2 10.1.98.93
set ENodeBFunction=1,TermPointToMme=MME_Vijayawada administrativeState 0

cr ENodeBFunction=1,TermPointToMme=MME_Uppal
set ENodeBFunction=1,TermPointToMme=MME_Uppal ipAddress1 10.1.28.247
set ENodeBFunction=1,TermPointToMme=MME_Uppal ipAddress2 10.1.253.168
set ENodeBFunction=1,TermPointToMme=MME_Uppal administrativeState 0
confbd-


"""

######################################################## NOKIA MME SCRIPT ####################################################################################################

NOKIA_MME_AP = """
###################################### NOKIA MME SCRIPT ######################################

gs+

crn ENodeBFunction=1,TermPointToMme=NokiaCMM-Uda
additionalCnRef
administrativeState 1
dcnType 0
domainName
ipAddress1 10.103.37.69
ipAddress2 10.103.37.70
ipv6Address1 ::
ipv6Address2 ::
mmeSupportLegacyLte true
mmeSupportNbIoT false
end

crn ENodeBFunction=1,TermPointToMme=NokiaCMM-Jod
additionalCnRef
administrativeState 1
dcnType 0
domainName
ipAddress1 10.103.37.21
ipAddress2 10.103.37.22
ipv6Address1 ::
ipv6Address2 ::
mmeSupportLegacyLte true
mmeSupportNbIoT false
end
gs-
"""