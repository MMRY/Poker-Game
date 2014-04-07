#!/usr/bin/python
import sys
import json

if (len(sys.argv) < 2):
	# exit with an error
	sys.exit(1)
else:
	game_string = sys.argv[1]
	game = json.loads(game_string)
	betting = game["betting"]
	print betting["raise"]
	sys.exit(0)