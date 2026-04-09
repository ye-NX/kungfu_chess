import pathlib
import unittest
from It1_interfaces.Game import Game
from It1_interfaces.Board import Board

class DummyBoard(Board):
    def __init__(self):
        # תוכן דמה אם צריך
        pass

class TestGameSingleton(unittest.TestCase):

    def setUp(self):
        # איפוס המופע בין בדיקות (רק אם את מוסיפה reset_instance)
        Game._instance = None

    def test_singleton_instance_identity(self):
        board1 = DummyBoard()
        path1 = pathlib.Path("some/path1")
        csv1 = pathlib.Path("some/file1.csv")

        board2 = DummyBoard()
        path2 = pathlib.Path("some/path2")
        csv2 = pathlib.Path("some/file2.csv")

        g1 = Game(board1, path1, csv1)
        g2 = Game(board2, path2, csv2)

        self.assertIs(g1, g2, "Game should be a singleton and always return the same instance")

    def test_singleton_initialization_once(self):
        board = DummyBoard()
        path = pathlib.Path("dummy/path")
        csv = pathlib.Path("dummy/file.csv")

        g1 = Game(board, path, csv)
        # שומרים ערך לבדיקה
        original_board = g1.board

        # יוצרים "מופע חדש"
        g2 = Game(DummyBoard(), pathlib.Path("new/path"), pathlib.Path("new.csv"))

        # בודקים שהמופע לא אותחל מחדש
        self.assertIs(g1.board, original_board, "Singleton should not reinitialize once created")
        self.assertIs(g1, g2)

if __name__ == '__main__':
    unittest.main()
