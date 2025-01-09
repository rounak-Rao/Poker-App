from poker_logic.deck import *
from poker_logic.player import *
from poker_logic.betting import *
from poker_logic.winner import *
from poker_logic.card_utils import *

class GameManager:
    def __init__(self):
        self.players = []
        self.game_state = 'waiting' # waiting/ playing/ finished
        self.community_cards = []
        self.deck = Deck()


    def create_player(self, stack, name, pos):
        if len(self.players) < 9:
            print('creating player')
            is_host = len(self.players) == 0 
            p = Player(stack, name, pos, is_host)
            self.players.append(p)
            return p
        return None
    
    def deal_cards(self):       
        for i in range(2):
            for p in self.players:
                card = self.deck.deal()
                p.deal_cards(card)

        for p in self.players:
            image_files = [get_card_image_filename(card) for card in p.hand]
    
    def card_img(self):
        dealt_card

    
    def get_game_state(self):
        return {
            "players": [{"name": p.name, "stack": p.stack} for p in self.players],
            "game_state": self.game_state,
            "community_cards": self.community_cards,
        }

    def end_game(self):
        self.game_state = 'finished'
    
    def start_game(self):
        if len(self.players) < 2:
            return False
        self.game_state = 'playing'
        return True
    

if __name__ =='__main__':
    pass
        