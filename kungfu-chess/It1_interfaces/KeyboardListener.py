from typing import Tuple

from Enums import StateTypes as Types
import threading
import keyboard
import time
from Board import Board
from Command import Command
from CommandProcessor import CommandProcessor



class KeyboardListener:
    blue_stop_event = threading.Event()
    green_stop_event = threading.Event()

    @staticmethod
    def start_blue_listener(board: Board, game_start_time, command_processor: CommandProcessor, pos_to_piece: dict):
        def blue_loop():
            while not KeyboardListener.blue_stop_event.is_set():
                new_row, new_col = board.blue_focus_cell
                if keyboard.is_pressed('w'):
                    new_row -= 1
                elif keyboard.is_pressed('s'):
                    new_row += 1
                elif keyboard.is_pressed('a'):
                    new_col -= 1
                elif keyboard.is_pressed('d'):
                    new_col += 1
                elif keyboard.is_pressed(' '):
                    piece = pos_to_piece.get(board.blue_select_cell)
                    if board.blue_select_cell is not None and piece and piece.id.endswith('W'):
                        next_state = KeyboardListener.next_state_for_command(board.blue_select_cell, board.blue_focus_cell)
                        timestamp = int((time.monotonic() - game_start_time) * 1000)
                        cmd = Command(timestamp, next_state, board.blue_select_cell, board.blue_focus_cell)
                        command_processor.add_command(cmd)
                    board.blue_select_cell = board.blue_focus_cell
                time.sleep(0.13)
                if board.is_valid_cell((new_row, new_col)):
                    board.blue_focus_cell = (new_row, new_col)
        threading.Thread(target=blue_loop, daemon=True).start()

    @staticmethod
    def stop_blue_listener():
        KeyboardListener.blue_stop_event.set()

    @staticmethod
    def start_green_listener(board: Board, game_start_time, command_processor: CommandProcessor, pos_to_piece: dict):
        def green_loop():
            while not KeyboardListener.green_stop_event.is_set():
                new_row, new_col = board.green_focus_cell
                if keyboard.is_pressed('up'):
                    new_row -= 1
                elif keyboard.is_pressed('down'):
                    new_row += 1
                elif keyboard.is_pressed('left'):
                    new_col -= 1
                elif keyboard.is_pressed('right'):
                    new_col += 1
                elif keyboard.is_pressed('return'):
                    piece = pos_to_piece.get(board.green_select_cell)
                    if board.green_select_cell is not None and piece and piece.id.endswith('B'):
                        next_state = KeyboardListener.next_state_for_command(board.green_select_cell, board.green_focus_cell)
                        timestamp = int((time.monotonic() - game_start_time) * 1000)
                        cmd = Command(timestamp, next_state, board.green_select_cell, board.green_focus_cell)
                        command_processor.add_command(cmd)
                    board.green_select_cell = board.green_focus_cell
                time.sleep(0.13)
                if board.is_valid_cell((new_row, new_col)):
                    board.green_focus_cell = (new_row, new_col)
        threading.Thread(target=green_loop, daemon=True).start()

    @staticmethod
    def stop_green_listener():
        KeyboardListener.green_stop_event.set()

    @staticmethod
    def next_state_for_command(select_cell: Tuple[int, int], focus_cell: Tuple[int, int]) -> Types:
        if select_cell == focus_cell:
            return Types.JUMP
        return Types.MOVE
