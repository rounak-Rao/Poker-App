from deck import *
from player import *
from betting import *
from winner import *

def main():
    '''
    i = 1
    sb, bb = blinds()
    players_list = create_players()
    while True:
        community_cards = []
        deck = Deck()
        bet = Betting(players_list, int(sb), int(bb))
        print(f'round {i}')
        deck.shuffle()
        deal_cards(players_list, deck)
        bet.collect_blinds()
        bet.preflop()
        flop = deal_flop(deck)
        print(f'flop: {flop}')
        community_cards.extend(flop)
        bet.reset_bet()
        if len(bet.active_players) > 1:
            bet.betting_round(0)

        turn = deal_postflop(deck)
        print(f'turn: {turn}')
        community_cards.append(turn)
        bet.reset_bet()
        bet.betting_round(0)
        river = deal_postflop(deck)
        community_cards.append(river)
        print(f'river: {river}')
        bet.reset_bet()
        bet.betting_round(0)

        winner = Winner(players_list, community_cards)
        winning_players = winner.winners()
        print(winning_players)


    '''
    community_cards = []
    flop = deal_flop(deck)
    




def create_players():
    i = 0
    players_list = []
    while True:
        name = input('Enter player name: ')
        stack = input(f'Enter {name} stack: ')
        position = i
        players_list.append(Player(int(stack), name, int(position)))
        i+=1

        cont = input('Continue adding players? (y/n): ')
        if cont.lower() == 'n':
            break
    return players_list


def blinds():
    sb = int(input('Enter small blind value: '))
    bb = int(input('enter big blind value'))

    return sb, bb

def deal_cards(players_list: list[Player], deck:Deck):
    for i in range(2):
        for p in players_list:
            card = deck.deal()
            p.deal_cards(card)

def deal_flop(deck:Deck):
    flop = []
    deck.deal() #burn
    flop.append(deck.deal())
    flop.append(deck.deal())
    flop.append(deck.deal())
    return flop

def deal_postflop(deck:Deck):
    deck.deal()#burn
    return deck.deal()



if __name__ == '__main__':
    main()
