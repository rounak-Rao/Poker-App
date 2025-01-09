import random
from collections import namedtuple

Card = namedtuple('Card', ['suit', 'rank'])
class Deck:
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self)
        self.cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]
        self.shuffle()
    
    def shuffle(self):
        for i in range(0,2)
        random.shuffle(self.cards)