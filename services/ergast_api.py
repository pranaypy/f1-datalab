import requests

BASE_URL = "https://api.jolpi.ca/ergast/f1"

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

