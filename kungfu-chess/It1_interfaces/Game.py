import time
from pathlib import Path
from typing import Dict, Tuple, Optional
from Board import Board
from Piece import Piece
from PieceFactory import PieceFactory
from KeyboardListener import KeyboardListener
from CommandProcessor import CommandProcessor
import cv2
from img import Img


class Game:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Game, cls).__new__(cls)
        return cls._instance

    def __init__(self, board: Board):
        if hasattr(self, '_initialized') and self._initialized:
            return
        base_path = Path(__file__).resolve().parent
        pieces_root = base_path.parent / "pieces"
        board_layout_csv = base_path.parent / "board.csv"

        self._initialized = True
        self.board = board
        self.start_time = time.monotonic()
        self.pos_to_piece: Dict[Tuple[int, int], Piece] = {}
        self.piece_factory = PieceFactory(pieces_root, board_layout_csv, self.pos_to_piece, board)
        self.command_processor = CommandProcessor(board, self.pos_to_piece)

    @staticmethod
    def get_instance() -> "Game":
        if Game._instance is None:
            board = Board(
                cell_H_pix=80,cell_W_pix=80,cell_H_m=1,cell_W_m=1,W_cells=8,H_cells=8,
                img=Img().read("../board.png", size=(640, 640)),
                green_focus_img=Img().read("../green_focus_cell.png", size=(80, 80)),
                blue_focus_img=Img().read("../blue_focus_cell.png", size=(80, 80)),
                green_focus_cell=(0, 0),blue_focus_cell=(7, 7),
                green_select_img=Img().read("../green_select_cell.png", size=(80, 80)),
                blue_select_img=Img().read("../blue_select_cell.png", size=(80, 80)),
            )
            Game(board)
        return Game._instance

    def game_time_ms(self) -> int:
        return int((time.monotonic() - self.start_time) * 1000)

    def clone_board(self) -> Board:
        return self.board.clone()

    def run(self):

        for pos, piece in self.pos_to_piece.items():
            piece.reset(self.start_time, pos)

        KeyboardListener.start_blue_listener(self.board, self.start_time, self.command_processor, self.pos_to_piece)
        KeyboardListener.start_green_listener(self.board, self.start_time, self.command_processor, self.pos_to_piece)

        while not self._is_win():

            now = self.game_time_ms()

            self.command_processor.clear()

            for piece in self.pos_to_piece.values():
                piece.update(now)

            self._draw()

            if not self._show():
                break

            # self._resolve_collisions()

        KeyboardListener.stop_blue_listener()
        KeyboardListener.stop_green_listener()
        self._announce_win()
        cv2.destroyAllWindows()

    def _show(self) -> bool:
        cv2.imshow("Chess", self._current_board.img.img)
        key = cv2.waitKey(30)
        return key != 27  # ESC = quit

    def _draw(self):
        board = self.clone_board()
        now_ms = self.game_time_ms()

        for piece in self.pos_to_piece.values():
            piece.draw_on_board(board, now_ms)

        blue_focus_x, blue_focus_y=board.cell_to_graphic_pos(board.blue_focus_cell)
        green_focus_x, green_focus_y=board.cell_to_graphic_pos(board.green_focus_cell)
        board.blue_focus_img.draw_on(board.img, blue_focus_x, blue_focus_y)
        board.green_focus_img.draw_on(board.img, green_focus_x, green_focus_y)

        if board.blue_select_cell:
            blue_select_x, blue_select_y=board.cell_to_graphic_pos(board.blue_select_cell)
            board.blue_select_img.draw_on(board.img, blue_select_x, blue_select_y)
        if board.green_select_cell:
            green_select_x, green_select_y=board.cell_to_graphic_pos(board.green_select_cell)
            board.green_select_img.draw_on(board.img, green_select_x, green_select_y)

        self._current_board = board


    def _is_win(self) -> bool:
        kings = [p for p in self.pos_to_piece.values() if p.id.lower().startswith("k")]
        return len(kings) <= 1

    def _announce_win(self):
        if len(self.pos_to_piece) == 0:
            print("Draw.")
        elif len(self.pos_to_piece) == 1:
            print(f"{list(self.pos_to_piece.values())[0].id()} wins!")
        else:
            print("Game over.")

    def remove_piece(self, cell: Tuple[int, int]):
        self.pos_to_piece.pop(cell, None)

    def move_piece(self, src: Tuple[int, int], dst: Tuple[int, int]):
        piece = self.pos_to_piece[src]
        self.pos_to_piece[dst] = piece
