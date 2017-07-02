"""
quoridor_base_player.py
"""
from quoridor import QuoridorBoard


class QuoridorBasePlayer(object):


    def __init__(self, num_fences, name="player_name"):
        self.num_fences = num_fences
        self.name = name
        self.move = None

    def handle_turn(self, board, piece, num_seconds):
        """
        this function will be run for num_seconds seconds
        if this function has not returned by then, it will use
        self.move as the move. Should be subclassed for a custom
        self.move = None
        player.
        THe board passed into handle_turn is a copy of the real board.
        So don't try to modify the board to cheat.

        legal_moves = piece.get_legal_moves()
        return legal_moves.pop()

        legal_fences = board.get_legal_fences()
        return legal_fences.pop()
        """
        raise NotImplementedError

