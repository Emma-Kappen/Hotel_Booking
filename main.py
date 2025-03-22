from nlp_parser import parse_input
from agent import BookingAgent

def main():
    print("🛎️ Welcome to AI Hotel Booking Agent!")
    print("You can ask me to book hotels, get details, or cancel bookings.")
    print("Example: 'Book a hotel in Goa under 2000 with WiFi'\n")

    agent = BookingAgent()

    while True:
        user_input = input("> ")

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye! Have a great trip! ✈️")
            break

        # If awaiting confirmation for booking
        if agent.awaiting_confirmation:
            response = agent.finalize_booking(user_input)
        else:
            intent, slots = parse_input(user_input)
            response = agent.handle_intent(intent, slots)

        print(response)
        print("-" * 50)

if __name__ == "__main__":
    main()

