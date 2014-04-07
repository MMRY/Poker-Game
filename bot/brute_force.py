#!/usr/bin/env python
"""brute_force.py:
   This file provides the brute-force method to calculate the win odds."""
import CT
import pokerlib
"""cal_win_odds_bf(hole, community):
   Given:
   (1) hole: An array storing two cards. Each card is a tuple.
             The first element of the tuple is rank.
             The second element of the tuple is suit.
             eg. (0, 's') = 2s
   (2) community: An array storing the dealt community cards. The length of
                  this array is the number of dealt community cards.
                  The length must be one of 3, 4, 5.
                  Each card is a tuple.
   Returns: The win odds given the cards you know.
   """
debugF = open('debugBruteForce','a')
def cal_win_odds_bf(hole, community):
    #debugF.write("hole: " + str(hole) + " community: " + str(community) + "\n")
    if len(hole) != 2:
        raise ValueError('There should be 2 hole cards!\n')
    if len(community) not in range(3,6):
        raise ValueError('Incorrect number of community cards!\n')

    """1. Translate the known cards into integers."""
    tempHole = hole
    hole = [CT.card_translate(tempHole[0][0],tempHole[0][1]),
            CT.card_translate(tempHole[1][0],tempHole[1][1])]
    tempCommunity = community
    community = []
    for card in tempCommunity:
        community.append(CT.card_translate(card[0],card[1]))

    """2. Create a deck without known cards."""
    knownCards = hole + community
    deck = [0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0]
    pokerlib.init_deck(deck)
    """   Delete known cards:"""
    i = 0
    lenDeck = len(deck)
    while i < lenDeck:
        if (deck[i] in hole) or (deck[i] in community):
            deck.pop(i)
            lenDeck = lenDeck - 1
        else:
            i = i + 1

    if len(community) == 3:
        return cal_win_odds_bf_flop(hole, community, deck)
    elif len(community) == 4:
        return cal_win_odds_bf_turn(hole, community, deck)
    else:
        return cal_win_odds_bf_river(hole, community, deck)
    debugF.close()

def cal_win_odds_bf_flop(hole, community, deck):
    """ The uncertainty are:
        1. Opponent's hole cards.
        2. Turn and River."""
   # debugF.write("hole: " + str(hole) + " community: " + str(community) + " deck: " + str(deck) + "\n")
    sumOfComparison = 0
    sumOfWin = 0
    sampleCards = [0,0,0,0] # 4 cards of uncertainty
    for a in range(0,44):
        sampleCards[0] = deck[a]
        for b in range(a+1,45):
            sampleCards[1] = deck[b]
            for c in range(b+1,46):
                sampleCards[2] = deck[c]
                for d in range(c+1,47):
                    sampleCards[3] = deck[d]
                    #DEBUGGGGGGGGGGGGGGGGGG
                    #print('sample cards:' + str(sampleCards))
                    """There are C(2,4) possible combinations of
                       opponent's hole cards + (turn + river)"""
                    for comb in combination4:
                        oppoHole = [sampleCards[comb[0]],sampleCards[comb[1]]]
                        myHand = (hole + community +
                                  [sampleCards[comb[2]],sampleCards[comb[3]]])
                        oppoHand = ([sampleCards[comb[0]],sampleCards[comb[1]]]
                                    + community +
                                    [sampleCards[comb[2]],sampleCards[comb[3]]])
                        #DEBUGGGGGGGGGGGGGGGGGG
                        #print('myHand:' + str(myHand))
                        #print('oppoHand:' + str(oppoHand))
                        sumOfComparison = sumOfComparison + 1
                        myValue = pokerlib.eval_7hand(myHand)
                        oppoValue = pokerlib.eval_7hand(oppoHand)
                        if myValue < oppoValue:
                            sumOfWin = sumOfWin + 1
    #debugF.write("odds: " + str(float(sumOfWin)/float(sumOfComparison)) + "\n")
    return float(sumOfWin)/float(sumOfComparison)

def cal_win_odds_bf_turn(hole, community, deck):
    """ The uncertainty are:
        1. Opponent's hole cards.
        2. River."""
   # debugF.write("hole: " + str(hole) + " community: " + str(community) + " deck: " + str(deck) + "\n")
    sumOfComparison = 0
    sumOfWin = 0
    sampleCards = [0,0,0]
    for a in range(0,44):
        sampleCards[0] = deck[a]
        for b in range(a+1,45):
            sampleCards[1] = deck[b]
            for c in range(b+1,46):
                sampleCards[2] = deck[c]
                """There are C(2,3) possible combinations of
                   opponent's hole cards + river"""
                for comb in combination3:
                    myHand = hole + community + [sampleCards[comb[2]]]
                    oppoHand = ([sampleCards[comb[0]],sampleCards[comb[1]]]
                                + community + [sampleCards[comb[2]]])
                    sumOfComparison = sumOfComparison + 1
                    myValue = pokerlib.eval_7hand(myHand)
                    oppoValue = pokerlib.eval_7hand(oppoHand)
                    if myValue < oppoValue:
                        sumOfWin = sumOfWin + 1
    #debugF.write("odds: " + str(float(sumOfWin)/float(sumOfComparison)) + "\n")
    return float(sumOfWin)/float(sumOfComparison)

def cal_win_odds_bf_river(hole, community, deck):
    """ The uncertainty are:
        Opponent's hole cards."""
    #debugF.write("hole: " + str(hole) + " community: " + str(community) + " deck: " + str(deck) + "\n")
    sumOfComparison = 0
    sumOfWin = 0
    oppoC1 = 0
    oppoC2 = 0
    for a in range(0,44):
        oppoC1 = deck[a]
        for b in range(a+1,45):
            oppoC2 = deck[b]
            myHand = hole + community
            oppoHand = [oppoC1,oppoC2] + community
            sumOfComparison = sumOfComparison + 1
            myValue = pokerlib.eval_7hand(myHand)
            oppoValue = pokerlib.eval_7hand(oppoHand)
            if myValue < oppoValue:
                sumOfWin = sumOfWin + 1
    #debugF.write("odds: " + str(float(sumOfWin)/float(sumOfComparison)) + "\n")
    return float(sumOfWin)/float(sumOfComparison)

combination4 = [(0,1,2,3),
                (0,2,1,3),
                (0,3,1,2),
                (1,2,0,3),
                (1,3,0,2),
                (2,3,0,1)]
combination3 = [(0,1,2),
                (0,2,1),
                (1,2,0)]
                        

if __name__ == '__main__':
    import time
    print('time: ' + str(time.time()))
    print('3 com: '+ str(cal_win_odds_bf([(0,'s'),(9,'h')],
                                         [(3,'d'),(12,'c'),(12,'d')])))
    print('time: ' + str(time.time()))
    print('4 com: '+ str(cal_win_odds_bf([(8,'s'),(8,'h')],
                                         [(3,'d'),(9,'c'),(10,'c'),(7,'d')])))
    print('time: ' + str(time.time()))
    print('5 com: '
          + str(cal_win_odds_bf([(12,'h'),(12,'c')],
                                [(4,'c'),(5,'c'),(6,'c'),(7,'c'),(8,'c')])))
    print('time: ' + str(time.time()))

    """Test result:
time: 1396594048.670823
0.390519440473187
time: 1396594153.816837
0.7185770750988142
time: 1396594161.787293
0.0
time: 1396594162.25332
"""
    
    
