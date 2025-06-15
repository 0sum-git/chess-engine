import engine


engine = engine.engine()

engine.getBoard().displayBoard()
while True:
    try:
        move = input("Enter your move (e.g., e2 e4): ")
        if move.lower() == "exit":
            break
        start, end = move.split()
        start_pos = (8 - int(start[1]), ord(start[0]) - ord('a'))
        end_pos = (8 - int(end[1]), ord(end[0]) - ord('a'))
        
        engine.getBoard().movePiece(start_pos, end_pos)
        engine.getBoard().displayBoard()
    except Exception as e:
        print(f"Error: {e}")