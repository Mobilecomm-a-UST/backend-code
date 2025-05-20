import pandas as pd
from rest_framework.response import Response

def required_col_check(file,required_col_list,):
    col_in_file= pd.read_excel(file,nrows=1).columns.tolist()
    
    print("Header Name-------------------",col_in_file)
    missing_col=[]
    sts=False
    for col in required_col_list:
          if col in col_in_file:
                pass
          else:
            sts=True
            missing_col.append(col)
    
    message= 'Did not get Some columns in uploaded ' +str(file.name)
    response={"status":False,"missing_sites":missing_col,"message":message}
    return sts,response


################################ To do comparision between required_sites by circle  and sites in the raw KPI ################### 
def site_comparision(sit_id_lis,site_list):
    not_found_sites=list(set(site_list)-set(sit_id_lis))
    return not_found_sites




####################################################################################################################################
####################################################################################################################################


import subprocess
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.exporters import PythonExporter
import pandas as pd
from django.http import HttpResponse
from rest_framework.response import Response



def run_ipynb(**parm):
    
        # Specify the path to the .ipynb file
        notebook_path = parm["script_path"]

        # Read the .ipynb file
        with open(notebook_path, 'r') as nb_file:
            notebook_content = nb_file.read()

        # Convert the .ipynb content to a Python script
        notebook = nbformat.reads(notebook_content, as_version=4)
        python_exporter = PythonExporter()
        python_script, _ = python_exporter.from_notebook_node(notebook)


        serialized_df_list=[]
        for key, value in parm.items():
            if isinstance(value, pd.DataFrame):
                
                
                serialized_df=value.to_json(orient='records')
                serialized_df_list.append(serialized_df)

        data=['python', '-c', python_script,serialized_df[0]]
        # data.extend(serialized_df_list)
        # print(data)
        print("calling subprocess.......")
        result = subprocess.check_output(data, stderr=subprocess.STDOUT, universal_newlines=True)
        
        # Assuming the script returns a DataFrame as a string (e.g., serialized as JSON)
        # You can deserialize the DataFrame back to a pandas DataFrame
        # print("result",result)
        df = pd.read_json(result)  # Adjust the deserialization method as needed
        # print(df)
        # Now you can work with the DataFrame (e.g., df.head(), df.to_csv(), etc.)
        # For this example, let's return the first few rows of the DataFrame as JSON
        print("exiting run_ipynb..")
        return df


def site_list_handler(request):
        site_list_file = request.FILES["site_list"] if 'site_list' in request.FILES else None
        str_site_list=request.POST.get("str_site_list") if "str_site_list" in request.POST else None
        
        if site_list_file:
            sts,response=required_col_check(site_list_file,["2G ID"])
            if sts:
               return Response(response)
            df_site_list = pd.read_excel(site_list_file)
            site_list=list(df_site_list["2G ID"])
            response=None
        
        elif str_site_list:
           
            site_list=str_site_list.split(",")
            site_list=[site.strip() for site in site_list]
            response=None
            ##print("site_list.........................",site_list)
        else:
            print("true")
            site_list=None
            response={"status":False,"message":"please provide site list"}
            # return Response({"status":False,"message":"please provide site list"})
        return response,site_list

def site_list_handler_2G(request):
        site_list_file = request.FILES["site_list_2G"] if 'site_list_2G' in request.FILES else None
        str_site_list=request.POST.get("str_site_list") if "str_site_list" in request.POST else None
        
        if site_list_file:
            sts,response=required_col_check(site_list_file,["2G ID"])
            if sts:
               return Response(response)
            df_site_list = pd.read_excel(site_list_file)
            site_list=list(df_site_list["2G ID"])
            response=None
        
        elif str_site_list:
           
            site_list=str_site_list.split(",")
            site_list=[site.strip() for site in site_list]
            response=None
            ##print("site_list.........................",site_list)
        else:
            print("true")
            site_list=None
            response={"status":False,"message":"please provide site list"}
            # return Response({"status":False,"message":"please provide site list"})
        return response,site_list

def site_list_handler_4G(request):
        site_list_file = request.FILES["site_list_4G"] if 'site_list_4G' in request.FILES else None
        str_site_list=request.POST.get("str_site_list") if "str_site_list" in request.POST else None
        
        if site_list_file:
            sts,response=required_col_check(site_list_file,["2G ID"])
            if sts:
               return Response(response)
            df_site_list = pd.read_excel(site_list_file)
            site_list=list(df_site_list["2G ID"])
            response=None
        
        elif str_site_list:
           
            site_list=str_site_list.split(",")
            site_list=[site.strip() for site in site_list]
            response=None
            ##print("site_list.........................",site_list)
        else:
            print("true")
            site_list=None
            response={"status":False,"message":"please provide site list"}
            # return Response({"status":False,"message":"please provide site list"})
        return response,site_list



def short_name_handler(request):
    str_short_name = (
        request.POST.get("str_short_list") if "str_short_list" in request.POST else None
    )
    

    if str_short_name:
        short_name_list = str_short_name.split(",")
        short_name_list = [site.strip() for site in short_name_list]

        response = None

    else:
        short_name_list = None
        response = {"Status": False, "message": "please Provide Site List"}

    return response, short_name_list