import requests
import streamlit as st
import datetime

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


@st.cache_data
def get_driver_stats(driver_id):
    """
    Fetch all race results for a driver and calculate career stats.
    Uses pagination to get all results.
    """
    all_results = []
    limit = 100
    offset = 0

    while True:
        url = f"{BASE_URL}/drivers/{driver_id}/results/"
        params = {"limit": limit, "offset": offset}
        response = requests.get(url, params=params)

        if response.status_code != 200:
            break

        data = response.json()
        mrdata = data["MRData"]
        races = mrdata["RaceTable"]["Races"]
        total = int(mrdata["total"])

        all_results.extend(races)

        if len(all_results) >= total:
            break

        offset += limit

    # Now calculate stats from all results
    total_races = len(all_results)
    wins = 0
    podiums = 0
    poles = 0
    fastest_laps = 0
    total_points = 0
    seasons = set()  # set automatically removes duplicates

    for race in all_results:
        result = race["Results"][0]  # each race has a Results list, we want [0]
        
        position = result.get("position", "0")
        grid = result.get("grid", "0")
        points = float(result.get("points", "0"))
        season = race.get("season", "")

        if position == "1":
            wins += 1
        if position in ["1", "2", "3"]:
            podiums += 1
        if grid == "1":
            poles += 1

        fastest_lap_rank = result.get("FastestLap", {}).get("rank", "0")
        if fastest_lap_rank == "1":
            fastest_laps += 1

        total_points += points
        seasons.add(season)

    return {
        "total_races": total_races,
        "wins": wins,
        "podiums": podiums,
        "poles": poles,
        "total_points": total_points,
        "fastest_laps": fastest_laps,  
        "seasons_active": len(seasons),
        "first_season": min(seasons),
        "last_season": max(seasons)
    }

@st.cache_data
def get_driver_championships(driver_id, first_season, last_season):
    """
    Count how many championships a driver won by checking
    each season's final standing.
    """
    championships = 0
    current_year = datetime.datetime.now().year

    for year in range(int(first_season), int(last_season) + 1):
        # Don't check current year — season isn't finished
        if year == current_year:
            continue

        url = f"{BASE_URL}/{year}/drivers/{driver_id}/driverStandings/"
        response = requests.get(url, params={"limit": 1})

        if response.status_code != 200:
            continue

        data = response.json()
        standings = data["MRData"]["StandingsTable"]["StandingsLists"]

        if not standings:
            continue

        position = standings[0]["DriverStandings"][0].get("position", "0")

        if position == "1":
            championships += 1

    return championships


@st.cache_data
def get_driver_season_stats(driver_id, first_season, last_season):
    """
    Get points and wins for each season a driver competed in.
    Returns a list of dicts, one per season.
    """
    season_stats = []
    current_year = datetime.datetime.now().year

    for year in range(int(first_season), int(last_season) + 1):
        url = f"{BASE_URL}/{year}/drivers/{driver_id}/driverStandings/"
        response = requests.get(url, params={"limit": 1})

        if response.status_code != 200:
            continue

        data = response.json()
        standings = data["MRData"]["StandingsTable"]["StandingsLists"]

        if not standings:
            continue

        standing = standings[0]["DriverStandings"][0]

        season_stats.append({
            "season": int(year),
            "points": float(standing.get("points", 0)),
            "wins": int(standing.get("wins", 0)),
            "position": int(standing.get("position", 0))
        })

    return season_stats