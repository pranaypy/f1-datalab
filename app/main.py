import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ergast_api import get_driver

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
    name_lst = driver_name.split()
    driver_id = name_lst[1].lower()
    driver = get_driver(driver_id)

    if driver:
        st.success(f"Driver found!")
        col1, col2 = st.columns(2)

        with col1:
            st.metric("First Name", driver["givenName"])
            st.metric("Last Name", driver["familyName"])
            st.metric("Nationality", driver["nationality"])

        with col2:
            st.metric("Driver ID", driver["driverId"])
            st.metric("Number", driver["permanentNumber"])
            st.metric("Code", driver["code"])

    else:
        st.error("Driver not found. Try: hamilton, verstappen, leclerc")

