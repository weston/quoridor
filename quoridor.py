"""
quoridor.py
"""
POSSIBLE_ROWS = [str(i) for i in range(9)]
POSSIBLE_COLUMNS = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]


class QuoridorBoard(object):

    def __init__(self):
        """
        Initializes the quoridor board
        """
        self.fences = []
        self.pieces = []
        self.foobar = []
        self.complete = False

        # fencelocations that are physically blocked by other fences
        self.blocked_fences = set()
        # fencelocations that are illegal because they would lock a player in
        self.illegal_fences = set()
        # moves that are blocked by fences
        self.blocked_moves = set()

        self.all_fence_locations = set()
        for col in POSSIBLE_COLUMNS[:-1]:
            for row in POSSIBLE_ROWS[:-1]:
                self.all_fence_locations.add(Fence(
                    FenceLocation(col + row + "v")))
                self.all_fence_locations.add(Fence(
                    FenceLocation(col + row + "h")))

    def add_player(self, player_name):
        assert isinstance(player_name, basestring)
        start_location = ("a4", "i4", "e0", "e8")[len(self.pieces)]
        piece = Piece(PieceLocation(start_location))
        piece.name = player_name
        self.pieces.append(piece)
        return piece

    def add_fence(self, fence):
        if isinstance(fence, basestring):
            fence = FenceLocation(fence)
        if isinstance(fence, FenceLocation):
            fence = Fence(fence)
        assert isinstance(fence, Fence)
        assert fence not in self.blocked_fences
        assert fence not in self.illegal_fences
        self.fences.append(fence)
        self.blocked_fences |= fence.get_blocked_fences()
        self.blocked_moves |= fence.get_blocked_moves()
        self.illegal_fences = self.get_illegal_fences()
        return fence

    def move_piece(self, piece, piece_move):
        assert isinstance(piece_move, PieceMove)
        # assert this piece is not hopping over a fence
        assert piece_move not in self.blocked_moves

        # assert this piece is not moving off the board
        assert piece_move.start.column in POSSIBLE_COLUMNS
        assert piece_move.start.row in POSSIBLE_ROWS
        assert piece_move.end.column in POSSIBLE_COLUMNS
        assert piece_move.end.row in POSSIBLE_ROWS

        # assert that piece_move is a valid move for piece
        assert piece_move.end in piece.get_legal_destinations(self.pieces,
                                                              self.blocked_moves)

        piece.location = piece_move.end
        if piece.location in piece.goal_locations:
            self.declare_winner(piece)
        self.illegal_fences = self.get_illegal_fences()

    def declare_winner(self, piece):
        print piece.name + " wins!"
        self.complete = True

    def get_legal_fences(self):
        return self.all_fence_locations - (self.blocked_fences |
                                           self.illegal_fences)

    def get_legal_moves(self, piece):
        legal_destinations = piece.get_legal_destinations(
            self.pieces, self.blocked_moves)
        return {PieceMove(piece.location, dst) for dst in legal_destinations}

    def get_illegal_fences(self):
        illegal_fences = set()
        for fence in self.all_fence_locations - self.blocked_fences:
            for piece in self.pieces:
                if self._piece_is_blocked(piece.goal_locations, piece.location,
                                          fence, set()):
                    illegal_fences.add(fence)
                    break
        return illegal_fences

    def _piece_is_blocked(self, goal_locations, location, fence, seen):
        if location in goal_locations:
            return False
        seen.add(location)
        blocked_moves = self.blocked_moves | fence.get_blocked_moves()
        for adj_loc in location.get_adjacent_locations():
            move = PieceMove(location, adj_loc)
            if move not in blocked_moves and adj_loc not in seen:
                if not self._piece_is_blocked(
                        goal_locations, adj_loc, fence, seen):
                    return False
        return True


class Fence(object):

    def __init__(self, fence_location):
        """
        Pass in a valid Fencelocation to init the fence
        """
        if isinstance(fence_location, FenceLocation):
            self.location = fence_location
            self.location_str = fence_location.location_str
        else:
            self.location = FenceLocation(fence_location)
            self.location_str = fence_location

    def get_blocked_moves(self):
        """
        Returns a list of piece movements that are now blocked
        based on the location of the fence. Some of these
        may be invalid moves, but that is okay.
        """
        nw = PieceLocation(self.location.column + self.location.row)
        sw = PieceLocation(self.location.column + self.location.add_row(1))
        ne = PieceLocation(self.location.add_column(1) + self.location.row)
        se = PieceLocation(self.location.add_column(1) +
                           self.location.add_row(1))
        if self.location.is_horizontal():
            return set([PieceMove(nw, sw), PieceMove(ne, se), PieceMove(sw, nw),
                        PieceMove(se, ne)])
        return set([PieceMove(nw, ne), PieceMove(sw, se), PieceMove(ne, nw),
                    PieceMove(se, sw)])

    def get_blocked_fences(self):
        """
        Returns a list o the illegal fence placements caused
        by placing this fence. Does NOT include the fences that
        are illegal because the player would be boxed in.
        """
        orientation = self.location.orientation
        blocked_fences = [
            Fence(self.location),
            Fence(self.location.perpendicular_fencelocation())
        ]
        if self.location.is_horizontal():
            blocked_fences.extend([
                Fence(FenceLocation(
                    self.location.add_column(-1) + self.location.row + "h")),
                Fence(FenceLocation(
                    self.location.add_column(1) + self.location.row + "h")),
            ])
        else:
            blocked_fences.extend([
                Fence(FenceLocation(
                    self.location.column + self.location.add_row(-1) + "v")),
                Fence(FenceLocation(
                    self.location.column + self.location.add_row(1) + "v")),
            ])
        return set(blocked_fences)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.location == other.location
        return False

    def __hash__(self):
        return hash(self.location)

    def __repr__(self):
        return "Fence at " + str(self.location)


