from cards import Cards
import heapq

def bestHand(cards):
    hand = 0
    tiebreak = 0

    # Check for 5 card combos
    # Royal flush
    tiebreak = isRoyalFlush(cards)
    if tiebreak:
        hand = 9
        return hand, tiebreak

    # Straight flush
    tiebreak = isStraightFlush(cards)
    if tiebreak:
        hand = 8
        return hand, tiebreak

    # Quad
    tiebreak = isQuad(cards)
    if tiebreak:
        hand = 7
        return hand, tiebreak

    # Full House
    tiebreak = isFullHouse(cards)
    if tiebreak:
        hand = 6
        return hand, tiebreak

    # Flush
    tiebreak = isFlush(cards)
    if tiebreak:
        hand = 5
        return hand, tiebreak
    # Straight
    tiebreak = isStraight(cards)
    if tiebreak:
        hand = 4
        return hand, tiebreak
    # 3s
    tiebreak = isTriple(cards)
    if tiebreak:
        hand = 3
        return hand, tiebreak
    # 2pair
    tiebreak = isTwoPair(cards)
    if tiebreak:
        hand = 2 
        return hand, tiebreak
    # double
    tiebreak = isPair(cards)
    if tiebreak:
        hand = 1
        return hand, tiebreak
    # nothing


def isRoyalFlush(cards):
    hand = []
    royalHearts = 0
    royalSpades = 0
    royalDiamonds = 0
    royalClubs = 0
    for c in cards:
        if c.value >= 10:
            if c.suit == "hearts":
                royalHearts += 1
            elif c.suit == "spades":
                royalSpades += 1
            elif c.suit == "diamonds":
                royalDiamonds += 1
            else:
                royalClubs += 1
    if royalHearts == 5:
        for c in cards:
            if c.value >= 10 and c.suit == "hearts":
                hand.append(c)
        return hand
    elif royalSpades == 5:
        for c in cards:
            if c.value >= 10 and c.suit == "spades":
                hand.append(c)
        return hand
    elif royalClubs == 5:
        for c in cards:
            if c.value >= 10 and c.suit == "clubs":
                hand.append(c)
        return hand
    elif royalDiamonds == 5:
        for c in cards:
            if c.value >= 10 and c.suit == "diamonds":
                hand.append(c)
        return hand
    return 0

#TODO check for A low straight
def isStraightFlush(cards):
    # 3 cards of same suit where difference between high and low is 5 or less
    hearts = []
    spades = []
    diamonds = []
    clubs = []
    for c in cards:
        if c.suit == "hearts":
            hearts.append(c)
        elif c.suit == "spades":
            spades.append(c)
        elif c.suit == "diamonds":
            diamonds.append(c)
        else:
            clubs.append(c)
    # note that cards should already have been sorted prior to running the function

    if len(hearts) >= 5:
        counter = 1 
        for i in range(len(hearts) - 1):
            val1 = hearts[len(hearts)-i-1].value
            val2 = hearts[len(hearts)-i-2].value
            if val1 - 1 == val2:
                counter += 1
            else:
                counter = 1
            if counter == 5:
                return hearts[len(hearts)-i-2:len(hearts)-i+3]

    
    if len(spades) >= 5:
        counter = 1 
        for i in range(len(spades) - 1):
            val1 = spades[len(spades)-i-1].value
            val2 = spades[len(spades)-i-2].value
            if val1 - 1 == val2:
                counter += 1
            else:
                counter = 1
            if counter == 5:
                return spades[len(spades)-i-2:len(spades)-i+3]
    if len(diamonds) >= 5:
        counter = 1 
        for i in range(len(diamonds) - 1):
            val1 = diamonds[len(diamonds)-i-1].value
            val2 = diamonds[len(diamonds)-i-2].value
            if val1 - 1 == val2:
                counter += 1
            else:
                counter = 1
            if counter == 5:
                return diamonds[len(diamonds)-i-2:len(diamonds)-i+3]
    if len(clubs) >= 5:
        counter = 1 
        for i in range(len(clubs) - 1):
            val1 = clubs[len(clubs)-i-1].value
            val2 = clubs[len(clubs)-i-2].value
            if val1 - 1 == val2:
                counter += 1
            else:
                counter = 1
            if counter == 5:
                return clubs[len(clubs)-i-2:len(clubs)-i+3]

    return False

