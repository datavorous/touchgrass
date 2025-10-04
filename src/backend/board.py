from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class MoveRecord:
    moved_piece: int
    captured_piece: int
    promotion: Optional[int] = None
    from_sq: Tuple[int, int] = (0, 0)
    to_sq: Tuple[int, int] = (0, 0)
    en_passant_target: Optional[Tuple[int, int]] = None
    was_en_passant_capture: bool = False
    en_passant_capture_sq: Optional[Tuple[int, int]] = None  # Where the captured pawn was


EMPTY = 0
WPAWN, WKNIGHT, WBISHOP, WROOK, WQUEEN, WKING = 1, 2, 3, 4, 5, 6
BPAWN, BKNIGHT, BBISHOP, BROOK, BQUEEN, BKING = -1, -2, -3, -4, -5, -6


class Board:
    def __init__(self):
        self.board = self.starting_pos()
        self.wking_pos = (7, 4)
        self.bking_pos = (0, 4)
        self.en_passant_target = None

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
        
        # Store previous en passant target to restore on undo
        prev_en_passant = self.en_passant_target
        self.en_passant_target = None  # Reset by default
        
        was_en_passant_capture = False
        en_passant_capture_sq = None

        # Check if this is an en passant capture
        if abs(original_piece) == WPAWN and prev_en_passant is not None and (tx, ty) == prev_en_passant:
            was_en_passant_capture = True
            # The captured pawn is not on the target square, it's beside us
            if original_piece == WPAWN:  # White capturing black
                en_passant_capture_sq = (tx + 1, ty)
            else:  # Black capturing white
                en_passant_capture_sq = (tx - 1, ty)
            captured = self.board[en_passant_capture_sq[0]][en_passant_capture_sq[1]]
            self.board[en_passant_capture_sq[0]][en_passant_capture_sq[1]] = EMPTY

        # Execute the move
        self.board[tx][ty] = original_piece
        self.board[fx][fy] = EMPTY

        # Update king positions
        if original_piece == WKING:
            self.wking_pos = (tx, ty)
        elif original_piece == BKING:
            self.bking_pos = (tx, ty)

        # Check if pawn moved two squares (enable en passant for next turn)
        if abs(original_piece) == WPAWN and abs(fx - tx) == 2:
            # Set en passant target square (the square the pawn "skipped over")
            en_passant_x = (fx + tx) // 2
            self.en_passant_target = (en_passant_x, fy)

        # HANDLE CASTLING
        if abs(original_piece) == WKING and abs(fy - ty) == 2:
            # SHORT
            if ty == 6:
                rook = self.board[fx][7]
                self.board[fx][5] = rook
                self.board[fx][7] = EMPTY
            # LONG
            elif ty == 2:
                rook = self.board[fx][0]
                self.board[fx][3] = rook
                self.board[fx][0] = EMPTY

        # Handle pawn promotion
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
            en_passant_target=prev_en_passant,
            was_en_passant_capture=was_en_passant_capture,
            en_passant_capture_sq=en_passant_capture_sq,
        )

    def undo_move(self, move, move_record):
        (fx, fy), (tx, ty) = move

        # Restore the piece to its original position
        self.board[fx][fy] = move_record.moved_piece
        
        # Restore the target square
        if move_record.was_en_passant_capture:
            # Target square should be empty
            self.board[tx][ty] = EMPTY
            # Restore the captured pawn to its actual position
            self.board[move_record.en_passant_capture_sq[0]][move_record.en_passant_capture_sq[1]] = move_record.captured_piece
        else:
            # Normal move - restore whatever was captured
            self.board[tx][ty] = move_record.captured_piece

        # Restore en passant state
        self.en_passant_target = move_record.en_passant_target

        # Restore king positions
        if move_record.moved_piece == WKING:
            self.wking_pos = (fx, fy)
        elif move_record.moved_piece == BKING:
            self.bking_pos = (fx, fy)
            
        # CASTLING UNDO
        if abs(move_record.moved_piece) == WKING and abs(fy - ty) == 2:
            # SHORT
            if ty == 6:
                rook = self.board[fx][5]
                self.board[fx][7] = rook
                self.board[fx][5] = EMPTY
            # LONG
            elif ty == 2:
                rook = self.board[fx][3]
                self.board[fx][0] = rook
                self.board[fx][3] = EMPTY