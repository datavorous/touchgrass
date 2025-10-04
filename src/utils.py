import os
from .backend.board import EMPTY, WPAWN, WKNIGHT, WBISHOP, WROOK, WQUEEN, WKING
from .backend.board import BPAWN, BKNIGHT, BBISHOP, BROOK, BQUEEN, BKING

piece_map = {
    0: "·",
    1: "♟",
    2: "♞",
    3: "♝",
    4: "♜",
    5: "♛",
    6: "♚",
    -1: "♙",
    -2: "♘",
    -3: "♗",
    -4: "♖",
    -5: "♕",
    -6: "♔",
}

# FEN piece mapping
fen_to_piece = {
    'P': WPAWN, 'N': WKNIGHT, 'B': WBISHOP, 'R': WROOK, 'Q': WQUEEN, 'K': WKING,
    'p': BPAWN, 'n': BKNIGHT, 'b': BBISHOP, 'r': BROOK, 'q': BQUEEN, 'k': BKING
}


def print_board(board):
    print("   a b c d e f g h")
    for i, row in enumerate(board):
        rank = 8 - i
        print(f"{rank}  " + " ".join(piece_map[p] for p in row) + f"  {rank}")
    print("   a b c d e f g h\n")


def coords_to_uci(move):
    (fx, fy), (tx, ty) = move
    return f"{'abcdefgh'[fy]}{8-fx}{'abcdefgh'[ty]}{8-tx}"


def uci_to_coords(s):
    fy = "abcdefgh".index(s[0])
    fx = 8 - int(s[1])
    ty = "abcdefgh".index(s[2])
    tx = 8 - int(s[3])
    return ((fx, fy), (tx, ty))


def clear_screen():
    os.system("clear")


def parse_fen(fen_string: str):
    """
    Parse a FEN string and return board position, active color, castling rights, etc.
    Returns a tuple: (board, active_color, castling_rights, en_passant, halfmove_clock, fullmove_number)
    """
    parts = fen_string.split()
    if len(parts) < 4:
        raise ValueError("Invalid FEN string")
    
    # Parse board position
    board = [[EMPTY for _ in range(8)] for _ in range(8)]
    ranks = parts[0].split('/')
    
    if len(ranks) != 8:
        raise ValueError("Invalid FEN: must have 8 ranks")
    
    for rank_idx, rank in enumerate(ranks):
        file_idx = 0
        for char in rank:
            if char.isdigit():
                # Empty squares
                file_idx += int(char)
            elif char in fen_to_piece:
                board[rank_idx][file_idx] = fen_to_piece[char]
                file_idx += 1
            else:
                raise ValueError(f"Invalid FEN character: {char}")
    
    # Parse active color
    active_color = "white" if parts[1] == "w" else "black"
    
    # Parse castling rights (simplified - we'll ignore for now)
    castling_rights = parts[2] if len(parts) > 2 else "-"
    
    # Parse en passant square (simplified - we'll ignore for now)
    en_passant = parts[3] if len(parts) > 3 else "-"
    
    # Parse halfmove clock and fullmove number
    halfmove_clock = int(parts[4]) if len(parts) > 4 else 0
    fullmove_number = int(parts[5]) if len(parts) > 5 else 1
    
    return board, active_color, castling_rights, en_passant, halfmove_clock, fullmove_number


def find_king_positions(board):
    """Find the positions of white and black kings on the board."""
    wking_pos = None
    bking_pos = None
    
    for i in range(8):
        for j in range(8):
            if board[i][j] == WKING:
                wking_pos = (i, j)
            elif board[i][j] == BKING:
                bking_pos = (i, j)
    
    return wking_pos, bking_pos
