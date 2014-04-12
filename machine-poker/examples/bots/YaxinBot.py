#!/usr/bin/python
import sys
import json

"""YaxinBot:
   YaxinBot will go all in if its winning chance >= 70%.
   It will call if its winning chance >= 50% but less than 70%.
   It will fold when the winning chance <50%.
   """

if (len(sys.argv) < 2):
    # exit with an error
    sys.exit(1)
else:
    game_data_location = sys.argv[1]
    game_string = open(game_data_location, 'r')
    game_info = game_string.read()
    game = json.loads(game_info)

    """1. Check the game state:"""
    gameState = game["state"]
    winOdds = 0
    """2. Get the cards:"""
    hole = game["self"]["cards"]
    community = []
    if len(game["community"]) > 0:
        community = game["community"]

    if (gameState == "pre-flop" or
        gameState == "flop" or
        gameState == "turn" or
        gameState == "river"):
        if gameState != "river":
            winOdds = float(monte_carlo.cal_win_odds_mc(hole, community))
        else:
            winOdds = float(brute_force.cal_win_odds_bf(hole, community))
        	
	betting = game["betting"]
	canRaise = betting["canRaise"]
	if winOdds >= .70 and canRaise:
            # go all in
            mine = game["self"]
            print(mine["chips"])
	elif winOdds >= .50:
            print(betting["call"])
	else: # fold
            print(0)
    else:
        #game completes.
        print(0)
    sys.exit(0)
