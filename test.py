"""
This is not a real testing file
"""

from quoridor import *

board = QuoridorBoard()
p1 = board.add_player("player1")
p2 = board.add_player("player2")
board.add_fence(Fence("a3h"))
board.add_fence("c3h")
board.add_fence(FenceLocation("e3h"))
board.add_fence(Fence(FenceLocation("g3h")))
board.add_fence(Fence(FenceLocation("h3v")))
board.move_piece(p1, "a5")


print board.get_illegal_fences()
print board.blocked_fences
print board.get_legal_fences()

