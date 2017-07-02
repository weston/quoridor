"""
human_player.py
"""
from quoridor import PieceLocation, PieceMove, Fence, FenceLocation
from quoridor_base_player import QuoridorBasePlayer

class HumanPlayer(QuoridorBasePlayer):
    """
    Implements the QuoridorBasePlayer methods.
    Use this player to have manual move inputs.
    """
    def handle_turn(self, board, piece, num_seconds):
        print "\n========== NEXT TURN =========="
        print self.name + ": you are at " + str(piece.location)
        move_string = raw_input("Enter your next move: ")
        if len(move_string) == 3:
            return Fence(FenceLocation(move_string))
        if len(move_string) == 2:
            end_location = PieceLocation(move_string)
            return PieceMove(piece.location, end_location)
