var startTime = new Date();

var MachinePoker = require('../lib/index')
    , LocalSeat = MachinePoker.seats.JsLocal
    , RemoteSeat = MachinePoker.seats.Remote
    , CallBot = require('./bots/callBot')
    , FoldBot = require('./bots/foldBot')
    , RandBot = require('./bots/randBot')
    , MemoryBot = require('./bots/wrapperBot')('potOddsBot.py', 'Memory Bot')
    , RandBot2 = require('./bots/wrapperBot')('randBot2.py', 'RandBot2')
    //, OptimistBot = require('./bots/wrapperBot')('optimistBot.py', 'OptimistBot')
    //, PessmistBot = require('./bots/wrapperBot')('pessimistBot.py', 'PessmistBot')
    , WizardBot = require('./bots/wrapperBot')('wizardBot.py', 'WizardBot')
    , MemoryBot = require('./bots/wrapperBot')('potOddsBot.py', 'Memory Bot')
    , fileLogger = MachinePoker.observers.fileLogger('./examples/results.json')
    , fs = require('fs');

// Functions to generate a GUID
// Used to generate a short random string to be used in guid()
function S4() {
    return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
};

// Used to generate a unique random string to be used
// as a globally unique ID
function guid() {
    return S4() + S4() + "-" + S4() + "-" + S4() + "-" + S4() +  "-" + S4() + S4() + S4();
}

// Number of games to run against each opponent
var gamesToRun = 10;

// This is going to be a tournament, so generate an array of possible opponents
var opponents = [CallBot, RandBot, OptimistBot, PessmistBot];
var winChance = {'CallBot':0, 'RandBot':0 , 'OptimistBot':0, 'PessmistBot':0};
var completedGames = 0;
var cachedCompletedGames = 0;

// TODO: the libraries aren't synchronous. Make this code asynchronous
console.log("Beginning Tournament Now!");
for (var i = 0; i < opponents.length; i += 1) {

	// Run a configurable number of games against each opponent
	for (var j = 0; j < gamesToRun; j += 1) {

		// Generate the array of players in the game, which will just be our player and 
		// the ith member of the opponents array
		var players = [LocalSeat.create(MemoryBot), LocalSeat.create(opponents[i])];

		var gameEndCallback = function gameEndCallback(enemyName, win) {
			completedGames += 1;

			// If we have more than 1000 chips, we won the game
			if (win) {
				winChance[enemyName] += 1;
			}

			// Otherwise, we're done
			console.log(winChance);
		};

		//var fileLoggerTwo = MachinePoker.observers.fileLogger(resultFileName);
		// Generate a new table
		var table = MachinePoker.create({
	  		maxRounds: 100,
	  		gameID: "poker" + guid()
		});

		// Add the players to the table
		table.addPlayers(players);

		// When this tournament is over, process the results
		table.on('tournamentClosed', gameEndCallback);
		/*if (i == 0 && j == 0) {
			table.addObserver(fileLogger);
		}*/

		//table.addObserver(fileLoggerTwo);

		// Run the game

		console.log("Starting game " + j + " against " + LocalSeat.create(opponents[i]).player.info.name);
	  	table.start();
	}
}


function printResults() {
	if (completedGames >= (gamesToRun * opponents.length)) {

		var resultsFileName = __dirname + '/results.json';

		var gameResults = "Memory Bot Win Rate Against: \n\n";

		for (var i = 0; i < opponents.length; i += 1) {
			var name = LocalSeat.create(opponents[i]).name;
			gameResults += name + ": ";
			gameResults += ( (winChance[name] / gamesToRun) * 100 ) + "%\n";
		}
		console.log(gameResults);
		fs.writeFileSync(resultsFileName, gameResults);
		var endTime = new Date();
		var timeLog = endTime - startTime;
		console.log("It took: " + (timeLog / 1000) + " seconds to run!");
		process.exit();
	} else {
		if (completedGames != cachedCompletedGames) {
			cachedCompletedGames += 1;
			console.log("Completed " + completedGames + " out of " + (gamesToRun * opponents.length) + " games!");
		}
	}
}

setInterval(printResults, 100);
