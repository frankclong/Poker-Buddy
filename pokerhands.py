from card import Card
import heapq

def cardCodeToCard(c):
    if c[-1] == 'h':
        return Card(int(c[:-1]), "hearts")
    elif c[-1] == 's':
        return Card(int(c[:-1]), "spades")
    elif c[-1] == 'c':
        return Card(int(c[:-1]), "clubs")
    elif c[-1] == 'd':
        return Card(int(c[:-1]), "diamonds")

def compareOpponentHand(deck, community, score, hand):
    wins = 0
    losses = 0
    ties = 0
    num_remaining = len(deck.cards)
    for i in range(num_remaining - 1):
        cc1 = deck.cards[i]
        for j in range(i+1, num_remaining):
            cc2 = deck.cards[j]
            opp_hand = [cardCodeToCard(cc1), cardCodeToCard(cc2)]
            opp_cards = community.copy()
            opp_cards.extend(opp_hand)
            opp_cards = sorted(opp_cards, key=lambda x : x.value)
            opp_score, opp_best_hand = bestHand(opp_cards)
            if opp_score > score:
                losses += 1
            elif opp_score < score:
                wins += 1
            else: 
                tb = tiebreak(score, hand, opp_best_hand)
                if tb == 1:
                    wins += 1
                    #print('w')
                elif tb == -1:
                    losses += 1
                    #print('l')
                else:
                    ties += 1
                    #print('t')
                #opp_card_list.show()
                #print(cc1, cc2)
                #print("-----------------------------------------------------------------------------")

    #print("Wins: ", wins)
    #print("Losses: ", losses)
    #print("Ties: ", ties)
    #print("Win/Tie %: ", (wins+ties)/(wins+ties+losses)*100)
    return wins, losses, ties

def bestHand(cards):
    # Check for 5 card combos
    # Count number of occurences for each suit
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

    # Determine if flush exists
    if len(hearts) >= 5:
        flush_cards = hearts
    elif len(spades) >= 5:
        flush_cards = spades
    elif len(clubs) >= 5:
        flush_cards = clubs
    elif len(diamonds) >= 5:
        flush_cards = diamonds
    else:
        flush_cards = 0

    # If at least 5 occurences, look for a STRAIGHT FLUSH within those values
    # Note: cards are sorted and since all cards are same suit, no duplicate values
    # TODO: Checking for A-5 straight
    if flush_cards:
        if len(flush_cards) == 5:
            if (flush_cards[4].value - flush_cards[0].value)==5:
                return 8, flush_cards
        if len(flush_cards) == 6:
            if (flush_cards[5].value - flush_cards[1].value)==5:
                return 8, flush_cards[-5:]
            if (flush_cards[4].value - flush_cards[0].value)==5:
                return 8, flush_cards[0:5]
        if len(flush_cards) == 7:
            if (flush_cards[6].value - flush_cards[2].value)==5:
                return 8, flush_cards[-5:]
            if (flush_cards[5].value - flush_cards[1].value)==5:
                return 8, flush_cards[1:6]
            if (flush_cards[4].value - flush_cards[0].value)==5:
                return 8, flush_cards[0:5]

        # Check if 14 is in cards
        # Check if 2-5 exists
        # If so, return 8 with A-5 of that suit

    hand = isQuad(cards)
    if hand:
        return 7, hand

    # Identifying triples and doubles
    vals = [c.value for c in cards]
    trip_vals = []
    doub_vals = []
    for v in set(vals):
        if vals.count(v) == 3:
            trip_vals.append(v)
        if vals.count(v) == 2:
            doub_vals.append(v)

    # Full house
    if trip_vals and doub_vals:
        hand = []
        max_trip_val = max(trip_vals)
        max_doub_val = max(doub_vals)
        # construct hand
        for c in cards:
            if c.value == max_trip_val or c.value == max_doub_val:
                hand.append(c)
        return 6, hand
    
    # Flush
    if flush_cards:
        return 5, flush_cards[-5:] # 5 highest cards since they are sorted

    # Straight
    # New algorithm idea:
    # Remove duplicates and then use the checks from straight flush 
    # Might be able to determine easily since the double and triple values were already found
    hand = isStraight(cards)
    if hand:
        return 4, hand
    
    # Triple
    if trip_vals:
        hand = []
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
        return 3, hand
    
    # 2-pair
    if len(doub_vals) >= 2:
        hand = []
        # determine which highest doubles
        if len(doub_vals) == 2:
            top_two_doub_vals = doub_vals
        else:
            top_two_doub_vals = []
            if doub_vals[0] > doub_vals[1]:
                if doub_vals[1] > doub_vals[2]:
                    top_two_doub_vals = [doub_vals[0], doub_vals[1]]
                else:
                    top_two_doub_vals = [doub_vals[0], doub_vals[2]]
            else:
                if doub_vals[0] > doub_vals[2]:
                    top_two_doub_vals = [doub_vals[0], doub_vals[1]]
                else:
                    top_two_doub_vals = [doub_vals[1], doub_vals[2]]
        # construct hand
        kickers = 0
        for c in reversed(cards):
            if c.value in top_two_doub_vals:
                hand.append(c)
            else:
                if kickers < 1:
                    hand.append(c)
                    kickers += 1
        return 2, hand
    
    # 1-pair
    if doub_vals:
        hand = []
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
        return 1, hand

    # High card
    hand = cards[-5:] # if nothing else, just high card
    return 0, hand


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
    # if quad exists, the 4th card in a sort set of 7 cards is always the value
    hand = []
    qval = cards[3].value
    count = 0
    for i in range(len(cards)):
        if qval == cards[i].value:
            count += 1
    if count == 4:
        kicker = True
        for c in reversed(cards):
            if c.value == qval:
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
    return 0

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


