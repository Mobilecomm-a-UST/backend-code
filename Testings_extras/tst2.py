import pandas as pd
import json

# Read the Excel file into a Pandas DataFrame
df = pd.read_excel(r'E:\Vendor management Portal\test.xlsx')

# Convert the DataFrame to a dictionary
data = df.to_dict(orient='records')
print(data)
# Convert the dictionary to JSON format
json_data = json.dumps(data)