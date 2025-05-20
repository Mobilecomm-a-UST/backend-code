import pandas as pd
import xml.etree.ElementTree as ET
import os 
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from mcom_website.settings import MEDIA_ROOT
# from mcom_website.settings import MEDIA_ROOT
import Mcom_scriptor.utils.dynamic_Rmod as dynamic_Rmod
import Mcom_scriptor.utils.NRDCDPR
import Mcom_scriptor.utils.creating_smod_bbmod 
import Mcom_scriptor.utils.creating_cablink
import Mcom_scriptor.utils.dynamic_ip
def replicator(cell_list, xml_string):
    cell_fill=lambda cell_:xml_string.format(cell_)
    op_xml_str=""" """
    for cell_ in cell_list:
        op_xml_str=op_xml_str +"\n" + cell_fill(cell_)


    return op_xml_str
def replacer(cell_list,xml_string):
     op_xml_str=""" """
     for cell_ in cell_list:
        op_xml_str= op_xml_str + xml_string.replace("LNCEL-1",f"LNCEL-{cell_}")
     return op_xml_str
def adding_activatedMimo_for_4t4r(all_lncel_class_element,cell_mimo):
        root=ET.fromstring(all_lncel_class_element)
        for cells, mimo in cell_mimo.items():
            if mimo=="4T4R":
                for cell in cells:
                    # print(cell)
                    target_element= root.find(f".//managedObject[@class='NOKLTE:LNCEL_TDD'][@distName='MRBTS-844360/LNBTS-844360/LNCEL-{cell}/LNCEL_TDD-0']")
                    
                    # Create a new element with attributes
                    new_element = ET.Element('p')
                    new_element.text = 'TM4'
                    
                    # Add attributes to the new element
                    new_element.set('name', 'activatedMimoTM')
                    
                    print(new_element)
                    # Add the new element inside the target element
                    target_element.append(new_element)
        return root

def insert_element_between(xml_string, new_element, before_attr, before_value, after_attr, after_value):
    root = ET.fromstring(xml_string)
    
    # Find the elements before and after the insertion point
    before_element = None
    after_element = None
    for element in root.iter():
        if before_element is None and element.get(before_attr) == before_value:
            before_element = element
            print(element.tag)
        elif before_element is not None and element.get(after_attr) == after_value:
            after_element = element
            break

    if before_element is not None and after_element is not None:
        # Insert the new element between the found elements
        parent = root
        for elem in root.iter():
            if elem.find(before_element.tag) is not None and elem.find(after_element.tag) is not None:
                parent = elem
                break

        index = list(parent).index(after_element)
        parent.insert(index, new_element)

        # Convert the modified XML to a string
        modified_xml = ET.tostring(root, encoding="utf-8").decode("utf-8")
        # modified_xml=modified_xml.replace("<root>","").replace("</root>","")
        print("Element inserted successfully.")
        return modified_xml
    else:
        print("Failed to find insertion points.")
        return None
def xml_file_to_str(path):
    with open(path, 'r') as file:
        # xml_string = file.read()
        tree = ET.parse(path)
        root = tree.getroot()

        # Convert the root element to a string
        xml_string = ET.tostring(root, encoding="utf-8").decode("utf-8")
        return xml_string

