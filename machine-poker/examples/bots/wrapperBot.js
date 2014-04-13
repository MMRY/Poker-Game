module.exports = function(varA, varB) {

    // Used to generate a short random string to be used in guid()
    function S4() {
        return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
    };

    // Used to generate a unique random string to be used
    // as a globally unique ID
    function guid() {
        return S4() + S4() + "-" + S4() + "-" + S4() + "-" + S4() +  "-" + S4() + S4() + S4();
    }

    // Return a function that generates an object with info and update components
    return function() {
        //console.log(varA);
        //console.log(varB);

        var fileName = varA;
        var botName = varB;

        // This is an info block for the bot
        // The only mandatory field is name, which is the name of the AI agent
        var info = { "name": botName };

        // This function is called whenever the AI needs to make a move
        // Returns the integer value that the agent wants to bet
        function update(game) {
            // If the game is complete, we don't need to update
            //if (game.state !== "complete") {

                // Require execSync so we can call the python AI code
                var execSync = require('execSync');

                // Require the file system so that we can write the temp game json
                var fs = require('fs');

                // Generate the name of the temp game json file
                // Use a GUID so that there's no risk of collision
                var gameFileName = __dirname + '/game' + guid() + '.json';

                // Turn the game info into a string to be written to the temp file
                var gameInfo = JSON.stringify(game);

                // Write the data to the file synchronously to avoid hiccups
                // and excessive callbacks
                fs.writeFileSync(gameFileName, gameInfo);

                // Properly parse the name of the file for the AI agent
                var botFileName = __dirname + '/' + fileName;

                // Generate the command to be used to run the agent
                var command = 'python ' + botFileName + ' ' + gameFileName;

                //console.log(gameFileName);
                //console.log(botFileName);
                //console.log(command);
                //console.log(this);

                // Run the AI agent
                var python = execSync.exec(command);

                // Clean up the game json temp file
                fs.unlinkSync(gameFileName);

                // Initialize the bet to -10, so we'll know if something
                // goes wrong in the agent module
                var bet = -10;

                if (python.code == 0) {
                    // Pull the bet from the python process's stdout
                    var tempBet = python.stdout.trim();

                    // Only use the result of the python module if it is at least 0
                    // TODO: Check for non-numerics?
                    if (tempBet >= 0) {
                        bet = tempBet;
                    }
                } else {
                    // An error has occurred with the interface
                    // Print the error
                    console.log("ERROR: " + python.code);
                }

                return bet;
            //}
        };

        return { update: update, info: info };
    };
}