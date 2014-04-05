var MachinePoker = require('../lib/index')
    , LocalSeat = MachinePoker.seats.JsLocal
    , RemoteSeat = MachinePoker.seats.Remote
    , CallBot = require('./bots/callBot')
    , FoldBot = require('./bots/foldBot')
    , RandBot = require('./bots/randBot')
    , MemoryBot = require('./bots/wrapperBot')
    , narrator = MachinePoker.observers.narrator
    //, fileLogger = MachinePoker.observers.fileLogger('./examples/results.json')
    , fs = require('fs');

// Number of games to run against each opponent
var gamesToRun = 3;

// This is going to be a tournament, so generate an array of possible opponents
var opponents = [CallBot, FoldBot, RandBot];
var winChance = {'CallBot':0, 'FoldBot':0, 'RandBot':0 };
var completedGames = 0;

// TODO: the libraries aren't synchronous. Make this code asynchronous

for (var i = 0; i < opponents.length; i += 1) {

	// Run a configurable number of games against each opponent
	for (var j = 0; j < gamesToRun; j += 1) {

		// Generate the array of players in the game, which will just be our player and 
		// the ith member of the opponents array
		var players = [LocalSeat.create(MemoryBot), LocalSeat.create(opponents[i])];

		// Dynamically create the file logger for each game

		var resultFileName = './examples/results' + players[1].name + j + '.json';

		var gameEndCallback = function gameEndCallback(enemyName, win) {
			console.log("Stuff should be happening");
			console.log(win);
			console.log(enemyName);
			completedGames += 1;

			// If we have more than 1000 chips, we won the game
			if (win) {
				console.log("WINNER! " + enemyName);
				winChance[enemyName] += 1;
			}

			// Otherwise, we're done

			console.log("DONE");
			console.log(winChance);
		};

		//var fileLoggerTwo = MachinePoker.observers.fileLogger(resultFileName);
		// Generate a new table
		var table = MachinePoker.create({
	  		maxRounds: 100
		});

		// Add the players to the table
		table.addPlayers(players);

		// When this tournament is over, process the results
		table.on('tournamentClosed', gameEndCallback);

		//table.addObserver(fileLoggerTwo);

		// Run the game
	  	table.start();
	}
}


function printResults() {
	if (completedGames >= (gamesToRun * opponents.length)) {

		var resultsFileName = './examples/results.json';

		var gameResults = "Memory Bot Win Rate Against: \n\n";

		for (var i = 0; i < opponents.length; i += 1) {
			var name = LocalSeat.create(opponents[i]).name;
			gameResults += name + ": ";
			gameResults += ( (winChance[name] / gamesToRun) * 100 ) + "%\n";
		}
		console.log(gameResults);
		fs.writeFileSync(resultsFileName, gameResults);
		process.exit();
	}
}

setInterval(printResults, 100);
