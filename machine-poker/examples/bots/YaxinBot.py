#!/usr/bin/python
import sys
import json

if (len(sys.argv) < 2):
	# exit with an error
	sys.exit(1)
else:
	game_data_location = sys.argv[1]
	game_string = open(game_data_location, 'r')
	game_info = game_string.read()
	game = json.loads(game_info)
	betting = game["betting"]
	can_raise = betting["canRaise"]
	# TODO get win chance
	win_chance = .75
	if win_chance >= .70 and can_raise:
		# go all in
		mine = game["self"]
		print mine["chips"]
	elif win_chance >= .50:
		print betting["call"]
	else: # fold
		print 0
