from .pieces import getPseudoLegalMoves, in_bounds
from .board import WPAWN, WKNIGHT, WBISHOP, WROOK, WQUEEN, WKING
from .board import EMPTY
from .board import BPAWN, BKNIGHT, BBISHOP, BROOK, BQUEEN, BKING


def isSquareAttacked(board, x, y, by_white):
    # pawns
    direction = 1 if by_white else -1
    for dy in [-1, 1]:
        nx, ny = x + direction, y + dy
        if in_bounds(nx, ny) and board.board[nx][ny] == (WPAWN if by_white else BPAWN):
            return True

    # knights
    for dx, dy in [
        (2, 1),
        (1, 2),
        (-1, 2),
        (-2, 1),
        (-2, -1),
        (-1, -2),
        (1, -2),
        (2, -1),
    ]:
        nx, ny = x + dx, y + dy
        if in_bounds(nx, ny) and board.board[nx][ny] == (
            WKNIGHT if by_white else BKNIGHT
        ):
            return True

    # bishops queens
    for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        nx, ny = x + dx, y + dy
        while in_bounds(nx, ny):
            p = board.board[nx][ny]
            if p != EMPTY:
                if p == (WBISHOP if by_white else BBISHOP) or p == (
                    WQUEEN if by_white else BQUEEN
                ):
                    return True
                break
            nx += dx
            ny += dy

    # rooks queens
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        while in_bounds(nx, ny):
            p = board.board[nx][ny]
            if p != EMPTY:
                if p == (WROOK if by_white else BROOK) or p == (
                    WQUEEN if by_white else BQUEEN
                ):
                    return True
                break
            nx += dx
            ny += dy

    # king
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if in_bounds(nx, ny) and board.board[nx][ny] == (
                WKING if by_white else BKING
            ):
                return True

    return False


def getEnPassantMoves(board, color, history):
    if not history:
        return []

    row = 3 if color == "white" else 4
    endingRow = row - 1 if color == "white" else row + 1
    enemyPawnStart = 1 if color == "white" else 6
    enemyPawn = BPAWN if color == "white" else WPAWN
    pawn = WPAWN if color == "white" else BPAWN
    moves = []

    # check last move was double pawn move
    lastMove = history[-1]
    if (
        lastMove.moved_piece == enemyPawn
        and lastMove.to_sq[0] == row
        and lastMove.from_sq[0] == enemyPawnStart
        and board[endingRow][lastMove.to_sq[1]] == EMPTY
    ):
        # Get adjacent player pawns
        cols = (lastMove.to_sq[1] - 1, lastMove.to_sq[1] + 1)
        for col in cols:
            if in_bounds(row, col) and board[row][col] == pawn:
                moves.append(((row, col), (endingRow, lastMove.to_sq[1])))
    return moves


def canCastle(board, color, side, history):
    row = 7 if color == "white" else 0
    king = WKING if color == "white" else BKING
    castle_rook = WROOK if color == "white" else BROOK
    by_white = color == "black"

    #  (SHORT)
    if side == "SHORT":
        # LOS CHECK AND Verigying if King and rook are at home positions
        if (
            board.board[row][5] == 0
            and board.board[row][6] == 0
            and board.board[row][7] == castle_rook
            and board.board[row][4] == king
            and all(
                not isSquareAttacked(board, row, col, by_white=by_white)
                for col in [4, 5, 6]
            )
        ):
            # History check if any of them has moved in the past
            for move in history:
                if move.moved_piece == king:
                    return False
                elif move.moved_piece == castle_rook and move.from_sq == (row, 7):
                    return False
            return True
        return False

    #  (LONG)
    elif side == "LONG":
        # LOS CHECK AND Verigying if King and rook are at home positions
        if (
            board.board[row][1] == 0
            and board.board[row][2] == 0
            and board.board[row][3] == 0
            and board.board[row][0] == castle_rook
            and board.board[row][4] == king
            and all(
                not isSquareAttacked(board, row, col, by_white=by_white)
                for col in [4, 3, 2]
            )
        ):
            # History check if any of them has moved in the past
            for move in history:
                if move.moved_piece == king:
                    return False
                elif move.moved_piece == castle_rook and move.from_sq == (row, 0):
                    return False
            return True
        return False

    return False


def getLegalMoves(board, color, history):
    moves = []

    for x in range(8):
        for y in range(8):
            piece = board.board[x][y]
            if piece == 0:
                continue
            if color == "white" and piece < 0:
                continue
            if color == "black" and piece > 0:
                continue

            for nx, ny in getPseudoLegalMoves(board.board, x, y):
                move = ((x, y), (nx, ny))

                record = board.apply_move(move)

                king_pos = board.wking_pos if color == "white" else board.bking_pos
                if not isSquareAttacked(board, *king_pos, by_white=(color == "black")):
                    moves.append(move)

                board.undo_move(move, record)

    # EN PASSANT LOGIC

    for move in getEnPassantMoves(board.board, color, history):
        record = board.apply_move(move)

        king_pos = board.wking_pos if color == "white" else board.bking_pos
        if not isSquareAttacked(board, *king_pos, by_white=(color == "black")):
            moves.append(move)

        board.undo_move(move, record)

    # CASTLING LOGIC

    row = 7 if color == "white" else 0
    king_start = (row, 4)

    # (SHORT) castling
    if canCastle(board, color, "SHORT", history):
        rook_start = (row, 7)
        # King moves
        moves.append((king_start, (row, 6)))

    # (LONG) castling
    if canCastle(board, color, "LONG", history):
        rook_start = (row, 0)
        # King moves
        moves.append((king_start, (row, 2)))

    return moves
