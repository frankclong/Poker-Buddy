from card import Card
from cards import Cards
from deck import Deck
from pokerhands import bestHand, tiebreak
import random
import csv

def cardCodeToCard(c):
    if c[-1] == 'h':
        return Card(int(c[:-1]), "hearts")
    elif c[-1] == 's':
        return Card(int(c[:-1]), "spades")
    elif c[-1] == 'c':
        return Card(int(c[:-1]), "clubs")
    elif c[-1] == 'd':
        return Card(int(c[:-1]), "diamonds")

# INPUTS
my_deck = Deck()

# Hand
hand = [Card(5,"hearts"), Card(8, "spades")]
# Flush
flop = [Card(7, "hearts"), Card(10, "hearts"), Card(6,"hearts")]
# Turn
turn = Card(4,"spades")
# River
river = Card(14, "diamonds")

community = []
for c in flop:
    community.append(c)
if turn:
    community.append(turn)
    if river:
        community.append(river)

# Determine probability of winning hand
cards = community.copy()
cards.extend(hand)
card_list = Cards(cards)
card_list.sort()
cards = card_list.cards

# SCORE AND BEST HAND
score, best_hand = bestHand(cards)

# Generate opposing hands based on remaining cards in deck and compare scores with our best hand
# Update deck
for c in cards:
    my_deck.remove(c)

num_remaining = len(my_deck.cards)
wins = 0
losses = 0
ties = 0

for i in range(num_remaining - 1):
    cc1 = my_deck.cards[i]
    for j in range(i+1, num_remaining):
        cc2 = my_deck.cards[j]
        opp_hand = [cardCodeToCard(cc1), cardCodeToCard(cc2)]
        opp_cards = community.copy()
        opp_cards.extend(opp_hand)
        opp_card_list = Cards(opp_cards)
        opp_card_list.sort()
        opp_cards = opp_card_list.cards
        opp_score, opp_best_hand = bestHand(opp_cards)
        if opp_score > score:
            losses += 1
        elif opp_score < score:
            wins += 1
        else: 
            tb = tiebreak(score, best_hand, opp_best_hand)
            if tb == 1:
                wins += 1
                print('w')
            elif tb == -1:
                losses += 1
                print('l')
            else:
                ties += 1
                print('t')
            #opp_card_list.show()
            print(cc1, cc2)
            print("-----------------------------------------------------------------------------")

print("Wins: ", wins)
print("Losses: ", losses)
print("Ties: ", ties)
print("Win/Tie %: ", (wins+ties)/(wins+ties+losses)*100)

pot_size = 500
call_amount = 100
