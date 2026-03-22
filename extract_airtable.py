from pyairtable import Api
import pandas as pd
import time

API_KEY = "your_token_here"
BASE_ID = "appO4HoerqJx13flv"
TABLE_NAME = "Shipments"

api = Api(API_KEY)
table = api.table(BASE_ID, TABLE_NAME)

records = []
for page in table.iterate(page_size=100):
    for record in page:
        records.append(record["fields"])
    time.sleep(0.25)  # handles rate limits: 5 req/sec

df = pd.DataFrame(records)
df.to_csv("raw_shipments.csv", index=False)
print(f"Extracted {len(df)} records")