def isFlush(cards):
    hand = []
    hearts = 0
    spades = 0
    diamonds = 0
    clubs = 0
    # count number of each suit
    for c in cards:
        if c.suit == "hearts":
            hearts += 1
        elif c.suit == "spades":
            spades += 1
        elif c.suit == "diamonds":
            diamonds += 1
        else:
            clubs += 1
    # determine which 5 cards make up the hand
    # cards are sorted coming in
    if hearts >= 5: 
        for c in reversed(cards):
            if c.suit == "hearts":
                # if already 5 of this suit, only update if it's a new high
                hand.append(c)
                if len(hand) == 5:
                    return hand

    elif diamonds >= 5:
        for c in reversed(cards):
            if c.suit == "diamonds":
                # if already 5 of this suit, only update if it's a new high
                hand.append(c)
                if len(hand) == 5:
                    return hand
    elif clubs >= 5:
        for c in reversed(cards):
            if c.suit == "clubs":
                # if already 5 of this suit, only update if it's a new high
                hand.append(c)
                if len(hand) == 5:
                    return hand
    elif spades >= 5:
        for c in reversed(cards):
            if c.suit == "spades":
                # if already 5 of this suit, only update if it's a new high
                hand.append(c)
                if len(hand) == 5:
                    return hand
    else:
        return 0

def isQuad(cards):
    hand = []
    to_check = len(cards)-3
    for i in range(to_check):
        val = cards[i].value
        count = 1
        for j in range(i+1, len(cards)):
            new_val = cards[j].value
            if new_val == val:
                count += 1
        if count == 4:
            kicker = True
            for c in reversed(cards):
                if c.value == val:
                    hand.append(c)
                else:
                    if kicker:
                        hand.append(c)
                        kicker = False                      
            return hand
    return 0

#TODO check for A low straight
def isStraight(cards):
    hand = []
    counter = 1 
    high = cards[-1].value
    for i in range(len(cards) - 1):
        val1 = cards[len(cards)-i-1].value
        val2 = cards[len(cards)-i-2].value
        # if next value is same, just ignore
        if val1 - 1 == val2:
            counter += 1
        elif val1 != val2:
            counter = 1
            high = val2
        
        if counter == 5:
            # construct the hand
            for c in reversed(cards):
                if c.value == high:
                    hand.append(c)
                    high -= 1
                if len(hand) == 5:
                    return hand
    print("none")
    return 0

#TODO
def isFullHouse(cards):
    hand = []
    vals = [c.value for c in cards]
    trip_vals = []
    doub_vals = []
    for v in set(vals):
        if vals.count(v) == 3:
            trip_vals.append(v)
        if vals.count(v) == 2:
            doub_vals.append(v)

    if trip_vals and doub_vals:
        max_trip_val = max(trip_vals)
        max_doub_val = max(doub_vals)
        # construct hand
        for c in cards:
            if c.value == max_trip_val or c.value == max_doub_val:
                hand.append(c)
        return hand
    else:
        return 0

#TODO
def isTriple(cards):
    hand = []
    vals = [c.value for c in cards]
    trip_vals = []
    for v in set(vals):
        if vals.count(v) == 3:
            trip_vals.append(v)

    if trip_vals:
        max_trip_val = max(trip_vals)
        # construct hand
        kickers = 0
        for c in reversed(cards):
            if c.value == max_trip_val:
                hand.append(c)
            else:
                if kickers < 2:
                    hand.append(c)
                    kickers += 1
        return hand
    else:
        return 0

#TODO
def isTwoPair(cards):
    hand = []
    vals = [c.value for c in cards]
    doub_vals = []
    for v in set(vals):
        if vals.count(v) == 2:
            doub_vals.append(v)


    if len(doub_vals) >= 2:
        top_two_doub_vals = heapq.nlargest(2, doub_vals)
        # construct hand
        kickers = 0
        for c in reversed(cards):
            if c.value in top_two_doub_vals:
                hand.append(c)
            else:
                if kickers < 1:
                    hand.append(c)
                    kickers += 1
        return hand
    else:
        return 0

#TODO
def isPair(cards):
    hand = []
    vals = [c.value for c in cards]
    doub_vals = []
    for v in set(vals):
        if vals.count(v) == 2:
            doub_vals.append(v)

    if doub_vals:
        max_doub_val = max(doub_vals)
        # construct hand
        kickers = 0
        for c in reversed(cards):
            if c.value == max_doub_val:
                hand.append(c)
            else:
                if kickers < 3:
                    hand.append(c)
                    kickers += 1
        return hand
    else:
        return 0


def isNothing(cards):
    hand = cards[-5:]
    return hand