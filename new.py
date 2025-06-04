import pandas as pd

csv_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQwCd1kjgzzFGtRVEiOi6nnGcbRJQEP12cfZTXdGJb2aX0EDy73TngeAJI1RaDugje7KRTO_kQRmRif/pub?gid=1147940658&single=true&output=csv'

df = pd.read_csv(csv_url)

# Visualizza tutto
print(df.to_string(index=False))
