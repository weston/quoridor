"""
bfs_player.py

Each turn this player does a BFS and makes a step in the direction
of the shortest path. This player does not play any fences.
"""

from quoridor import POSSIBLE_ROWS, POSSIBLE_COLUMNS, PieceMove
from quoridor_base_player import QuoridorBasePlayer


class BFSPlayer(QuoridorBasePlayer):

    def handle_turn(self, board, piece, num_seconds):
        destination = perform_bfs(piece.location, piece.goal_locations,
                board.blocked_moves)
        move = PieceMove(piece.location, destination)

        # We have to make sure that this is a legal move because
        # get_adjacent_locations does not take into consideration
        # fences or other pieces.
        if move in board.get_legal_moves(piece):
            return move
        return board.get_legal_moves(piece).pop()


def perform_bfs(start, goals, blocked_moves):
    #destination = board.get_legal_moves(piece)
    parents = {}    #Map from location to parent location
    seen = {start}
    queue = [start]
    current = None
    while len(queue):
        current = queue.pop()
        if current in goals:
            break
        for adj_loc in current.get_adjacent_locations():
            potential_move = PieceMove(current, adj_loc)
            if adj_loc not in seen and potential_move not in blocked_moves:
                seen.add(adj_loc)
                parents[adj_loc] = current
                queue = [adj_loc] + queue

    # follow the parents back up to the start
    parent = parents[current]
    while parent != start:
        current = parent
        parent = parents[parent]
    return current

