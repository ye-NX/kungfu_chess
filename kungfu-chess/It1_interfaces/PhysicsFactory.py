from Physics import *
from Enums import StateTypes as Types


class PhysicsFactory:
    @staticmethod
    def create(state: Types,cfg, board) -> Physics:
        physics_cfg = cfg.get("physics", {})
        speed = physics_cfg.get("speed_m_per_sec", 1.0)

        if state == Types.IDLE:
            return IdlePhysics(board, speed)
        elif state == Types.MOVE:
            return MovePhysics(board, speed)
        elif state == Types.JUMP:
            return JumpPhysics(board, speed)
        elif state == Types.SHORT_REST:
            return ShortRestPhysics(board, speed)
        elif state == Types.LONG_REST:
            return LongRestPhysics(board, speed)
        else:
            raise ValueError(f"Unknown state name: {state}")