class Piece(object):

    def __init__(self, start_location, name="Player"):
        """
        staart location can be either a start location string, or
        a StartPosition object.
        """
        if isinstance(start_location, PieceLocation):
            self.start_location = start_location
            self.location = start_location
        else:
            self.start_location = PieceLocation(start_location)
            self.location = PieceLocation(start_location)
        self.name = name
        self.goal_locations = self._get_goal_locations()

    def _get_goal_locations(self):
        if self.start_location.location_str == "a4":
            return [PieceLocation("i" + str(row)) for row in POSSIBLE_ROWS]
        if self.start_location.location_str == "i4":
            return [PieceLocation("a" + str(row)) for row in POSSIBLE_ROWS]
        if self.start_location.location_str == "e0":
            return [PieceLocation(col + "8") for col in POSSIBLE_COLUMNS]
        if self.start_location.location_str == "e8":
            return [PieceLocation(col + "0") for col in POSSIBLE_COLUMNS]
        raise Exception("invalid start location")

    def get_legal_destinations(self, pieces, blocked_moves):
        adjacent_locations = self.location.get_adjacent_locations()
        occupied_locations = [piece.location for piece in pieces]
        current_location = self.location
        legal_destinations = set()
        for adj_loc in adjacent_locations:
            if PieceMove(current_location, adj_loc) in blocked_moves:
                continue
            if adj_loc in occupied_locations:
                colinear_loc = current_location.get_colinear_location(adj_loc)
                if (colinear_loc is not None and
                        PieceMove(adj_loc, colinear_loc) not in blocked_moves and
                        colinear_loc not in occupied_locations):

                    legal_destinations.add(colinear_loc)
                else:
                    noncolinear_locs = (current_location.
                                        get_non_colinear_locations(adj_loc))
                    for loc in noncolinear_locs:
                        if (PieceMove(adj_loc, loc) not in blocked_moves and
                                loc not in occupied_locations):
                            legal_destinations.add(loc)
            else:
                legal_destinations.add(adj_loc)

        return legal_destinations


class PieceMove(object):

    def __init__(self, start, end):
        """
        both start and end are PieceLocations
        """
        self.start = start
        self.end = end

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.start == other.start and self.end == other.end
        return False

    def __hash__(self):
        return hash(self.start.location_str + self.end.location_str)

    def __repr__(self):
        return str(self.start) + " to " + str(self.end)


class Location(object):

    def __init__(self, location_str):
        self.location_str = location_str
        self.column = location_str[0]
        self.row = location_str[1]

    def add_row(self, n):
        return str(int(self.row) + n)

    def add_column(self, n):
        return chr(ord(self.column) + n)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.location_str == other.location_str
        return False

    def __hash__(self):
        return hash(self.location_str)

    def __repr__(self):
        return self.location_str


class FenceLocation(Location):

    def __init__(self, location_str):
        super(FenceLocation, self).__init__(location_str)
        self.orientation = self.location_str[2]

    def is_horizontal(self):
        return self.orientation == "h"

    def is_vertical(self):
        return self.orientation == "v"

    def perpendicular_fencelocation(self):
        if self.is_horizontal():
            return FenceLocation(self.column + self.row + "v")
        return FenceLocation(self.column + self.row + "h")


class PieceLocation(Location):

    def get_adjacent_locations(self):
        adjacent_locations = []
        right = PieceLocation(self.add_column(1) + self.row)
        left = PieceLocation(self.add_column(-1) + self.row)
        up = PieceLocation(self.column + self.add_row(1))
        down = PieceLocation(self.column + self.add_row(-1))
        for location in (right, left, up, down):
            if (location.column in POSSIBLE_COLUMNS
                    and location.row in POSSIBLE_ROWS):
                adjacent_locations.append(location)
        return adjacent_locations

    def get_colinear_location(self, other_location):
        """
        given self and other_location, finds a third location that
        makes a line starting at self, going through other_location,
        and ending at the third location. All of these must be adjacent.
        Used only for hopping logic.
        """
        candidate = None
        if other_location == PieceLocation(self.add_column(1) + self.row):
            candidate = PieceLocation(self.add_column(2) + self.row)
        if other_location == PieceLocation(self.add_column(-1) + self.row):
            candidate = PieceLocation(self.add_column(-2) + self.row)
        if other_location == PieceLocation(self.column + self.add_row(1)):
            candidate = PieceLocation(self.column + self.add_row(2))
        if other_location == PieceLocation(self.column + self.add_row(-1)):
            candidate = PieceLocation(self.column + self.add_row(-2))
        if (candidate is not None and candidate.column in POSSIBLE_COLUMNS
                and candidate.row in POSSIBLE_ROWS):
            return candidate
        return None

    def get_non_colinear_locations(self, other_location):
        """
        does the opposite of get_colinear_location. Used for hopping logic.
        """
        return (set(other_location.get_adjacent_locations()) -
                ({self.get_colinear_location(other_location), self}))
