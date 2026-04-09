import pathlib
from typing import List, Tuple
class Moves:
    def __init__(self, txt_path: pathlib.Path):
        """Initialize moves with rules from text file and board dimensions."""
        self._rules = []
        try:
            with txt_path.open('r') as file:
                for line in file:
                    # Parse each line as a tuple of integers (e.g., "1,2" -> (1, 2))
                    parts = line.strip().split(',')
                    if len(parts) != 2:
                        raise ValueError(f"Invalid format on line: {line}")
                    self._rules.append((int(parts[0]), int(parts[1])))
        except Exception as e:
            raise ValueError(f"Error loading rules from {self.txt_path}: {e}")

    def get_moves(self, r: int, c: int) -> List[Tuple[int, int]]:
        """Get all possible moves from a given position."""
        possible_moves = []
        for dr, dc in self._rules:
            new_cell = r + dr, c + dc
            possible_moves.append(new_cell)
        return possible_moves


