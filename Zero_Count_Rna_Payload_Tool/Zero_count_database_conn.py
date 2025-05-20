import pandas as pd
from django.db import connection

def get_data_from_table(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]  
        
    df = pd.DataFrame(rows, columns=columns)
    return df
