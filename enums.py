from enum import Enum

class Color(str, Enum):
    WHITE = "white"
    BLACK = "black"
    
class PieceType(str, Enum):
    PAWN = "pawn"
    ROOK = "rook"
    KNIGHT = "knight"
    BISHOP = "bishop"
    QUEEN = "queen"
    KING = "king"

class PieceSymbol(str, Enum):
    WHITE_PAWN = "♙"
    WHITE_ROOK = "♖"
    WHITE_KNIGHT = "♘"
    WHITE_BISHOP = "♗"
    WHITE_QUEEN = "♕"
    WHITE_KING = "♔"
    BLACK_PAWN = "♟"
    BLACK_ROOK = "♜"
    BLACK_KNIGHT = "♞"
    BLACK_BISHOP = "♝"
    BLACK_QUEEN = "♛"
    BLACK_KING = "♚"
