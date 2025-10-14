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


def uci_to_coords(s):
    fy = "abcdefgh".index(s[0])
    fx = 8 - int(s[1])
    ty = "abcdefgh".index(s[2])
    tx = 8 - int(s[3])
    return ((fx, fy), (tx, ty))


def clear_screen():
    os.system("clear")
