import pandas as pd

df = pd.read_excel('merged.xlsx')

with open('arrears_ovd_timeline_seed.sql', 'a', encoding='utf-8') as f:

  for row in df.itertuples(index=False):
    sql = f"""
            WITH overdue_timeline_insertion AS (
              INSERT INTO arrears_timeline_loan_ovd(arrears_timeline_id, arrears_loan_id, created_at, updated_at) VALUES({row.arrears_timeline_id}, {row.arrears_loan_id}, '2025-04-17 10:17', '2025-04-17 10:17')
              RETURNING id
            )

            INSERT INTO arrears_timeline_loan_ovd_detail(as_of_date, arrears_timeline_loan_ovd_id, ovd_days, principal_due, interest_due, outstanding_due, provision_status)
            SELECT '2025-04-17', id, {row.ovd_day}, {row.ovd_prn}, {row.ovd_int}, {row.ovd_amt}, '{row.status}'
            FROM overdue_timeline_insertion;
          """

    f.write(sql)