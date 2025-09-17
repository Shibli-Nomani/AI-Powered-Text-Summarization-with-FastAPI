# inspect_chroma_db.py
import duckdb
import os

# Path to your ChromaDB persistent directory
db_path = os.path.join("chroma_db", "chroma.db")  # <-- adjust if different

# Connect to DuckDB
con = duckdb.connect(db_path)

# List all tables
tables = con.execute("SHOW TABLES").fetchall()
print("Tables in DB:", tables)

# Query a collection table (replace 'collection_video_transcripts' with actual table name)
results = con.execute("SELECT * FROM collection_video_transcripts LIMIT 5").fetchall()
print("Sample rows:", results)
