import xml.etree.ElementTree as ET
import re
def process(POST_request):
        smod_str=""" 
            <managedObject class="com.nokia.srbts.eqm:SMOD" distName="MRBTS-844360/EQM-1/APEQM-1/CABINET-1/SMOD-1" version="EQM23R1_2221_110" operation="create">
            <p name="climateControlOcxoTemperatureLearning">true</p>
            <p name="climateControlProfiling">Optimized Cooling</p>
            <p name="moduleLocation">Housai Bunglow</p>
            <p name="portMode">RF</p>
            <p name="prodCodePlanned">472181A</p>
            <p name="radioProtSearchOrder">OBSAI</p>
            </managedObject>"""

        bbmod_str="""     
            <managedObject class="com.nokia.srbts.eqm:BBMOD" distName="MRBTS-844360/EQM-1/APEQM-1/CABINET-1/BBMOD-{bbmod}" version="EQM23R1_2221_110" operation="create">
            <p name="administrativeState">Unlocked</p>
            <p name="fddNrCellConfigTradeoff">not used</p>
            <p name="prodCodePlanned">{card}</p>
            <p name="useFullCapacity">true</p>
            </managedObject> """
            
        op_str=""" """
        print(POST_request)
        Hardware=POST_request.get('hardware')
        print(Hardware) 
        bbmod_count=1
        if Hardware == "FSMF":
            if POST_request.get("card") == '':
                 len_card_list= 0
            else:
                cards=list(POST_request.get("card").split(','))
                print(cards)
                len_card_list = len(cards)
                card_count=list(POST_request.get("count").split(','))
                print(card_count)


            # exit(0)
            op_str=op_str + smod_str
            if len_card_list > 0  :
                for i,card in enumerate(cards):
                    for j in range(1,(int(card_count[i])+1)):
                        op_str=op_str + bbmod_str.format(bbmod=bbmod_count,card=card)
                        bbmod_count=bbmod_count+1
        else:
            pass


        smod_bbmod_str= "<root>" + op_str + "</root>"
        print(smod_bbmod_str)
        smod_bbmod =ET.fromstring(smod_bbmod_str)
        return smod_bbmod

if __name__  == "__main__":
     POST_request={'hardware':"FSMF",'card':'abc(233a),abbc(2324a)','count':'1,1'}
     process(POST_request)