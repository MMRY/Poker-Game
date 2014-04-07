#!/usr/bin/python
import sys
import json
import random

# this bot will call in it has over 33% of its starting chips, otherwise it will go all in

if (len(sys.argv) < 2):
	# exit with an error
	sys.exit(1)
else:
	game_string = sys.argv[1]
	game = json.loads(game_string)
	betting = game["betting"]
	mine = game["self"]
	if mine["chips"] < 333 #TODO: this is hardcoded to assume that all players start with 1000 chips. That might not be the case
		# check if we can raise
		if betting["canRaise"] == "true":
			# go all in
			return mine["chips"]
	# else call
	return betting["call"]
	
	
	
	