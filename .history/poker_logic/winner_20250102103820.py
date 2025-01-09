from player import *
from deck import *

from treys import Card, Evaluator

evaluator = Evaluator()

class Winner:
    def __init__(self, players, community_cards):
        self.converted_hands = {
            player.name: [Card.new(f"{card[0].rank}{card[0].suit}") for card in player.hand]
            for player in players
        }
        self.converted_board = [Card.new(f"{card.rank}{card[0].suit}") for card in community_cards]
        self.results = []
        self.winners = []

    def winner(self):
        unsorted_results = {}
        for player, hand in self.converted_hands.items():
            rank = evaluator.evaluate(self.converted_board, hand)
            unsorted_results[player] = rank

        self.results = sorted(unsorted_results.items(), key=lambda x: x[1])
        winning_rank = self.results[0][1]
        self.winners = [player for player, rank in self.results if rank == winning_rank]

        return self.winners


if __name__ == "__main__":
    p1 = Player(100, 'r', 0)
    p2 = Player(100, 'q', 1)
    p3 = Player(100, 'a', 2)
    deck = Deck()
    p1.hand = [
           deck.deal(),
           deck.deal()
        ]
    p2.hand = [
           deck.deal(),
           deck.deal()
        ]
    p3.hand = [
           deck.deal(),
           deck.deal()
        ]

    community_cards = []
    community_cards.extend(p1.hand)
    community_cards.extend(p2.hand)
    community_cards.extend(p3.hand)


    players = [p1, p2, p3]
    for player in players:
        print(f'player {player.name}, player hand: {player.hand}')

    print(community_cards)
    winner = Winner(players, community_cards)
    x = winner.winner()
    print(x)