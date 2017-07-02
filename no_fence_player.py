"""
no_fence_player.py

This player never uses fences, but just randomly chooses a
piece move to make each turn.
"""

import random
from quoridor_base_player import QuoridorBasePlayer


class NoFencePlayer(QuoridorBasePlayer):

    def handle_turn(self, board, piece, num_seconds):
            moves = board.get_legal_moves(piece)
            return random.sample(moves, 1)[0]
