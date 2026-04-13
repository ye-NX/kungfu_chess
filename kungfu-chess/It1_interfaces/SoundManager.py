import pygame

pygame.mixer.init()

from EventBus import EventBus
from Enums import EventTypes

class SoundManager:
    def __init__(self):
        self.sounds = {}
        # Load sounds here, but since no files, just placeholders
        event_bus = EventBus()
        event_bus.subscribe(EventTypes.MOVE_MADE, self.on_move_made)
        event_bus.subscribe(EventTypes.PIECE_CAPTURED, self.on_piece_captured)
        event_bus.subscribe(EventTypes.GAME_STARTED, self.on_game_started)
        event_bus.subscribe(EventTypes.GAME_ENDED, self.on_game_ended)

    def on_move_made(self, data):
        print("Playing move sound")
        pygame.mixer.Sound('../sound_files/move.wav').play()

    def on_piece_captured(self, data):
        print("Playing capture sound")
        pygame.mixer.Sound('../sound_files/capture.wav').play()

    def on_game_started(self, data):
        print("Playing start sound")
        pygame.mixer.Sound('../sound_files/start.wav').play()

    def on_game_ended(self, data):
        print("Playing end sound")
        pygame.mixer.Sound('../sound_files/end.wav').play()
