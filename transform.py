import pandas as pd
import numpy as np

df = pd.read_csv("raw_shipments.csv", encoding="latin-1")

df["Freight Cost (USD)"] = pd.to_numeric(df["Freight Cost (USD)"], errors="coerce")
df["Weight (Kilograms)"] = pd.to_numeric(df["Weight (Kilograms)"], errors="coerce")
df["Shipment Mode"] = df["Shipment Mode"].str.strip().str.title()
df["Scheduled Delivery Date"] = pd.to_datetime(df["Scheduled Delivery Date"], errors="coerce")
df["Delivered to Client Date"] = pd.to_datetime(df["Delivered to Client Date"], errors="coerce")
df["Cost per KG"] = df["Freight Cost (USD)"] / df["Weight (Kilograms)"]
df["Delivery Status"] = np.where(
    df["Delivered to Client Date"] <= df["Scheduled Delivery Date"],
    "On-Time", "Late"
)
df_clean = df.dropna(subset=["Freight Cost (USD)", "Weight (Kilograms)", "Delivered to Client Date"])
df_clean.to_csv("shipments_clean.csv", index=False)
print(f"Clean dataset: {len(df_clean)} rows")
