var MachinePoker = require('../lib/index')
    , LocalSeat = MachinePoker.seats.JsLocal
    , RemoteSeat = MachinePoker.seats.Remote
    , LoosePassiveBot = require('./bots/loosePassiveBot')
    , TightPassiveBot = require('./bots/tightPassiveBot')
    , RandBot = require('./bots/randBot')
    , MemoryBot = require('./bots/wrapperBot')('potOddsBot.py', 'Memory Bot')
    , LooseAgressiveBot = require('./bots/wrapperBot')('looseAgressiveBot.py', 'LooseAgressiveBot')
    , OptimistBot = require('./bots/wrapperBot')('optimistBot.py', 'OptimistBot')
    , PessimistBot = require('./bots/wrapperBot')('pessimistBot.py', 'PessmistBot')
    , WizardBot = require('./bots/wrapperBot')('wizardBot.py', 'WizardBot')
    , MemoryBot = require('./bots/wrapperBot')('potOddsBot.py', 'Memory Bot')
    , narrator = MachinePoker.observers.narrator
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

var table = MachinePoker.create({
  maxRounds: 100,
  gameID: "poker" + guid()
});


  var players = [LocalSeat.create(MemoryBot), LocalSeat.create(PessimistBot)];
  table.addPlayers(players);
  table.on('tournamentClosed', function (a, b) { 
      // Delete the data file
      var deleteFileName = "data_" + this.gameID;
      if (fs.existsSync(deleteFileName)) {
          fs.unlinkSync(deleteFileName);
      }
      process.exit();
  });
  table.start();

// Add some observers
table.addObserver(narrator);
table.addObserver(fileLogger);

