import re


def extract_entities(text: str):
    entities = {"names": [], "places": [], "dates": [], "events": []}

    # Names (better heuristic)
    entities["names"] = list(set(re.findall(r"\b[A-Z][a-z]{2,}\b", text)))

    # Dates
    entities["dates"] = re.findall(r"\b\d{4}\b", text)

    # Places
    place_keywords = ["park", "hospital", "school", "home", "market", "hall", "wedding"]
    entities["places"] = [p for p in place_keywords if p in text.lower()]

    # Events
    event_keywords = ["wedding", "birthday", "meeting", "ceremony"]
    entities["events"] = [e for e in event_keywords if e in text.lower()]

    return entities
