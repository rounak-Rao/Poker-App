
from deck import *
from collections import namedtuple

card_image_mapping = {
    'c': {  # Clubs
        '2': 'c02', '3': 'c03', '4': 'c04', '5': 'c05', '6': 'c06', '7': 'c07', '8': 'c08', 
        '9': 'c09', 'T': 'c10', 'J': 'c11', 'Q': 'c12', 'K': 'c13', 'A': 'c01'
    },
    'd': {  # Diamonds
        '2': 'd02', '3': 'd03', '4': 'd04', '5': 'd05', '6': 'd06', '7': 'd07', '8': 'd08', 
        '9': 'd09', 'T': 'd10', 'J': 'd11', 'Q': 'd12', 'K': 'd13', 'A': 'd01'
    },
    'h': {  # Hearts
        '2': 'h02', '3': 'h03', '4': 'h04', '5': 'h05', '6': 'h06', '7': 'h07', '8': 'h08', 
        '9': 'h09', 'T': 'h10', 'J': 'h11', 'Q': 'h12', 'K': 'h13', 'A': 'h01'
    },
    's': {  # Spades
        '2': 's02', '3': 's03', '4': 's04', '5': 's05', '6': 's06', '7': 's07', '8': 's08', 
        '9': 's09', 'T': 's10', 'J': 's11', 'Q': 's12', 'K': 's13', 'A': 's01'
    }
}

def get_card_image_filename(card):
    return card_image_mapping[card.suit][card.rank]

if __name__ == '__main__':
    card = Card('A', 'c')
    c = get_card_image_filename(card)
    print(c)