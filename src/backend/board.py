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

    def apply_move(self, move, promotion_choice=None):
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
            promotion = promotion_choice if promotion_choice else WQUEEN
            self.board[tx][ty] = promotion
        elif original_piece == BPAWN and tx == 7:
            promotion = promotion_choice if promotion_choice else BQUEEN
            self.board[tx][ty] = promotion

        return MoveRecord(
            moved_piece=original_piece,
            captured_piece=captured,
            promotion=promotion,
            from_sq=(fx, fy),
            to_sq=(tx, ty),
        )

    def undo_move(self, move, move_record):
        (fx, fy), (tx, ty) = move
        # piece = self.board[tx][ty]

        if move_record.promotion is not None:
         # Pawn was promoted → put pawn back to original square
            if move_record.moved_piece > 0:  # White pawn
                self.board[fx][fy] = WPAWN
            else:  # Black pawn
                self.board[fx][fy] = BPAWN
         
            # Restore captured piece at promotion square
            self.board[tx][ty] = move_record.captured_piece
        
        else:
            # Normal undo     
            self.board[fx][fy] = move_record.moved_piece
            self.board[tx][ty] = move_record.captured_piece

        if move_record.moved_piece == WKING:
            self.wking_pos = (fx, fy)
        elif move_record.moved_piece == BKING:
            self.bking_pos = (fx, fy)
