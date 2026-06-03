import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ergast_api import get_driver, search_driver_by_name

# --- Page Configuration ---
st.set_page_config(
    page_title="F1 DataLab",
    page_icon="🏎️",
    layout="wide"
)

# --- Header ---
st.title("🏎️ F1 DataLab")
st.subheader("Formula 1 Driver Statistics and Analytics")

# --- Divider ---
st.divider()

# --- Search Box ---
st.subheader("🔍 Search for a Driver")
driver_name = st.text_input("Enter driver name (e.g. Lewis Hamilton)")

 
if driver_name:
    with st.spinner("Searching..."):
        driver = search_driver_by_name(driver_name)


    if driver:
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
        st.error("Driver not found. Try: hamilton, verstappen, leclerc")

