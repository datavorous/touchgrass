"""
UCI (Universal Chess Interface) protocol implementation for touchgrass chess engine.
This allows the engine to be used with chess GUIs like Arena, CuteChess, or Lichess-bot.
"""

import sys
from typing import Optional, List
from .backend.api import API
from .engine.dumbo import DumboEngine
from .utils import uci_to_coords, coords_to_uci


class UCIProtocol:
    """Handles UCI protocol communication with chess GUIs."""
    
    def __init__(self):
        self.api = API()
        self.engine = DumboEngine(self.api)
        self.running = True
        
    def run(self):
        """Main UCI protocol loop."""
        while self.running:
            try:
                line = input().strip()
                if not line:
                    continue
                    
                self.handle_command(line)
            except EOFError:
                break
            except KeyboardInterrupt:
                break
                
    def handle_command(self, command: str):
        """Handle incoming UCI commands."""
        parts = command.split()
        if not parts:
            return
            
        cmd = parts[0].lower()
        
        if cmd == "uci":
            self.handle_uci()
        elif cmd == "isready":
            self.handle_isready()
        elif cmd == "ucinewgame":
            self.handle_ucinewgame()
        elif cmd == "position":
            self.handle_position(parts[1:])
        elif cmd == "go":
            self.handle_go(parts[1:])
        elif cmd == "quit":
            self.handle_quit()
        else:
            # Ignore unknown commands
            pass
            
    def handle_uci(self):
        """Respond to uci command with engine identification."""
        print("id name touchgrass")
        print("id author datavorous")
        print("uciok")
        
    def handle_isready(self):
        """Respond to isready command."""
        print("readyok")
        
    def handle_ucinewgame(self):
        """Reset the game state for a new game."""
        self.api = API()
        self.engine = DumboEngine(self.api)
        
    def handle_position(self, args: List[str]):
        """Handle position command: position startpos moves ... or position fen ..."""
        if not args:
            return
            
        if args[0] == "startpos":
            # Reset to starting position
            self.api = API()
            self.engine = DumboEngine(self.api)
            
            # Apply moves if provided
            if len(args) > 1 and args[1] == "moves":
                moves = args[2:]
                for move_str in moves:
                    self.apply_move_from_uci(move_str)
                    
        elif args[0] == "fen":
            # Parse FEN position
            if len(args) < 2:
                return
                
            # Reconstruct FEN string (handle spaces in FEN)
            fen_parts = []
            i = 1
            while i < len(args) and args[i] != "moves":
                fen_parts.append(args[i])
                i += 1
            
            fen_string = " ".join(fen_parts)
            
            try:
                self.api.set_position_from_fen(fen_string)
                self.engine = DumboEngine(self.api)
                
                # Apply moves if provided
                if i < len(args) and args[i] == "moves":
                    moves = args[i + 1:]
                    for move_str in moves:
                        self.apply_move_from_uci(move_str)
            except ValueError:
                # Invalid FEN, ignore
                pass
            
    def handle_go(self, args: List[str]):
        """Handle go command and return best move."""
        # Parse depth if provided
        depth = 1
        if "depth" in args:
            try:
                depth_idx = args.index("depth")
                if depth_idx + 1 < len(args):
                    depth = int(args[depth_idx + 1])
            except (ValueError, IndexError):
                pass
                
        # Get best move from engine
        best_move = self.engine.get_best_move()
        
        if best_move:
            move_str = coords_to_uci(best_move)
            print(f"bestmove {move_str}")
        else:
            # No legal moves available
            print("bestmove 0000")
            
    def handle_quit(self):
        """Handle quit command."""
        self.running = False
        
    def apply_move_from_uci(self, move_str: str):
        """Apply a move from UCI notation to the current position."""
        try:
            move = uci_to_coords(move_str)
            self.api.make_move(move)
        except (ValueError, IndexError):
            # Invalid move format, ignore
            pass


def main():
    """Main entry point for UCI protocol."""
    uci = UCIProtocol()
    uci.run()


if __name__ == "__main__":
    main()
