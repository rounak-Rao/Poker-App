from poker_logic.deck import *
from poker_logic.player import *
from poker_logic.betting import *
from poker_logic.winner import *
from poker_logic.card_utils import *

class GameManager:
    def __init__(self):
        self.players = []
        self.game_state = 'waiting' # waiting/ playing
        self.community_cards = []
        self.deck = Deck()
        self.community_cards = []
        self.bet = None
        self.win = None
        self.sb = 1
        self.bb = 2

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
            'current_seat': self.players[0].seat,
            'current_bet': self.bet,
            'player_stack': self.players[0].stack
        }

    def end_game(self):
        self.game_state = 'waiting'
    
    def start_game(self):
        if len(self.players) < 2:
            return False
        self.game_state = 'playing'
        return True
    
    def initialize_game(self, sb, bb):
        self.sb = sb
        self.bb = bb

    
    def initialize_hand(self):
        self.bet = Betting(self.players, self.sb, self.bb)
        self.deck.shuffle()
        self.deal_cards()
        self.bet.collect_blinds() 

    def play_game(self):
        self.bet.preflop()
        flop = self.deal_flop()
        self.community_cards.extend(flop)


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
    
    def create_winner(self):
        self.win = Winner(self.bet.players_in_hand, self.community_cards)

    def continue_betting_rounds(self):
        return len(self.bet.active_players) > 1
    
    def is_round_over(self):
        return len(self.bet.players_in_hand) > 1
    
    def update_winners(self):
        winners = self.win.winner()
        pot = self.bet.pot
        #we first handle winners that are all in and update stack accordingly
        for player in self.bet.players_in_hand:
            if player.name in winners:
                if player.all_in:
                    amt_return = min(player.max_win, pot/len(winners))
                    player.stack += amt_return
                    pot -= amt_return
                    winners.remove(player)
                    self.bet.players_in_hand.remove(player)

        #then handle winners that are not all in
        for player in self.bet.players_in_hand:
            if player.name in winners:
                amt_return = pot / len(winners)
                player.stack += amt_return
                pot -= amt_return

        #if there is still money in the pot, go to the next best hand and update.
        if pot!=0:
            results = self.win.get_results()
            i = 0
            while pot != 0:
                for p in self.bet.players_in_hand:
                    if p.name == results[i][0] and p.name not in winners:
                        if p.all_in:
                            p.stack += p.max_win
                            pot -= p.max_win

                        elif not p.all_in:
                            p.stack += pot
                            pot = 0
                i += 1

    def handle_action(self, action, amount=0):
        return self.bet.handle_action(self.bet.current_player_index, action, amount)


    def reset_values(self):
        for p in self.players:
            p.reset()
            if p .stack == 0:
                self.players.remove(p)
        self.community_cards = []
        self.bet = None
        self.win = None


if __name__ =='__main__':
    pass