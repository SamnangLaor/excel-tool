import pandas as pd
import json


def trim_all(df):
  # Select columns with string dtype (object)
  string_cols = df.select_dtypes(include=['object'])
  # Apply strip function to each string column
  return df.assign(**string_cols.apply(lambda x: x.str.strip()))


def excel_to_json(excel_file):
  to_date = {'cif': str, 'submit_date': str, 'repayment_date': str}
  data = pd.read_excel(excel_file, sheet_name='Sheet1', converters=to_date)
  trim_all(data.copy())

  return json.loads(trim_all(data.copy()).to_json(orient='records'))


def convert_to_json(excel_file, json_file):
  with open(json_file, 'w') as f:
    f.write(json.dumps(excel_to_json(excel_file), indent=4))


excel = 'public/files/excel/Book1.xlsx'
json_file = 'public/files/json/nature_move.json'


if __name__ == '__main__':
  convert_to_json(excel, json_file)