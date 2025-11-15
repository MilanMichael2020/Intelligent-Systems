import streamlit as st
from agentsv4 import hotel_agent, restaurant_agent, filter_hotels_near_restaurants, summarizer_agent, gemini_response
import re

st.set_page_config(page_title="AI Trip Planner", page_icon="🤖", layout="wide")
st.title("🤖 AI Trip Planner Assistant")

# --- Unified Input ---
st.write("Describe your trip preferences below:")
user_prompt = st.text_area("Example: Find me Italian restaurants and a hotel in Paris under £100.")

if st.button("Plan My Trip"):
    with st.spinner("Agents are working..."):
        # Step 1: Extract city, budget, and cuisine using Gemini
        interpret_prompt = gemini_response(
            f"""
            Extract the city, budget, and cuisine from this user prompt: "{user_prompt}".
            Reply in JSON format with keys: city, budget, and cuisine.
            If not mentioned, use defaults: city='London', budget='150', cuisine='any'.
            """
        )
        st.write("🧠 AI Interpretation:", interpret_prompt)

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

        # Step 3: Agent interaction
        hotels_near_restaurants = filter_hotels_near_restaurants(hotels, restaurants)

        # Step 4: Summarize
        summary = summarizer_agent(hotels_near_restaurants, restaurants)

        # Step 5: Display neatly
        st.subheader(f"🏨 Hotels Near {city}")
        if hotels_near_restaurants:
            cols = st.columns(2)
            for i, h in enumerate(hotels_near_restaurants):
                with cols[i % 2]:
                    st.markdown(f"### {h['name']}")
                    if h.get("thumbnail"):
                        st.image(h["thumbnail"], use_container_width=False, width=250)
                    st.write(f"💰 Price: {h['price']}")
                    st.write(f"⭐ Rating: {h['rating']}")
                    if h.get("link"):
                        st.markdown(f"[View Details]({h['link']})")
                    st.divider()
        else:
            st.write("No hotels found near highly-rated restaurants.")

        st.subheader(f"🍽️ Nearby {cuisine.title()} Restaurants")
        if restaurants:
            cols = st.columns(2)
            for i, r in enumerate(restaurants):
                with cols[i % 2]:
                    st.markdown(f"### {r['name']}")
                    if r.get("thumbnail"):
                        st.image(r["thumbnail"], use_container_width=False, width=250)
                    st.write(f"⭐ {r['rating']} | 📍 {r['address']}")
                    if r.get("link"):
                        st.markdown(f"[View on Google Maps]({r['link']})")
                    st.divider()
        else:
            st.write("No restaurants found.")

        st.subheader("💬 AI Recommendation Summary")
        st.info(summary)

# --- Optional Chat ---
st.divider()
st.subheader("💬 Chat with Travel Assistant")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).write(msg["content"])

user_msg = st.chat_input("Ask follow-up questions (e.g., show only 4-star hotels)")
if user_msg:
    st.session_state.chat_history.append({"role": "user", "content": user_msg})
    reply = gemini_response(f"You are a travel assistant. Respond to: {user_msg}")
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
