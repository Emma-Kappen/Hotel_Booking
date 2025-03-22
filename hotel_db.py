import json
import os

# Load hotel data from JSON
def load_hotels(file_path="data/hotels.json"):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Hotel data not found at {file_path}")
    
    with open(file_path, 'r') as f:
        hotels = json.load(f)
    return hotels

# Search hotels by filters
def find_hotels(location=None, max_price=None, min_stars=None, required_amenities=None):
    hotels = load_hotels()
    results = []

    for hotel in hotels:
        if location and hotel['location'].lower() != location.lower():
            continue
        if max_price and hotel['price'] > max_price:
            continue
        if min_stars and hotel['stars'] < min_stars:
            continue
        if required_amenities:
            if not all(amenity.lower() in map(str.lower, hotel.get('amenities', [])) for amenity in required_amenities):
                continue
        results.append(hotel)

    return results

# Retrieve hotel by name
def get_hotel_by_name(name):
    hotels = load_hotels()
    for hotel in hotels:
        if hotel['name'].lower() == name.lower():
            return hotel
    return None

