import re
import dateparser
from transformers import pipeline

# Load Hugging Face pipelines for zero-shot classification and NER
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
ner_tagger = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")

# Define intents and relevant keywords (used for classification)
INTENTS = {
    "book_hotel": "I want to book a hotel room",
    "get_info": "I want information about a hotel",
    "cancel_booking": "I want to cancel a booking",
}

# Intent Recognition
def identify_intent(user_input):
    candidate_labels = list(INTENTS.keys())
    hypothesis_template = "The user wants to {}."
    
    result = classifier(user_input, candidate_labels, hypothesis_template=hypothesis_template)
    intent = result['labels'][0] if result['scores'][0] > 0.5 else "unknown"
    return intent

# Slot Extraction
def extract_slots(user_input, intent):
    slots = {}
    ner_results = ner_tagger(user_input)

    for entity in ner_results:
        label = entity['entity_group']
        word = entity['word']

        if label == "LOC":  # Location
            slots['location'] = word

        elif label == "DATE":  # Date
            parsed_date = dateparser.parse(word)
            if parsed_date:
                date_str = parsed_date.strftime('%Y-%m-%d')
                if "dates" not in slots:
                    slots["dates"] = []
                slots["dates"].append(date_str)

    # Budget detection (₹, $, or plain numbers)
    budget_match = re.search(r'(₹|\$)?\s?(\d{3,5})', user_input)
    if budget_match:
        slots["budget"] = int(budget_match.group(2))

    # Hotel Name (if user asks for info about a specific hotel)
    if intent == "get_info":
        name_match = re.search(r'about\s+([A-Z][a-zA-Z\s]+)', user_input)
        if name_match:
            slots["hotel_name"] = name_match.group(1).strip()

    return slots

# Main Parser Function
def parse_input(user_input):
    intent = identify_intent(user_input)
    slots = extract_slots(user_input, intent)
    return intent, slots

# Test the parser
if __name__ == "__main__":
    sample_input = "I want to book a hotel in Goa for 3 nights from April 10 under ₹2000"
    intent, slots = parse_input(sample_input)
    print("Intent:", intent)
    print("Slots:", slots)

