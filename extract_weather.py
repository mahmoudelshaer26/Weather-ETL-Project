import requests
import csv
from datetime import datetime

API_KEY = "98815b52f92e202113b5411eba190c6c"
CITIES = ["Munich", "Berlin", "Cairo", "Madrid", "Amsterdam"]
CSV_FILE = "weather_raw.csv"

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return {
        "city": city,
        "temperature_c": round(data["main"]["temp"] - 273.15, 2),
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "weather": data["weather"][0]["main"],
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    }

def write_csv(data):
    file_exists = False
    try:
        with open(CSV_FILE, 'r'):
            file_exists = True
    except FileNotFoundError:
        pass

    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

if __name__ == "__main__":
    for city in CITIES:
        weather = get_weather(city)
        write_csv(weather)
    print("✅ Weather data extracted and saved to CSV.")
