import re
import dateparser

# Extract amenities from user input (basic keyword matching)
def extract_amenities(user_input, known_amenities=None):
    if not known_amenities:
        known_amenities = ["WiFi", "Pool", "Breakfast", "Parking", "Spa", "Sea View", "Gym"]

    extracted = []
    for amenity in known_amenities:
        pattern = re.compile(rf'\b{amenity}\b', re.IGNORECASE)
        if pattern.search(user_input):
            extracted.append(amenity)

    return extracted

# Parse date strings into YYYY-MM-DD format
def parse_date(date_str):
    parsed = dateparser.parse(date_str)
    if parsed:
        return parsed.strftime('%Y-%m-%d')
    return None

# Check if all required slots are present
def validate_slots(slots, required_keys):
    missing = [key for key in required_keys if key not in slots or not slots[key]]
    return missing

# Capitalize hotel names properly
def normalize_hotel_name(name):
    return ' '.join([word.capitalize() for word in name.strip().split()])

# Format hotel info nicely
def format_hotel(hotel):
    return (f"{hotel['name']} - ₹{hotel['price']} per night - {hotel['stars']}★\n"
            f"Amenities: {', '.join(hotel['amenities'])}")

