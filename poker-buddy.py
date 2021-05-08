from card import Card
from deck import Deck
from pokerhands import bestHand, tiebreak, compareOpponentHand
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

def showCards(cards):
    for c in cards:
        print(c.value, c.suit)

# INPUTS
my_deck = Deck()

# Hand
hand = [Card(5,"hearts"), Card(8, "hearts")]
# Flush
flop = [Card(7, "hearts"), Card(10, "hearts"), Card(6,"hearts")]
# Turn
turn = Card(4,"spades")
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

total_wins = 0
total_losses = 0
total_ties = 0

# Fill out community cards
if not river:
    for i in range(len(my_deck.cards)):
        # draw a card and add to community
        working_deck = my_deck.copy()
        working_community = community.copy()
        river = cardCodeToCard(my_deck.cards[i])
        working_community.append(river)
        working_deck.remove(river)

        my_cards = working_community.copy()
        my_cards.extend(hand)
        my_cards = sorted(my_cards, key=lambda x : x.value)

        # SCORE AND BEST HAND
        score, best_hand = bestHand(my_cards)
        
        # Generate opposing hands based on remaining cards in deck and compare scores with our best hand
        wins, losses, ties = compareOpponentHand(working_deck, working_community, score, best_hand)
        total_wins += wins
        total_losses += losses
        total_ties += ties  
else:
    my_cards = community.copy()
    my_cards.extend(hand)
    my_cards = sorted(my_cards, key=lambda x : x.value)

    # SCORE AND BEST HAND
    score, best_hand = bestHand(my_cards)
    
    # Generate opposing hands based on remaining cards in deck and compare scores with our best hand
    wins, losses, ties = compareOpponentHand(working_deck, working_community, score, best_hand)
    total_wins += wins
    total_losses += losses
    total_ties += ties  

print("Wins: ", total_wins)
print("Losses: ", total_losses)
print("Ties: ", total_ties)
total_outcomes = total_wins + total_losses + total_ties
win_percent = total_wins/total_outcomes
tie_percent = total_ties/total_outcomes
lose_percent = total_losses/total_outcomes
print("Win/Tie %: ", win_percent+tie_percent)

# TODO: expected value stuff
pot_size = 500
call_amount = 100