#___________ for IRFIM __________________
def process(cells,irfim_lnhoif_list,cell_mimo,POST_request,input2_dict):
        # irfim_xml_path=r"C:\Users\Lenovo\Desktop\Django..., Projects\Mobile_com_web_app\mcom_website\Mcom_scriptor\xml_templates\irfim_element.xml"
        irfim_xml_path=  os.path.join(MEDIA_ROOT,"Mcom_scriptor","xml_templates","irfim_element.xml")

        irfim_str=xml_file_to_str(irfim_xml_path)
        grouped_irfim=replicator(irfim_lnhoif_list,irfim_str)
        # print("starting.........................")
        # print(grouped_irfim)
        # print("ending...........................")
        grouped_irfim= """<root> """ + grouped_irfim + """ </root>"""
        # ___________**********__________________

        #___________ for LNHOIF __________________
        lnhoif_xml_path=os.path.join(MEDIA_ROOT,"Mcom_scriptor","xml_templates","lnhoif_element.xml")
        lnhoif_str=xml_file_to_str(lnhoif_xml_path)
        grouped_lnhoif=replicator(irfim_lnhoif_list,lnhoif_str)

        # print("starting.........................")
        # print(grouped_lnhoif)
        # print("ending...........................")
        grouped_lnhoif= """<root> """ + grouped_lnhoif + """ </root>"""
        # ___________**********__________________


        complete_lncel_1_path=os.path.join(MEDIA_ROOT,"Mcom_scriptor","xml_templates","complete_lncel_1_element.xml")

        complete_lncel_1_str=xml_file_to_str(complete_lncel_1_path)

        # ________________ for irfim __________________
        grouped_irfim_element=ET.fromstring(grouped_irfim)

        result_xml = insert_element_between(complete_lncel_1_str, grouped_irfim_element, "distName", "MRBTS-844360/LNBTS-844360/LNCEL-1/GFIM-1/GNFL-1", "distName", "MRBTS-844360/LNBTS-844360/LNCEL-1/LNCEL_TDD-0")

        # ________________ for lnhoif __________________
        grouped_lnhoif_element=ET.fromstring(grouped_lnhoif)
        result_xml = insert_element_between(result_xml, grouped_lnhoif_element, "distName", "MRBTS-844360/LNBTS-844360/LNCEL-1/LNHOG-1", "distName", "MRBTS-844360/LNBTS-844360/LNCEL-1/REDRT-0")

        result_xml = replacer(cells,result_xml)

        result_xml="<root>" + result_xml.replace("<root>","").replace("</root>","") + "</root>" 

        result_xml=adding_activatedMimo_for_4t4r(result_xml,cell_mimo)

        main_xml_path=r"C:\Users\Lenovo\Desktop\Django..., Projects\Mobile_com_web_app\mcom_website\media\Mcom_scriptor\xml_templates\main_xml.xml"
        main_xml_path= os.path.join(BASE_DIR,"media","Mcom_scriptor","xml_templates","main_xml.xml")
        main_xml=xml_file_to_str(main_xml_path)
        # print(main_xml)
        # result_xml=ET.fromstring(result_xml)

        
        # main_xml_template = insert_element_between(main_xml, result_xml, "distName", f"MRBTS-844360/LNBTS-844360/LNCEL-{cells[-1]}/SIB-0", "distName", "MRBTS-844360/LNBTS-844360/LNMME-0")
        main_xml_template = insert_element_between(main_xml, result_xml, "distName", "MRBTS-844360/LNBTS-844360/LNBTS_TDD-0", "distName", "MRBTS-844360/LNBTS-844360/MODPR-0")
       
        # for inserting the dynamically created RMOD cell maping Elements
        Rmod_cellmapping_element=dynamic_Rmod.dynamic_Rmod_cellmapping(cell_mimo)[0]
        main_xml_template =insert_element_between(main_xml_template, Rmod_cellmapping_element, "distName", "MRBTS-844360/MNL-1/MNLENT-1/CELLMAPPING-1", "distName", "MRBTS-844360/MNL-1/MNLENT-1/CERTHENT-1")
       
    #    for inserting the Dynamically created Rmod Element
        Rmod_element=dynamic_Rmod.dynamic_Rmod_cellmapping(cell_mimo)[1]
        main_xml_template =insert_element_between(main_xml_template, Rmod_element, "distName", "MRBTS-844360/EQM-1/APEQM-1/CABINET-1/SMOD-1/EAC_IN-4", "distName", "MRBTS-844360/EQM-1/HWTOP-1")
       

       # for inserting dynamically created NRDCDPR
        NRDCDPR_element=Mcom_scriptor.utils.NRDCDPR.dynamic_NRDCDPR(cells)
        main_xml_template =insert_element_between(main_xml_template,NRDCDPR_element, "distName", "MRBTS-844360/LNBTS-844360/MOPR-4/MORED-4", "distName", "MRBTS-844360/LNBTS-844360/NRDCDPR-0/ENDCDMEASCONF-0")
        # print(main_xml_template)

        smod_bbmod_element = Mcom_scriptor.utils.creating_smod_bbmod.process(POST_request)
        main_xml_template =insert_element_between(main_xml_template,smod_bbmod_element, "distName", "MRBTS-844360/EQM-1/APEQM-1/CABINET-1", "distName", "MRBTS-844360/EQM-1/APEQM-1/CABINET-1/SMOD-1/EAC_IN-1")
        
        cablink_mos_element = Mcom_scriptor.utils.creating_cablink.process(cell_mimo)
        main_xml_template =insert_element_between(main_xml_template,cablink_mos_element, "distName", "MRBTS-844360/EQM-1/HWTOP-1", "distName", "MRBTS-844360/LNBTS-844360")
        
        gtpu_mo_element=Mcom_scriptor.utils.dynamic_ip.dynamic_sgw_ip(input2_dict['S-GW'])
        main_xml_template =insert_element_between(main_xml_template,gtpu_mo_element, "distName", "MRBTS-844360/LNBTS-844360/CTRLTS-1/MTRACE-1", "distName", "MRBTS-844360/LNBTS-844360/LBPUCCHRDPR-0")
       
        lnmme_mo_element=Mcom_scriptor.utils.dynamic_ip.dynamic_mme_ip(input2_dict['MME IP'])
        main_xml_template =insert_element_between(main_xml_template,lnmme_mo_element, "distName", "MRBTS-844360/LNBTS-844360/LNBTS_TDD-0", "distName", "MRBTS-844360/LNBTS-844360/MODPR-0")
       
       
        main_xml_template=main_xml_template.replace("<root>","").replace("</root>","")
        root=ET.fromstring(main_xml_template)
        namespace = "raml21.xsd"
        version = "2.1"

        # Add the namespace to the root element
        root.set("xmlns", namespace)
        root.set("version", version)


        # print(main_xml_template)
        # file_path=r"C:\Users\Lenovo\Desktop\Django..., Projects\Mobile_com_web_app\mcom_website\media\Mcom_scriptor\singe_module_testing\main_temp.xml"
        # ET.ElementTree(root).write(file_path, encoding="utf-8", xml_declaration=True)

        return root

