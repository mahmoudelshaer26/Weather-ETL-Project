import pandas as pd

RAW_CSV = "weather_raw.csv"
CLEAN_CSV = "weather_clean.csv"

def clean_data():
    df = pd.read_csv(RAW_CSV)

    # Drop duplicates (if any)
    df.drop_duplicates(inplace=True)

    # Drop nulls (not expected, but for safety)
    df.dropna(inplace=True)

    # Standardize city names
    df["city"] = df["city"].str.title()

    df.to_csv(CLEAN_CSV, index=False)
    print("✅ Data cleaned and saved to new CSV.")

if __name__ == "__main__":
    clean_data()
