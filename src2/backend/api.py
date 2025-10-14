from .game import Game

# from .board import MoveRecord


class API:
    def __init__(self):
        self.g = Game()

    def get_state(self):
        return {
            "board": self.g.board.board,
            "turn": self.g.turn,
            "over": self.g.game_over,
            "result": self.g.result,
        }

    def get_legal_moves(self):
        return self.g.legal_moves()

    def make_move(self, move):
        return self.g.make_move(move)

    def apply_move(self, move):
        return self.g.board.apply_move(move)

    def undo_move(self, move, record):
        return self.g.board.undo_move(move, record)

    def get_board(self):
        return self.g.board.board