if __name__=="__main__":
    input_df2=pd.read_excel(r"E:\Mcom_Projects_files\Mcom_Scriptor_project\ULS_Input Sheet_modified_6_cells.xlsx", sheet_name="Sheet2",dtype=str)
    # input_df2=input_df2.dropna().astype(str)
    input2_dict=input_df2.to_dict(orient='list')
    # print(input2_dict)
    for key,value in input2_dict.items():
        print(key,":",value)
        # print(value)

    input_df1=pd.read_excel(r"E:\Mcom_Projects_files\Mcom_Scriptor_project\ULS_Input Sheet_modified_6_cells.xlsx", sheet_name="CellWise",dtype=str)
    input_df1.dropna(subset=['Cell ID'], inplace=True)
    print(input_df1)
    input1_dict=input_df1.to_dict(orient='record')
    # print(input1_dict)
    for x in input1_dict:
        print(x)

    POST_request ={'circle': ['undefined'], 'OEM': ['undefined'], 'BTS': ['undefined'], 'Technology': ['undefined'], 'hardware': ['FSMF'], 'card': ['472182A,472797A'], 'count': ['1,1,1']}
    cells=[11,12,13,21,22,23]
    irfim_lnhoif_list=[1,2,3,4,5,6]
    cell_mimo={(11,21):"4T4R",(12,22):"2T2R",(13,23):"2T2R"}
    op=process(cells,irfim_lnhoif_list,cell_mimo,POST_request,input2_dict)
    # print(op)