# Determine if hand1 is better than hand2
def tiebreak(score, hand1, hand2):
    vals1 = sorted([c.value for c in hand1])
    vals2 = sorted([c.value for c in hand2])
    if score == 1: # pair
        # determine pair
        for i in range(4):
            if vals1[i] == vals1[i+1]:
                p1 = vals1[i]
        for i in range(4):
            if vals2[i] == vals2[i+1]:
                p2 = vals2[i]
        if p1 > p2:
            return 1
        elif p2 > p1:
            return -1
        else:
            for i in range(5):
                if vals1[4-i] > vals2[4-i]:
                    return 1
                elif vals1[4-i] < vals2[4-i]:
                    return -1
        return 0

    elif score == 2: # 2pair
        highdoub1 = vals1[3]
        highdoub2 = vals2[3]
        if highdoub1 > highdoub2:
            return 1
        elif highdoub1 < highdoub2:
            return -1
        else:
            lowdoub1 = vals1[1]
            lowdoub2 = vals2[1]
            if lowdoub1 > lowdoub2:
                return 1
            elif lowdoub1 < lowdoub2:
                return -1
            else:
                # kicker - can only be in position 1, 3, 5 if sorted
                if vals1[-1] > vals2[-1]:
                    return 1
                elif vals1[-1] < vals2[-1]:
                    return -1
                else:
                    if vals1[2] > vals2[2]:
                        return 1
                    elif vals1[2] < vals2[2]:
                        return -1
                    else:
                        if vals1[0] > vals2[0]:
                            return 1
                        elif vals1[0] < vals2[0]:
                            return -1
        return 0
    elif score == 3: # triple
        trip1 = vals1[2]
        trip2 = vals2[2]
        if trip1 > trip2:
            return 1
        elif trip1 < trip2:
            return -1
        else:
            for i in range(5):
                if vals1[4-i] > vals2[4-i]:
                    return 1
                elif vals1[4-i] < vals2[4-i]:
                    return -1
        return 0
    elif score == 4 or score == 8 or score == 9: # straights
        if max(vals1) > max(vals2):
            return 1
        elif max(vals1) < max(vals2):
            return -1
        else:
            return 0
    elif score == 0 or score == 5: #flush
        for i in range(5):
            if vals1[-i-1] > vals2[-i-1]:
                return 1
            elif vals1[-i-1] < vals2[-i-1]:
                return -1
        return 0
    elif score == 6: # full house 
        trip1 = vals1[2]
        trip2  = vals2[2]
        if trip1 > trip2:
            return 1
        elif trip1 < trip2:
            return -1
        else:
            if vals1[0] == trip1:
                doub1 = vals1[3]
            else:
                doub1 = vals1[0]
            if vals2[0] == trip2:
                doub2 = vals2[3]
            else:
                doub2 = vals2[0]
            if doub1 > doub2:
                return 1
            elif doub1 < doub2:
                return -1
        return 0
    elif score == 7: #quad
        quad1 = vals1[2]
        quad2 = vals2[2]  
        if quad1 > quad2:
            return 1
        elif quad1 < quad2:
            return -1
        else:
            if vals1[0] == quad1:
                kicker1 = vals1[-1]
            else:
                kicker1 = vals1[0]
            if vals2[0] == quad2:
                kicker2 = vals2[-1]
            else:
                kicker2 = vals2[0]
            if kicker1 > kicker2:
                return 1
            elif kicker1 < kicker2:
                return -1
        return 0
    return 0