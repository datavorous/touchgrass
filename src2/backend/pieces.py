from .board import WPAWN, WKNIGHT, WBISHOP, WROOK, WQUEEN, WKING
from .board import EMPTY

# from .board import BPAWN, BKNIGHT, BBISHOP, BROOK, BQUEEN, BKING


def in_bounds(x, y):
    return 0 <= x < 8 and 0 <= y < 8


def pawn_moves(board, x, y, piece):
    moves = []
    direction = -1 if piece > 0 else 1

    nx, ny = x + direction, y

    if in_bounds(nx, ny) and board[nx][ny] == EMPTY:
        moves.append((nx, ny))

        if (piece > 0 and x == 6) or (piece < 0 and x == 1):
            nx2 = nx + direction
            if in_bounds(nx2, ny) and board[nx2][ny] == EMPTY:
                moves.append((nx2, ny))

    for dy in [-1, 1]:
        nx, ny = x + direction, y + dy

        if in_bounds(nx, ny) and board[nx][ny] != EMPTY and board[nx][ny] * piece < 0:
            moves.append((nx, ny))

    return moves


def knight_moves(board, x, y, piece):
    moves = []
    # direction = -1 if piece > 0 else 1
    jumps = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]

    # nx, ny = x + direction, y
    # if in_bounds(nx, ny) and board[nx][ny] == EMPTY:
    # moves.append((nx, ny))

    for dx, dy in jumps:
        nx, ny = x + dx, y + dy

        if in_bounds(nx, ny) and (board[nx][ny] == EMPTY or board[nx][ny] * piece < 0):
            moves.append((nx, ny))

    return moves


def sliding_moves(board, x, y, piece, directions):
    moves = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        while in_bounds(nx, ny):
            if board[nx][ny] == EMPTY:
                moves.append((nx, ny))
            elif board[nx][ny] * piece < 0:
                moves.append((nx, ny))
                break
            else:
                break
            nx += dx
            ny += dy
    return moves


def bishop_moves(board, x, y, piece):
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    return sliding_moves(board, x, y, piece, directions)


def rook_moves(board, x, y, piece):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    return sliding_moves(board, x, y, piece, directions)


def queen_moves(board, x, y, piece):
    return bishop_moves(board, x, y, piece) + rook_moves(board, x, y, piece)


def king_moves(board, x, y, piece):
    moves = []

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if in_bounds(nx, ny) and (
                board[nx][ny] == EMPTY or board[nx][ny] * piece < 0
            ):
                moves.append((nx, ny))
    return moves


def getPseudoLegalMoves(board, x, y):
    piece = board[x][y]
    if piece == EMPTY:
        return []
    if abs(piece) == WPAWN:
        return pawn_moves(board, x, y, piece)
    if abs(piece) == WKNIGHT:
        return knight_moves(board, x, y, piece)
    if abs(piece) == WBISHOP:
        return bishop_moves(board, x, y, piece)
    if abs(piece) == WROOK:
        return rook_moves(board, x, y, piece)
    if abs(piece) == WQUEEN:
        return queen_moves(board, x, y, piece)
    if abs(piece) == WKING:
        return king_moves(board, x, y, piece)
    return []
