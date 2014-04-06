#!/usr/bin/python
import sys
import json
import random

# this bot will always bet with a value between the minimum bet and the maxmimum bet (all in)

if (len(sys.argv) < 2):
	# exit with an error
	sys.exit(1)
else:
	game_string = sys.argv[1]
	game = json.loads(game_string)
	# first check if we can raise
	betting = game["betting"]
	if betting["canRaise"] == "true":
		mine = game["self"]
		min_bet = betting["raise"]
		max_chips = mine["chips"]
		if max_chips <= min_bet:
			# we must go all in
			return max_chips
		else:
			# get a random bet which is a multiple of 5 (TODO: is 5 the correct betting increment?)
			bet = randrange(min_bet, max_chips, 5)
			return bet
	else: # if we can't raise
		return betting["call"]
	betting = game["betting"]
	print betting["raise"]
	sys.exit(0)