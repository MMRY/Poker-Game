#!/usr/bin/python
"""potOddsBot.py:
   This is an agent which will bet the exact amount of chips according
   to the pot odds."""
import sys
import json
import monte_carlo
import brute_force
import CT
import os
import random

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
    """get the game's unique ID. We use this to read/write from our persistent game data file"""
    game_id = game["gameID"]
    file_exists = os.path.isfile("data_" + game_id)
    if file_exists:
        dataFile = open("data_" + game_id, 'r+')
        fileData = dataFile.read()
        data = json.loads(fileData)
    else:
        dataFile = open("data_" + game_id, 'w')
        # construct the json data
        data = {}
        data["bluffChance"] = 0.5
        data["lastBluffHand"] = 0
        data["bluffStage"] = ""
        data["needToUpdateBluffChance"] = 0
        debugF.write(str(data) + "\n")

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
        bet = abs(winOdds * pot / (1-2*winOdds))
        debugF.write("intial bet: " + str(bet) + "\n")
        if bet < game["betting"]["call"]:
            """The largest amout you can bet < what you need to call.
               Can only fold."""
            debugF.write("TAFDSDASFDAS")
            debugF.write("WIN ODDS: " + str(winOdds) + " FOLDING\n")
            bet = 0
        elif game["betting"]["canRaise"] == False:
            debugF.write("TAFDSDASFDAS")
            debugF.write("WIN ODDS: " + str(winOdds) +  " CALLING: "
                         + str(game["betting"]["call"]) + "\n")
            bet = game["betting"]["call"]
        else:
            willBluff = random.random()
            willBluff = (willBluff <= data["bluffChance"])
            if willBluff:
                bet = (int(bet/game["betting"]["raise"]) *
                  (2 * game["betting"]["raise"]))
            else:
                bet = int(bet/game["betting"]["raise"]) * game["betting"]["raise"]
            debugF.write("TAFDSDASFDAS")
            debugF.write("WIN ODDS: " + str(winOdds) +  " BET: "
                         + str(bet) + " BLUFFING: " + str(willBluff) + "\n")
        print(bet)
    else:
        """complete """
        print(0)

    """ dump our data JSON back into the file """
    data_string = json.dumps(data)
    if file_exists:
        dataFile.seek(0)
    dataFile.write(data_string)
    dataFile.truncate()
    dataFile.close()
    debugF.close()
    sys.exit(0)
