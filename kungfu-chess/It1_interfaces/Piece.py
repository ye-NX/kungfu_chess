from _pytest import pathlib
import time
from State import State
from Moves import Moves
from Board import Board
from PhysicsFactory import PhysicsFactory
from Enums import StateTypes as Types
from Command import Command
import cv2
import json

class Piece:
    nextCode = 0


    def __init__(self, piece_id: str, piece_dir: pathlib.Path, board: Board):
            self._id = piece_id
            self._uniqueNumber = Piece.nextCode
            Piece.nextCode += 1
            self._piece_dir = piece_dir
            self._board = board
            self._transitions = {}
            self.load_transitions()
            self._moves = Moves(piece_dir / "moves.txt")
            self._state = self._transitions[Types.IDLE][1]

    def load_transitions(self):
        states_dir = self._piece_dir / "states"
        for state_folder in states_dir.iterdir():
            if not state_folder.is_dir():
                continue

            try:
                state_type = Types(state_folder.name)
            except ValueError:
                continue

            config_path = state_folder / "config.json"
            sprites_dir = state_folder / "sprites"
            if not config_path.exists():
                continue

            with open(config_path, "r") as f:
                cfg = json.load(f)

            next_state_str = cfg.get("physics", {}).get("next_state_when_finished", "idle")
            next_state_type = Types(next_state_str)

            state = State(state_type, cfg, self._board, sprites_dir)
            self._transitions[state_type] = (next_state_type, state)

    @property
    def id(self):
        return self._id

    @property
    def moves(self):
        return self._moves

    @property
    def uniqueNumber(self):
        return self._uniqueNumber

    @property
    def state(self):
        return self._state

    def reset(self, start_time: float, start_cell: tuple[int, int], state_type=Types.IDLE,
              end_cell: tuple[int, int] = None):
        self._state = self._transitions[state_type][1]
        self._state.reset(start_time, start_cell, end_cell)

    def command_treatment(self, cmd: Command):
        src_cell = Command.algebraic_to_cell(cmd.params[0])
        if cmd.params[1]:
            dst_cell = Command.algebraic_to_cell(cmd.params[1])
        else:
            dst_cell = None
        self.reset(cmd.timestamp, src_cell, cmd.type, dst_cell)

    def update(self, now_ms: int):
        self._state.update(now_ms)
        if self._state.physics.finished:
            current_type = self._state.state_type
            next_type= self._transitions[current_type][0]
            self.reset(now_ms, self._state.physics.end_cell, state_type=next_type)

    # def command_treatment(self, cmd: Command) -> "State":
    #     next_state = self._transitions.get(cmd.type)
    #     if next_state is None:
    #         return self  # stay in current state
    #     next_state.reset(cmd)
    #     #reset(self, start_time: float, start_cell: Tuple[int, int], end_cell: Tuple[int, int] = None):
    #
    #     return next_state

    def draw_on_board(self, board: Board, now_ms: int):
        t0 = time.perf_counter()
        pos = self._state.physics.pos
        # t1 = time.perf_counter()

        img = self._state.graphics.get_img().img
        # t2 = time.perf_counter()

        if img is not None:
            h, w = img.shape[:2]
            x, y = int(pos[0]), int(pos[1])
            # t3 = time.perf_counter()

            board_img = board.img.img
            # t4 = time.perf_counter()

            h = min(h, board_img.shape[0] - y)
            w = min(w, board_img.shape[1] - x)
            # t5 = time.perf_counter()

            if h > 0 and w > 0:
                piece_img = img[:h, :w]
                # t6 = time.perf_counter()

                base = board_img[y:y + h, x:x + w]
                # t7 = time.perf_counter()

                target_channels = base.shape[2]
                piece_img = self._match_channels(piece_img, target_channels)
                # t8 = time.perf_counter()

                blended = self._blend(base, piece_img)
                # t9 = time.perf_counter()

                board_img[y:y + h, x:x + w] = blended
                # t10 = time.perf_counter()

                # if t9-t8 > 0.1:
                #     pass
                # print(
                #     f"pos: {t1 - t0:.4f}s | get_img: {t2 - t1:.4f}s | coords: {t3 - t2:.4f}s | "
                #     f"board img: {t4 - t3:.4f}s | bounds: {t5 - t4:.4f}s | slice: {t6 - t5:.4f}s | "
                #     f"base slice: {t7 - t6:.4f}s | match_channels: {t8 - t7:.4f}s | "
                #     f"blend: {t9 - t8:.4f}s | assign: {t10 - t9:.4f}s | total: {t10 - t0:.4f}s"
                # )

    @staticmethod
    def _blend(base, overlay):
        alpha = 0.8  # Simple fixed alpha
        return cv2.addWeighted(overlay, alpha, base, 1 - alpha, 0)

    @staticmethod
    def _match_channels(img, target_channels=3):
        """Convert image to target_channels (3=BGR, 4=BGRA)."""
        if img.shape[2] == target_channels:
            return img
        if target_channels == 3 and img.shape[2] == 4:
            return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        if target_channels == 4 and img.shape[2] == 3:
            return cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        return img

    def clone_to(self, cell: tuple[int, int], physics_factory: PhysicsFactory, board: Board) -> "Piece":
        """
        Clone this piece to a new instance at the given cell, using the same id and moves.
        A new State is created with copied graphics and fresh physics.
        """
        graphics_copy = self._state.graphics.copy()

        state_name = self._state.physics.__class__.__name__.replace("Physics", "").lower()
        speed = getattr(self._state.physics, "speed", 1.0)
        cfg = {"physics": {"speed_m_per_sec": speed}}

        new_physics = physics_factory.create(state_name, cfg, board)
        new_physics.set_pos_from_cell(cell)

        new_state = State.from_components(self._moves, graphics_copy, new_physics)

        for event, target in self._state.transitions.items():
            new_state.set_transition(event, target)

        cloned_piece = Piece(self._id, self._state.graphics.piece_dir, board)
        cloned_piece._state = new_state  # override state directly

        return cloned_piece
