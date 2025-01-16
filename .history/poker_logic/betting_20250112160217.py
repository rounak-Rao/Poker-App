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
        self.side_pot = []
        self.players_in_hand = [player for player in players if player.is_active or player.all_in]
        self.community_cards = []

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


    def handle_raise(self, player):
        while True:
            try:
                raise_amt = float(input(f"Enter raise amount (minimum {self.current_bet * 2}): "))
                if self.current_bet
                if raise_amt < self.current_bet * 2 <= player.stack:
                    print('Raise must be at least double the current bet.')
                    continue
                elif raise_amt >= player.stack:
                    raise_amt = player.stack + player.bet
                actual_raise = raise_amt - player.bet
                player.check_bet(actual_raise)
                self.pot += actual_raise
                if not player.all_in:
                    print(f"{player.name} raises to {raise_amt}")
                elif player.all_in:
                    print(f"{player.name} goes all in with {raise_amt}")
                self.current_bet = raise_amt
                if player.stack == 0:
                    player.is_active = False
                    player.all_in = True
                break
            except ValueError:
                print("Invalid amount, try again.")

    def handle_fold(self, player):
        player.fold()
        print(f"{player.name} folds")
        self.check_active()  # Remove folded players immediately

    def betting_round(self, index):
        i = index # Start after the blinds
        cycle = False
        while True:
            player = self.active_players[i]
            
            # Skip inactive players
            if not player.is_active:
                i = (i + 1) % len(self.active_players)
                continue

            if player.bet != self.current_bet:
                print(f"{player.name}, your action (Call, Raise, Fold) (Call/Raise/Fold): ")
            elif player.bet == self.current_bet:
                print(f"{player.name}, your action (Check, Raise) (Check/Raise): ")

            action = input().strip().upper()

            # Get player action
            if player.bet != self.current_bet:
                if action not in ['CALL', 'RAISE', 'FOLD']:
                    print("Invalid action, please try again.")
                    continue
            elif player.bet == self.current_bet:
                if action not in ['CHECK', 'RAISE']:
                    print("Invalid action, please try again.")
                    continue
            # Handle Call
            if action == 'CALL':
                self.handle_call(player)
            
            elif action == 'RAISE':
                self.handle_raise(player)

            elif action == 'FOLD':
                self.handle_fold(player)
                i-=1

            elif action == 'CHECK':
                print(f'{player.name} checks')

            if len(self.active_players) > 0:
                if i == len(self.active_players)-1 :
                    cycle = True
                i = (i + 1) % len(self.active_players)

            active_bets = [p.bet for p in self.active_players if p.is_active]
            if all(bet == self.current_bet for bet in active_bets) and cycle == True:
                break

        self.post_round()


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

    def preflop(self):
        print('this is the preflop round')
        self.betting_round(2)
        print(f"Preflop round complete. Pot: {self.pot}")

    def reset_bet(self):
        self.current_bet = 0
        for player in self.players:
            player.bet = 0


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
    test.preflop()
    test.print_players()
    for player in test.players:
        print(f'name: {player.name}, max win amt: {player.max_win}')


            







    
                    



