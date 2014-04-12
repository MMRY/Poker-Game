#!/usr/bin/env python
"""monte_carlo.py:
   This file provides the monte carlo simulation method to calculate
   win odds when you only have the information of your hole cards."""
import CT
import pokerlib
import random

"""cal_win_odds_mc(hole, community):
   Given:
   (1) hole: An array storing two cards.
             Each card is a string representing the card.
             eg. 'Qd' where Q is the rank, d is the suit(Diamonds).
                 'Ts' where T(10) is the rank, s is the suit(Spades).
                 '2h' where 2 is the rank, h is the suit(Hearts).
   (2) community: An array storing the dealt community cards. The length of
                  this array is the number of dealt community cards.
                  The length must be one of 3, 4, 5.
                  Each card is a string. Refer to "hole".
       IF COMMUNITY IS EMPTY: pass [] as community.
   Returns: The win odds given the cards you know.
            Float number.
   """
def cal_win_odds_mc(hole, community):
    #Does not check the len of hole and community.
    #Please use it according to the contract.

    """N = sample number"""
    N = 5000

    """1. Translate the known cards into integers."""
    hole[0] = CT.trans_string_to_int(hole[0])
    hole[1] = CT.trans_string_to_int(hole[1])
    for i in range(0,len(community)):
        community[i] = CT.trans_string_to_int(community[i])

    """2. Call the corresponding function to calculate."""
    if len(community) == 0:
        return cal_win_odds_mc_preflop(hole,N)
    elif len(community) == 3:
        return cal_win_odds_mc_flop(hole,community,N)
    else: # len(community) == 4
        return cal_win_odds_mc_turn(hole,community,N)
    
"""cal_win_odds_mc_preflop(hole,N):
   This function will be called by the cal_win_odds_mc() method.
   Given: hole: an array with two integers.
          N: the number of sampling.
   Returns: Using monte-carlo method, sampling N times and compare who wins.
            return the win odds of current state.
            """
def cal_win_odds_mc_preflop(hole, N):
    deck = deck_without_known_cards(hole)
    sumOfWin = 0
    for i in range(0,N-1):
        """1. Randomly fetch 7 cards."""
        cardSamples = random.sample(deck,7)
        """2. Compute hand strength."""
        myValue = pokerlib.eval_7hand(hole + cardSamples[2:])
        oppoValue = pokerlib.eval_7hand(cardSamples)
        if myValue < oppoValue:
            sumOfWin = sumOfWin + 1
    return float(sumOfWin)/float(N)

"""Given: len(community) = 3"""
def cal_win_odds_mc_flop(hole, community, N):
    deck = deck_without_known_cards(hole + community)
    sumOfWin = 0
    for i in range(0,N-1):
        """1. Randomly fetch 4 cards."""
        cardSamples = random.sample(deck,4)
        """2. Compute hand strength."""
        myValue = pokerlib.eval_7hand(hole + community + cardSamples[2:])
        oppoValue = pokerlib.eval_7hand(cardSamples + community)
        if myValue < oppoValue:
            sumOfWin = sumOfWin + 1
    return float(sumOfWin)/float(N)

"""Given: len(community) = 4"""
def cal_win_odds_mc_turn(hole,community,N):
    deck = deck_without_known_cards(hole + community)
    sumOfWin = 0
    for i in range(0,N-1):
        """1. Randomly fetch 3 cards."""
        cardSamples = random.sample(deck,3)
        """2. Compute hand strength."""
        myValue = pokerlib.eval_7hand(hole + community + cardSamples[2:])
        oppoValue = pokerlib.eval_7hand(cardSamples + community)
        if myValue < oppoValue:
            sumOfWin = sumOfWin + 1
    return float(sumOfWin)/float(N)

"""deck_without_known_cards(knownCards):
   Given: an array with known cards
   Returns: a deck without known cards."""
def deck_without_known_cards(knownCards):
    deck = [0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0]
    pokerlib.init_deck(deck)
    """2.1 Delete known cards:"""
    i = 0
    lenDeck = len(deck)
    while i < lenDeck:
        if deck[i] in knownCards:
            deck.pop(i)
            lenDeck = lenDeck - 1
        else:
            i = i + 1
    return deck

if __name__ == '__main__':
    import time
    """1. Preflop Stage:"""
    print('time: ' + str(time.time()))
    print('preflop eg 1: ' + str(cal_win_odds_mc(['8s','Js'],[])))
    print('preflop eg 1: ' + str(cal_win_odds_mc(['9s','7s'],[])))
    print('preflop eg 1: ' + str(cal_win_odds_mc(['2s','3d'],[])))
    print('time: ' + str(time.time()))

    """2. Flop Stage:"""
    print('flop eg 1: ' + str(cal_win_odds_mc(['2c','2s'],
                                              ['9c','7h','5c'])))
    print('time: ' + str(time.time()))

    """3. Turn Stage:"""
    print('turn eg 1: ' + str(cal_win_odds_mc(['Qh','2c'],
                                              ['As','Tc','4c','2d'])))

    print('time: ' + str(time.time()))

"""When N = 5000, each monte-carlo prediction takes about 3 secs."""
"""When N = 10000, the time doubles."""
