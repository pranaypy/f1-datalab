import streamlit as st
import os
import sys
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ergast_api import search_drivers, get_driver_stats, get_driver_championships, get_driver_season_stats
from visualizations.driver_charts import points_per_season_chart, wins_per_season_chart

# --- Page Configuration ---
st.set_page_config(
    page_title="DataLab.F1",
    page_icon="🏎️",
    layout="wide"
)

# --- Header ---
st.markdown("""
    <h1 style='color: #BF1200;'>🏎️ F1 DataLab</h1>
    <p style='color: #AAAAAA; font-size: 18px;'>Formula 1 Driver Statistics and Analytics</p>
""", unsafe_allow_html=True)

# --- Divider ---
st.divider()

# --- Search Box ---
st.subheader("🔍 Search for a Driver")
driver_name = st.text_input("Enter driver name (e.g. Lewis Hamilton)")

 
if driver_name:
    with st.spinner("Searching..."):
        matches = search_drivers(driver_name)


    if len(matches) == 0:
        st.error("No driver found. Check the name and try again.")
    
    elif len(matches) == 1:
        driver = matches[0]
        st.success(f"Driver found!")
        col1, col2 = st.columns(2)

        with col1:
            st.metric("First Name", driver.get("givenName", "N/A"))
            st.metric("Last Name", driver.get("familyName", "N/A"))
            st.metric("Nationality", driver.get("nationality", "N/A"))

        with col2:
            st.metric("Driver ID", driver.get("driverId", "N/A"))
            st.metric("Number", driver.get("permanentNumber", "N/A"))
            st.metric("Code", driver.get("code", "N/A"))

        # Fetch and display driver stats
        st.divider()
        st.subheader("📊 Career Statistics")

        with st.spinner("Loading career stats..."):
            stats = get_driver_stats(driver.get("driverId"))
            championships = get_driver_championships(driver.get("driverId"), stats["first_season"], stats["last_season"])

        col3, col4, col5, col6 = st.columns(4)

        with col3:
            st.metric("Total Races", stats["total_races"])
            st.metric("Wins", stats["wins"])

        with col4:
            st.metric("Podiums", stats["podiums"])
            st.metric("Pole Positions", stats["poles"])

        with col5:
            st.metric("Total Points", stats["total_points"])
            st.metric("Seasons Active", stats["seasons_active"])
        current_year = datetime.datetime.now().year
        last_season = int(stats["last_season"])

        if last_season == current_year:
            active_str = f"{stats['first_season']} — {last_season}*"
            st.caption(f"Active: {active_str}")
            st.caption("* Currently active in F1")
        else:
            st.caption(f"Active: {stats['first_season']} — {stats['last_season']}")

        with col6:
            st.metric("🏆 Championships", championships)
            st.metric("Fastest Laps", stats["fastest_laps"])
        
        st.divider()
        st.subheader("📈 Season Performance")

        with st.spinner("Loading season data..."):
            season_stats = get_driver_season_stats(
                driver.get("driverId"),
                stats["first_season"],
                stats["last_season"]
            )

            if season_stats:
                col_chart1, col_chart2 = st.columns(2)

                with col_chart1:
                    st.plotly_chart(
                        points_per_season_chart(season_stats),
                        width="stretch"
                    )

                with col_chart2:
                    st.plotly_chart(
                        wins_per_season_chart(season_stats),
                        width="stretch"
                    )
    else:
        st.warning(f"Found {len(matches)} drivers matching **'{driver_name}'**. Please be more specific:")
        for match in matches:
            given = match.get("givenName", "")
            family = match.get("familyName", "")
            nationality = match.get("nationality", "")
            st.write(f"• **{given} {family}** — {nationality}")

