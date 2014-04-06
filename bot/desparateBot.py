#!/usr/bin/python
import sys
import json
import random

# this bot will call in it has over 33% of its starting chips, otherwise it will go all in

if (len(sys.argv) < 2):
	# exit with an error
	sys.exit(1)
else:
	game_data_location = sys.argv[1]
	game_string = open(game_data_location, 'r')
	game_info = game_string.read()
	game = json.loads(game_info)
	betting = game["betting"]
	mine = game["self"]
	if mine["chips"] < 333 #TODO: this is hardcoded to assume that all players start with 1000 chips. That might not be the case
		# check if we can raise
		if betting["canRaise"] == "true":
			# go all in
			return mine["chips"]
	# else call
	return betting["call"]
	
	
	
	