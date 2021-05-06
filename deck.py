from card import Card

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