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
        self.has_moved = False

    def getType(self):
        return self.type
    
    def getColor(self):
        return self.color
    
    def getSymbol(self):
        return self.symbol.value
    
    def getPosition(self):
        return self.position
    
    def setPosition(self, position, moved=True):
        self.position = position
        if moved:
            self.has_moved = True
    
    def getPossibleMoves(self, board, en_passant_target=None):
        possible_moves = []
        r, c = self.position

        def in_bounds(row, col):
            return 0 <= row < 8 and 0 <= col < 8

        if self.type == PieceType.ROOK:
            directions = [(1,0), (-1,0), (0,1), (0,-1)]
        elif self.type == PieceType.BISHOP:
            directions = [(1,1), (1,-1), (-1,1), (-1,-1)]
        elif self.type == PieceType.QUEEN:
            directions = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]
        elif self.type == PieceType.KNIGHT:
            directions = [
                (r - 2, c - 1), (r - 2, c + 1), (r - 1, c - 2), (r - 1, c + 2),
                (r + 1, c - 2), (r + 1, c + 2), (r + 2, c - 1), (r + 2, c + 1)
            ]
            for move in directions:
                if in_bounds(move[0], move[1]):
                    target = board.getPieceAt(move)
                    if target is None or target.color != self.color:
                        possible_moves.append(move)
            return possible_moves
        elif self.type == PieceType.KING:
            directions = [
                (r - 1, c - 1), (r - 1, c), (r - 1, c + 1),
                (r, c - 1), (r, c + 1),
                (r + 1, c - 1), (r + 1, c), (r + 1, c + 1)
            ]
            for move in directions:
                if in_bounds(move[0], move[1]):
                    target = board.getPieceAt(move)
                    if target is None or target.color != self.color:
                        possible_moves.append(move)
            
            # castling logic
            if not self.has_moved:
                # kingside castling
                rook = board.getPieceAt((r, c + 3))
                if rook and rook.getType() == PieceType.ROOK and not rook.has_moved:
                    if board.getPieceAt((r, c + 1)) is None and board.getPieceAt((r, c + 2)) is None:
                        possible_moves.append((r, c + 2))

                # queenside castling
                rook = board.getPieceAt((r, c - 4))
                if rook and rook.getType() == PieceType.ROOK and not rook.has_moved:
                    if board.getPieceAt((r, c - 1)) is None and \
                       board.getPieceAt((r, c - 2)) is None and \
                       board.getPieceAt((r, c - 3)) is None:
                        possible_moves.append((r, c - 2))

            return possible_moves
        elif self.type == PieceType.PAWN:
            direction = -1 if self.color == Color.WHITE else 1
            start_row = 6 if self.color == Color.WHITE else 1

            # forward move
            one_step = r + direction
            if in_bounds(one_step, c) and board.getPieceAt((one_step, c)) is None:
                possible_moves.append((one_step, c))
                # initial double move
                if r == start_row:
                    two_steps = r + 2 * direction
                    if in_bounds(two_steps, c) and board.getPieceAt((two_steps, c)) is None:
                        possible_moves.append((two_steps, c))
            
            # captures
            for dc in [-1, 1]:
                capture_pos = (r + direction, c + dc)
                if in_bounds(capture_pos[0], capture_pos[1]):
                    target = board.getPieceAt(capture_pos)
                    if target is not None and target.color != self.color:
                        possible_moves.append(capture_pos)
            
            # en passant
            correct_rank = (self.color == Color.WHITE and r == 3) or \
                           (self.color == Color.BLACK and r == 4)

            if en_passant_target and correct_rank:
                # check if en_passant_target is adjacent to the pawn
                if abs(c - en_passant_target[1]) == 1 and r + direction == en_passant_target[0]:
                   possible_moves.append(en_passant_target)

            return possible_moves
        else:
            directions = []

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            while in_bounds(nr, nc):
                target = board.getPieceAt((nr, nc))
                if target is None:
                    possible_moves.append((nr, nc))
                else:
                    if target.color != self.color:
                        possible_moves.append((nr, nc))  
                    break  
                nr += dr
                nc += dc

        return possible_moves