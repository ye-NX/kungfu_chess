from EventBus import EventBus
from Enums import EventTypes

class MoveLogger:
    def __init__(self):
        self.moves = []
        event_bus = EventBus()
        event_bus.subscribe(EventTypes.MOVE_MADE, self.on_move_made)

    def on_move_made(self, data):
        src = data['src']
        dst = data['dst']
        piece = data['piece']
        move_str = f"{piece} from {src} to {dst}"
        self.moves.append(move_str)
        print(f"Move logged: {move_str}")

    def get_moves(self):
        return self.moves
