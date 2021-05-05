from card import Card
from cards import Cards
from pokerhands import *

# INPUTS
# Hand
hand = [Card(3,"hearts"), Card(3, "diamonds")]
# Flush
flop = [Card(3, "spades"), Card(5, "clubs"), Card(5,"hearts")]
# Turn
turn = Card(6,"hearts")
# River
river = Card(7, "hearts")

community = []
for c in flop:
    community.append(c)
if turn:
    community.append(turn)
    if river:
        community.append(river)

# Determine probability of winning hand
cards = community
cards.extend(hand)

card_list = Cards(cards)
card_list.sort()
cards = card_list.cards

best_hand = Cards(isFullHouse(cards))
best_hand.show()

# Maybe some other stuff for like if you have nothing but 
# Can't just determine if straight or not -- need to consider kicker 