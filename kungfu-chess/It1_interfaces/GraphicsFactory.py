import pathlib
from Graphics import Graphics
from Board import Board

class GraphicsFactory:
    @staticmethod
    def create(sprites_dir: pathlib.Path, cfg: dict, board: Board) -> Graphics:
        graphics_cfg = cfg.get("graphics", {})
        fps = graphics_cfg.get("frames_per_sec", 6.0)
        loop = graphics_cfg.get("is_loop", True)

        return Graphics(
            sprites_folder=sprites_dir,
            board=board,
            loop=loop,
            fps=fps
        )

