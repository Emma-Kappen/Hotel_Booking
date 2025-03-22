import json
import os
import uuid
from datetime import datetime

# Path to store booking data
BOOKING_FILE = "data/bookings.json"

# Ensure bookings file exists
def _init_booking_file():
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(BOOKING_FILE):
        with open(BOOKING_FILE, 'w') as f:
            json.dump([], f)

# Confirm a booking and return booking ID
def confirm_booking(hotel_info):
    _init_booking_file()
    booking_id = str(uuid.uuid4())[:8]  # Short unique ID
    booking_record = {
        "booking_id": booking_id,
        "hotel_name": hotel_info['name'],
        "location": hotel_info['location'],
        "price": hotel_info['price'],
        "stars": hotel_info['stars'],
        "booking_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    with open(BOOKING_FILE, 'r+') as f:
        bookings = json.load(f)
        bookings.append(booking_record)
        f.seek(0)
        json.dump(bookings, f, indent=2)

    return booking_id

# Optional: Retrieve booking by ID
def get_booking_by_id(booking_id):
    _init_booking_file()
    with open(BOOKING_FILE, 'r') as f:
        bookings = json.load(f)
        for booking in bookings:
            if booking['booking_id'] == booking_id:
                return booking
    return None

# Optional: Cancel booking by ID
def cancel_booking(booking_id):
    _init_booking_file()
    with open(BOOKING_FILE, 'r+') as f:
        bookings = json.load(f)
        updated_bookings = [b for b in bookings if b['booking_id'] != booking_id]
        f.seek(0)
        f.truncate()
        json.dump(updated_bookings, f, indent=2)

    return True

