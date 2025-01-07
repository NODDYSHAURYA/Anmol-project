import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# API Keys
OPENWEATHER_API_KEY = "4501aee27954f15fd53811ba2d48e8be"
NEWS_API_KEY = "3e7e57b970a146ad9f0fbb43100b1b72"
UNSPLASH_ACCESS_KEY = "M7thmktfAAslxTtuGRo0-vL1wp79LRZDL-wKOomCM5I"

# List of Rivers and Coordinates
rivers = {
    "Ganga": (25.276987, 83.006825),
    "Yamuna": (28.613939, 77.209023),
    "Brahmaputra": (26.200604, 92.937573),
    "Godavari": (17.007093, 81.783240),
    "Narmada": (22.034895, 76.030124),
    "Kaveri": (12.295810, 76.639381),
    "Krishna": (16.167040, 80.403137),
    "Mahanadi": (20.264884, 85.827046),
    "Tapti": (21.222020, 73.038780),
    "Indus": (30.979812, 75.857276),
}

# Function to fetch real-time pollution data
def get_pollution_data(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Function to fetch news about the river
def get_news(river_name):
    url = f"https://newsapi.org/v2/everything?q={river_name}%20pollution&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["articles"]
    return []

# Function to fetch river image
def get_image(river_name):
    url = f"https://api.unsplash.com/search/photos?query={river_name}&client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get("results")
        if results:
            return results[0]["urls"]["regular"]
    return None

# Function to list major causes of pollution
def get_pollution_causes(river_name):
    causes = {
        "Ganga": "Industrial waste, untreated sewage, religious offerings.",
        "Yamuna": "Industrial effluents, sewage, agricultural runoff.",
        "Brahmaputra": "Urbanization, deforestation, agricultural runoff.",
        "Godavari": "Industrial discharge, mining, domestic waste.",
        "Narmada": "Urban waste, agricultural runoff, sand mining.",
        "Kaveri": "Industrial discharge, domestic waste, agricultural runoff.",
        "Krishna": "Sand mining, industrial pollution, untreated sewage.",
        "Mahanadi": "Coal mining, industrial discharge, agricultural runoff.",
        "Tapti": "Industrial discharge, urban waste, sand mining.",
        "Indus": "Industrial effluents, agricultural runoff, untreated waste."
    }
    return causes.get(river_name, "No data available.")

# Streamlit App
st.title("Water Pollution Tracker")
st.sidebar.title("Select a River")
selected_river = st.sidebar.selectbox("Choose a river to explore", list(rivers.keys()))

if selected_river:
    lat, lon = rivers[selected_river]

    # Display River Name and Image
    st.header(selected_river)
    image_url = get_image(selected_river)
    if image_url:
        st.image(image_url, caption=f"{selected_river} River", use_column_width=True)

    # Display Pollution Data
    st.subheader("Real-time Pollution Levels")
    pollution_data = get_pollution_data(lat, lon)
    if pollution_data:
        air_quality = pollution_data["list"][0]["main"]["aqi"]
        st.write(f"Air Quality Index (AQI): {air_quality}")
    else:
        st.error("Could not fetch pollution data.")

    # Display Causes of Pollution
    st.subheader("Major Causes of Pollution")
    causes = get_pollution_causes(selected_river)
    st.write(causes)
    google_search_url = f"https://www.google.com/search?q={selected_river}+pollution+causes"
    st.markdown(f"[Learn more about causes]({google_search_url})")

    # Display News Articles
    st.subheader("Recent News")
    news_articles = get_news(selected_river)
    if news_articles:
        for article in news_articles[:5]:
            st.markdown(f"### [{article['title']}]({article['url']})")
            st.write(article["description"])
            st.write(f"Published At: {article['publishedAt']}")
            st.write("---")
    else:
        st.error("No news articles found.")
