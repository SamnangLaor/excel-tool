import pandas as pd

# 1. Read Excel file
df = pd.read_excel('application-originated-owner.xlsx')  # Replace with your file path

# 2. Generate INSERT SQL statements
table_name = 'your_table'  # Replace with your actual table name
sql_lines = []

for _, row in df.iterrows():
    acode = row[df.columns[0]]
    uid = row[df.columns[2]]

    sql_line = f"UPDATE application SET created_by_id = {uid} WHERE code = '{acode}';\n"
    sql_lines.append(sql_line)

# 3. Write to .sql file
with open('application-originated-owner.sql', 'w', encoding='utf-8') as f:
    f.write('\n'.join(sql_lines))

print('✅ SQL file created: output.sql')
