import pandas as pd
import requests
from io import BytesIO 


spreadsheet_id = '1hrR2lJW32sRmHS5kZPdvRys-dNEYRgTIEGzaOjOJjCk'
file_name = 'https://docs.google.com/spreadsheets/d/{}/export?format=csv'.format(spreadsheet_id) 
r = requests.get(file_name) 
df = pd.read_csv(BytesIO(r.content), dtype = {'Глава':'object'})

df = df.reset_index()
for i in range(len(df)):
    print(df.iat[i,3])
