from hotel_db import find_hotels, get_hotel_by_name
from booking import confirm_booking

class BookingAgent:
    def __init__(self):
        self.pending_hotels = []
        self.awaiting_confirmation = False

    def handle_intent(self, intent, slots):
        if intent == "book_hotel":
            return self._handle_booking(slots)

        elif intent == "get_info":
            return self._handle_info(slots)

        elif intent == "cancel_booking":
            return self._handle_cancellation(slots)

        else:
            return "I'm sorry, I didn't understand that. Could you please rephrase?"

    def _handle_booking(self, slots):
        location = slots.get("location")
        budget = slots.get("budget")
        amenities = slots.get("amenities", [])  # Optional future feature

        if not location or not budget:
            return "Please provide both location and budget to proceed with booking."

        hotels = find_hotels(location=location, max_price=budget)
        if not hotels:
            return f"Sorry, no hotels found in {location} under ₹{budget}."

        self.pending_hotels = hotels
        self.awaiting_confirmation = True

        response = f"Found {len(hotels)} hotel(s) in {location} under ₹{budget}:\n"
        for idx, hotel in enumerate(hotels, 1):
            response += f"{idx}. {hotel['name']} - ₹{hotel['price']} ({hotel['stars']}★)\n"

        response += "\nPlease reply with the hotel number to confirm your booking."
        return response

    def finalize_booking(self, choice_idx):
        if not self.await

