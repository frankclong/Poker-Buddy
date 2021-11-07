from card import Card
from deck import Deck
from pokerhands import bestHand
import random
import csv

# INPUTS
new_deck = Deck()
print(new_deck.cards)
# TEST
with open('poker_test.csv','w', newline='', encoding='utf-8-sig') as test_file:
    writer = csv.writer(test_file)

    for i in range(1000):
        sample_cards = sorted(random.sample(new_deck.cards, 7))
        print(sample_cards)
        my_cards = []
        for c in sample_cards:
            if c[-1] == 'h':
                card = Card(int(c[:-1]), "hearts")
            elif c[-1] == 's':
                card = Card(int(c[:-1]), "spades")
            elif c[-1] == 'c':
                card = Card(int(c[:-1]), "clubs")
            elif c[-1] == 'd':
                card = Card(int(c[:-1]), "diamonds")
            my_cards.append(card)
        
        cards = sorted(my_cards, key=lambda x : x.value)
        score, best_hand = bestHand(cards)
        #print("Score = ", score)
        #best_hand.show()

        row = sample_cards
        row.append(score)
        writer.writerow(row)