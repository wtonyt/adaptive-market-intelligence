class NarrativeMemory:

    def __init__(self):

        self.memory = []

    def store_event(
        self,
        event
    ):

        self.memory.append(event)

        # Prevent unbounded growth
        self.memory = self.memory[-100:]

    def summarize(self):

        themes = {}

        for event in self.memory:

            event_type = (
                event.get(
                    "event_type",
                    "UNKNOWN"
                )
            )

            themes[event_type] = (
                themes.get(
                    event_type,
                    0
                ) + 1
            )

    
        return themes
    
    def get_summary(self):

        return self.summarize()