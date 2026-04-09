from typing import List, Tuple
from Enums import StateTypes as Types


class Command:
    timestamp: int  # ms since game start
    type: Types  # "Move" | "Jump" | …
    params: List[str]  # payload (e.g. ["e2", "e4"])

    def __init__(self, timestamp: int, next_state: Types, src_cell: Tuple[int, int], dst_cell: Tuple[int, int]):
        """initialize a command when the player choose a piece for an action"""
        self.timestamp = timestamp
        self.type = next_state

        self.params = [
            self.cell_to_algebraic(src_cell),
            self.cell_to_algebraic(dst_cell),
        ]

    @staticmethod
    def algebraic_to_cell(notation: str) -> Tuple[int, int]:
        """
        Converts algebraic notation (e.g., "a1") to board coordinates.
        Example: "a1" -> (7, 0) if (0,0) is top-left
        """
        col = ord(notation[0].lower()) - ord('a')
        row = 8 - int(notation[1])  # Assuming board is 8x8
        return row, col

    @staticmethod
    def cell_to_algebraic(cell: Tuple[int, int]) -> str:
        """
        Converts board coordinates to algebraic notation.
        Example: (7, 0) -> "a1" if (0,0) is top-left
        """
        row, col = cell
        file = chr(ord('a') + col)
        rank = str(8 - row)
        return file + rank
