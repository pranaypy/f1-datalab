import streamlit as st

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

# --- Temporary output to test input works ---
if driver_name:
    st.write(f"You searched for: **{driver_name}**")