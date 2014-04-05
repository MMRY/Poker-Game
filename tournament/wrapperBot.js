module.exports = function () {

  // TODO: Get documentation for this function.
  function S4() {
      return (((1 + Math.random()) * 0x10000) | 0)
          .toString(16)
          .substring(1);
  };

  // Generates an RFC-4122 compliant GUID.  Because.
  // TODO: Get documentation for this function.
  function guid () {
      return S4() + S4() + "-" + S4() + "-" + S4() + "-" + S4() +
          "-" + S4() + S4() + S4();
  };

  var info = {
    name: "Memory Bot"
  };

  function update(game) {

    // Ok, it looks like I'm going to have to make a temp file to hold the json
    if (game.state !== "complete") {
      var sh = require('execSync');
      var fs = require('fs');

      // Generated a GUID for the game file, to avoid concurrent games overwriting each other
      var tempName = __dirname + '\\game' + guid() + '.json';


      // arg will be the stringified game JSON
      var gameString = JSON.stringify(game);

      // Write the game state data to a file
      fs.writeFileSync(tempName, gameString);

      // We have to have the name of the python script as the first argument in the array
      var nameString = __dirname + '\\ai.py';

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
