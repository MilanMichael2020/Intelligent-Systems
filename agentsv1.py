import os
import csv
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    try:
        import google.generativeai as genai
        genai.configure(api_key=GOOGLE_API_KEY)
    except Exception:
        genai = None
else:
    genai = None

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
BOOKINGS_CSV = os.path.join(DATA_DIR, "bookings.csv")

# Ensure bookings.csv exists
if not os.path.exists(BOOKINGS_CSV):
    with open(BOOKINGS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp","item_type","name","city","check_in","check_out",
            "guest_name","guest_email","num_guests"
        ])

# ------------------------- Load Hotels -------------------------
HOTELS = []
with open(os.path.join(DATA_DIR, "hotels.csv"), newline='', encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        HOTELS.append({
            "city": row["city"],
            "name": row["name"],
            "price": float(row["price"]),
            "rating": float(row["rating"]),
            "address": row["address"]
        })

# ------------------------- Load Restaurants -------------------------
RESTAURANTS = []
with open(os.path.join(DATA_DIR, "restaurants.csv"), newline='', encoding="utf-8") as file:
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

# ------------------------- Restaurant Agent -------------------------
def restaurant_agent(city: str, cuisines=None, rest_budget=None, top_k=20):
    results = [r for r in RESTAURANTS if r["city"].lower() == city.lower()]
    if cuisines:
        clower = [c.strip().lower() for c in cuisines if c.strip()]
        results = [r for r in results if any(c in r["cuisine"].lower() for c in clower)]
    if rest_budget:
        results = [r for r in results if r.get("price") is not None and r["price"] <= rest_budget]
    results.sort(key=lambda x: ((-x["rating"]) if x.get("rating") else 0, x.get("price") or 9999))
    return results[:top_k]

# ------------------------- Hotel Agent -------------------------
def hotel_agent(city: str, check_in, check_out, hotel_budget=None, top_k=20):
    results = [h for h in HOTELS if h["city"].lower() == city.lower()]
    if hotel_budget:
        results = [h for h in results if h.get("price") is not None and h["price"] <= hotel_budget]
    results.sort(key=lambda x: ((-x["rating"]) if x.get("rating") else 0, x.get("price") or 9999))
    return results[:top_k]

# ------------------------- Summary Agent -------------------------
def summarizer_agent(hotels, restaurants):
    hotel_lines = [f"{h['name']} (£{h['price']}/night, {h['rating']}⭐) — {h.get('address','')}" for h in hotels]
    rest_lines = [f"{r['name']} ({r['cuisine']}, £{r['price']}, {r['rating']}⭐) — {r.get('address','')}" for r in restaurants]
    summary = "Hotels:\n" + ("\n".join(hotel_lines) if hotel_lines else "No hotels found.") + \
              "\n\nRestaurants:\n" + ("\n".join(rest_lines) if rest_lines else "No restaurants found.") + \
              "\n\nTop 3 suggestions and a short itinerary idea."
    return summary

# ------------------------- Booking -------------------------
def book_item(item_type: str, item: dict, check_in, check_out, guest_name: str, guest_email: str, num_guests: int = 1):
    timestamp = datetime.utcnow().isoformat()
    city = item.get("city", "")
    name = item.get("name") or item.get("title") or "Unknown"

    with open(BOOKINGS_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            timestamp, item_type, name, city, str(check_in), str(check_out),
            guest_name, guest_email, num_guests
        ])

    confirmation = (
        f"Simulated booking confirmation\n\n"
        f"Type: {item_type.title()}\n"
        f"Name: {name}\n"
        f"City: {city}\n"
        f"Check-in: {check_in}\n"
        f"Check-out: {check_out}\n"
        f"Guest: {guest_name}\n"
        f"Email: {guest_email}\n"
        f"Number of Guests: {num_guests}\n\n"
        f"Note: This is a simulated booking (no real email was sent)."
    )
    return confirmation

# ------------------------- Combined Budget Helper -------------------------
def split_budget(total_budget, hotel_ratio=0.7):
    hotel_budget = total_budget * hotel_ratio
    restaurant_budget = total_budget * (1 - hotel_ratio)
    return hotel_budget, restaurant_budget

def find_best_combinations(hotels, restaurants, total_budget, top_k=5):
    combos = []
    for h in hotels:
        for r in restaurants:
            combined_price = h["price"] + r["price"]
            if combined_price <= total_budget:
                score = h["rating"] + r["rating"]
                combos.append((score, h, r))
    combos.sort(key=lambda x: (-x[0], x[1]["price"] + x[2]["price"]))
    return combos[:top_k]
