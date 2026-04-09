from typing import Tuple

from _pytest import pathlib

from GraphicsFactory import GraphicsFactory
from PhysicsFactory import PhysicsFactory
from Enums import StateTypes as Types
from Moves import Moves
from Board import Board

class State:
    def __init__(self, state_type: Types, cfg, board: Board, sprites_dir: pathlib.Path):
        self._state_time=0
        self._state_type = state_type
        self._graphics = GraphicsFactory.create(sprites_dir, cfg, board)
        self._physics = PhysicsFactory.create(state_type, cfg, board)

    @property
    def graphics(self):
        return self._graphics

    @property
    def physics(self):
        return self._physics

    @property
    def state_type(self):
        return self._state_type

    def reset(self,start_time:float,start_cell:Tuple[int,int],end_cell: Tuple[int ,int] = None):
        self._state_time = start_time
        self._graphics.reset(start_time)
        self._physics.reset(start_time, start_cell, end_cell)

    def update(self, now_ms: int):
        self._graphics.update(now_ms)
        self._physics.update(now_ms)

    def can_transition(self, now_ms: int) -> bool:
        return self._physics.update(now_ms) is not None

    @staticmethod
    def from_components(moves: Moves, graphics, physics) -> "State":
        new_state = State.__new__(State)  # Bypass __init__

        new_state._moves = moves
        new_state._graphics = graphics
        new_state._physics = physics
        new_state._transitions = {}

        return new_state


