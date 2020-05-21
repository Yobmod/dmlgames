from unittest import TestCase

# from pytest import approx

from gamer.memorygame import MemoryGame


class TestCaseGame(TestCase):
    """"""

    def test_1(self) -> None:
        game = MemoryGame()
        assert game.FPSCLOCK is not None

        cols = game.board
        rows = game.board[0]
        assert isinstance(cols, list) and len(cols) == 3
        assert isinstance(rows, list) and len(rows) == 2

        # game.main()
