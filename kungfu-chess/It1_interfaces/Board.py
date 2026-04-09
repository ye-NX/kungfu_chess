from dataclasses import dataclass
import copy
from typing import Tuple, Optional
from img import Img

@dataclass
class Board:
    cell_H_pix: int
    cell_W_pix: int
    cell_H_m: int
    cell_W_m: int
    W_cells: int
    H_cells: int
    img: Img
    green_focus_img: Img
    blue_focus_img: Img
    green_focus_cell: Tuple[int, int]
    blue_focus_cell: Tuple[int, int]
    green_select_img: Img
    blue_select_img: Img
    green_select_cell: Optional[Tuple[int, int]] = None
    blue_select_cell: Optional[Tuple[int, int]] = None

    def clone(self) -> "Board":
        return Board(
            cell_H_pix=self.cell_H_pix,
            cell_W_pix=self.cell_W_pix,
            cell_H_m=self.cell_H_m,
            cell_W_m=self.cell_W_m,
            W_cells=self.W_cells,
            H_cells=self.H_cells,
            img=copy.deepcopy(self.img),
            green_focus_img=copy.deepcopy(self.green_focus_img),
            blue_focus_img=copy.deepcopy(self.blue_focus_img),
            green_focus_cell=self.green_focus_cell,
            blue_focus_cell=self.blue_focus_cell,
            green_select_img=copy.deepcopy(self.green_select_img),
            blue_select_img=copy.deepcopy(self.blue_select_img),
            green_select_cell=self.green_select_cell,
            blue_select_cell=self.blue_select_cell,
        )

    def cell_to_graphic_pos(self, cell: tuple[int, int]) -> tuple[int, int]:
        """Converts from physical measurements to graphical measurements"""
        row, col = cell
        x = col * self.cell_W_pix
        y = row * self.cell_H_pix
        return x, y

    def graphic_pos_to_cell(self, pos: Tuple[float, float]) -> Tuple[int, int]:
        """Converts from graphical measurements to physical measurements"""
        x, y = pos
        col = int(x // self.cell_W_pix)
        row = int(y // self.cell_H_pix)
        return row, col

    def is_valid_cell(self, cell: Tuple[int,int]) -> bool:
        col, row=cell
        if col>self.W_cells-1 or col<0:
            return False
        if row>self.H_cells-1 or row<0:
            return False
        return True
