module.exports = function () {

  var info = {
    name: "Memory Bot Mark III"
  };

  function update(game) {

    // Ok, it looks like I'm going to have to make a temp file to hold the json
    if (game.state !== "complete") {
      var sh = require('execSync');
      var fs = require('fs');

      var tempName = __dirname + '\\game.json';


      // arg will be the stringified game JSON
      var gameString = JSON.stringify(game);

      // Write the game state data to a file
      fs.writeFileSync(tempName, gameString);

      // We have to have the name of the python script as the first argument in the array
      var nameString = __dirname + '\\MemoryBot.py';

      var commandString = 'python ' + nameString + ' ' + tempName;
     
      var python = sh.exec(commandString);

      // Delete the file
      fs.unlinkSync(tempName);

      var bet = -10;
      if (python.code == 0){
        var bet = python.stdout.trim();
        if (bet >= 0) {
          return bet;
        }
      } else {
        console.log("ERROR: " + python.code);
      }

      return 0;
    }
  };

  return { update: update, info: info };

};
