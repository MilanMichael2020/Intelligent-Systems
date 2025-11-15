# app.py
import streamlit as st
from datetime import date, timedelta
from agentsv2 import restaurant_agent, hotel_agent, summarizer_agent, book_item, HOTELS, RESTAURANTS

st.set_page_config(page_title="AI Trip Planner", page_icon="🌍", layout="wide")
st.title("🌍 AI Trip Planner")

st.info("This app uses local sample data. Fill the form below and click Plan My Trip.")

# ----------------- Dynamic city options -----------------
cities = sorted({h["city"] for h in HOTELS}.union({r["city"] for r in RESTAURANTS}))

# ----------------- Trip Planning Form -----------------
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

# ----------------- Process Submission -----------------
if submitted:
    cuisines = [c.strip() for c in cuisines_raw.split(",")] if cuisines_raw.strip() else []
    rest_budget_val = None if rest_budget == 0 else rest_budget

    # Persist search results and trip info in session_state
    st.session_state['hotels'] = hotel_agent(city, check_in, check_out, hotel_budget)
    st.session_state['restaurants'] = restaurant_agent(city, cuisines if cuisines else None, rest_budget_val)
    st.session_state['city'] = city
    st.session_state['check_in'] = check_in
    st.session_state['check_out'] = check_out

# ----------------- Retrieve persisted data -----------------
hotels = st.session_state.get('hotels', [])
restaurants = st.session_state.get('restaurants', [])
city = st.session_state.get('city', "")
check_in = st.session_state.get('check_in', date.today())
check_out = st.session_state.get('check_out', date.today() + timedelta(days=1))

# ----------------- Show Search Results -----------------
if hotels or restaurants:
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

    st.header("💬 Summary / Recommendation")
    summary = summarizer_agent(hotels, restaurants)
    st.write(summary)

# ----------------- Booking Section -----------------
st.header("🔔 Book a Hotel or Restaurant")
want_book = st.radio("Would you like to book any of these?", ("No","Yes"), key="want_book")

if want_book == "Yes":
    choice_type = st.radio("Book a Hotel or a Restaurant?", ("Hotel","Restaurant"), key="choice_type")

    # ----- Hotel Booking -----
    if choice_type == "Hotel" and hotels:
        selected = st.selectbox("Select hotel to book", options=[h["name"] for h in hotels], key="hotel_select")
        guest_name = st.text_input("Your full name", key="hotel_name")
        guest_email = st.text_input("Your email address", key="hotel_email")
        num_guests = st.number_input("Number of guests", min_value=1, max_value=20, value=1, key="hotel_guests")
        
        if st.button("Confirm Hotel Booking", key="hotel_btn"):
            chosen = next((h for h in hotels if h["name"] == selected), hotels[0])
            confirmation = book_item(
                "hotel", chosen, check_in, check_out,
                guest_name or "Guest", guest_email or "guest@example.com",
                num_guests
            )
            st.success("Hotel booking recorded")
            st.code(confirmation)

    # ----- Restaurant Booking -----
    elif choice_type == "Restaurant" and restaurants:
        selected_r = st.selectbox("Select restaurant to book", options=[r["name"] for r in restaurants], key="rest_select")
        guest_name = st.text_input("Your full name", key="rest_name")
        guest_email = st.text_input("Your email address", key="rest_email")
        num_guests = st.number_input("Number of guests", min_value=1, max_value=20, value=1, key="rest_guests")
        
        if st.button("Confirm Restaurant Booking", key="rest_btn"):
            chosen = next((r for r in restaurants if r["name"] == selected_r), restaurants[0])
            # Only record check-in date (restaurant visit date)
            confirmation = book_item(
                "restaurant", chosen, check_in, check_in, 
                guest_name or "Guest", guest_email or "guest@example.com",
                num_guests
            )
            st.success("Restaurant booking recorded.")
            st.code(confirmation)
