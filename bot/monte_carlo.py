#!/usr/bin/env python
"""monte_carlo.py:
   This file provides the monte carlo simulation method to calculate
   win odds when you only have the information of your hole cards."""
import CT
import pokerlib
import random
"""cal_win_odds_mc(hole, community):
   Given:
   (1) hole: An array storing two cards. Each card is a tuple.
             The first element of the tuple is rank.
             The second element of the tuple is suit.
             eg. (0, 's') = 2s
   (2) community: An array storing the dealt community cards. The length of
                  this array is the number of dealt community cards.
                  The length must be one of 0,3,4.
                  Each card is a tuple.
   Returns: The win odds given the cards you know.
   """
def cal_win_odds_mc(hole, community):
    #Does not check the len of hole and community.
    #Please use it according to the contract.

    """N = sample number"""
    N = 5000

    """1. Translate the cards into integers."""
    tempHole = hole
    hole = [CT.card_translate(tempHole[0][0],tempHole[0][1]),
            CT.card_translate(tempHole[1][0],tempHole[1][1])]
    tempCommunity = community
    community = []
    for card in tempCommunity:
        community.append(CT.card_translate(card[0],card[1]))

    """2. Create a deck without the known cards."""
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
            

    if len(community) == 0:
        return cal_win_odds_mc_preflop(hole,deck,N)
    elif len(community) == 3:
        return cal_win_odds_mc_flop(hole,community,deck,N)
    else: # len(community) == 4
        return cal_win_odds_mc_turn(hole,community,deck,N)
    

def cal_win_odds_mc_preflop(hole, deck, N):
    sumOfWin = 0
    for i in range(0,N-1):
        """1. Pick different cards for opponent and community randomly."""
        oppoC1 = deck[random.randint(0,len(deck)-1)]
        oppoC2 = deck[random.randint(0,len(deck)-1)]
        c1 = deck[random.randint(0,len(deck)-1)]
        c2 = deck[random.randint(0,len(deck)-1)]
        c3 = deck[random.randint(0,len(deck)-1)]
        c4 = deck[random.randint(0,len(deck)-1)]
        c5 = deck[random.randint(0,len(deck)-1)]
        while not no_cards_equal_7([oppoC1,oppoC2,c1,c2,c3,c4,c5]):
            oppoC1 = deck[random.randint(0,len(deck)-1)]
            oppoC2 = deck[random.randint(0,len(deck)-1)]
            c1 = deck[random.randint(0,len(deck)-1)]
            c2 = deck[random.randint(0,len(deck)-1)]
            c3 = deck[random.randint(0,len(deck)-1)]
            c4 = deck[random.randint(0,len(deck)-1)]
            c5 = deck[random.randint(0,len(deck)-1)]

        """2. Compute hand strength."""
        myHand = hole + [c1,c2,c3,c4,c5]
        oppoHand = [oppoC1,oppoC2,c1,c2,c3,c4,c5]
        myValue = pokerlib.eval_7hand(myHand)
        oppoValue = pokerlib.eval_7hand(oppoHand)
        if myValue < oppoValue:
            sumOfWin = sumOfWin + 1

    return float(sumOfWin)/float(N)

"""Given: len(community) = 3"""
def cal_win_odds_mc_flop(hole, community, deck, N):
    sumOfWin = 0
    for i in range(0,N-1):
        """1. Pick different cards for opponent and community randomly."""
        oppoC1 = deck[random.randint(0,len(deck)-1)]
        oppoC2 = deck[random.randint(0,len(deck)-1)]
        turn = deck[random.randint(0,len(deck)-1)]
        river = deck[random.randint(0,len(deck)-1)]
        while not no_cards_equal_4([oppoC1,oppoC2,turn,river]):
            oppoC1 = deck[random.randint(0,len(deck)-1)]
            oppoC2 = deck[random.randint(0,len(deck)-1)]
            turn = deck[random.randint(0,len(deck)-1)]
            river = deck[random.randint(0,len(deck)-1)]
        """2. Compute hand strength."""
        myHand = hole + community + [turn,river]
        oppoHand = [oppoC1,oppoC2] + community + [turn,river]
        myValue = pokerlib.eval_7hand(myHand)
        oppoValue = pokerlib.eval_7hand(oppoHand)
        if myValue < oppoValue:
            sumOfWin = sumOfWin + 1
    return float(sumOfWin)/float(N)

