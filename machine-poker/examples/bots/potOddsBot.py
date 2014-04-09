#!/usr/bin/python
"""potOddsBot.py:
   This is an agent which will bet the exact amount of chips according
   to the pot odds."""
import sys
import json
import monte_carlo
import brute_force
import CT

debugF = open('debugPotOddsBot','a')
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
        bet = winOdds * pot / (1-winOdds)
        if bet < game["betting"]["call"]:
            """The largest amount you can bet < what you need to call.
               Can only fold."""
            debugF.write("WIN ODDS: " + str(winOdds) + " FOLDING\n")
            print(0)
        elif game["betting"]["canRaise"] == "false":
            debugF.write("WIN ODDS: " + str(winOdds)
                         +  " CALLING: "
                         + str(game["betting"]["call"]) + "\n")
            print(game["betting"]["call"])
        else:
            debugF.write("WIN ODDS: " + str(winOdds)
                         +  " BET: "
                         + str(int(bet/game["betting"]["raise"]) *
                               game["betting"]["raise"]) + "\n")
            print(int(bet/game["betting"]["raise"]) *
                  game["betting"]["raise"])
    else:
        """complete"""
        print(0)
    debugF.close()
    sys.exit(0)
