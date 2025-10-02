# Bitboard-based move generation
from .bitboard import *
from .board import WPAWN, WKNIGHT, WBISHOP, WROOK, WQUEEN, WKING
from .board import BPAWN, BKNIGHT, BBISHOP, BROOK, BQUEEN, BKING, EMPTY


def generate_pawn_moves(board, color):
    """Generate all pawn moves for the given color"""
    moves = []
    pawn_bb = board.piece_bitboards[color][PAWN]
    
    if color == WHITE:
        # White pawns move "up" (decreasing row numbers)
        # Single pawn push
        single_push = (pawn_bb >> 8) & ~board.all_pieces
        
        # Double pawn push (from starting rank)
        double_push = ((single_push & RANK_6) >> 8) & ~board.all_pieces
        
        # Pawn attacks
        attacks_left = (pawn_bb >> 7) & ~FILE_A & board.color_bitboards[BLACK]
        attacks_right = (pawn_bb >> 9) & ~FILE_H & board.color_bitboards[BLACK]
        
        # Convert moves to coordinate format
        while single_push:
            to_bit, single_push = pop_bit(single_push)
            from_bit = to_bit + 8
            moves.append((bit_to_square(from_bit), bit_to_square(to_bit)))
        
        while double_push:
            to_bit, double_push = pop_bit(double_push)
            from_bit = to_bit + 16
            moves.append((bit_to_square(from_bit), bit_to_square(to_bit)))
        
        while attacks_left:
            to_bit, attacks_left = pop_bit(attacks_left)
            from_bit = to_bit + 7
            moves.append((bit_to_square(from_bit), bit_to_square(to_bit)))
        
        while attacks_right:
            to_bit, attacks_right = pop_bit(attacks_right)
            from_bit = to_bit + 9
            moves.append((bit_to_square(from_bit), bit_to_square(to_bit)))
    
    else:  # BLACK
        # Black pawns move "down" (increasing row numbers)
        # Single pawn push
        single_push = (pawn_bb << 8) & ~board.all_pieces
        
        # Double pawn push (from starting rank)
        double_push = ((single_push & RANK_3) << 8) & ~board.all_pieces
        
        # Pawn attacks
        attacks_left = (pawn_bb << 9) & ~FILE_A & board.color_bitboards[WHITE]
        attacks_right = (pawn_bb << 7) & ~FILE_H & board.color_bitboards[WHITE]
        
        # Convert moves to coordinate format
        while single_push:
            to_bit, single_push = pop_bit(single_push)
            from_bit = to_bit - 8
            moves.append((bit_to_square(from_bit), bit_to_square(to_bit)))
        
        while double_push:
            to_bit, double_push = pop_bit(double_push)
            from_bit = to_bit - 16
            moves.append((bit_to_square(from_bit), bit_to_square(to_bit)))
        
        while attacks_left:
            to_bit, attacks_left = pop_bit(attacks_left)
            from_bit = to_bit - 9
            moves.append((bit_to_square(from_bit), bit_to_square(to_bit)))
        
        while attacks_right:
            to_bit, attacks_right = pop_bit(attacks_right)
            from_bit = to_bit - 7
            moves.append((bit_to_square(from_bit), bit_to_square(to_bit)))
    
    return moves


def generate_knight_moves(board, color):
    """Generate all knight moves for the given color"""
    moves = []
    knight_bb = board.piece_bitboards[color][KNIGHT]
    own_pieces = board.color_bitboards[color]
    
    while knight_bb:
        from_bit, knight_bb = pop_bit(knight_bb)
        attacks = KNIGHT_ATTACKS[from_bit] & ~own_pieces
        
        while attacks:
            to_bit, attacks = pop_bit(attacks)
            moves.append((bit_to_square(from_bit), bit_to_square(to_bit)))
    
    return moves


def generate_bishop_moves(board, color):
    """Generate all bishop moves for the given color"""
    moves = []
    bishop_bb = board.piece_bitboards[color][BISHOP]
    own_pieces = board.color_bitboards[color]
    
    while bishop_bb:
        from_bit, bishop_bb = pop_bit(bishop_bb)
        attacks = get_bishop_attacks(from_bit, board.all_pieces) & ~own_pieces
        
        while attacks:
            to_bit, attacks = pop_bit(attacks)
            moves.append((bit_to_square(from_bit), bit_to_square(to_bit)))
    
    return moves


def generate_rook_moves(board, color):
    """Generate all rook moves for the given color"""
    moves = []
    rook_bb = board.piece_bitboards[color][ROOK]
    own_pieces = board.color_bitboards[color]
    
    while rook_bb:
        from_bit, rook_bb = pop_bit(rook_bb)
        attacks = get_rook_attacks(from_bit, board.all_pieces) & ~own_pieces
        
        while attacks:
            to_bit, attacks = pop_bit(attacks)
            moves.append((bit_to_square(from_bit), bit_to_square(to_bit)))
    
    return moves


