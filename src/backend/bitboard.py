# Bitboard utilities for chess engine
# Each bitboard is a 64-bit integer representing piece positions on the board
# Bit 0 = a1, Bit 1 = b1, ..., Bit 7 = h1, Bit 8 = a2, ..., Bit 63 = h8

# Piece types
PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING = 0, 1, 2, 3, 4, 5
WHITE, BLACK = 0, 1

# Square mapping: (row, col) to bit index
def square_to_bit(row, col):
    """Convert (row, col) coordinates to bit index"""
    return row * 8 + col

def bit_to_square(bit):
    """Convert bit index to (row, col) coordinates"""
    return bit // 8, bit % 8

# Bitboard operations
def set_bit(bitboard, bit):
    """Set a bit in the bitboard"""
    return bitboard | (1 << bit)

def clear_bit(bitboard, bit):
    """Clear a bit in the bitboard"""
    return bitboard & ~(1 << bit)

def get_bit(bitboard, bit):
    """Check if a bit is set in the bitboard"""
    return (bitboard >> bit) & 1

def pop_bit(bitboard):
    """Remove and return the least significant bit"""
    if bitboard == 0:
        return 0, 0
    bit = (bitboard & -bitboard).bit_length() - 1
    return bit, bitboard & (bitboard - 1)

def count_bits(bitboard):
    """Count the number of set bits"""
    return bin(bitboard).count('1')

def lsb(bitboard):
    """Get the least significant bit index"""
    if bitboard == 0:
        return -1
    return (bitboard & -bitboard).bit_length() - 1

# Direction constants for sliding pieces
NORTH = 8
SOUTH = -8
EAST = 1
WEST = -1
NORTHEAST = 9
NORTHWEST = 7
SOUTHEAST = -7
SOUTHWEST = -9

# File and rank masks
FILE_A = 0x0101010101010101
FILE_B = 0x0202020202020202
FILE_C = 0x0404040404040404
FILE_D = 0x0808080808080808
FILE_E = 0x1010101010101010
FILE_F = 0x2020202020202020
FILE_G = 0x4040404040404040
FILE_H = 0x8080808080808080

RANK_1 = 0x00000000000000FF
RANK_2 = 0x000000000000FF00
RANK_3 = 0x0000000000FF0000
RANK_4 = 0x00000000FF000000
RANK_5 = 0x000000FF00000000
RANK_6 = 0x0000FF0000000000
RANK_7 = 0x00FF000000000000
RANK_8 = 0xFF00000000000000

FILES = [FILE_A, FILE_B, FILE_C, FILE_D, FILE_E, FILE_F, FILE_G, FILE_H]
RANKS = [RANK_1, RANK_2, RANK_3, RANK_4, RANK_5, RANK_6, RANK_7, RANK_8]

# Edge masks (for preventing wrap-around in move generation)
NOT_A_FILE = ~FILE_A
NOT_H_FILE = ~FILE_H
NOT_AB_FILE = ~(FILE_A | FILE_B)
NOT_GH_FILE = ~(FILE_G | FILE_H)

# Knight move masks
KNIGHT_ATTACKS = [0] * 64
def init_knight_attacks():
    for square in range(64):
        row, col = bit_to_square(square)
        attacks = 0
        
        # Knight moves: 8 possible L-shaped moves
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                attacks = set_bit(attacks, square_to_bit(new_row, new_col))
        
        KNIGHT_ATTACKS[square] = attacks

# King move masks
KING_ATTACKS = [0] * 64
def init_king_attacks():
    for square in range(64):
        row, col = bit_to_square(square)
        attacks = 0
        
        # King moves: 8 directions
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    attacks = set_bit(attacks, square_to_bit(new_row, new_col))
        
        KING_ATTACKS[square] = attacks

# Pawn attack masks
WHITE_PAWN_ATTACKS = [0] * 64
BLACK_PAWN_ATTACKS = [0] * 64

def init_pawn_attacks():
    for square in range(64):
        row, col = bit_to_square(square)
        
        # White pawn attacks (moving up the board, decreasing row)
        white_attacks = 0
        if row > 0:  # Not on first rank
            if col > 0:  # Can attack left
                white_attacks = set_bit(white_attacks, square_to_bit(row - 1, col - 1))
            if col < 7:  # Can attack right
                white_attacks = set_bit(white_attacks, square_to_bit(row - 1, col + 1))
        WHITE_PAWN_ATTACKS[square] = white_attacks
        
        # Black pawn attacks (moving down the board, increasing row)
        black_attacks = 0
        if row < 7:  # Not on last rank
            if col > 0:  # Can attack left
                black_attacks = set_bit(black_attacks, square_to_bit(row + 1, col - 1))
            if col < 7:  # Can attack right
                black_attacks = set_bit(black_attacks, square_to_bit(row + 1, col + 1))
        BLACK_PAWN_ATTACKS[square] = black_attacks

# Sliding piece attack generation
def get_rook_attacks(square, occupancy):
    """Generate rook attacks for a given square and occupancy"""
    attacks = 0
    row, col = bit_to_square(square)
    
    # North
    for r in range(row - 1, -1, -1):
        bit = square_to_bit(r, col)
        attacks = set_bit(attacks, bit)
        if get_bit(occupancy, bit):
            break
    
    # South
    for r in range(row + 1, 8):
        bit = square_to_bit(r, col)
        attacks = set_bit(attacks, bit)
        if get_bit(occupancy, bit):
            break
    
    # West
    for c in range(col - 1, -1, -1):
        bit = square_to_bit(row, c)
        attacks = set_bit(attacks, bit)
        if get_bit(occupancy, bit):
            break
    
    # East
    for c in range(col + 1, 8):
        bit = square_to_bit(row, c)
        attacks = set_bit(attacks, bit)
        if get_bit(occupancy, bit):
            break
    
    return attacks

def get_bishop_attacks(square, occupancy):
    """Generate bishop attacks for a given square and occupancy"""
    attacks = 0
    row, col = bit_to_square(square)
    
    # Northeast
    r, c = row - 1, col + 1
    while r >= 0 and c < 8:
        bit = square_to_bit(r, c)
        attacks = set_bit(attacks, bit)
        if get_bit(occupancy, bit):
            break
        r -= 1
        c += 1
    
    # Northwest
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0:
        bit = square_to_bit(r, c)
        attacks = set_bit(attacks, bit)
        if get_bit(occupancy, bit):
            break
        r -= 1
        c -= 1
    
    # Southeast
    r, c = row + 1, col + 1
    while r < 8 and c < 8:
        bit = square_to_bit(r, c)
        attacks = set_bit(attacks, bit)
        if get_bit(occupancy, bit):
            break
        r += 1
        c += 1
    
    # Southwest
    r, c = row + 1, col - 1
    while r < 8 and c >= 0:
        bit = square_to_bit(r, c)
        attacks = set_bit(attacks, bit)
        if get_bit(occupancy, bit):
            break
        r += 1
        c -= 1
    
    return attacks

def get_queen_attacks(square, occupancy):
    """Generate queen attacks (combination of rook and bishop)"""
    return get_rook_attacks(square, occupancy) | get_bishop_attacks(square, occupancy)

# Initialize attack tables
init_knight_attacks()
init_king_attacks()
init_pawn_attacks()

def print_bitboard(bitboard):
    """Print a bitboard in a readable 8x8 format"""
    for row in range(8):
        for col in range(8):
            bit = square_to_bit(row, col)
            if get_bit(bitboard, bit):
                print("1 ", end="")
            else:
                print("0 ", end="")
        print()
    print()