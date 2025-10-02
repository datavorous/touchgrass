from dataclasses import dataclass
from typing import Optional, Tuple
from .bitboard import *


@dataclass
class MoveRecord:
    moved_piece: int
    captured_piece: int
    promotion: Optional[int] = None
    from_sq: Tuple[int, int] = (0, 0)
    to_sq: Tuple[int, int] = (0, 0)


# Legacy piece constants for backward compatibility
EMPTY = 0
WPAWN, WKNIGHT, WBISHOP, WROOK, WQUEEN, WKING = 1, 2, 3, 4, 5, 6
BPAWN, BKNIGHT, BBISHOP, BROOK, BQUEEN, BKING = -1, -2, -3, -4, -5, -6


class Board:
    def __init__(self):
        # Bitboards for each piece type and color
        # Index: [WHITE/BLACK][PIECE_TYPE]
        self.piece_bitboards = [[0 for _ in range(6)] for _ in range(2)]
        self.color_bitboards = [0, 0]  # [WHITE, BLACK]
        self.all_pieces = 0
        
        # King positions for quick access
        self.wking_pos = (7, 4)
        self.bking_pos = (0, 4)
        
        self.init_starting_position()

    def init_starting_position(self):
        """Initialize the starting chess position using bitboards"""
        # Clear all bitboards
        self.piece_bitboards = [[0 for _ in range(6)] for _ in range(2)]
        self.color_bitboards = [0, 0]
        self.all_pieces = 0
        
        # Set up white pieces
        self.piece_bitboards[WHITE][ROOK] = set_bit(self.piece_bitboards[WHITE][ROOK], square_to_bit(7, 0))  # a1
        self.piece_bitboards[WHITE][ROOK] = set_bit(self.piece_bitboards[WHITE][ROOK], square_to_bit(7, 7))  # h1
        self.piece_bitboards[WHITE][KNIGHT] = set_bit(self.piece_bitboards[WHITE][KNIGHT], square_to_bit(7, 1))  # b1
        self.piece_bitboards[WHITE][KNIGHT] = set_bit(self.piece_bitboards[WHITE][KNIGHT], square_to_bit(7, 6))  # g1
        self.piece_bitboards[WHITE][BISHOP] = set_bit(self.piece_bitboards[WHITE][BISHOP], square_to_bit(7, 2))  # c1
        self.piece_bitboards[WHITE][BISHOP] = set_bit(self.piece_bitboards[WHITE][BISHOP], square_to_bit(7, 5))  # f1
        self.piece_bitboards[WHITE][QUEEN] = set_bit(self.piece_bitboards[WHITE][QUEEN], square_to_bit(7, 3))  # d1
        self.piece_bitboards[WHITE][KING] = set_bit(self.piece_bitboards[WHITE][KING], square_to_bit(7, 4))  # e1
        
        # White pawns
        for col in range(8):
            self.piece_bitboards[WHITE][PAWN] = set_bit(self.piece_bitboards[WHITE][PAWN], square_to_bit(6, col))
        
        # Set up black pieces
        self.piece_bitboards[BLACK][ROOK] = set_bit(self.piece_bitboards[BLACK][ROOK], square_to_bit(0, 0))  # a8
        self.piece_bitboards[BLACK][ROOK] = set_bit(self.piece_bitboards[BLACK][ROOK], square_to_bit(0, 7))  # h8
        self.piece_bitboards[BLACK][KNIGHT] = set_bit(self.piece_bitboards[BLACK][KNIGHT], square_to_bit(0, 1))  # b8
        self.piece_bitboards[BLACK][KNIGHT] = set_bit(self.piece_bitboards[BLACK][KNIGHT], square_to_bit(0, 6))  # g8
        self.piece_bitboards[BLACK][BISHOP] = set_bit(self.piece_bitboards[BLACK][BISHOP], square_to_bit(0, 2))  # c8
        self.piece_bitboards[BLACK][BISHOP] = set_bit(self.piece_bitboards[BLACK][BISHOP], square_to_bit(0, 5))  # f8
        self.piece_bitboards[BLACK][QUEEN] = set_bit(self.piece_bitboards[BLACK][QUEEN], square_to_bit(0, 3))  # d8
        self.piece_bitboards[BLACK][KING] = set_bit(self.piece_bitboards[BLACK][KING], square_to_bit(0, 4))  # e8
        
        # Black pawns
        for col in range(8):
            self.piece_bitboards[BLACK][PAWN] = set_bit(self.piece_bitboards[BLACK][PAWN], square_to_bit(1, col))
        
        # Update combined bitboards
        self.update_combined_bitboards()

    def update_combined_bitboards(self):
        """Update the combined color and all-pieces bitboards"""
        self.color_bitboards[WHITE] = 0
        self.color_bitboards[BLACK] = 0
        
        for piece_type in range(6):
            self.color_bitboards[WHITE] |= self.piece_bitboards[WHITE][piece_type]
            self.color_bitboards[BLACK] |= self.piece_bitboards[BLACK][piece_type]
        
        self.all_pieces = self.color_bitboards[WHITE] | self.color_bitboards[BLACK]

    def get_piece_at(self, row, col):
        """Get the piece at a given square (for backward compatibility)"""
        bit = square_to_bit(row, col)
        
        if not get_bit(self.all_pieces, bit):
            return EMPTY
        
        # Check which piece is at this square
        for color in [WHITE, BLACK]:
            if get_bit(self.color_bitboards[color], bit):
                for piece_type in range(6):
                    if get_bit(self.piece_bitboards[color][piece_type], bit):
                        # Convert to legacy piece values
                        piece_value = piece_type + 1
                        return piece_value if color == WHITE else -piece_value
        
        return EMPTY

    def starting_pos(self):
        """Return an 8x8 array representation for backward compatibility"""
        board = []
        for row in range(8):
            row_pieces = []
            for col in range(8):
                row_pieces.append(self.get_piece_at(row, col))
            board.append(row_pieces)
        return board

    @property
    def board(self):
        """Property to maintain backward compatibility with the 8x8 array interface"""
        return self.starting_pos()

    def apply_move(self, move):
        """Apply a move to the board and return a record for undoing"""
        (fx, fy), (tx, ty) = move
        
        from_bit = square_to_bit(fx, fy)
        to_bit = square_to_bit(tx, ty)
        
        # Find the piece being moved
        moved_piece_legacy = self.get_piece_at(fx, fy)
        captured_piece_legacy = self.get_piece_at(tx, ty)
        
        if moved_piece_legacy == EMPTY:
            raise ValueError(f"No piece at source square ({fx}, {fy})")
        
        # Convert legacy piece to color and type
        is_white = moved_piece_legacy > 0
        color = WHITE if is_white else BLACK
        piece_type = abs(moved_piece_legacy) - 1
        
        # Remove piece from source square
        self.piece_bitboards[color][piece_type] = clear_bit(self.piece_bitboards[color][piece_type], from_bit)
        
        # If there's a captured piece, remove it
        if captured_piece_legacy != EMPTY:
            captured_color = WHITE if captured_piece_legacy > 0 else BLACK
            captured_piece_type = abs(captured_piece_legacy) - 1
            self.piece_bitboards[captured_color][captured_piece_type] = clear_bit(
                self.piece_bitboards[captured_color][captured_piece_type], to_bit
            )
        
        # Place piece on destination square
        self.piece_bitboards[color][piece_type] = set_bit(self.piece_bitboards[color][piece_type], to_bit)
        
        # Update king positions
        if moved_piece_legacy == WKING:
            self.wking_pos = (tx, ty)
        elif moved_piece_legacy == BKING:
            self.bking_pos = (tx, ty)
        
        # Handle pawn promotion
        promotion = None
        if abs(moved_piece_legacy) == WPAWN:
            if (moved_piece_legacy == WPAWN and tx == 0) or (moved_piece_legacy == BPAWN and tx == 7):
                # Remove pawn and add queen
                self.piece_bitboards[color][PAWN] = clear_bit(self.piece_bitboards[color][PAWN], to_bit)
                self.piece_bitboards[color][QUEEN] = set_bit(self.piece_bitboards[color][QUEEN], to_bit)
                promotion = WQUEEN if is_white else BQUEEN
        
        # Update combined bitboards
        self.update_combined_bitboards()
        
        return MoveRecord(
            moved_piece=moved_piece_legacy,
            captured_piece=captured_piece_legacy,
            promotion=promotion,
            from_sq=(fx, fy),
            to_sq=(tx, ty),
        )

    def undo_move(self, move, move_record):
        """Undo a move using the move record"""
        (fx, fy), (tx, ty) = move
        
        from_bit = square_to_bit(fx, fy)
        to_bit = square_to_bit(tx, ty)
        
        moved_piece_legacy = move_record.moved_piece
        captured_piece_legacy = move_record.captured_piece
        
        # Convert legacy piece to color and type
        is_white = moved_piece_legacy > 0
        color = WHITE if is_white else BLACK
        piece_type = abs(moved_piece_legacy) - 1
        
        # Handle promotion undo
        if move_record.promotion:
            # Remove promoted piece and restore pawn
            self.piece_bitboards[color][QUEEN] = clear_bit(self.piece_bitboards[color][QUEEN], to_bit)
            self.piece_bitboards[color][PAWN] = set_bit(self.piece_bitboards[color][PAWN], to_bit)
        
        # Remove piece from destination square
        current_piece_type = PAWN if move_record.promotion else piece_type
        self.piece_bitboards[color][current_piece_type] = clear_bit(
            self.piece_bitboards[color][current_piece_type], to_bit
        )
        
        # Restore piece to source square
        self.piece_bitboards[color][piece_type] = set_bit(self.piece_bitboards[color][piece_type], from_bit)
        
        # Restore captured piece if any
        if captured_piece_legacy != EMPTY:
            captured_color = WHITE if captured_piece_legacy > 0 else BLACK
            captured_piece_type = abs(captured_piece_legacy) - 1
            self.piece_bitboards[captured_color][captured_piece_type] = set_bit(
                self.piece_bitboards[captured_color][captured_piece_type], to_bit
            )
        
        # Restore king positions
        if moved_piece_legacy == WKING:
            self.wking_pos = (fx, fy)
        elif moved_piece_legacy == BKING:
            self.bking_pos = (fx, fy)
        
        # Update combined bitboards
        self.update_combined_bitboards()