def generate_queen_moves(board, color):
    """Generate all queen moves for the given color"""
    moves = []
    queen_bb = board.piece_bitboards[color][QUEEN]
    own_pieces = board.color_bitboards[color]
    
    while queen_bb:
        from_bit, queen_bb = pop_bit(queen_bb)
        attacks = get_queen_attacks(from_bit, board.all_pieces) & ~own_pieces
        
        while attacks:
            to_bit, attacks = pop_bit(attacks)
            moves.append((bit_to_square(from_bit), bit_to_square(to_bit)))
    
    return moves


def generate_king_moves(board, color):
    """Generate all king moves for the given color"""
    moves = []
    king_bb = board.piece_bitboards[color][KING]
    own_pieces = board.color_bitboards[color]
    
    if king_bb:
        from_bit = lsb(king_bb)  # King is unique, so just get its position
        attacks = KING_ATTACKS[from_bit] & ~own_pieces
        
        while attacks:
            to_bit, attacks = pop_bit(attacks)
            moves.append((bit_to_square(from_bit), bit_to_square(to_bit)))
    
    return moves


def generate_pseudo_legal_moves(board, color):
    """Generate all pseudo-legal moves for the given color"""
    moves = []
    
    moves.extend(generate_pawn_moves(board, color))
    moves.extend(generate_knight_moves(board, color))
    moves.extend(generate_bishop_moves(board, color))
    moves.extend(generate_rook_moves(board, color))
    moves.extend(generate_queen_moves(board, color))
    moves.extend(generate_king_moves(board, color))
    
    return moves


def is_square_attacked_bb(board, square, by_color):
    """Check if a square is attacked by pieces of the given color using bitboards"""
    row, col = square
    target_bit = square_to_bit(row, col)
    
    # Check pawn attacks
    if by_color == WHITE:
        # White pawns attack diagonally "up" (from higher row numbers to lower)
        if target_bit < 56:  # Not on rank 8
            # Check if white pawns can attack this square
            pawn_attack_sources = 0
            if col > 0:  # Left attack (from pawn's perspective)
                pawn_attack_sources |= (1 << (target_bit + 7))
            if col < 7:  # Right attack (from pawn's perspective)
                pawn_attack_sources |= (1 << (target_bit + 9))
            
            if board.piece_bitboards[WHITE][PAWN] & pawn_attack_sources:
                return True
    else:  # BLACK
        # Black pawns attack diagonally "down" (from lower row numbers to higher)
        if target_bit >= 8:  # Not on rank 1
            # Check if black pawns can attack this square
            pawn_attack_sources = 0
            if col > 0:  # Left attack (from pawn's perspective)
                pawn_attack_sources |= (1 << (target_bit - 9))
            if col < 7:  # Right attack (from pawn's perspective)
                pawn_attack_sources |= (1 << (target_bit - 7))
            
            if board.piece_bitboards[BLACK][PAWN] & pawn_attack_sources:
                return True
    
    # Check knight attacks
    knight_attacks = KNIGHT_ATTACKS[target_bit]
    if board.piece_bitboards[by_color][KNIGHT] & knight_attacks:
        return True
    
    # Check bishop/queen diagonal attacks
    bishop_attacks = get_bishop_attacks(target_bit, board.all_pieces)
    if (board.piece_bitboards[by_color][BISHOP] | board.piece_bitboards[by_color][QUEEN]) & bishop_attacks:
        return True
    
    # Check rook/queen straight attacks
    rook_attacks = get_rook_attacks(target_bit, board.all_pieces)
    if (board.piece_bitboards[by_color][ROOK] | board.piece_bitboards[by_color][QUEEN]) & rook_attacks:
        return True
    
    # Check king attacks
    king_attacks = KING_ATTACKS[target_bit]
    if board.piece_bitboards[by_color][KING] & king_attacks:
        return True
    
    return False


def get_legal_moves_bb(board, color):
    """Generate all legal moves for the given color using bitboards"""
    pseudo_legal = generate_pseudo_legal_moves(board, color)
    legal_moves = []
    
    for move in pseudo_legal:
        # Apply the move
        record = board.apply_move(move)
        
        # Check if the king is in check after the move
        king_pos = board.wking_pos if color == WHITE else board.bking_pos
        enemy_color = BLACK if color == WHITE else WHITE
        
        if not is_square_attacked_bb(board, king_pos, enemy_color):
            legal_moves.append(move)
        
        # Undo the move
        board.undo_move(move, record)
    
    return legal_moves


# Legacy compatibility functions
def isSquareAttacked(board, x, y, by_white):
    """Legacy function for backward compatibility"""
    by_color = WHITE if by_white else BLACK
    return is_square_attacked_bb(board, (x, y), by_color)


def getLegalMoves(board, color):
    """Legacy function for backward compatibility"""
    color_index = WHITE if color == "white" else BLACK
    return get_legal_moves_bb(board, color_index)