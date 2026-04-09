import pathlib
from typing import Dict, Tuple, Optional
from Piece import Piece
import csv
import copy
from Board import Board


class PieceFactory:
    def __init__(self,pieces_root: pathlib.Path, board_layout_csv: pathlib.Path,pos_to_piece: Optional[Dict[Tuple[int, int], Piece]], board: Board):
        self.pieces_root = pieces_root
        self.board = board
        self._templates: Dict[str, Piece] = {}
        self._load_pieces_from_csv(board_layout_csv, pos_to_piece)


    def create_piece(self, p_type: str, cell: Tuple[int, int]) -> Piece:
        if p_type not in self._templates:
            piece_dir = self.pieces_root / p_type
            template = Piece(p_type, piece_dir, self.board)
            self._templates[p_type] = template

        piece_copy = copy.deepcopy(self._templates[p_type])
        piece_copy._cell = cell
        return piece_copy

    def _load_pieces_from_csv(self, board_layout_csv: pathlib.Path, pos_to_piece: Optional[Dict[Tuple[int, int], Piece]]):
        with board_layout_csv.open() as board_layout:
            reader = csv.reader(board_layout)
            for row_idx, row in enumerate(reader):
                for col_idx, code in enumerate(row):
                    code = code.strip()
                    if not code:
                        continue
                    cell = (row_idx, col_idx)
                    piece = self.create_piece(code, cell)
                    pos_to_piece[cell] = piece



