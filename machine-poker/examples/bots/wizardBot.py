#!/usr/bin/python
"""potOddsBot.py:
   This is an agent which will bet the exact amount of chips according
   to the pot odds."""
import sys
import json
import monte_carlo
import brute_force
import CT


def bettingAmount(winOdds, chips, minCap, multiplyer, callAmount):
    if winOdds >= minCap:
        if chips >= multiplyer * callAmount:
            print(multiplyer * callAmount)
        else:
            print(chips)
        return True
    return False

debugF = open('debugWizardBot','a')
if (len(sys.argv) < 2):
    debugF.write(sys.argv + '\n')
    debugF.close()
    sys.exit(1)
else:
    game_data_location = sys.argv[1]
    game_string = open(game_data_location, 'r')
    game_info = game_string.read()
    game = json.loads(game_info)

    #debugF.write(str(game) + "\n")

    """1. Get the current amount in pot"""
    pot = 0 #Current amount in bot
    for player in game["players"]:
        pot = pot + player["wagered"]

    """1.1 Get how many chips you have:"""
    chips = game["self"]["chips"]
    
    """2. Check the game state:"""
    gameState = game["state"]
    winOdds = 0
    hole = [game["self"]["cards"][0],game["self"]["cards"][1]]
    community = []
    if len(game["community"]) > 0:
        community = game["community"]
    #debugF.write("hole " + str(hole) + " community: " + str(community) + " ")
    
    if (gameState == "pre-flop" or
        gameState == "flop" or
        gameState == "turn" or
        gameState == "river"):
        if gameState != "river":
            winOdds = float(monte_carlo.cal_win_odds_mc(hole, community))
        else:
            winOdds = float(brute_force.cal_win_odds_bf(hole, community))

        """ 3. Return the bet:"""
        if game["betting"]["canRaise"] == True:
            if (bettingAmount(winOdds, chips, 0.7, 8,
                             game["betting"]["raise"])):
                a = 1
            elif bettingAmount(winOdds, chips, 0.52, 4,
                               game["betting"]["raise"]):
                a = 1
            elif bettingAmount(winOdds, chips, 0.45, 2,
                               game["betting"]["raise"]):
                a = 1
            elif bettingAmount(winOdds, chips, 0.35, 1,
                               game["betting"]["raise"]):
                a = 1
            else:
                print(0)
        else:
            if chips < game["betting"]["call"]:
                print(0)
            else:
                print(game["betting"]["call"])     
                
    else:
        """complete"""
        print(0)
    debugF.close()
    sys.exit(0)
    
