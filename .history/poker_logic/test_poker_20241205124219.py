from player import Player
from deck import Deck
from betting import Betting

def test_player_class():
    print("Testing Player class...")
    player = Player(100, "Alice", 1)
    assert player.stack == 100
    assert player.is_active == True
    assert player.all_in == False

    # Test betting
    player.check_bet(20)
    assert player.stack == 80
    assert player.bet == 20
    assert player.all_in == False

    # Test all-in
    player.check_bet(80)
    assert player.stack == 0
    assert player.all_in == True
    assert player.is_active == False

    # Test folding
    player.reset()
    player.fold()
    assert player.is_active == False
    assert player.folded == True
    print("Player class passed!")

def test_deck_class():
    print("Testing Deck class...")
    deck = Deck()
    assert len(deck.cards) == 52

    # Test shuffling
    pre_shuffle_cards = deck.cards.copy()
    deck.shuffle()
    assert deck.cards != pre_shuffle_cards  # Check if shuffle changes the order

    # Test dealing cards
    hand = deck.deal()
    assert len(hand) == 2
    assert len(deck.cards) == 50  # Ensure two cards are removed

    print("Deck class passed!")

def test_betting_class():
    print("Testing Betting class...")
    players = [
        Player(100, "Player1", 1),
        Player(200, "Player2", 2),
        Player(300, "Player3", 3)
    ]
    betting = Betting(players, 5, 10)
    
    # Test collecting blinds
    betting.collect_blinds()
    assert betting.pot == 15
    assert players[0].stack == 95
    assert players[1].stack == 190
    assert players[2].stack == 300  # Player3 did not post blinds

    # Test active players list
    assert len(betting.active_players) == 3
    players[2].fold()
    betting.check_active()
    assert len(betting.active_players) == 2
    print("Betting class passed!")

if __name__ == "__main__":
    test_player_class()
    test_deck_class()
    test_betting_class()
    print("All tests passed!")
