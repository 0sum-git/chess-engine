from enums import PieceType, Color, PieceSymbol

class piece:
    def __init__(self, type: PieceType , color : Color, position):
        self.type = type
        self.color = color
        if color == Color.WHITE:
            self.symbol = PieceSymbol[f"WHITE_{type.upper()}"]
        else:
            self.symbol = PieceSymbol[f"BLACK_{type.upper()}"]
        self.position = position

    def getType(self):
        return self.type
    
    def getColor(self):
        return self.color
    
    def getSymbol(self):
        return self.symbol.value
    
    def getPosition(self):
        return self.position
    
    def setPosition(self, position):
        self.position = position
    
    def getPossibleMoves(self):

        possible_moves = []
        r, c = self.position

        def in_bounds(pos):
            return 0 <= pos[0] < 8 and 0 <= pos[1] < 8
    
        match self.type:
            case PieceType.PAWN:
                direction = -1 if self.color == Color.WHITE else 1
                forward = (r + direction, c)
                if in_bounds(forward):
                    possible_moves.append(forward)

            case PieceType.ROOK:
                possible_moves.extend([(r + i, c) for i in range(-7, 8) if i != 0 and in_bounds((r + i, c))])
                possible_moves.extend([(r, c + i) for i in range(-7, 8) if i != 0 and in_bounds((r, c + i))])

            case PieceType.KNIGHT:
                knight_moves = [
                    (r+2, c+1), (r+2, c-1), (r-2, c+1), (r-2, c-1),
                    (r+1, c+2), (r+1, c-2), (r-1, c+2), (r-1, c-2)
                ]
                possible_moves.extend([pos for pos in knight_moves if in_bounds(pos)])

            case PieceType.BISHOP:
                possible_moves.extend([(r + i, c + i) for i in range(-7, 8) if i != 0 and in_bounds((r + i, c + i))])
                possible_moves.extend([(r + i, c - i) for i in range(-7, 8) if i != 0 and in_bounds((r + i, c - i))])

            case PieceType.QUEEN:
                possible_moves.extend([(r + i, c) for i in range(-7, 8) if i != 0 and in_bounds((r + i, c))])
                possible_moves.extend([(r, c + i) for i in range(-7, 8) if i != 0 and in_bounds((r, c + i))])
                possible_moves.extend([(r + i, c + i) for i in range(-7, 8) if i != 0 and in_bounds((r + i, c + i))])
                possible_moves.extend([(r + i, c - i) for i in range(-7, 8) if i != 0 and in_bounds((r + i, c - i))])

            case PieceType.KING:
                king_moves = [(r + i, c + j) for i in range(-1, 2) for j in range(-1, 2) if not (i == 0 and j == 0)]
                possible_moves.extend([pos for pos in king_moves if in_bounds(pos)])

        return possible_moves    
        
    