from abc import ABC, abstractmethod
from typing import Tuple
from Command import Command
from Board import Board
from Enums import StateTypes as Types

class Physics(ABC):
    def __init__(self,board: Board, speed_m_s: float = 1.0):
        self._pos = None
        self._start_cell = None
        self._end_cell = None
        self.board = board
        self._speed = speed_m_s * 100 #why is it multiplied by 100?
        self._start_time = 0
        self._duration_ms = 0
        self._finished = False

    @property
    def finished(self):
        return self._finished

    def reset(self, start_time, start_cell: Tuple[int, int],end_cell: Tuple[int, int]):
        self._start_cell = start_cell
        self._pos = self.board.cell_to_graphic_pos(self._start_cell)
        self._start_time = start_time
        if end_cell is not None:
            self._end_cell = end_cell
        else:
            self._end_cell = start_cell
        self._finished = False

    @abstractmethod
    def update(self, now_ms: int):
        self._finished = (now_ms - self._start_time) >= self._duration_ms

    @abstractmethod
    def can_be_captured(self) -> bool:
        pass

    @abstractmethod
    def can_capture(self) -> bool:
        pass

    @property
    def pos(self):
        return self._pos

    @property
    def end_cell(self):
        return self._end_cell

    def get_pos_in_cell(self):
        return self.board.graphic_pos_to_cell(self.pos)


class IdlePhysics(Physics):

    def reset(self,start_time, start_cell: Tuple[int, int],end_cell: Tuple[int, int]):
        super().reset(start_time, start_cell,end_cell)

    def update(self, now_ms: int):
        pass

    def can_be_captured(self) -> bool:
        return True

    def can_capture(self) -> bool:
        return True


class MovePhysics(Physics):
    def __init__(self,board: Board, speed_m_s: float = 1.0):
        super().__init__(board, speed_m_s)

    def reset(self,start_time, start_cell: Tuple[int, int],end_cell: Tuple[int, int]):
        super().reset(start_time, start_cell,end_cell)
        start_pos = self.board.cell_to_graphic_pos(self._start_cell)
        end_pos = self.board.cell_to_graphic_pos(self._end_cell)
        dist = ((end_pos[0] - start_pos[0]) ** 2 +
                (end_pos[1] - start_pos[1]) ** 2) ** 0.5
        self._duration_ms = max(1, int((dist / self._speed) * 1000))

    def update(self, now_ms: int):
        super().update(now_ms)

        if self._start_time is None:
            self._start_time = now_ms

        elapsed = now_ms - self._start_time
        t = min(1.0, elapsed / self._duration_ms)

        start_pos = self.board.cell_to_graphic_pos(self._start_cell)
        end_pos = self.board.cell_to_graphic_pos(self._end_cell)

        self._pos = (
            start_pos[0] + t * (end_pos[0] - start_pos[0]),
            start_pos[1] + t * (end_pos[1] - start_pos[1])
        )

        if t >= 1.0:
            self._finished = True


    def can_be_captured(self) -> bool:
        return False

    def can_capture(self) -> bool:
        return False



class JumpPhysics(Physics):

    def reset(self,start_time, start_cell: Tuple[int, int],end_cell: Tuple[int, int]):
        super().reset(start_time, start_cell,end_cell)
        self._duration_ms = 1500  # 1.5 sec jump duration

    def update(self, now_ms: int):
        super().update(now_ms)

    def can_be_captured(self) -> bool:
        return False

    def can_capture(self) -> bool:
        return False


class ShortRestPhysics(Physics):

    def reset(self,start_time, start_cell: Tuple[int, int],end_cell: Tuple[int, int]):
        super().reset(start_time, start_cell,end_cell)
        self._duration_ms = 1000  # sec

    def update(self, now_ms: int):
        super().update(now_ms)

    def can_be_captured(self) -> bool:
        return True

    def can_capture(self) -> bool:
        return False


class LongRestPhysics(Physics):

    def reset(self,start_time:float, start_cell: Tuple[int, int],end_cell: Tuple[int, int]):
        super().reset(start_time, start_cell,end_cell)
        self._duration_ms = 3000  # 3 sec

    def update(self, now_ms: int):
        super().update(now_ms)

    def can_be_captured(self) -> bool:
        return True

    def can_capture(self) -> bool:
        return False