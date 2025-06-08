import requests
import sqlite3
from datetime import datetime
import time
import pandas as pd

# === CONFIG ===
API_KEY = "98815b52f92e202113b5411eba190c6c"
CITIES = ["Munich", "Berlin", "Cairo", "Madrid", "Amsterdam"]
DB_NAME = "weather.db"

# === EXTRACT ===
def get_weather(city, api_key):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching data for {city}: {e}")
        return None

# === TRANSFORM ===
def transform_weather(raw):
    # Basic cleaning: convert Kelvin to Celsius, format timestamp
    return {
        "city": raw["name"],
        "temperature_c": round(raw["main"]["temp"] - 273.15, 2),
        "humidity": raw["main"]["humidity"],
        "wind_speed": raw["wind"]["speed"],
        "weather": raw["weather"][0]["main"],
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    }

# === LOAD ===
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            temperature_c REAL,
            humidity INTEGER,
            wind_speed REAL,
            weather TEXT,
            timestamp DATETIME
        )
    """)
    conn.commit()

def insert_data(conn, data):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO weather_data (city, temperature_c, humidity, wind_speed, weather, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (data["city"], data["temperature_c"], data["humidity"], data["wind_speed"], data["weather"], data["timestamp"]))
    conn.commit()

# === RUN ETL ===
def run_etl():
    conn = sqlite3.connect(DB_NAME)
    create_table(conn)

    for city in CITIES:
        raw = get_weather(city, API_KEY)
        if raw:
            transformed = transform_weather(raw)
            insert_data(conn, transformed)
            print(f"Inserted data for {city}")
        time.sleep(1)  # to avoid API rate limits

    conn.close()
    print("ETL completed.")

if __name__ == "__main__":
    run_etl()
