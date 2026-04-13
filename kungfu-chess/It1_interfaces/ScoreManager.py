from EventBus import EventBus
from Enums import EventTypes

class ScoreManager:
    def __init__(self):
        self.scores = {'W': 0, 'B': 0}
        self.piece_values = {
            'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0  # King has no value
        }
        event_bus = EventBus()
        event_bus.subscribe(EventTypes.PIECE_CAPTURED, self.on_piece_captured)

    def on_piece_captured(self, data):
        piece_id = data['piece']
        piece_type = piece_id[0]
        color = piece_id[1]
        capturer_color = 'W' if color == 'B' else 'B'
        value = self.piece_values.get(piece_type.upper(), 0)
        self.scores[capturer_color] += value
        print(f"Score updated: {self.scores}")

    def get_scores(self):
        return self.scores
