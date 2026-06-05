class MemoryAgent:
    def __init__(self):
        self.history = []
        self.known_entities = {"names": set(), "places": set(), "events": set()}

    def update_history(self, user_input, response):
        self.history.append({"user": user_input, "assistant": response})

    def update_entities(self, entities):
        for key in self.known_entities:
            self.known_entities[key].update(entities.get(key, []))

    def get_context(self):
        recent_history = self.history[-3:]  # last 3 interactions
        return recent_history, self.known_entities

    def get_memory_timeline(self):
        timeline = []

        for i, item in enumerate(self.history):
            timeline.append(f"Step {i+1}: {item['user']}")

        return timeline
