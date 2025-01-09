class Player:
    def __init__(self, stack, name, position, is_host):
        self.stack = stack
        self.max_pot_contribution = stack
        self.max_win = 0
        self.name = name
        self.hand = []
        self.position = position
        self.bet = 0
        self.is_active = True
        self.folded = False
        self.all_in = False
        self.called_amt = 0
        self.starting_stack = stack
        self.is_host = False

    def check_bet(self, bet):
        if bet>self.stack:
            raise ValueError('You cannot bet more than your stack')
        
        self.stack -= bet 
        self.bet += bet
        if self.stack == 0:  
            self.all_in = True
            self.is_active = False
    
    def deal_cards(self, card):
        self.hand.append(card)

    def fold(self):
        self.folded = True
        self.is_active = False

    def reset(self):
        self.hand = []
        self.bet = 0
        self.folded = False
        self.is_active = True
        self.all_in = False



