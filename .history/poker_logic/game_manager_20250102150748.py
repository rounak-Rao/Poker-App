from player import Player
from betting import *

class GameManager:
    def __init__(self):
        self.players = []
        self.max_players = 9

    def add_player(self, name, stack):
        if len(self.players) < self.max_players:
            position = len(self.players) - 1
            new_player = Player(name, stack, position)
            self.players.append(new_player)
            return new_player
        return None  # Game is full

    def get_game_state(self):

        return {
        "players": [
            {"name": p.name, "stack": p.stack, "position": p.position}
            for p in self.players
        ]
    }
