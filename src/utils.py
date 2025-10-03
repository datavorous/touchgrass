import os

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


def print_board(board):
    print("   a b c d e f g h")
    for i, row in enumerate(board):
        rank = 8 - i
        print(f"{rank}  " + " ".join(piece_map[p] for p in row) + f"  {rank}")
    print("   a b c d e f g h\n")


def coords_to_uci(move):
    (fx, fy), (tx, ty) = move
    return f"{'abcdefgh'[fy]}{8-fx}{'abcdefgh'[ty]}{8-tx}"



def clear_screen():
    os.system("clear")

def uci_to_coords(uci_move):
    """Convert UCI move notation (e.g. 'e2e4') to internal coordinate format ((x1,y1), (x2,y2))"""
    if len(uci_move) < 4:
        return None
        
    try:
        from_file = ord(uci_move[0]) - ord('a')
        from_rank = int(uci_move[1]) - 1
        to_file = ord(uci_move[2]) - ord('a')
        to_rank = int(uci_move[3]) - 1
        
        # Validate coordinates
        if not (0 <= from_file <= 7 and 0 <= from_rank <= 7 and
                0 <= to_file <= 7 and 0 <= to_rank <= 7):
            return None
            
        return ((from_file, from_rank), (to_file, to_rank))
    except (ValueError, IndexError):
        return None
