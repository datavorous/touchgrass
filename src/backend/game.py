from .board import Board
from .board import WPAWN, WKNIGHT, WBISHOP, WROOK, WQUEEN, WKING
from .board import BPAWN, BKNIGHT, BBISHOP, BROOK, BQUEEN, BKING, EMPTY
from dataclasses import dataclass
from typing import List, Optional
import copy

from .move_gen import getLegalMoves, isSquareAttacked
from .move_gen import canCastle


@dataclass
class GameState:
    board_state: List[List[int]]
    wking_pos: tuple
    bking_pos: tuple
    turn: str
    halfmove_clock: int
    game_over: bool
    result: Optional[str]

class Game:
    def __init__(self):
        self.board = Board()
        self.turn = "white"
        self.game_over = False
        self.result = None
        self.halfmove_clock = 0
        
        self.state_stack = []
        self.redo_stack = []
        self.history = []

    def is_check(self, color):
        king_pos = self.board.wking_pos if color == "white" else self.board.bking_pos
        return isSquareAttacked(self.board, *king_pos, by_white=(color == "black"))


    def get_gamestate(self):
        moves = self.legal_moves()

        if self.halfmove_clock >= 100:
            return "draw_fifty_move_rule"

        if moves:
            return "ongoing"

        if self.is_check(self.turn):
            winner = "white" if self.turn == "black" else "black"
            return f"checkmate_{winner}"
        else:
            return "stalemate"

    def legal_moves(self):
        return getLegalMoves(self.board, self.turn, self.history)
    
    def save_state(self):
        state = GameState(
            board_state=copy.deepcopy(self.board.board),
            wking_pos=self.board.wking_pos,
            bking_pos=self.board.bking_pos,
            turn=self.turn,
            halfmove_clock=self.halfmove_clock,
            game_over=self.game_over,
            result=self.result
        )
        return state
    
    def restore_state(self, state):
        self.board.board = copy.deepcopy(state.board_state)
        self.board.wking_pos = state.wking_pos
        self.board.bking_pos = state.bking_pos
        self.turn = state.turn
        self.halfmove_clock = state.halfmove_clock
        self.game_over = state.game_over
        self.result = state.result

    def make_move(self, move):
        if move not in self.legal_moves():
            print("> illegal move\n")
            return None

        current_state = self.save_state()
        self.state_stack.append(current_state)
        self.redo_stack.clear()

        record = self.board.apply_move(move)
        self.history.append(record)

        if record.moved_piece in [WPAWN, BPAWN] or record.captured_piece != EMPTY:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

        state = self.get_gamestate()
        if state != "ongoing":
            self.game_over = True
            self.result = state
        else:
            self.turn = "black" if self.turn == "white" else "white"

        return record

    def undo(self):
        if not self.state_stack:
            return False
        current_state = self.save_state()
        self.redo_stack.append(current_state)
        previous_state = self.state_stack.pop()
        self.restore_state(previous_state)
        if self.history:
            self.history.pop()
        return True
    
    def redo(self):
        if not self.redo_stack:
            return False
        current_state = self.save_state()
        self.state_stack.append(current_state)
        next_state = self.redo_stack.pop()
        self.restore_state(next_state)
        return True
    
    def can_undo(self):
        return len(self.state_stack) > 0
    
    def can_redo(self):
        return len(self.redo_stack) > 0
    
    def undo_last(self):
        return self.undo()
