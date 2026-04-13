from enum import Enum
class StateTypes(Enum):
    IDLE = "idle"
    MOVE = "move"
    JUMP = "jump"
    LONG_REST = "long_rest"
    SHORT_REST = "short_rest"

class EventTypes(Enum):
    GAME_STARTED = "game_started"
    GAME_ENDED = "game_ended"
    MOVE_MADE = "move_made"
    PIECE_CAPTURED = "piece_captured"
