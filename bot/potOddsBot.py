#!/usr/bin/python
"""potOddsBot.py:
   This is an agent which will bet the exact amount of chips according
   to the pot odds."""
import sys
import json
import monte_carlo
import brute_force
import CT

if (len(sys.argv) < 2):
    # exit with an error
    debugF = open('debugPotOddsBot.txt','a')
    debugF.write(sys.argv + '\n')
    debugF.close()
    sys.exit(1)
else:
    game_data_location = sys.argv[1]
    game_string = open(game_data_location, 'r')
    game_info = game_string.read()
    game = json.loads(game_info)

    """1. Get the current amount in pot"""
    pot = 0
    for player in game["players"]:
        pot = pot + player["wagered"]
    
    """2. Check the game state:"""
    gameState = game["state"]
    winOdds = 0
    hole = [game["self"]["cards"][0],game["self"]["cards"][1]]
    hole[0] = CT.translate_from_mp_to_string(hole[0])
    hole[1] = CT.translate_from_mp_to_string(hole[1])
    community = []
    if len(game["community"]) > 0:
        community = game["community"]
        lenCom = len(community)
        for i in range(0,lenCom):
            community[i] = CT.translate_from_mp_to_string(community[i])
    
    if (gameState == "pre-flop" or
        gameState == "flop" or
        gameState == "turn" or
        gameState == "river"):
        if gameState != "river":
            winOdds = monte_carlo.cal_win_odds_mc(hole, community)
        else:
            winOdds = brute_force.cal_win_odds_bf(hole, community)
        bet = winOdds * pot / (1-winOdds)
        if bet < game["betting"]["call"]:
            """The largest amout you can bet < what you need to call.
               Can only fold."""
            print(0)
        elif game["betting"]["canRaise"] == "false":
            print(game["betting"]["call"])
        else:
            print(int(bet/game["betting"]["raise"]) *
                  game["betting"]["raise"])
    else:
        """complete"""
        print(0)
    sys.exit(0)
