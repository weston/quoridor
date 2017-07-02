"""
quoridor_game.py
"""
import copy
import importlib

from quoridor import QuoridorBoard
from quoridor import Fence, PieceMove
from quoridor_base_player import QuoridorBasePlayer

TOTAL_FENCES = 20


class QuoridorGame(object):

    def __init__(self, num_players=2):
        self.num_players = num_players
        self.init_players()

    def init_players(self):
        self.players = []
        self.pieces = []
        self.board = QuoridorBoard()
        num_fences = TOTAL_FENCES / self.num_players
        self.num_fences = num_fences
        print "Welcome to Quoridor"
        print "Please specify the player classes you want to use"
        print "Leave blank for human_player:HumanPlayer"
        for i in range(self.num_players):
            module_class_str = raw_input("class for player " + str(i) + ": ")
            if module_class_str == "":
                module_str = "human_player"
                class_name = "HumanPlayer"
            else:
                module_str = module_class_str.split(":")[0]
                class_name = module_class_str.split(":")[1]
            module = importlib.import_module(module_str)
            class_ = getattr(module, class_name)
            if not issubclass(class_, QuoridorBasePlayer):
                print "Not a valid class. Exiting."
            print "Leave blank for player" + str(i)
            name = raw_input("Name for player " + str(i) + ": ")
            if name == "":
                name = "player" + str(i)
            player = class_(num_fences, name)
            self.players.append(player)
            piece = self.board.add_player(player.name)
            self.pieces.append(piece)
        self.fence_counts = {player: num_fences for player in self.players}

    def run(self):
        turn = 0
        while not self.board.complete:
            player_to_go = turn % self.num_players
            player = self.players[player_to_go]
            piece = self.pieces[player_to_go]
            board_copy = copy.deepcopy(self.board)
            piece_copy = copy.deepcopy(piece)
            action = player.handle_turn(board_copy, piece_copy, 0)
            if isinstance(action, Fence):
                assert self.fence_counts[player] > 0
                self.board.add_fence(action)
                self.fence_counts[player] -= 1
                player.num_fences = self.fence_counts[player]
            else:
                assert isinstance(action, PieceMove)
                self.board.move_piece(piece, action)
            turn += 1
        print "Game lasted {} turns!".format(turn)

QuoridorGame().run()

