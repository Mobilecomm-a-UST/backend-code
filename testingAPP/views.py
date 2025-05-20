import subprocess
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.exporters import PythonExporter
import pandas as pd
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(["GET"])
def run_ipynb(request):
    try:
        # Specify the path to the .ipynb file
        notebook_path = r'E:\datascience\testing.ipynb'

        # Read the .ipynb file
        with open(notebook_path, 'r') as nb_file:
            notebook_content = nb_file.read()

        # Convert the .ipynb content to a Python script
        notebook = nbformat.reads(notebook_content, as_version=4)
        python_exporter = PythonExporter()
        python_script, _ = python_exporter.from_notebook_node(notebook)
        
        data = {'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35]}
        df1 = pd.DataFrame(data)
        serialized_df1 = df1.to_json(orient='records')
        # serialized_df2 = df2.to_json(orient='records')

        # python_script_str = python_script.decode('utf-8')
        # Execute the Python script using subprocess and capture its output
        # result = subprocess.check_output(['python'], input=python_script.encode(), stderr=subprocess.STDOUT, universal_newlines=True)
        result = subprocess.check_output(['python', '-c', python_script,serialized_df1], stderr=subprocess.STDOUT, universal_newlines=True)
        # Assuming the script returns a DataFrame as a string (e.g., serialized as JSON)
        # You can deserialize the DataFrame back to a pandas DataFrame
        print("result",result)
        df = pd.read_json(result)  # Adjust the deserialization method as needed
        print(df)
        # Now you can work with the DataFrame (e.g., df.head(), df.to_csv(), etc.)
        # For this example, let's return the first few rows of the DataFrame as JSON
        return Response({"sts":True,"data":df})
    except subprocess.CalledProcessError as e:
        return Response({"sts":False})





