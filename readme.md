# 🌤️ Weather Data Dashboard

A weather monitoring dashboard built with Streamlit, pulling live data from the OpenWeatherMap API.

## 📁 Project Structure

- `extract_weather.py`: Extracts live weather data from the API and saves it as raw CSV.
- `clean_weather.py`: Cleans and processes the raw CSV.
- `load_weather.py`: Loads cleaned data into an SQLite database.
- `app.py`: Launches the interactive Streamlit dashboard.

## 🚀 How to Run

1. Clone the repo
2. Run the scripts in this order:
    ```bash
    python extract_weather.py
    python clean_weather.py
    python load_weather.py
    streamlit run app.py
    ```

## 🔧 Requirements

- Python 3.x
- Streamlit
- pandas
- requests
- altair
- sqlite3

Install dependencies:
```bash
pip install -r requirements.txt
