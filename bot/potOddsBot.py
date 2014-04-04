#!/usr/bin/python
"""potOddsBot.py:
   This is an agent which will bet the exact amount of chips according
   to the pot odds."""
import sys
import json

"""
if (len(sys.argv) < 2):
	# exit with an error
	sys.exit(1)
else:
	game_data_location = sys.argv[1]
	game_string = open(game_data_location, 'r')
	game_info = game_string.read()
	game = json.loads(game_info)
	betting = game["betting"]
	print betting["raise"]
	sys.exit(0)
"""


""" Test without interacting with the MachinePoker game:"""
""" 1. Test preflop - Monte Carlo method:"""

""" 2. Test flop - brute-force method:"""
