from card import Card

class Cards:
    def __init__(self, cards):
        self.cards = cards

    def sort(self):
        for i in range(len(self.cards)-1):
            card1 = self.cards[i]
            min_val = card1.value
            min_ind = i
            for j in range(i+1, len(self.cards)):
                card2 = self.cards[j]
                new_val = card2.value
                if new_val < min_val:
                    min_ind = j
                    min_val = new_val
            
            if min_ind != i:
                temp = card1
                self.cards[i] = self.cards[min_ind]
                self.cards[min_ind] = temp

        return self.cards

    def show(self):
        for c in self.cards:
            print(c.value, c.suit)