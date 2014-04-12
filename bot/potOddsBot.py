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
    pot = 0
    for player in game["players"]:
        pot = pot + player["wagered"]
    
    """2. Check the game state:"""
    gameState = game["state"]
    winOdds = 0
    hole = [CT.trans_string_to_int(game["self"]["cards"][0]),
            CT.trans_string_to_int(game["self"]["cards"][1])]
    community = []
    if len(game["community"]) > 0:
        community = game["community"]
        lenCom = len(community)
        for i in range(0,lenCom):
            community[i] = CT.trans_string_to_int(community[i])
    #debugF.write("hole " + str(hole) + " community: " + str(community) + " ")
    
    if (gameState == "pre-flop" or
        gameState == "flop" or
        gameState == "turn" or
        gameState == "river"):
        if gameState != "river":
            winOdds = float(monte_carlo.cal_win_odds_mc(hole, community))
        else:
            winOdds = float(brute_force.cal_win_odds_bf(hole, community))
            
        """Calculate the bet:"""
        bet = abs(winOdds * pot / (1-2winOdds))
        
        if bet < game["betting"]["call"]:
            """The largest amout you can bet < what you need to call.
               Can only fold."""
            debugF.write("WIN ODDS: " + str(winOdds) + " FOLDING\n")
            print(0)
        elif game["betting"]["canRaise"] == False:
            debugF.write("WIN ODDS: " + str(winOdds) +  " CALLING: "
                         + str(game["betting"]["call"]) + "\n")
            print(game["betting"]["call"])
        else:
            debugF.write("WIN ODDS: " + str(winOdds) +  " BET: "
                         + str(int(bet/game["betting"]["raise"]) *
                  game["betting"]["raise"]) + "\n")
            print(int(bet/game["betting"]["raise"]) *
                  game["betting"]["raise"])
    else:
        """complete"""
        print(0)
    debugF.close()
    sys.exit(0)
