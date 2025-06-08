import sqlite3
import pandas as pd

DB_NAME = "weather_data.db"
CLEAN_CSV = "weather_clean.csv"

def load_data():
    df = pd.read_csv(CLEAN_CSV)
    conn = sqlite3.connect(DB_NAME)
    df.to_sql("weather", conn, if_exists="append", index=False)
    conn.close()
    print("✅ Data loaded into SQLite database.")

if __name__ == "__main__":
    load_data()
