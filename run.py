import engine


engine = engine.engine()

engine.getBoard().displayBoard()
while True:
    try:
        turn_color = engine.current_turn.value.capitalize()
        move = input(f"({turn_color}) enter your move (e.g., e2 e4): ")
        if move.lower() == "exit":
            break
        if move.lower() == "undo":
            engine.undo_last_move()
            engine.getBoard().displayBoard()
            continue
        start, end = move.split()
        start_pos = (8 - int(start[1]), ord(start[0]) - ord('a'))
        end_pos = (8 - int(end[1]), ord(end[0]) - ord('a'))
        
        engine.makeMove(start_pos, end_pos)
        engine.getBoard().displayBoard()

        opponent_color = engine.current_turn
        if engine.is_checkmate(opponent_color):
            winner = "White" if opponent_color == Color.BLACK else "Black"
            print(f"Checkmate! {winner} wins.")
            break
        elif engine.is_stalemate(opponent_color):
            print("Draw by stalemate.")
            break
        elif engine.is_insufficient_material():
            print("Draw by insufficient material.")
            break
        elif engine.is_repetition_draw():
            print("Draw by repetition.")
            break
        elif engine.is_in_check(opponent_color):
            print(f"{opponent_color.value.capitalize()} is in check!")

    except Exception as e:
        print(f"Error: {e}")