# agents.py
import os
import csv
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Optional Gemini integration (safe)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    try:
        import google.generativeai as genai
        genai.configure(api_key=GOOGLE_API_KEY)
    except Exception:
        genai = None
else:
    genai = None

HOTELS = []

with open("data/hotels.csv", newline='', encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        HOTELS.append({
            "city": row["city"],
            "name": row["name"],
            "price": float(row["price"]),
            "rating": float(row["rating"]),
            "address": row["address"]
        })

RESTAURANTS = []

with open("data/restaurants.csv", newline='', encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        RESTAURANTS.append({
            "city": row["city"],
            "name": row["name"],
            "cuisine": row["cuisine"],
            "price": float(row["price"]),
            "rating": float(row["rating"]),
            "address": row["address"]
        })

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
BOOKINGS_CSV = os.path.join(DATA_DIR, "bookings.csv")


# -------------------------
# Gemini wrapper (safe)
# -------------------------
def gemini_response(prompt: str) -> str:
    """
    Use Gemini if available. If Gemini not configured or fails, return a fallback string.
    """
    if not genai:
        # simple local fallback summary
        return "(No Gemini key) Summary: use offline summary or provide GOOGLE_API_KEY in .env."
    try:
        # pick a commonly available model name; if this errors, it will be caught
        model = genai.GenerativeModel("gemini-2.5-flash")
        resp = model.generate_content(prompt)
        return resp.text
    except Exception as e:
        return f"(Gemini error) {e}"


# -------------------------
# Restaurant Agent
# -------------------------
def restaurant_agent(city: str, cuisines=None, rest_budget=None, top_k=20):
    """
    city: "London", "Paris", ...
    cuisines: list of cuisine strings (case-insensitive). If None or empty -> all cuisines.
    rest_budget: max price per person (float) or None for no limit.
    """
    # basic filtering
    results = [r for r in RESTAURANTS if r["city"].lower() == city.lower()]
    if cuisines:
        clower = [c.strip().lower() for c in cuisines if c.strip()]
        def matches(r):
            return any(c in r["cuisine"].lower() for c in clower)
        results = [r for r in results if matches(r)]
    if rest_budget:
        try:
            rb = float(rest_budget)
            results = [r for r in results if r.get("price") is not None and r["price"] <= rb]
        except:
            pass
    # sort by rating desc then price asc
    results.sort(key=lambda x: ((-x["rating"]) if x.get("rating") else 0, x.get("price") or 9999))
    return results[:top_k]


# -------------------------
# Hotel Agent
# -------------------------
def hotel_agent(city: str, check_in, check_out, hotel_budget=None, top_k=20):
    """
    Returns hotels filtered by city and budget.
    check_in/check_out provided for UX but no availability check (offline dataset).
    """
    results = [h for h in HOTELS if h["city"].lower() == city.lower()]
    if hotel_budget:
        try:
            hb = float(hotel_budget)
            results = [h for h in results if h.get("price") is not None and h["price"] <= hb]
        except:
            pass
    # sort by rating desc then price asc
    results.sort(key=lambda x: ((-x["rating"]) if x.get("rating") else 0, x.get("price") or 9999))
    return results[:top_k]


# -------------------------
# Summarizer Agent (fallback + Gemini)
# -------------------------
def summarizer_agent(hotels, restaurants):
    """
    Prepare a prompt and call Gemini (if available). If not, produce a local textual summary.
    """
    hotel_lines = []
    for h in hotels:
        hotel_lines.append(f"{h['name']} (£{h['price']}/night, {h['rating']}⭐) — {h.get('address','')}")
    rest_lines = []
    for r in restaurants:
        rest_lines.append(f"{r['name']} ({r['cuisine']}, £{r['price']}, {r['rating']}⭐) — {r.get('address','')}")
    prompt = (
        "You are a travel assistant. Provide a short recommendation for a traveler based on these lists.\n\n"
        "Hotels:\n" + ("\n".join(hotel_lines) if hotel_lines else "No hotels found.") +
        "\n\nRestaurants:\n" + ("\n".join(rest_lines) if rest_lines else "No restaurants found.") +
        "\n\nGive top 3 suggestions and one short itinerary idea."
    )
    return gemini_response(prompt)


# -------------------------
# Booking (dummy)
# -------------------------
def book_item(item_type: str, item: dict, check_in, check_out, guest_name: str, guest_email: str):
    """
    item_type: "hotel" or "restaurant"
    item: selected dict
    Writes a booking row to data/bookings.csv and returns a simulated confirmation string.
    """
    exists = os.path.exists(BOOKINGS_CSV)
    with open(BOOKINGS_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(["timestamp","item_type","name","city","check_in","check_out","guest_name","guest_email"])
        timestamp = datetime.utcnow().isoformat()
        city = item.get("city") or item.get("city", "")
        name = item.get("name") or item.get("title") or "Unknown"
        writer.writerow([timestamp, item_type, name, city, str(check_in), str(check_out), guest_name, guest_email])
    # Simulated email text
    confirmation = (
        f"Simulated booking confirmation\n\n"
        f"Type: {item_type.title()}\n"
        f"Name: {name}\n"
        f"City: {city}\n"
        f"Check-in: {check_in}\n"
        f"Check-out: {check_out}\n"
        f"Guest: {guest_name}\n"
        f"Email: {guest_email}\n\n"
        f"Note: This is a simulated booking (no real email was sent)."
    )
    return confirmation
