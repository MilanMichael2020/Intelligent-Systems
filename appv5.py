import streamlit as st
import time
import re
from agentsv4 import hotel_agent, restaurant_agent, filter_hotels_near_restaurants, summarizer_agent, gemini_response

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="AI Trip Planner", page_icon="🤖", layout="wide")

st.title("🤖 AI Trip Planning Assistant")
st.markdown("Plan your dream trip with the help of multiple AI agents — hotels, restaurants, and smart recommendations!")

# ------------------ USER INPUT ------------------
st.write("📝 Describe your trip preferences below:")
user_prompt = st.text_area(
    "Example: Find me Italian restaurants and a hotel in Paris under £100.",
    height=100,
    placeholder="e.g., Find me sushi restaurants and a hotel in Tokyo under £200."
)

if st.button("✨ Plan My Trip"):
    with st.spinner("Agents are working... please wait ⏳"):
        # Step 1: Extract city, budget, cuisine via Gemini
        interpret_prompt = gemini_response(
            f"""
            Extract the city, budget, and cuisine from this user prompt: "{user_prompt}".
            Reply strictly in JSON format: {{"city": "CityName", "budget": "Amount", "cuisine": "CuisineType"}}
            If not mentioned, use defaults city='London', budget='150', cuisine='any'.
            """
        )

        if interpret_prompt and interpret_prompt:
            st.info(f"🧠 AI Interpretation: {interpret_prompt}")
        else:
            st.info("🧠 AI Interpretation: (No valid response from Gemini)")

        # Parse JSON-like response
        city_match = re.search(r'"city":\s*"([^"]+)"', interpret_prompt)
        budget_match = re.search(r'"budget":\s*"([^"]+)"', interpret_prompt)
        cuisine_match = re.search(r'"cuisine":\s*"([^"]+)"', interpret_prompt)
        city = city_match.group(1) if city_match else "London"
        budget = budget_match.group(1) if budget_match else "150"
        cuisine = cuisine_match.group(1) if cuisine_match else "any"

        # Step 2: Run agents
        hotels = hotel_agent(city, budget)
        restaurants = restaurant_agent(city, cuisine)
        time.sleep(2)  # slight delay to allow images/API results

        # Step 3: Agent interaction
        hotels_near_restaurants = filter_hotels_near_restaurants(hotels, restaurants)

        # Step 4: Summarizer
        summary = summarizer_agent(hotels_near_restaurants, restaurants)

    # ------------------ DISPLAY ------------------
    st.divider()
    st.subheader(f"🌍 Destination: **{city.title()}**  |  💰 Budget: £{budget}  |  🍽️ Cuisine: {cuisine.title()}")

    # Create Tabs
    tab1, tab2, tab3 = st.tabs(["🏨 Hotels", "🍽️ Restaurants", "💬 Summary"])

    # --- Hotels Tab ---
    with tab1:
        st.markdown("### 🏨 Top Hotels Near Restaurants")
        if hotels_near_restaurants:
            for h in hotels_near_restaurants:
                with st.container():
                    cols = st.columns([1, 3])
                    with cols[0]:
                        if h.get("thumbnail"):
                            st.image(h["thumbnail"], use_container_width=True)
                    with cols[1]:
                        st.markdown(f"**{h['name']}**")
                        st.write(f"💰 Price: {h['price']} | ⭐ {h['rating']}")
                        if h.get("link"):
                            st.markdown(f"[View Details]({h['link']})")
                    st.divider()
        else:
            st.warning("No hotels found near highly-rated restaurants.")

    # --- Restaurants Tab ---
    with tab2:
        st.markdown(f"### 🍽️ {cuisine.title()} Restaurants in {city.title()}")
        if restaurants:
            for r in restaurants:
                with st.container():
                    cols = st.columns([1, 3])
                    with cols[0]:
                        if r.get("thumbnail"):
                            st.image(r["thumbnail"], use_container_width=True)
                    with cols[1]:
                        st.markdown(f"**{r['name']}** — ⭐ {r['rating']}")
                        st.write(f"📍 {r['address']}")
                        if r.get("link"):
                            st.markdown(f"[View on Google Maps]({r['link']})")
                    st.divider()
        else:
            st.warning("No restaurants found.")

    # --- Summary Tab ---
    with tab3:
        st.markdown("### 💬 AI Recommendation Summary")
        st.success(summary)

# ------------------ Optional Chat ------------------
st.divider()
st.subheader("💬 Chat with Your Travel Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).write(msg["content"])

user_msg = st.chat_input("Ask follow-up questions (e.g., show only 4-star hotels)")
if user_msg:
    st.session_state.chat_history.append({"role": "user", "content": user_msg})
    reply = gemini_response(f"You are a helpful travel assistant. Respond conversationally to: {user_msg}")
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
