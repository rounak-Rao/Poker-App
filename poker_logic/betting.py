from poker_logic.player import *
from poker_logic.deck import *

class Betting:
    def __init__(self, players, sb, bb):
        self.players = players
        self.active_players = [player for player in players if player.is_active]
        self.pot = 0
        self.sb = sb
        self.bb = bb
        self.current_bet = bb
        self.players_in_hand = [player for player in players if player.is_active or player.all_in]
        self.current_player_index = 0
        self.cycle_completed = False

    def collect_blinds(self):
        # Collecting blinds from the first two players (SB and BB)
        self.active_players[0].check_bet(self.sb)
        self.active_players[1].check_bet(self.bb)
        self.pot += self.sb + self.bb
        self.current_bet = self.bb

    def check_active(self):
        # Filter out players who have folded
        self.active_players = [player for player in self.active_players if player.is_active]

    def check_in_hand(self):
        self.players_in_hand = [player for player in self.players_in_hand if player.is_active or player.all_in]


    def handle_call(self, player):
        call_amount = self.current_bet - player.bet
        if call_amount > 0:
            try:
                if player.stack >= call_amount:
                    player.check_bet(call_amount)
                    self.pot += call_amount
                    print(f"{player.name} calls {call_amount}")
                    player.called_amt = call_amount
                else:
                    # Player goes all-in if they can't fully call
                    all_in_amount = player.stack
                    player.check_bet(all_in_amount)
                    self.pot += all_in_amount
                    player.called_amt = all_in_amount
            except ValueError:
                print(f"{player.name} couldn't bet.")
        else:
            print(f"{player.name} checks.")


    def handle_raise(self, player, amt):

            min_raise = max(self.current_bet * 2, self.bb)
            if amt < min_raise and amt < player.stack:
                raise ValueError("Raise amount is too low")
            elif amt >= player.stack:
                amt = player.stack + player.bet
            actual_raise = amt - player.bet
            player.check_bet(actual_raise)
            self.pot += actual_raise
            self.current_bet = amt
            if player.stack == 0:
                player.is_active = False
                player.all_in = True


    def handle_fold(self, player):
        player.fold()
        self.check_active()  # Remove folded players immediately


    def handle_action(self, player, action, amt = None):
        if action == "CALL":
            self.handle_call(player)
        elif action == "RAISE":
            self.handle_raise(player, amt)
        elif action == "FOLD":
            self.handle_fold(player)
        elif action == "CHECK":
            print(f"{player.name} checks")

    def start_betting_round(self, index):
        self.current_player_index = index
        return self.active_players[index]

    def advance_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.active_players)
        if self.current_player_index == 0:
            self.cycle_completed = True

    def check_end_betting_round(self):
        active_bets = [p.bet for p in self.active_players if p.is_active]
        if all(bet == self.current_bet for bet in active_bets) and self.cycle_completed == True:
            return True
        return False


    def post_round(self):
        self.check_in_hand()
        for p in self.players:
            if p.all_in:
                for player in self.players:
                    if player.bet >= p.bet:
                        p.max_win += p.max_pot_contribution
                    elif player.bet < p.bet:
                        p.max_win += player.bet

        if self.check_return_bets():
            p, amt = self.return_bets()
            p.stack += amt
            if p.all_in:
                p.all_in = False
            self.pot -= amt
            p.max_win = self.pot
    
    def print_players(self):
        for player in self.players:
            print(f'name: {player.name}, stack: {player.stack}')

    def check_return_bets(self):
        if len(self.active_players)<=1:
            stacks = sorted(self.players_in_hand, key=lambda player: max(player.called_amt, player.bet))
            bet1 = max(stacks[-1].called_amt, stacks[-1].bet)
            bet2 = max(stacks[-2].called_amt, stacks[-2].bet)
            if bet1 > bet2:
                return True
        return False

    def return_bets(self):
        stacks = sorted(self.players_in_hand, key=lambda player: player.starting_stack)
        bet_to_return = self.current_bet - stacks[-2].starting_stack
        top_player = stacks[-1]
        return top_player, bet_to_return

    def reset_bet(self):
        self.current_bet = 0
        for player in self.players:
            player.reset()
        self.active_players = self.players
        self.players_in_hand = self.players



if __name__ == '__main__':
    players = [
        Player(100, "Alice", 0),  # Small stack
        Player(300, "Bob", 1),   # Mid stack
        Player(500, "Charlie", 2),
        Player(700, "Dana", 3),
        Player(1000, "Eve", 4),  # Largest stack
    ]
    test = Betting(players, 5, 10)
    test.collect_blinds()
    test.print_players()
    test.print_players()
    for player in test.players:
        print(f'name: {player.name}, max win amt: {player.max_win}')


            







    
                    



