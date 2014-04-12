#!/usr/bin/python
import sys
import json

if (len(sys.argv) < 2):
	# exit with an error
	print "DYING"
	sys.exit(1)
else:
	game_data_location = sys.argv[1]
	game_string = open(game_data_location, 'r')
	game_info = game_string.read()
	game = json.loads(game_info)
	if game["betting"]["canRaise"]:
		print game["self"]["chips"]
	else:
		print game["betting"]["call"]
	sys.exit(0)