# calc-test

from calc import calculate
from deck import Deck
from card import Card

# INPUTS
my_deck = Deck()

# Hand
hand = [Card(5,"hearts"), Card(8, "hearts")]
# Flush
flop = [Card(7, "hearts"), Card(10, "hearts"), Card(6,"hearts")]
# Turn
turn = 0
# River
#river = Card(14, "diamonds")
river = 0

# Initialize known community cards and remove from deck
community = []
for c in flop:
    community.append(c)
    my_deck.remove(c)
if turn:
    community.append(turn)
    my_deck.remove(turn)
    if river:
        community.append(river)
        my_deck.remove(river)
# Remove cards in hand from deck
for c in hand:
    my_deck.remove(c)

wins, losses, ties = calculate(my_deck, community, hand)