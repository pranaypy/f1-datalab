import requests
import streamlit as st

BASE_URL = "https://api.jolpi.ca/ergast/f1"

@st.cache_data  
def get_driver(driver_id):
    """
    Fetch driver information by driver ID.
    
    Args:
        driver_id (str): The unique identifier for the driver (e.g. 'hamilton').
    
    Returns:
        dict: A dictionary containing driver information, or None if not found.
    """
    url = f"{BASE_URL}/drivers/{driver_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        # Navigate the nested JSON to get driver info
        drivers = data["MRData"]["DriverTable"]["Drivers"]
        if drivers:
            return drivers[0]  # Return the first (and only) driver in the list
        else:
            return None  # No driver found
        
    else: 
        return None  # Handle errors or non-200 responses gracefully    

@st.cache_data
def search_driver_by_name(full_name):
    """
    Search for a driver by their full name.
    Returns the matching driver dict or None.
    """
    all_drivers = []
    limit = 100
    offset = 0

    while True:
        url = f"{BASE_URL}/drivers/"
        # API returns max 30 by default — we need all drivers ever
        params = {"limit": limit, "offset": offset}
        response = requests.get(url, params=params)

        if response.status_code != 200:
            break

        data = response.json()
        mrdata = data["MRData"]
        drivers = mrdata["DriverTable"]["Drivers"]
        total = int(mrdata["total"])

        all_drivers.extend(drivers)

            # Check if we've fetched all drivers
        if len(all_drivers) >= total:
            break

        offset += limit

    limit = 1000
    params = {"limit": limit}
    url = f"{BASE_URL}/drivers/"
    response = requests.get(url, params=params)
 
    print(f"Total drivers fetched: {len(all_drivers)}")

    if response.status_code == 200:
        # Search through all drivers for a name match
        full_name_lower = full_name.lower()
        print(f"Searching for: '{full_name_lower}'")
        
        for driver in all_drivers:
            given = driver.get("givenName", "").lower()
            family = driver.get("familyName", "").lower()
            full_driver_name = f"{given} {family}"

            if "hamilton" in full_driver_name:
                print(f"Found candidate: '{full_driver_name}'")

            if (full_name_lower == full_driver_name):               # full name match
                return driver
                
    return None