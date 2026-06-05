import requests
import streamlit as st

BASE_URL = "https://api.jolpi.ca/ergast/f1"

@st.cache_data
def get_all_drivers():
    """
    Fetch all F1 drivers ever. Cached so API is only called once.
    """
    all_drivers = []
    limit = 100
    offset = 0

    while True:
        url = f"{BASE_URL}/drivers/"
        params = {"limit": limit, "offset": offset}
        response = requests.get(url, params=params)

        if response.status_code != 200:
            break

        data = response.json()
        mrdata = data["MRData"]
        drivers = mrdata["DriverTable"]["Drivers"]
        total = int(mrdata["total"])

        all_drivers.extend(drivers)

        if len(all_drivers) >= total:
            break

        offset += limit

    return all_drivers


def search_drivers(query):
    """
    Search for drivers by name query.
    Returns a list of all matching drivers.
    """
    all_drivers = get_all_drivers()
    query_lower = query.lower()
    matches = []

    for driver in all_drivers:
        given = driver.get("givenName", "").lower()
        family = driver.get("familyName", "").lower()
        full_driver_name = f"{given} {family}"

        if (query_lower == full_driver_name or    # exact full name
            query_lower == family or              # exact last name
            query_lower == given or               # exact first name
            query_lower in full_driver_name):     # partial match
            matches.append(driver)

    return matches


