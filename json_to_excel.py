import pandas as pd
import json
import csv

def read_json(filename: str) -> dict:
    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except:
        raise Exception(f"Reading {filename} file encountered an error")

    return data

def convert_json_to_excel(json_file: str, excel_file: str):
    data = read_json(json_file)
    print(data)
    df = pd.json_normalize(data)
    df.to_excel(excel_file, index=False)

# Usage:
json_file = 'public/files/json/credit-history.json'
excel_file = 'public/files/excel/court_casess.xlsx'
convert_json_to_excel(json_file, excel_file)
