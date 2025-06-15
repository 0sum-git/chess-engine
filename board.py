from enums import PieceType, Color
import piece

class board:
    def __init__(self):
        self.positions = [[None for _ in range(8)] for _ in range(8)]
        self.initialize_pieces()
      
    def initialize_pieces(self):
        for i in range(8):
            self.positions[6][i] = piece.piece(PieceType.PAWN, Color.WHITE, (6, i))
        for i in range(8):
            self.positions[1][i] = piece.piece(PieceType.PAWN, Color.BLACK, (1, i))
        back_row = [PieceType.ROOK, PieceType.KNIGHT, PieceType.BISHOP, PieceType.QUEEN,
                    PieceType.KING, PieceType.BISHOP, PieceType.KNIGHT, PieceType.ROOK]
        for i in range(8):
            self.positions[7][i] = piece.piece(back_row[i], Color.WHITE, (7, i))
            self.positions[0][i] = piece.piece(back_row[i], Color.BLACK, (0, i))

    def getPieceAt(self, position):
        row, col = position
        return self.positions[row][col]

    def setPieceAt(self, position, piece):
        row, col = position
        self.positions[row][col] = piece

    def movePiece(self, position, new_position):
        piece = self.getPieceAt(position)
        if piece is None:
            raise ValueError("No piece at the starting position.")
        possible_moves = piece.getPossibleMoves() 
            self.setPieceAt(new_position, piece)
            self.setPieceAt(position, None)
            piece.setPosition(new_position)
        else:
            raise ValueError("Invalid move for the piece.")

    def displayBoard(self):
        for row in self.positions:
            for piece in row:
                if piece is None:
                    print(" . ", end="")
                else:
                    print(f" {piece.getSymbol()} ", end="")
            print("\n")
