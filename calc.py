from pokerhands import bestHand, compareOpponentHand, cardCodeToCard
import time

def calculate(deck, community, my_hand):
    total_wins = 0
    total_losses = 0
    total_ties = 0
    
    if len(community) == 5:
        
        my_cards = community.copy()
        my_cards.extend(my_hand)
        my_cards = sorted(my_cards, key=lambda x : x.value)
        # SCORE AND BEST HAND
        score, best_hand = bestHand(my_cards)
        # Generate opposing hands based on remaining cards in deck and compare scores with our best hand
        wins, losses, ties = compareOpponentHand(deck, community, score, best_hand)
       
        return wins, losses, ties
    elif len(community) == 4:
        for i in range(len(deck.cards)):
            # draw a card and add to community
            working_deck = deck.copy()
            working_community = community.copy()
            river = cardCodeToCard(deck.cards[i])
            working_community.append(river)
            working_deck.remove(river)

            wins, losses, ties = calculate(working_deck, working_community, my_hand)
            total_wins += wins
            total_losses += losses
            total_ties += ties
        return total_wins, total_losses, total_ties
    elif len(community) == 3:
        for i in range(len(deck.cards)-1):
            start_time = time.time()
            for j in range(i+1, len(deck.cards)):
                # draw two card and add to community
                working_deck = deck.copy()
                working_community = community.copy()
                turn = cardCodeToCard(deck.cards[i])
                river = cardCodeToCard(deck.cards[j])
                working_community.append(turn)
                working_deck.remove(turn)
                working_community.append(river)
                working_deck.remove(river)

                wins, losses, ties = calculate(working_deck, working_community, my_hand)
                total_wins += wins
                total_losses += losses
                total_ties += ties
                #print(i, wins)
            print("--- %s seconds ---" % (time.time() - start_time))
        return total_wins, total_losses, total_ties
    else:
        return 0,0,0