import duckdb

conn = duckdb.connect("shipments.duckdb")
conn.execute("""
    CREATE TABLE IF NOT EXISTS shipments AS
    SELECT * FROM read_csv_auto("shipments_clean.csv")
""")
print(conn.execute("SELECT COUNT(*) FROM shipments").fetchone())
