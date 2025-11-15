import streamlit as st
from agentsv3 import restaurant_agent, hotel_agent, summarizer_agent

st.set_page_config(page_title="AI Travel Multi-Agent", page_icon="🌍")

st.title("🌍 AI Travel Planner")
st.markdown("This app uses multiple AI agents (Gemini + SerpAPI) to find hotels and restaurants intelligently.")

# ---------- User Inputs ----------
city = st.text_input("🏙️ Enter a location:", "London")
cuisine = st.text_input("🍽️ Preferred cuisine:", "Italian")
budget = st.number_input("💰 Max hotel budget (£):", min_value=50, max_value=1000, value=200)

if st.button("✨ Find My Trip"):
    with st.spinner("Agents are collaborating..."):
        # Agent 1 → Restaurant Agent
        restaurants = restaurant_agent(city, cuisine)
        st.subheader(f"🍴 Top Restaurants in {city}")
        if restaurants:
            for r in restaurants[:5]:
                st.markdown(f"- **{r['name']}** — ⭐ {r['rating']} — {r['address']}")
        else:
            st.warning("No restaurants found.")

        # Let restaurant agent pick top area
        if restaurants:
            best_area = restaurants[0]["area"]
            st.info(f"📍 Best dining area identified: {best_area}")
        else:
            best_area = city

        # Agent 2 → Hotel Agent (guided by restaurant area)
        hotels = hotel_agent(best_area, budget)
        st.subheader(f"🏨 Hotels near {best_area}")
        if hotels:
            for h in hotels[:5]:
                st.markdown(f"- **{h['name']}** — ⭐ {h['rating']} — {h['price']}")
        else:
            st.warning("No hotels found for that area.")

        # Agent 3 → Summarizer Agent
        if hotels and restaurants:
            st.subheader("🧠 Gemini Summary & Recommendation")
            summary = summarizer_agent(hotels, restaurants)
            st.write(summary)
