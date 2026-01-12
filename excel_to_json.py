import pandas as pd
import json
from datetime import datetime, timedelta


def trim_all(df):
  # Select columns with string dtype (object)
  string_cols = df.select_dtypes(include=['object'])
  # Apply strip function to each string column
  return df.assign(**string_cols.apply(lambda x: x.str.strip()))


def excel_to_iso(value):
    if pd.isna(value):
        return None
    # Case 1 — already a datetime object
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d")

    # Case 2 — numeric Excel serial
    if isinstance(value, (int, float)):
        return (datetime(1899, 12, 30) + timedelta(days=value)).strftime("%Y-%m-%d")

    # Case 3 — string input
    try:
        return pd.to_datetime(value).strftime("%Y-%m-%d")
    except:
        return value  # fallback


def excel_to_json(excel_file):
  to_date = {'cif': str, 'as_of_date': excel_to_iso, 'disbursement_date': excel_to_iso, 'repayment_date': excel_to_iso, 'date': excel_to_iso }
  data = pd.read_excel(excel_file, sheet_name='Sheet1', converters=to_date)
  trim_all(data.copy())

  return json.loads(trim_all(data.copy()).to_json(orient='records'))


def convert_to_json(excel_file, json_file):
  with open(json_file, 'w') as f:
    f.write(json.dumps(excel_to_json(excel_file), indent=4))


excel = 'public/files/excel/legal-action-2.xlsx'
json_file = 'public/files/json/legal-action-2.json'


if __name__ == '__main__':
  convert_to_json(excel, json_file)