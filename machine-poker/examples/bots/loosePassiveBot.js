module.exports = function () {

  var info = {
    name: "LoosePassiveBot"
  };

  function update(game) {
    if (game.state !== "complete") {
      return game.betting.call
    }
  };

  return { update: update, info: info }

}
