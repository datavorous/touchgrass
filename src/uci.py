from .backend.api import API
from .utils import coords_to_uci, uci_to_coords

class UCIHandler:
    def __init__(self, engine, api):
        self.engine = engine
        self.api = api
        self.running = True

    def handle_command(self, command):
        tokens = command.strip().split()
        if not tokens:
            return

        cmd = tokens[0]

        if cmd == "uci":
            print("id name touchgrass")
            print("id author datavorous")
            print("uciok")
        
        elif cmd == "isready":
            print("readyok")

        elif cmd == "ucinewgame":
            self.api = API()  # Reset game state
            
        elif cmd == "position":
            if len(tokens) < 2:
                return
                
            if tokens[1] == "startpos":
                self.api = API()  # Reset to starting position
                move_idx = 3 if len(tokens) > 2 and tokens[2] == "moves" else 2
            elif tokens[1] == "fen":
                # FEN support not implemented yet
                self.api = API()
                move_idx = 8 if len(tokens) > 7 and tokens[7] == "moves" else 7
            else:
                return

            # Apply all moves in sequence
            if move_idx < len(tokens):
                for move in tokens[move_idx:]:
                    coords = uci_to_coords(move)
                    if coords:
                        self.api.make_move(coords)

        elif cmd == "go":
            depth = 1  # Default depth
            for i in range(len(tokens)-1):
                if tokens[i] == "depth":
                    try:
                        depth = int(tokens[i+1])
                    except (ValueError, IndexError):
                        pass
                    break
                    
            # Get and output best move
            move = self.engine.get_best_move()
            if move:
                print(f"bestmove {coords_to_uci(move)}")
            else:
                print("bestmove 0000")  # No legal moves

        elif cmd == "quit":
            self.running = False

    def run(self):
        while self.running:
            try:
                command = input()
                self.handle_command(command)
            except EOFError:
                break
