from enums import Color, PieceType, PieceSymbol
import board

class Move:
    def __init__(self, start_pos, end_pos, piece_moved, piece_captured=None, is_castling=False, is_en_passant=False, is_promotion=False, original_en_passant_target=None):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.piece_moved = piece_moved
        self.piece_captured = piece_captured
        self.is_castling = is_castling
        self.is_en_passant = is_en_passant
        self.is_promotion = is_promotion
        self.original_en_passant_target = original_en_passant_target
        # store has_moved state for the pieces involved
        self.piece_moved_had_moved = piece_moved.has_moved if piece_moved else False
        if piece_captured:
            self.piece_captured_had_moved = piece_captured.has_moved
        else:
            self.piece_captured_had_moved = False

class engine:
    def __init__(self):
        self.board = board.board()
        self.current_turn = Color.WHITE
        self.en_passant_target = None
        self.move_history = []
        self.board_history = {} # for repetition detection

    def get_board_hash(self):
        # creates a string representation of the board state
        board_str = ""
        for r in range(8):
            for c in range(8):
                piece = self.board.getPieceAt((r,c))
                if piece:
                    board_str += piece.getSymbol()
                else:
                    board_str += "."
        
        board_str += self.current_turn.value
        board_str += str(self.en_passant_target)
        
        # add castling rights
        for color in [Color.WHITE, Color.BLACK]:
            king = self.board.find_piece(PieceType.KING, color)
            if king and not king.has_moved:
                # simplification: only checks king. for full check, rooks are needed.
                board_str += 'K' if color == Color.WHITE else 'k'
        
        return board_str

    def getBoard(self):
        return self.board
    
    def makeMove(self, start_pos, end_pos):
        piece = self.board.getPieceAt(start_pos)

        if piece is None:
            raise ValueError("No piece at the starting position.")
        
        if piece.getColor() != self.current_turn:
            raise ValueError("Not your turn.")

        is_castling_move = piece.getType() == PieceType.KING and abs(start_pos[1] - end_pos[1]) == 2
        if is_castling_move:
            if self.is_in_check(self.current_turn):
                raise ValueError("Cannot castle while in check.")

            # check path for attacks
            path_col = (start_pos[1] + end_pos[1]) // 2
            path_pos = (start_pos[0], path_col)

            # temporarily move king to check for attack on path
            original_piece_at_path = self.board.getPieceAt(path_pos)
            self.board.setPieceAt(path_pos, piece)
            self.board.setPieceAt(start_pos, None)

            if self.is_in_check(self.current_turn):
                # undo temporary move
                self.board.setPieceAt(start_pos, piece)
                self.board.setPieceAt(path_pos, original_piece_at_path)
                raise ValueError("King passes through an attacked square during castling.")

            # undo temporary move
            self.board.setPieceAt(start_pos, piece)
            self.board.setPieceAt(path_pos, original_piece_at_path)

        possible_moves = piece.getPossibleMoves(self.board, self.en_passant_target)
        if end_pos not in possible_moves:
            raise ValueError("Invalid move for the piece.")

        # Armazena a peça capturada, se houver
        captured_piece = self.board.getPieceAt(end_pos)

        # save state for a potential undo
        original_en_passant_target = self.en_passant_target
        piece_moved_had_moved = piece.has_moved
        captured_piece_had_moved = captured_piece.has_moved if captured_piece else False
        
        is_en_passant = (piece.getType() == PieceType.PAWN and end_pos == self.en_passant_target)
        
        if is_en_passant:
            pawn_to_capture_pos = (end_pos[0] + (1 if self.current_turn == Color.WHITE else -1), end_pos[1])
            captured_pawn = self.board.getPieceAt(pawn_to_capture_pos)
            self.board.setPieceAt(pawn_to_capture_pos, None)
        
        # reset en passant target for next turn
        self.en_passant_target = None

        # set new en passant target if it's a double pawn push
        if piece.getType() == PieceType.PAWN and abs(start_pos[0] - end_pos[0]) == 2:
            self.en_passant_target = (start_pos[0] + (end_pos[0] - start_pos[0]) // 2, start_pos[1])

        is_castling = is_castling_move

        # move piece on the board
        self.board.setPieceAt(end_pos, piece)
        self.board.setPieceAt(start_pos, None)
        piece.setPosition(end_pos)

        if is_castling:
            # move the rook
            if end_pos[1] > start_pos[1]: # kingside
                rook_start = (start_pos[0], 7)
                rook_end = (start_pos[0], 5)
            else: # queenside
                rook_start = (start_pos[0], 0)
                rook_end = (start_pos[0], 3)
            rook = self.board.getPieceAt(rook_start)
            if rook:
                self.board.setPieceAt(rook_end, rook)
                self.board.setPieceAt(rook_start, None)
                rook.setPosition(rook_end)
        
        # check if move leaves king in check
        if self.is_in_check(self.current_turn):
            # undo the move
            self.board.setPieceAt(start_pos, piece)
            piece.setPosition(start_pos, moved=False)
            self.board.setPieceAt(end_pos, captured_piece)

            if is_castling:
                # undo rook move
                if end_pos[1] > start_pos[1]: # kingside
                    rook_start = (start_pos[0], 7)
                    rook_end = (start_pos[0], 5)
                else: # queenside
                    rook_start = (start_pos[0], 0)
                    rook_end = (start_pos[0], 3)
                rook = self.board.getPieceAt(rook_end)
                if rook:
                    self.board.setPieceAt(rook_start, rook)
                    self.board.setPieceAt(rook_end, None)
                    rook.setPosition(rook_start, moved=False)

            if is_en_passant:
                pawn_to_capture_pos = (end_pos[0] + (1 if self.current_turn == Color.WHITE else -1), end_pos[1])
                self.board.setPieceAt(pawn_to_capture_pos, captured_pawn)
            self.en_passant_target = original_en_passant_target
            raise ValueError("Move leaves king in check.")

        # pawn promotion
        is_promotion = False
        if piece.getType() == PieceType.PAWN:
            last_row = 0 if piece.getColor() == Color.WHITE else 7
            if end_pos[0] == last_row:
                # auto-promote to queen for simplicity
                promoted_piece = self.board.getPieceAt(end_pos)
                is_promotion = True
                promoted_piece.type = PieceType.QUEEN
                promoted_piece.symbol = PieceSymbol[f"{promoted_piece.color.value.upper()}_QUEEN"]

        # store move in history
        move = Move(start_pos, end_pos, piece, captured_piece, is_castling, is_en_passant, is_promotion, original_en_passant_target)
        move.piece_moved_had_moved = piece_moved_had_moved
        if captured_piece:
            move.piece_captured_had_moved = captured_piece_had_moved
        self.move_history.append(move)

        # add to board history for repetition
        board_hash = self.get_board_hash()
        self.board_history[board_hash] = self.board_history.get(board_hash, 0) + 1

        # switch turn
        self.switchTurn()

    def is_in_check(self, color):
        king = self.board.find_piece(PieceType.KING, color)
        if not king:
            return False # should not happen in a normal game
        
        king_pos = king.getPosition()
        opponent_color = Color.BLACK if color == Color.WHITE else Color.WHITE

        for r in range(8):
            for c in range(8):
                piece = self.board.getPieceAt((r, c))
                if piece and piece.getColor() == opponent_color:
                    possible_moves = piece.getPossibleMoves(self.board)
                    if king_pos in possible_moves:
                        return True
        return False

    def is_checkmate(self, color):
        if not self.is_in_check(color):
            return False

        # check if any legal move exists
        for r in range(8):
            for c in range(8):
                piece = self.board.getPieceAt((r,c))
                if piece and piece.getColor() == color:
                    start_pos = (r, c)
                    possible_moves = piece.getPossibleMoves(self.board, self.en_passant_target)
                    for end_pos in possible_moves:
                        # try the move
                        captured_piece = self.board.getPieceAt(end_pos)
                        self.board.setPieceAt(end_pos, piece)
                        self.board.setPieceAt(start_pos, None)
                        piece.setPosition(end_pos)
                        
                        # if the king is not in check anymore, it's not checkmate
                        if not self.is_in_check(color):
                            # undo the move
                            self.board.setPieceAt(start_pos, piece)
                            piece.setPosition(start_pos, moved=False)
                            self.board.setPieceAt(end_pos, captured_piece)
                            return False

                        # undo the move
                        self.board.setPieceAt(start_pos, piece)
                        piece.setPosition(start_pos, moved=False)
                        self.board.setPieceAt(end_pos, captured_piece)
        
        return True

    def is_stalemate(self, color):
        if self.is_in_check(color):
            return False

        # check if any legal move exists
        for r in range(8):
            for c in range(8):
                piece = self.board.getPieceAt((r,c))
                if piece and piece.getColor() == color:
                    start_pos = (r, c)
                    possible_moves = piece.getPossibleMoves(self.board, self.en_passant_target)
                    for end_pos in possible_moves:
                        # try the move
                        captured_piece = self.board.getPieceAt(end_pos)
                        self.board.setPieceAt(end_pos, piece)
                        self.board.setPieceAt(start_pos, None)
                        piece.setPosition(end_pos)
                        
                        # if king is not in check after move, not a stalemate
                        if not self.is_in_check(color):
                            # undo the move
                            self.board.setPieceAt(start_pos, piece)
                            piece.setPosition(start_pos, moved=False)
                            self.board.setPieceAt(end_pos, captured_piece)
                            return False

                        # undo the move
                        self.board.setPieceAt(start_pos, piece)
                        piece.setPosition(start_pos, moved=False)
                        self.board.setPieceAt(end_pos, captured_piece)
        
        return True

    def is_insufficient_material(self):
        pieces = [p for row in self.board.positions for p in row if p is not None]
        
        if len(pieces) <= 3:
            # k vs k
            if len(pieces) == 2:
                return True
            # k vs k+n or k vs k+b
            if len(pieces) == 3:
                if any(p.getType() in [PieceType.KNIGHT, PieceType.BISHOP] for p in pieces):
                    return True

        # check for "powerful" pieces
        if any(p.getType() in [PieceType.QUEEN, PieceType.ROOK, PieceType.PAWN] for p in pieces):
            return False
            
        return False

    def switchTurn(self):
        self.current_turn = Color.BLACK if self.current_turn == Color.WHITE else Color.WHITE
    
    def undo_last_move(self):
        if not self.move_history:
            print("No moves to undo.")
            return

        last_move = self.move_history.pop()
        
        # switch turn back
        self.switchTurn()

        # undo piece move
        piece = last_move.piece_moved
        self.board.setPieceAt(last_move.start_pos, piece)
        self.board.setPieceAt(last_move.end_pos, last_move.piece_captured)
        piece.has_moved = last_move.piece_moved_had_moved
        piece.position = last_move.start_pos

        if last_move.piece_captured:
            last_move.piece_captured.has_moved = last_move.piece_captured_had_moved

        # undo castling
        if last_move.is_castling:
            if last_move.end_pos[1] > last_move.start_pos[1]: # kingside
                rook_start = (last_move.start_pos[0], 7)
                rook_end = (last_move.start_pos[0], 5)
            else: # queenside
                rook_start = (last_move.start_pos[0], 0)
                rook_end = (last_move.start_pos[0], 3)
            rook = self.board.getPieceAt(rook_end)
            if rook:
                self.board.setPieceAt(rook_start, rook)
                self.board.setPieceAt(rook_end, None)
                rook.has_moved = False
        
        # undo en passant
        self.en_passant_target = last_move.original_en_passant_target
        if last_move.is_en_passant:
             pawn_to_capture_pos = (last_move.end_pos[0] + (1 if self.current_turn == Color.WHITE else -1), last_move.end_pos[1])
             self.board.setPieceAt(pawn_to_capture_pos, last_move.piece_captured)
             self.board.setPieceAt(last_move.end_pos, None)
        
        # undo promotion
        if last_move.is_promotion:
            piece.type = PieceType.PAWN
            piece.symbol = PieceSymbol[f"{piece.color.value.upper()}_PAWN"]
        
        # remove last state from repetition history
        board_hash = self.get_board_hash()
        if board_hash in self.board_history:
            self.board_history[board_hash] -= 1
            if self.board_history[board_hash] == 0:
                del self.board_history[board_hash]

    def is_repetition_draw(self):
        board_hash = self.get_board_hash()
        return self.board_history.get(board_hash, 0) >= 3
    