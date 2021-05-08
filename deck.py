from card import Card
import random

def cardCodeToCard(c):
    if c[-1] == 'h':
        return Card(int(c[:-1]), "hearts")
    elif c[-1] == 's':
        return Card(int(c[:-1]), "spades")
    elif c[-1] == 'c':
        return Card(int(c[:-1]), "clubs")
    elif c[-1] == 'd':
        return Card(int(c[:-1]), "diamonds")

class Deck:
    def __init__(self):
        self.cards = [] # set of cards
        suits = ["h", "c", "d", "s"]
        for val in range(2,15):
            for suit in suits:
                card = str(val) + suit
                self.cards.append(card)
    
    def remove(self, card):
        card_code = str(card.value) + card.suit[0]
        self.cards.remove(card_code)
    def add(self, card):
        card_code = str(card.value) + card.suit[0]
        self.cards.append(card_code)

    def copy(self):
        deck_copy = Deck()
        deck_copy.cards = self.cards.copy()
        return deck_copy

    def draw(self):
        card_code = random.choice(self.cards)
        card = cardCodeToCard(card_code)
        self.remove(card)
        return card