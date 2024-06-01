import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

def handle_uploaded_file(f):
    try:
        df = pd.read_excel(f)
    except Exception as e:
        return f"Error reading Excel file: {str(e)}"

    summary = df.groupby(['Date', 'ACCNO', 'CustState', 'CustPin', 'DPD']).size().reset_index(name='Count')
    return summary.to_dict(orient='records')

def generate_summary_excel(summary, response):
    df = pd.DataFrame(summary)
    wb = Workbook()
    ws = wb.active
    for r in dataframe_to_rows(df, index=False, header=True):
        ws.append(r)
    wb.save(response)
