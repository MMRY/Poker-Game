Poker-Game
==========


Run Instructions:

Install the latest version of NodeJs

Checkout the Poker-Game Repository

cd to the machine-poker directory

Run the command "npm install execSync" (There is a known issue where not manually installing this module will cause an incorrect version to be used by Node)

While in the machine-poker directory:

Run "node examples/game.js" to run a sample game with a Narrator between our Agent and a testing Bot
 - The default testing bot is: WizardBot
 - You can change the testing bot in game.js by replacing "WizardBot" in "LocalSeat.create(WizardBot)" with the name of one of the testing bots from the top

Run "node examples/tournament.js" to run a sample tournament between our Agent and a variety of testing bots
- This will run a default of 10 (configurable) games against EACH of its opponent bots and return the win rate against each bot at the end




