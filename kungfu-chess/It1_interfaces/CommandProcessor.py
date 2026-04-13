from typing import List, Tuple
from Command import Command
from Enums import StateTypes as Types
from Board import Board
from EventBus import EventBus
from Enums import EventTypes

class CommandProcessor:

    def __init__(self, board: Board, pos_to_piece: dict, event_bus: EventBus):
        self._queue: List[Command] = []
        self.board = board
        self._pos_to_piece = pos_to_piece
        self.event_bus = event_bus


    def empty(self):
        return len(self._queue) == 0

    def add_command(self, cmd: Command):
        self._queue.append(cmd)

    def clear(self):
        while not self.empty():
                cmd = self._queue.pop(0)
                if not self._is_command_possible(cmd):
                    continue

                src_cell = Command.algebraic_to_cell(cmd.params[0])
                dst_cell = Command.algebraic_to_cell(cmd.params[1])
                src_piece = self._pos_to_piece[src_cell]
                del self._pos_to_piece[src_cell]
                
                captured_piece = None
                if dst_cell in self._pos_to_piece:
                    captured_piece = self._pos_to_piece[dst_cell]
                
                self._pos_to_piece[dst_cell] = src_piece
                src_piece.reset(cmd.timestamp, src_cell, cmd.type, dst_cell)

                # Publish events
                self.event_bus.publish(EventTypes.MOVE_MADE, {"src": src_cell, "dst": dst_cell, "piece": src_piece.id})
                if captured_piece:
                    self.event_bus.publish(EventTypes.PIECE_CAPTURED, {"piece": captured_piece.id, "position": dst_cell})

                #if the is piece at dst cell, the function game.solve_collision will solve it


    #things to check by the right order:
        #if the dish at the src cell isn't idle now return false
        #if the src piece it's eaten already return false
        #if the action is MOVE:
            #if at this cell there is my dish return false
            #if the dish at the src cell can't do that move return false
            #if it's not horse and the way isn't clear return false
        #if the action is JUMP:

    #when I return false, if the dst is with my dish change the select cell on dst, else don't do anything

    def _is_command_possible(self, cmd: Command) -> bool:
        src_cell = Command.algebraic_to_cell(cmd.params[0])
        dst_cell = Command.algebraic_to_cell(cmd.params[1])

        src_piece = self._pos_to_piece[src_cell]

        #check if current piece state is IDLE
        if src_piece.state.state_type != Types.IDLE:
            return False

        # check if the src is still exist
        if src_piece is None:
            return False

        if cmd.type == Types.MOVE:
            # check if there is no piece in the same color at dst
            if dst_cell in self._pos_to_piece:
                dst_piece = self._pos_to_piece[dst_cell]
                if dst_piece.id[1] == src_piece.id[1]:
                    return False

            # check if the movement is fit to the piece type
            # EDGE CASE WRONG! for p at the first move, it can move 2 cells forward
            legal = src_piece.moves.get_moves(*src_cell)
            if dst_cell not in legal:
                return False

            # check if the way is clear (except of Knight)
            if src_piece.id[0] != "N":
                if not self._is_path_clear(src_cell, dst_cell):
                    return False

        return True


    def _is_path_clear(self, src: Tuple[int, int], dst: Tuple[int, int]) -> bool:
        row1, col1 = src
        row2, col2 = dst
        d_row = row2 - row1
        d_col = col2 - col1

        step_row = (d_row > 0) - (d_row < 0)
        step_col = (d_col > 0) - (d_col < 0)

        r, c = row1 + step_row, col1 + step_col
        while (r, c) != (row2, col2):
            if (r, c) in self._pos_to_piece:
                return False
            r += step_row
            c += step_col
        return True
