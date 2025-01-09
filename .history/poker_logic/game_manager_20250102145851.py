from player import *
from betting import *

class GameManager:
    def __init__(self):
        self.players = []
        self.max_players = 9

    def add_player(self, name, stack):
        position = len(self.players) - 1
        self.players.append(Player(int(stack), name, int(position)))