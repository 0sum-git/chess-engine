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
        self.setPieceAt(new_position, piece)
        self.setPieceAt(position, None)
        if piece:
            piece.setPosition(new_position)

    def find_piece(self, piece_type, color):
        for r in range(8):
            for c in range(8):
                piece = self.getPieceAt((r, c))
                if piece and piece.getType() == piece_type and piece.getColor() == color:
                    return piece
        return None

    def displayBoard(self):
        columns = ' '.join(f' {c} ' for c in 'abcdefgh')
        print('   ' + columns)
        for row_idx, row in enumerate(self.positions):
            line_number = 8 - row_idx
            print(f"{line_number} ", end=' ')
            for piece in row:
                if piece is None:
                    print(" . ", end=' ')
                else:
                    print(f" {piece.getSymbol()} ", end=' ')
            print(f" {line_number}")
        print('   ' + columns)