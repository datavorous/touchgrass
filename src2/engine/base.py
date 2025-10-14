from ..backend.api import API


class BaseEngine:
    def __init__(self, api: API):
        self.api = api

    def get_best_move(self):
        # ((fx,fy),(tx,ty)) or None
        raise NotImplementedError
