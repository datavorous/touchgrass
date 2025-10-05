from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class MoveRecord:
    moved_piece: int
    captured_piece: int
    promotion: Optional[int] = None
    from_sq: Tuple[int, int] = (0, 0)
    to_sq: Tuple[int, int] = (0, 0)
    en_passant: bool = False


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

        en_passant = False

        if original_piece == WKING:
            self.wking_pos = (tx, ty)
        elif original_piece == BKING:
            self.bking_pos = (tx, ty)

        # HANDLE EN PASSANT
        elif captured == EMPTY and abs(original_piece) == WPAWN:
            if fy != ty:
                captured = self.board[tx + abs(original_piece)][ty]
                self.board[tx + abs(original_piece)][ty] = EMPTY
                en_passant = True
        # HANDLE CASTLING
        # CHECK IF KING MADE A 2SQR MOVE
        if abs(original_piece) == WKING and abs(fy - ty) == 2:
            # SHORT
            if ty == 6:
                rook = self.board[fx][7]
                self.board[fx][5] = rook  # move rook
                self.board[fx][7] = EMPTY  # empty the sqr
            # LONG
            elif ty == 2:
                rook = self.board[fx][0]
                self.board[fx][3] = rook  # move rook
                self.board[fx][0] = EMPTY

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
            en_passant=en_passant,
        )

    def undo_move(self, move, move_record):
        (fx, fy), (tx, ty) = move
        # piece = self.board[tx][ty]

        self.board[fx][fy] = move_record.moved_piece
        self.board[tx][ty] = move_record.captured_piece

        if move_record.moved_piece == WKING:
            self.wking_pos = (fx, fy)
        elif move_record.moved_piece == BKING:
            self.bking_pos = (fx, fy)
        # CASTLING UNDO
        if abs(move_record.moved_piece) == WKING and abs(fy - ty) == 2:
            # SHORT
            if ty == 6:
                rook = self.board[fx][5]
                self.board[fx][7] = rook  # undo rook
                self.board[fx][5] = EMPTY
            # LONG
            elif ty == 2:
                rook = self.board[fx][3]
                self.board[fx][0] = rook  # nudo rook
                self.board[fx][3] = EMPTY

        # ENPASSANT UNDO
        elif move_record.en_passant:
            self.board[tx][ty] = EMPTY
            rank = tx + abs(move_record.moved_piece)
            self.board[rank][ty] = move_record.captured_piece
