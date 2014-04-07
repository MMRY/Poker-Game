var MachinePoker = require('../lib/index')
    , LocalSeat = MachinePoker.seats.JsLocal
    , RemoteSeat = MachinePoker.seats.Remote
    , CallBot = require('./bots/callBot')
    , RandBot = require('./bots/randBot')
    , WrapperBot = require('./bots/wrapperBot')
    , narrator = MachinePoker.observers.narrator
    , fileLogger = MachinePoker.observers.fileLogger('./examples/results.json');

var table = MachinePoker.create({
  maxRounds: 100
});


  var players = [LocalSeat.create(RandBot), LocalSeat.create(WrapperBot)];
  table.addPlayers(players);
  table.on('tournamentClosed', function (a, b) { process.exit() } );
  table.start();

// Add some observers
table.addObserver(narrator);
table.addObserver(fileLogger);

