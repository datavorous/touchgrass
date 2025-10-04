from .board import WPAWN, WKNIGHT, WBISHOP, WROOK, WQUEEN, WKING
from .board import EMPTY


def in_bounds(x, y):
    return 0 <= x < 8 and 0 <= y < 8


def pawn_moves(board_matrix, x, y, piece, en_passant_target=None):
    moves = []
    direction = -1 if piece > 0 else 1

    nx, ny = x + direction, y

    if in_bounds(nx, ny) and board_matrix[nx][ny] == EMPTY:
        moves.append((nx, ny))

        if (piece > 0 and x == 6) or (piece < 0 and x == 1):
            nx2 = nx + direction
            if in_bounds(nx2, ny) and board_matrix[nx2][ny] == EMPTY:
                moves.append((nx2, ny))

    # Regular diagonal captures
    for dy in [-1, 1]:
        nx, ny = x + direction, y + dy

        if (
            in_bounds(nx, ny)
            and board_matrix[nx][ny] != EMPTY
            and board_matrix[nx][ny] * piece < 0
        ):
            moves.append((nx, ny))

    # En passant capture
    if en_passant_target is not None:
        ep_x, ep_y = en_passant_target
        # Check if we can capture en passant (target square is diagonal to us)
        if abs(ep_y - y) == 1 and ep_x == x + direction:
            moves.append((ep_x, ep_y))

    return moves


def knight_moves(board_matrix, x, y, piece):
    moves = []
    jumps = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]

    for dx, dy in jumps:
        nx, ny = x + dx, y + dy

        if in_bounds(nx, ny) and (
            board_matrix[nx][ny] == EMPTY or board_matrix[nx][ny] * piece < 0
        ):
            moves.append((nx, ny))

    return moves


def sliding_moves(board_matrix, x, y, piece, directions):
    moves = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        while in_bounds(nx, ny):
            if board_matrix[nx][ny] == EMPTY:
                moves.append((nx, ny))
            elif board_matrix[nx][ny] * piece < 0:
                moves.append((nx, ny))
                break
            else:
                break
            nx += dx
            ny += dy
    return moves


def bishop_moves(board_matrix, x, y, piece):
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    return sliding_moves(board_matrix, x, y, piece, directions)


def rook_moves(board_matrix, x, y, piece):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    return sliding_moves(board_matrix, x, y, piece, directions)


def queen_moves(board_matrix, x, y, piece):
    return bishop_moves(board_matrix, x, y, piece) + rook_moves(
        board_matrix, x, y, piece
    )


def king_moves(board_matrix, x, y, piece):
    moves = []

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if in_bounds(nx, ny) and (
                board_matrix[nx][ny] == EMPTY or board_matrix[nx][ny] * piece < 0
            ):
                moves.append((nx, ny))
    return moves


def getPseudoLegalMoves(board_matrix, x, y, en_passant_target=None):
    piece = board_matrix[x][y]
    if piece == EMPTY:
        return []
    if abs(piece) == WPAWN:
        return pawn_moves(board_matrix, x, y, piece, en_passant_target)
    if abs(piece) == WKNIGHT:
        return knight_moves(board_matrix, x, y, piece)
    if abs(piece) == WBISHOP:
        return bishop_moves(board_matrix, x, y, piece)
    if abs(piece) == WROOK:
        return rook_moves(board_matrix, x, y, piece)
    if abs(piece) == WQUEEN:
        return queen_moves(board_matrix, x, y, piece)
    if abs(piece) == WKING:
        return king_moves(board_matrix, x, y, piece)
    return []
