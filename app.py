# app.py
import streamlit as st
from datetime import date, timedelta
from agents import restaurant_agent, hotel_agent, summarizer_agent, book_item, HOTELS, RESTAURANTS

st.set_page_config(page_title="AI Trip Planner", page_icon="🌍", layout="wide")
st.title("🌍 Local AI Trip Planner")

st.info("This app uses local sample data (no external APIs). Fill the form below and click Plan My Trip.")

cities = sorted(set(h['city'] for h in HOTELS + RESTAURANTS))

# ----------------- Input form -----------------
with st.form("trip_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        city = st.selectbox("City", options=cities, index=0)
        check_in = st.date_input("Check-in date", date.today())
        check_out = st.date_input("Check-out date", date.today() + timedelta(days=1))
    with col2:
        hotel_budget = st.number_input("Max hotel budget per night (£)", min_value=20, max_value=2000, value=150)
        rest_budget = st.number_input("Max restaurant price per person (£) (0 = no limit)", min_value=0, max_value=500, value=0)
    with col3:
        cuisines_raw = st.text_input("Preferred cuisines (comma-separated). Leave blank for any.", value="Italian")
        submitted = st.form_submit_button("Plan My Trip")

if submitted:
    # parse cuisines
    cuisines = [c.strip() for c in cuisines_raw.split(",") if c.strip()]
    rest_budget_val = None if rest_budget == 0 else rest_budget

    # Run agents
    restaurants = restaurant_agent(city, cuisines if cuisines else None, rest_budget_val)
    hotels = hotel_agent(city, check_in, check_out, hotel_budget)

    # Display counts
    st.write(f"Found **{len(hotels)}** hotels and **{len(restaurants)}** restaurants for {city}.")

    # ----------------- Results UI -----------------
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
            st.warning("No hotels match your filters.")

    with right:
        st.header("🍽️ Restaurants")
        if restaurants:
            for r in restaurants:
                st.subheader(r["name"])
                st.write(f"{r['cuisine']} | £{r['price']} per person | ⭐ {r['rating']}")
                st.write(r.get("address",""))
                st.markdown("---")
        else:
            st.warning("No restaurants match your filters.")

    # ----------------- Summary -----------------
    st.header("💬 Summary / Recommendation")
    summary = summarizer_agent(hotels, restaurants)
    st.write(summary)

    # ----------------- Booking Flow -----------------
    st.header("🔔 Book a Hotel or Restaurant (Simulated)")
    want_book = st.radio("Would you like to book any of these?", ("No","Yes"))

    if want_book == "Yes":
        choice_type = st.radio("Book a Hotel or a Restaurant?", ("Hotel","Restaurant"))
        if choice_type == "Hotel":
            if not hotels:
                st.warning("No hotels to book.")
            else:
                hotel_names = [h["name"] for h in hotels]
                selected = st.selectbox("Select hotel to book", options=hotel_names)
                guest_name = st.text_input("Your full name")
                guest_email = st.text_input("Your email address")
                if st.button("Confirm Hotel Booking (Simulated)"):
                    chosen = next((h for h in hotels if h["name"]==selected), hotels[0])
                    confirmation = book_item("hotel", chosen, check_in, check_out, guest_name or "Guest", guest_email or "guest@example.com")
                    st.success("Booking recorded (simulated).")
                    st.code(confirmation)

        else:  # Restaurant booking
            if not restaurants:
                st.warning("No restaurants to book.")
            else:
                rest_names = [r["name"] for r in restaurants]
                selected_r = st.selectbox("Select restaurant to book", options=rest_names)
                guest_name = st.text_input("Your full name for restaurant booking", key="r_name")
                guest_email = st.text_input("Your email address for restaurant booking", key="r_email")
                if st.button("Confirm Restaurant Booking (Simulated)"):
                    chosen = next((r for r in restaurants if r["name"]==selected_r), restaurants[0])
                    confirmation = book_item("restaurant", chosen, check_in, check_out, guest_name or "Guest", guest_email or "guest@example.com")
                    st.success("Restaurant booking recorded (simulated).")
                    st.code(confirmation)

    st.info("Bookings are simulated and saved to data/bookings.csv in the project folder.")
