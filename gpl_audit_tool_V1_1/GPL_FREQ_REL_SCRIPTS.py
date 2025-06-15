gpl_para_correction_script = """
$date = `date +%y%m%d_%H`
cvms Pre_Parameters_correction_$date
gs+
gs+ safe
{gpl_parameter_commands}
###################################################################################
$date = `date +%y%m%d_%H`
cvms Post_LTE_GPL_Correction_$date
gs-

"""

GeranFrequency_defination = """
####GeranFrequency Definition#####

gs+                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
crn ENodeBFunction=1,GeraNetwork=1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
userLabel                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
end

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency={arfcnValueGeranDl}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
arfcnValueGeranDl {arfcnValueGeranDl}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
bandIndicator 0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
userLabel                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
end   
"""

EUtranFrequency_Definition = """
crn ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency={arfcnValueEUtranDl}
arfcnValueEUtranDl {arfcnValueEUtranDl}
end
"""


Eutran_Frequency_Relation_Script = """
$date = `date +%y%m%d_%H%M`

cvms Pre_Relation_$date
gs+

######################### GERAN Frequency Relation Script (creating the missing relation) ###########################
{GERAN_Frequency_Relation}

{Eutran_freq_relation_creation}

$date = `date +%y%m%d_%H%M`

cvms Post_Relation_$date
gs-
"""