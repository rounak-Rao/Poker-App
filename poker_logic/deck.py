import random
from collections import namedtuple

Card = namedtuple('Card', ['rank', 'suit'])
class Deck:
    suits = ['h', 'd', 'c', 's']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

    def __init__(self):
        self.cards = [Card(rank, suit) for rank in self.ranks for suit in self.suits]
        self.shuffle()
    
    def shuffle(self):
        for i in range(0,2):
            random.shuffle(self.cards)

    def deal(self):
        dealt_cards = self.cards[:1]
        self.cards = self.cards[1:]
        return dealt_cards


if __name__ == "__main__":
    deck = Deck()
    print("Shuffled Deck:", deck.cards)
    hand = deck.deal()
    print("Dealt Hand:", hand)
    print(deck.deal())
    print("Remaining Deck:", deck.cards)