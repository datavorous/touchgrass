import random
from ..backend.api import API
from .base import BaseEngine


class DumboEngine(BaseEngine):
    def __init__(self, api: API):
        super().__init__(api)

    def get_best_move(self):
        moves = self.api.get_legal_moves()
        return random.choice(moves) if moves else None