"""Given: len(community) = 4"""
def cal_win_odds_mc_turn(hole,community,deck,N):
    sumOfWin = 0
    for i in range(0,N-1):
        """1. Pick different cards for opponent and community randomly."""
        oppoC1 = deck[random.randint(0,len(deck)-1)]
        oppoC2 = deck[random.randint(0,len(deck)-1)]
        river = deck[random.randint(0,len(deck)-1)]
        while not no_cards_equal_3([oppoC1,oppoC2,river]):
            oppoC1 = deck[random.randint(0,len(deck)-1)]
            oppoC2 = deck[random.randint(0,len(deck)-1)]
            river = deck[random.randint(0,len(deck)-1)]
        """2. Compute hand strength."""
        myHand = hole + community + [river]
        oppoHand = [oppoC1,oppoC2] + community + [river]
        myValue = pokerlib.eval_7hand(myHand)
        oppoValue = pokerlib.eval_7hand(oppoHand)
        if myValue < oppoValue:
            sumOfWin = sumOfWin + 1
    return float(sumOfWin)/float(N)
        

"""no_cards_equal_7(cards):
   Given: cards is an array of 7 integers. Each integer represents a card.
   Returns: True if all of these 7 cards are distinct with each other.
            Else False.
            """
def no_cards_equal_7(cards):
    #We do not check the len(cards), please use as the contract says.
    if (cards[0] == cards[1] or
        cards[0] == cards[2] or
        cards[0] == cards[3] or
        cards[0] == cards[4] or
        cards[0] == cards[5] or
        cards[0] == cards[6] or
        cards[1] == cards[2] or
        cards[1] == cards[3] or
        cards[1] == cards[4] or
        cards[1] == cards[5] or
        cards[1] == cards[6] or
        cards[2] == cards[3] or
        cards[2] == cards[4] or
        cards[2] == cards[5] or
        cards[2] == cards[6] or
        cards[3] == cards[4] or
        cards[3] == cards[5] or
        cards[3] == cards[6] or
        cards[4] == cards[5] or
        cards[4] == cards[6] or
        cards[5] == cards[6]):
        return False
    else:
        return True

"""no_cards_equal_4(cards):
   Given: cards is an array of 4 integers."""
def no_cards_equal_4(cards):
    #We do not check the len(cards), please use as the contract says.
    if (cards[0] == cards[1] or
        cards[0] == cards[2] or
        cards[0] == cards[3] or
        cards[1] == cards[2] or
        cards[1] == cards[3] or
        cards[2] == cards[3]):
        return False
    else:
        return True

"""no_cards_equal_3(cards):
   Given: cards is an array of 3 integers."""
def no_cards_equal_3(cards):
    #We do not check the len(cards), please use as the contract says.
    if (cards[0] == cards[1] or
        cards[0] == cards[2] or
        cards[1] == cards[2]):
        return False
    else:
        return True

if __name__ == '__main__':
    import time
    """1. Only two hole cards are known."""
    print("Only two hole cards are known.")
    print('time: ' + str(time.time()))
    print(str(cal_win_odds_mc([(0,'s'),(9,'h')],[])))
    print('time: ' + str(time.time()))
    print(str(cal_win_odds_mc([(8,'s'),(8,'h')],[])))
    print('time: ' + str(time.time()))
    print(str(cal_win_odds_mc([(12,'h'),(12,'c')],[])))
    print('time: ' + str(time.time()))

    """2. Flop: (2 hole cards + 3 community cards):"""
    print("flop: " + str(cal_win_odds_mc([(0,'s'),(9,'h')],
                                         [(3,'d'),(12,'c'),(12,'d')])))

    print('time: ' + str(time.time()))
    """3. Turn: (2 hole cards + 4 community cards):"""
    print('turn:' + str(cal_win_odds_mc([(8,'s'),(8,'h')],
                                        [(3,'d'),(9,'c'),(10,'c'),(7,'d')])))

    print('time: ' + str(time.time()))

"""Below shows the test result. Time is in seconds."""
"""(Only your two hole cards are known.)"""
"""Test result 1: N = 5000
time: 1396637043.692616
0.4264
time: 1396637049.496948
0.7502
time: 1396637055.931316
0.8408
time: 1396637062.602697 """

"""Test result 2: N = 5000
time: 1396637310.199859
0.4126
time: 1396637313.205031
0.7542
time: 1396637316.409214
0.8526
time: 1396637319.854411"""

"""Test result 3: N = 5000
time: 1396637353.903359
0.4178
time: 1396637357.028537
0.7542
time: 1396637360.285724
0.843
time: 1396637363.71392"""

"""Test result 4: N = 10000. Much slower.
time: 1396637419.594116
0.4205
time: 1396637432.561858
0.7443
time: 1396637449.399821
0.8522
time: 1396637469.373963"""

"""Test result 5: N = 10000
time: 1396637527.590293
0.4202
time: 1396637544.059235
0.7481
time: 1396637553.115753
0.8464
time: 1396637564.815422"""

"""Test result 6: N = 7000
time: 1396639115.768132
0.4218571428571429
time: 1396639119.894368
0.7517142857142857
time: 1396639124.228615
0.8477142857142858
time: 1396639128.527861"""
