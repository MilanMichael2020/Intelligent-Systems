import streamlit as st
from datetime import date, timedelta
from agentsv1 import (
    restaurant_agent, hotel_agent, summarizer_agent,
    book_item, HOTELS, RESTAURANTS,
    split_budget, find_best_combinations
)

st.set_page_config(page_title="Local AI Trip Planner", page_icon="🌍", layout="wide")
st.title("🌍 Local AI Trip Planner (Offline)")

st.info("This app uses local sample data. Fill the form and click Plan My Trip.")

# ----------------- Dynamic city options -----------------
cities = sorted({h["city"] for h in HOTELS}.union({r["city"] for r in RESTAURANTS}))

# ----------------- Input form -----------------
with st.form("trip_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        city = st.selectbox("City", options=cities, index=0)
        check_in = st.date_input("Check-in date", date.today())
        check_out = st.date_input("Check-out date", date.today() + timedelta(days=1))
    with col2:
        total_budget = st.number_input("Total budget for hotel + restaurant (£)", min_value=20, max_value=3000, value=300)
        num_guests = st.number_input("Number of Guests", min_value=1, max_value=20, value=1)
    with col3:
        cuisines_raw = st.text_input("Preferred cuisines (comma-separated)", value="Italian")
        submitted = st.form_submit_button("Plan My Trip")

if submitted:
    cuisines = [c.strip() for c in cuisines_raw.split(",")] if cuisines_raw.strip() else []

    # Split combined budget
    hotel_budget, rest_budget = split_budget(total_budget)

    # Fetch top hotels and restaurants
    hotels = hotel_agent(city, check_in, check_out, hotel_budget)
    restaurants = restaurant_agent(city, cuisines if cuisines else None, rest_budget)

    st.write(f"Found **{len(hotels)}** hotels and **{len(restaurants)}** restaurants for {city}.")

    left, right = st.columns(2)

    with left:
        st.header("🏨 Hotels")
        if hotels:
            for h in hotels:
                st.subheader(h["name"])
                st.write(f"£{h['price']} per night | ⭐ {h['rating']}")
                st.write(h.get("address",""))
                st.markdown("---")
        else:
            st.warning("No hotels match your budget.")

    with right:
        st.header("🍽️ Restaurants")
        if restaurants:
            for r in restaurants:
                st.subheader(r["name"])
                st.write(f"{r['cuisine']} | £{r['price']} per person | ⭐ {r['rating']}")
                st.write(r.get("address",""))
                st.markdown("---")
        else:
            st.warning("No restaurants match your budget.")

    # Summary
    st.header("💬 Summary / Recommendation")
    summary = summarizer_agent(hotels, restaurants)
    st.write(summary)

    # Best hotel+restaurant combinations
    best_combos = find_best_combinations(hotels, restaurants, total_budget)
    if best_combos:
        st.header("💡 Best Hotel + Restaurant Combos Within Your Budget")
        for score, h, r in best_combos:
            st.subheader(f"{h['name']} + {r['name']}")
            st.write(f"Combined Price: £{h['price'] + r['price']} | Score: {score:.1f}")
            st.write(f"Hotel: £{h['price']} per night, ⭐ {h['rating']}")
            st.write(f"Restaurant: £{r['price']} per person, ⭐ {r['rating']}")
            st.markdown("---")

    # Booking
    st.header("🔔 Book a Hotel or Restaurant (Simulated)")
    want_book = st.radio("Would you like to book any of these?", ("No","Yes"))

    if want_book == "Yes":
        choice_type = st.radio("Book a Hotel or a Restaurant?", ("Hotel","Restaurant"))

        if choice_type == "Hotel" and hotels:
            selected = st.selectbox("Select hotel to book", options=[h["name"] for h in hotels])
            guest_name = st.text_input("Your full name", key="hotel_name")
            guest_email = st.text_input("Your email address", key="hotel_email")
            if st.button("Confirm Hotel Booking (Simulated)"):
                chosen = next((h for h in hotels if h["name"]==selected), hotels[0])
                confirmation = book_item(
                    "hotel", chosen, check_in, check_out,
                    guest_name or "Guest", guest_email or "guest@example.com",
                    num_guests
                )
                st.success("Booking recorded (simulated).")
                st.code(confirmation)

        elif choice_type == "Restaurant" and restaurants:
            selected_r = st.selectbox("Select restaurant to book", options=[r["name"] for r in restaurants])
            guest_name = st.text_input("Your full name for restaurant booking", key="r_name")
            guest_email = st.text_input("Your email address for restaurant booking", key="r_email")
            if st.button("Confirm Restaurant Booking (Simulated)"):
                chosen = next((r for r in restaurants if r["name"]==selected_r), restaurants[0])
                confirmation = book_item(
                    "restaurant", chosen, check_in, check_in,  # same check-in/check-out for restaurant
                    guest_name or "Guest", guest_email or "guest@example.com",
                    num_guests
                )
                st.success("Restaurant booking recorded (simulated).")
                st.code(confirmation)

    st.info("Bookings are simulated and saved to data/bookings.csv.")
