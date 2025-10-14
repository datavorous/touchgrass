from ..backend.api import API
from .base import BaseEngine


class MinimaxEngine(BaseEngine):
    def __init__(self, api: API, depth=2):
        super().__init__(api)
        self.depth = depth
        self.values = {0: 0, 1: 100, 2: 320, 3: 330, 4: 500, 5: 900, 6: 20000}

    def evaluate_board(self, board, turn):
        score = 0
        for row in board:
            for piece in row:
                val = self.values.get(abs(piece), 0)
                score += val if piece > 0 else -val
        return score if turn == "white" else -score

    def minimax(self, depth, maximizing):
        state = self.api.get_state()
        if state["over"] or depth == 0:
            return self.evaluate_board(state["board"], state["turn"])

        moves = self.api.get_legal_moves()
        if not moves:
            return 0

        if maximizing:
            best = float("-inf")
            for move in moves:
                record = self.api.apply_move(move)
                score = self.minimax(depth - 1, False)
                self.api.undo_move(move, record)
                best = max(best, score)
            return best
        else:
            best = float("inf")
            for move in moves:
                record = self.api.apply_move(move)
                score = self.minimax(depth - 1, True)
                self.api.undo_move(move, record)
                best = min(best, score)
            return best

    def get_best_move(self):
        best_move = None
        best_score = float("-inf")
        moves = self.api.get_legal_moves()
        for move in moves:
            record = self.api.apply_move(move)
            score = self.minimax(self.depth - 1, False)
            self.api.undo_move(move, record)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move
