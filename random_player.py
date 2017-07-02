"""
random_player.py

Just chooses a move at random. 50 percent chance of a fence,
50 percent change of a piece movement. (until fences run out).
"""

import random
from quoridor_base_player import QuoridorBasePlayer


class RandomPlayer(QuoridorBasePlayer):

    def handle_turn(self, board, piece, num_seconds):
        if random.randint(0, 1) and self.num_fences > 0:
            # choose a random fence to place
            return random.sample(board.get_legal_fences(), 1)[0]
        else:
            # choose a random place to move
            destination = board.get_legal_moves(piece)
            return random.sample(destination, 1)[0]
