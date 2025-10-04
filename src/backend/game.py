from .board import Board

# import random
from .move_gen import getLegalMoves, isSquareAttacked
from .move_gen import canCastle


class Game:
    def __init__(self):
        self.board = Board()
        self.turn = "white"

        self.game_over = False
        self.result = None

        self.history = []

    def is_check(self, color):
        king_pos = self.board.wking_pos if color == "white" else self.board.bking_pos
        return isSquareAttacked(self.board, *king_pos, by_white=(color == "black"))

    def get_gamestate(self):
        moves = self.legal_moves()

        if moves:
            return "ongoing"

        if self.is_check(self.turn):
            winner = "white" if self.turn == "black" else "black"
            return f"checkmate_{winner}"
        else:
            return "stalemate"

    def legal_moves(self):
        return getLegalMoves(self.board, self.turn, self.history)

    def make_move(self, move):
        if move not in self.legal_moves():
            print("> illegal move\n")
            return None

        record = self.board.apply_move(move)
        self.history.append(record)

        state = self.get_gamestate()
        if state != "ongoing":
            self.game_over = True
            self.result = state
        else:
            self.turn = "black" if self.turn == "white" else "white"

        return record

    def undo_last(self):
        if not self.history:
            return
        last_move = self.history.pop()

        move = (last_move.from_sq, last_move.to_sq)
        self.board.undo_move(move, last_move)

        self.turn = "black" if self.turn == "white" else "white"
        self.game_over = False
        self.result = None