from poker_logic.deck import *
from poker_logic.player import *
from poker_logic.betting import *
from poker_logic.winner import *
from poker_logic.card_utils import *

class GameManager:
    def __init__(self, players, ):
        self.players = []
        self.game_state = 'waiting' # waiting/ playing
        self.community_cards = []
        self.deck = Deck()
        self.community_cards = []

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
    
    def card_img(self):
        dealt_cards = {}
        for p in self.players:
            image_files = [get_card_image_filename(card[0]) for card in p.hand]
            dealt_cards[p.position] = image_files
        return dealt_cards
    
    def get_game_state(self):
        return {
            "players": [{"name": p.name, "stack": p.stack} for p in self.players],
            "game_state": self.game_state,
            "community_cards": self.community_cards,
        }

    def end_game(self):
        self.game_state = 'waiting'
    
    def start_game(self):
        if len(self.players) < 2:
            return False
        self.game_state = 'playing'
        return True
    
    def initialize_game(self):
        sb = int(input('enter small blind value: '))
        bb = int(input('enter bb value: '))
        return sb, bb

    
    def initialize_hand(self):
        sb, bb = self.initialize_game()
        bet = Betting(self.players, sb, bb)
        self.deck.shuffle()
        self.deal_cards()
        bet.collect_blinds() 


    def deal_flop(self):
        flop = []
        self.deck.deal() #burn
        flop.append(self.deck.deal())
        flop.append(self.deck.deal())
        flop.append(self.deck.deal())
        return flop

    def deal_postflop(self):
        self.deck.deal()#burn
        return self.deck.deal()

if __name__ =='__main__':
    pass