import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# Load data
df = pd.read_csv("weather_clean.csv")

# Page config
st.set_page_config(page_title="Weather Dashboard", layout="wide")

# Title
st.title("🌤️ Weather Dashboard")

# Show raw data toggle
if st.checkbox("Show Raw Data"):
    st.dataframe(df)

# Average temperature by city
st.subheader("📊 Average Temperature by City")

avg_temp = df.groupby("city")["temperature_c"].mean().reset_index()

chart = alt.Chart(avg_temp).mark_bar().encode(
    x=alt.X('city', sort=None, axis=alt.Axis(labelAngle=0, title="City")),
    y=alt.Y('temperature_c', title="Temperature (°C)")
).properties(width=600, height=400)

st.altair_chart(chart, use_container_width=True)

# Humidity line chart with one line per city
st.subheader("💧 Humidity Over Time by City")

humidity_line = alt.Chart(df).mark_line().encode(
    x=alt.X('timestamp:T', axis=alt.Axis(title='Timestamp', format='%H:%M', labelAngle=45)),
    y=alt.Y('humidity', title='Humidity'),
    color='city:N',
    tooltip=['city', 'timestamp', 'humidity']
).properties(width=700, height=400).interactive()

st.altair_chart(humidity_line, use_container_width=True)

# Custom CSS for smaller dropdowns aligned to the left
st.markdown("""
    <style>
    .small-selectbox .stSelectbox > div:first-child {
        max-width: 5rem;
        min-width: 5rem;
    }
    </style>
    """, unsafe_allow_html=True)


# ----------- Row 1: Wind speed dropdown + Histogram -----------

row1_col1, row1_col2 = st.columns([1, 3])

with row1_col1:
    wind_city = st.selectbox("Wind Speed City", df["city"].unique(), key="wind", label_visibility="visible")

with row1_col2:
    wind_df = df[df["city"] == wind_city]

    st.subheader("🌬️ Wind Speed Distribution")
    wind_hist = alt.Chart(wind_df).mark_bar().encode(
        x=alt.X("wind_speed:Q", bin=alt.Bin(maxbins=20), title="Wind Speed (m/s)"),
        y=alt.Y("count():Q", title="Number of readings"),
        tooltip=["wind_speed"]
    ).properties(width=600, height=400, title=f"Wind Speed Distribution in {wind_city}")

    st.altair_chart(wind_hist, use_container_width=True)
    st.caption("This histogram shows how often wind speeds were recorded within each range.")


# ----------- Row 2: Weather condition dropdown + Pie chart -----------

row2_col1, row2_col2 = st.columns([1, 3])

with row2_col1:
    weather_city = st.selectbox("Weather Condition City", df["city"].unique(), key="weather", label_visibility="visible")

with row2_col2:
    weather_df = df[df["city"] == weather_city]
    weather_counts = weather_df["weather"].value_counts().reset_index()
    weather_counts.columns = ["weather", "count"]

    # MAIN TITLE — same style and alignment as the wind histogram
    st.subheader("🌦️ Weather Condition Distribution by City")

    # Pie chart with dynamic subtitle as chart title and spacing using `dy`
    pie_chart = alt.Chart(weather_counts).mark_arc(innerRadius=60).encode(
        theta=alt.Theta(field="count", type="quantitative"),
        color=alt.Color(field="weather", type="nominal", legend=alt.Legend(title="Weather Condition")),
        tooltip=['weather', 'count']
    ).properties(
        width=500,
        height=500,
        title=alt.TitleParams(
            text=f"Weather Condition Distribution in {weather_city}",
            anchor='start',
            fontSize=16,
            dy=20  # vertical spacing between title and chart
        )
    )

    st.altair_chart(pie_chart, use_container_width=True)




# Temperature vs Humidity scatter plot
st.subheader("🌡️ Temperature vs Humidity by City")

scatter = alt.Chart(df).mark_circle(size=60).encode(
    x=alt.X('temperature_c', title='Temperature (°C)'),
    y=alt.Y('humidity', title='Humidity (%)'),
    color='city',
    tooltip=['city', 'temperature_c', 'humidity']
).properties(width=700, height=400).interactive()

st.altair_chart(scatter, use_container_width=True)
