import csv
import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from login import login

INPUT_FILE = "./public/files/csv/acc_transactions/acc_transactions__180001.csv"

API_URL = "http://localhost:3000/api/core-banking/account-transaction"
LOS_API_URL = "https://api-los.ababank.com/api"


MAX_WORKERS = 9
BATCH_SIZE = 500

TOKEN = None
TOKEN_LOCK = threading.Lock()
TOKEN_REFRESH_SECONDS = 60 * 60  # 1 hour


def get_token():
    global TOKEN, TOKEN_TIME

    now = time.time()

    if TOKEN is None or now - TOKEN_TIME >= TOKEN_REFRESH_SECONDS:
        with TOKEN_LOCK:
            # Check again after acquiring the lock
            now = time.time()

            if TOKEN is None or now - TOKEN_TIME >= TOKEN_REFRESH_SECONDS:
                TOKEN = login()
                TOKEN_TIME = now

    return TOKEN


def request_account(row):
    params = {
        "applicationID": row["application_id"],
        "from": datetime.strptime(row["from_date"], "%d/%m/%y").strftime("%Y-%m-%d"),
        "to": datetime.strptime(row["to_date"], "%d/%m/%y").strftime("%Y-%m-%d"),
        "offset": 0,
        "limit": 99,
        "cif": row["cif"].zfill(7),
        "account_no": row["account_no"].zfill(9),
    }

    try:
        token = get_token()

        headers = {
            "Authorization": f"Bearer {token}",
        }

        response = requests.get(
            API_URL,
            headers=headers,
            params=params,
            timeout=30,
        )

        if response.status_code == 500:
            print(response.request.__dict__)

        return row, response.status_code, response.text

    except requests.RequestException as e:
        return row, "ERROR", str(e)


def batches(reader, size):
    batch = []

    for row in reader:
        batch.append(row)

        if len(batch) == size:
            yield batch
            batch = []

    if batch:
        yield batch


processed = 0

with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

        for batch in batches(reader, BATCH_SIZE):

            futures = [
                executor.submit(request_account, row)
                for row in batch
            ]

            for future in as_completed(futures):
                row, status, data = future.result()

                processed += 1

                if status != 200:
                  with open("failed.log", "a", encoding="utf-8") as log_file:
                      log_file.write(
                          f"FAILED {processed}: "
                          f"{row['cif']} / {row['account_no']} "
                          f"application={row['application_id']} "
                          f"status={status} "
                          f"error={data}\n"
                      )

                  with open("failed.csv", "a", newline="", encoding="utf-8") as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=row.keys())
                    writer.writerow(row)

                if processed % 1000 == 0:
                    print(f"Processed {processed}/100000")

print("Finished")
