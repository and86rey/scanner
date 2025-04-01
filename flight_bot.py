import requests
import os
from datetime import datetime, timedelta
import json

# API setup (Skyscanner via RapidAPI)
API_KEY = os.getenv('RAPIDAPI_KEY')  # Stored in GitHub Secrets
HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com"
}
BASE_URL = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browseroutes/v1.0/DE/EUR/en-DE/"

# EU airport codes (simplified list - expand as needed)
EU_AIRPORTS = ["AMS", "ARN", "ATH", "BCN", "BRU", "BUD", "CDG", "CPH", "DUB", "FRA", "HEL", "LIS", "LHR", "MAD", "MUC", "OSL", "PRG", "RIX", "SOF", "VIE", "WAW", "ZRH"]

# Conditions
ORIGIN = "BER"
MAX_PRICE = 100  # EUR
MIN_GAP = 5  # Hours between arrival and return departure

def get_flight_offers(date):
    results = []
    date_str = date.strftime("%Y-%m-%d")
    
    # API call for round-trip flights (same day)
    url = f"{BASE_URL}{ORIGIN}-sky/anywhere/{date_str}/{date_str}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"API error for {date_str}: {response.status_code}")
        return results
    
    data = response.json()
    quotes = data.get("Quotes", [])
    places = {p["PlaceId"]: p["IataCode"] for p in data.get("Places", [])}
    
    for quote in quotes:
        price = quote.get("MinPrice", float("inf"))
        if price > MAX_PRICE or not quote.get("Direct"):
            continue  # Skip expensive or non-direct flights
        
        outbound = quote.get("OutboundLeg", {})
        inbound = quote.get("InboundLeg", {})
        dest_id = outbound.get("DestinationId")
        dest_airport = places.get(dest_id)
        
        # Filter for EU destinations
        if dest_airport not in EU_AIRPORTS:
            continue
        
        # Time parsing (assumes API returns times - mock if not)
        out_depart = outbound.get("DepartureDate")  # API may not provide time
        in_depart = inbound.get("DepartureDate")    # Placeholder - needs time data
        
        # Mock times for now (API lacks detailed times in this endpoint)
        out_arrival = datetime.strptime(out_depart, "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=2)  # Assume 2h flight
        in_departure = datetime.strptime(in_depart, "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=4)  # Assume later return
        
        gap = (in_departure - out_arrival).total_seconds() / 3600
        if gap < MIN_GAP:
            continue
        
        results.append({
            "date": date_str,
            "outbound_departure": out_depart,
            "destination": dest_airport,
            "inbound_departure": in_depart,
            "price": price
        })
    
    return results

def main():
    # Check tomorrow to 6 months ahead
    start_date = datetime.now() + timedelta(days=1)
    end_date = start_date + timedelta(days=180)  # ~6 months
    
    all_results = []
    current_date = start_date
    while current_date <= end_date:
        offers = get_flight_offers(current_date)
        all_results.extend(offers)
        current_date += timedelta(days=1)
    
    # Save to JSON
    with open("flight_offers.json", "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"Found {len(all_results)} offers")

if __name__ == "__main__":
    main()
