from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class MoveRecord:
    moved_piece: int
    captured_piece: int
    promotion: Optional[int] = None
    from_sq: Tuple[int, int] = (0, 0)
    to_sq: Tuple[int, int] = (0, 0)


EMPTY = 0
WPAWN, WKNIGHT, WBISHOP, WROOK, WQUEEN, WKING = 1, 2, 3, 4, 5, 6
BPAWN, BKNIGHT, BBISHOP, BROOK, BQUEEN, BKING = -1, -2, -3, -4, -5, -6


class Board:
    def __init__(self):
        self.board = self.starting_pos()
        self.wking_pos = (7, 4)
        self.bking_pos = (0, 4)

    def starting_pos(self):
        return [
            [BROOK, BKNIGHT, BBISHOP, BQUEEN, BKING, BBISHOP, BKNIGHT, BROOK],
            [BPAWN, BPAWN, BPAWN, BPAWN, BPAWN, BPAWN, BPAWN, BPAWN],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [WPAWN, WPAWN, WPAWN, WPAWN, WPAWN, WPAWN, WPAWN, WPAWN],
            [WROOK, WKNIGHT, WBISHOP, WQUEEN, WKING, WBISHOP, WKNIGHT, WROOK],
        ]

    def apply_move(self, move):
        (fx, fy), (tx, ty) = move

        original_piece = self.board[fx][fy]

        captured = self.board[tx][ty]

        self.board[tx][ty] = original_piece
        self.board[fx][fy] = EMPTY

        if original_piece == WKING:
            self.wking_pos = (tx, ty)
        elif original_piece == BKING:
            self.bking_pos = (tx, ty)

        promotion = None
        if original_piece == WPAWN and tx == 0:
            promotion = WQUEEN
            self.board[tx][ty] = WQUEEN
        elif original_piece == BPAWN and tx == 7:
            promotion = BQUEEN
            self.board[tx][ty] = BQUEEN

        return MoveRecord(
            moved_piece=original_piece,
            captured_piece=captured,
            promotion=promotion,
            from_sq=(fx, fy),
            to_sq=(tx, ty),
        )

    def set_position(self, board_array, wking_pos=None, bking_pos=None):
        """Set the board to a specific position."""
        self.board = [row[:] for row in board_array]  # Deep copy
        if wking_pos:
            self.wking_pos = wking_pos
        if bking_pos:
            self.bking_pos = bking_pos
