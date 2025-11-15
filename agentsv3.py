import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# ----------------- Gemini Configuration -----------------
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def gemini_response(prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text


# ----------------- Restaurant Agent -----------------
def restaurant_agent(location, cuisine="any"):
    """Find restaurants using SerpAPI (Google Maps engine)."""
    api_key = os.getenv("SERPAPI_KEY")
    url = "https://serpapi.com/search.json"

    params = {
        "engine": "google_maps",
        "q": f"{cuisine} restaurants in {location}",
        "type": "search",
        "hl": "en",
        "gl": "uk",
        "api_key": api_key
    }

    res = requests.get(url, params=params)
    data = res.json()
    restaurants = []

    for place in data.get("local_results", [])[:10]:
        restaurants.append({
            "name": place.get("title"),
            "rating": float(place.get("rating", 0)),
            "address": place.get("address"),
            "area": place.get("address").split(",")[0] if place.get("address") else location,
        })

    return restaurants


# ----------------- Hotel Agent -----------------
def hotel_agent(location, budget):
    """Find hotels using SerpAPI (Google Hotels engine)."""
    api_key = os.getenv("SERPAPI_KEY")
    url = "https://serpapi.com/search.json"

    params = {
        "engine": "google_hotels",
        "q": f"hotels in {location}",
        "check_in_date": "2025-11-10",
        "check_out_date": "2025-11-11",
        "currency": "GBP",
        "hl": "en",
        "gl": "uk",
        "api_key": api_key
    }

    res = requests.get(url, params=params)
    data = res.json()
    hotels = []

    for h in data.get("properties", [])[:10]:
        hotels.append({
            "name": h.get("name"),
            "rating": float(h.get("overall_rating", 0)),
            "price": h.get("rate_per_night", {}).get("lowest", "N/A"),
            "link": h.get("link")
        })

    return hotels


# ----------------- Summarizer Agent -----------------
def summarizer_agent(hotels, restaurants):
    hotel_text = "\n".join([f"{h['name']} ({h['rating']}⭐, {h['price']})" for h in hotels])
    restaurant_text = "\n".join([f"{r['name']} ({r['rating']}⭐, {r['address']})" for r in restaurants])

    prompt = f"""
    Based on this data, summarize and recommend the best travel plan:
    Hotels:
    {hotel_text}

    Restaurants:
    {restaurant_text}
    """
    return gemini_response(prompt)