"""
players.py
"""
import random

from quoridor import (
    Fence,
    FenceLocation,
    PieceLocation,
    PieceMove,
    POSSIBLE_COLUMNS,
    POSSIBLE_ROWS,
)


class QuoridorBasePlayer(object):
    """
    Subclass QuoridorBasePlayer to implement your own quoridor bot.
    See below for examples
    """

    def __init__(self, num_fences, name="player_name"):
        self.num_fences = num_fences
        self.name = name
        self.move = None

    def handle_turn(self, board, piece, num_seconds):
        """
        num_seconds is the timeout for this function.
        This is not currently being enforced.

        THe board passed into handle_turn is a copy of the real board.
        So don't try to modify the board to cheat.

        legal_moves = piece.get_legal_moves()
        return legal_moves.pop()

        legal_fences = board.get_legal_fences()
        return legal_fences.pop()
        """
        raise NotImplementedError

    def __repr__(self):
        return self.name


class HumanPlayer(QuoridorBasePlayer):
    """
    Implements the QuoridorBasePlayer methods.
    Use this player to have manual move inputs.
    """

    def handle_turn(self, board, piece, num_seconds):
        print "\n========== ENTER ACTION  =========="
        print self.name + ": you are at " + str(piece.location)
        print "your legal moves are:"
        print piece.get_legal_destinations(board.pieces, board.blocked_moves)
        move_string = raw_input("Enter your next move: ")
        if len(move_string) == 3:
            return Fence(FenceLocation(move_string))
        if len(move_string) == 2:
            end_location = PieceLocation(move_string)
            return PieceMove(piece.location, end_location)


class RandomPlayer(QuoridorBasePlayer):
    """
    Randomly chooses a move out of the legal moves
    """

    def handle_turn(self, board, piece, num_seconds):
        if random.randint(0, 1) and self.num_fences > 0:
            # choose a random fence to place
            return random.sample(board.get_legal_fences(), 1)[0]
        else:
            # choose a random place to move
            destination = board.get_legal_moves(piece)
            return random.sample(destination, 1)[0]


class NoFencePlayer(QuoridorBasePlayer):
    """
    Randomly chooses a piece movement. Never places a fence.
    """

    def handle_turn(self, board, piece, num_seconds):
        moves = board.get_legal_moves(piece)
        return random.sample(moves, 1)[0]


class BFSPlayer(QuoridorBasePlayer):
    """
    Computes a BFS and takes a step in the direction of the shortest
    path to the end goal.
    """

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
    # destination = board.get_legal_moves(piece)
    parents = {}  # Map from location to parent location
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
