from EventBus import EventBus
from Enums import EventTypes

class AnimationManager:
    def __init__(self):
        event_bus = EventBus()
        event_bus.subscribe(EventTypes.GAME_STARTED, self.on_game_started)
        event_bus.subscribe(EventTypes.GAME_ENDED, self.on_game_ended)

    def on_game_started(self, data):
        print("Starting game animation")
        # Add animation logic, e.g., display start screen

    def on_game_ended(self, data):
        winner = data.get('winner')
        print(f"Ending game animation for winner: {winner}")
        # Add animation logic, e.g., display winner screen
