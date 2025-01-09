import random
from collections import namedtuple

Card = namedtuple('Card', ['suit', 'rank'])
class Deck:
    suit = ['hearts', 'diamonds', 'clubs', 'spades']
    rank = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self
        self.cards = [Card(rank, suit) for suit in ]