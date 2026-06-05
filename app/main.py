import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ergast_api import search_drivers

# --- Page Configuration ---
st.set_page_config(
    page_title="DataLab.F1",
    page_icon="🏎️",
    layout="wide"
)

# --- Header ---
st.title("🏎️ Formula 1 DataLab")
st.subheader("Formula 1 Driver Statistics and Analytics")

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

    else:
        st.warning(f"Found {len(matches)} drivers matching **'{driver_name}'**. Please be more specific:")
        for match in matches:
            given = match.get("givenName", "")
            family = match.get("familyName", "")
            nationality = match.get("nationality", "")
            st.write(f"• **{given} {family}** — {nationality}")

