import pandas as pd

# Load both Excel files
df1 = pd.read_excel("public/files/excel/arrears_data.xlsx")
df2 = pd.read_excel("public/files/excel/ovd17.xlsx")

# Merge on matching column, e.g. "loan_ref"
merged = pd.merge(df1, df2, on="loan_ref", how="inner")

# Save the result
merged.to_excel("merged.xlsx", index=False)
