import datetime
import pandas as pd
from gpl_audit_tool_V1_1.GPL_FREQ_REL_SCRIPTS import gpl_para_correction_script, Eutran_Frequency_Relation_Script, GeranFrequency_defination

def process_correction_script_generation(commands: list, output_file_path):
    gpl_parameter_commands = "\n".join(commands)

    with open(output_file_path, "a", encoding='utf-8') as file:
        file.write(gpl_para_correction_script.format(gpl_parameter_commands = gpl_parameter_commands))





def create_freqency_relation_script(arfcn_value_eutran_dl: str, eutran_command_lines: list,output_file_path):
    Eutran_freq_relation_creation = "\n".join(eutran_command_lines)
    with open(output_file_path, "a", encoding='utf-8') as file:
        file.write(Eutran_Frequency_Relation_Script.format(GERAN_Frequency_Relation=arfcn_value_eutran_dl, Eutran_freq_relation_creation=Eutran_freq_relation_creation) + '\n')

