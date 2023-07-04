# Lugo - The Dummies Py

The Dummies Py is a Python implementation of a player (bot) for [Lugo](https://lugobots.dev) game.

This bot was made using the [Python Client Player](https://github.com/lugobots/lugo4py).

Use this bot as a starting point to a new one. 

## Dependencies

* Docker ([https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/))
* Docker Compose ([https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/))
* Python 3.8.10 or greater

## Before starting

Are you familiar with Lugo? 
If not, before continuing, please visit [the project website](https://lugobots.dev) and read about the game.

## How to use this source code

1. **Checkout the code** or download the most recent tag release
2. Initialize your venv `virtualenv venv --python=python3.9` 
3. Install the requirements `pip install -r requirements.txt`
2. **Test it out**: Before any change, make the Dummies JS play to ensure you are not working on a broken code.

   ```sh 
   docker compose up
   ```
   and open [http://localhost:8080/](http://localhost:8080/) to watch the game.
3. **Now, make your changes**: (see :question:[How to change the bot](#how-to-edit-the-bot))
4. Play again to see your changes results: 

   ```sh 
   docker compose up
   ```
5. **Are you ready to compete? Build your Docker image:** 
    
    ```sh 
   docker build -t my-super-bot .
   ```
6. :checkered_flag: Before pushing your changes

    On Linux
   ```sh 
   MY_BOT=my-super-bot 
   docker compose --file docker-compose.yml -p tester up
   ```

    On Windows
   ```sh 
   $Env:MY_BOT = "my-super-bot"
   docker compose --file docker-compose.yml -p tester up
   ```

## How to edit the bot   

### Main file [src/main.py](src/main.py)

You probably will not change this file. It only initializes the bot.

### My bot [src/my_bot.py](./src/my_bot.py)

:eyes: This is the most important file!

There will be 5 important methods that you must edit to change the bot behaviour.

```python

    def onDisputing (self, orderSet: lugo4py.OrderSet, snapshot: GameSnapshot)
    
    def onDefending (self, orderSet: OrderSet, snapshot: GameSnapshot)

    def onHolding (self, orderSet: OrderSet, snapshot: GameSnapshot) 
    
    def onSupporting (self, orderSet: OrderSet, snapshot: GameSnapshot)

    def asGoalkeeper (self, orderSet: OrderSet, snapshot: GameSnapshot, state: PLAYER_STATE)
```

## Running directly in your machine (:ninja: advanced) 

If you want to run the Python code in your machine instead of inside the container, you definitely can do this.

The command to start locally is `LUGO_LOCAL=true npm run start`. However, when you run the Docker compose 
file, all players from both teams will start. Then, if you run another bot directly from your machine, it will not
be allowed to join the game.

But you also cannot start your bot before the game server has started.

You have two options to run your bot locally.

### Option 1 - comment out the bot from the Docker compose file

You can edit the file `docker-compose.yml` and comment out the player 2 of the home team.

The game server will wait all 11 players from both teams to connect before starting the game.

### Option 2 - starting the game server first

You can start _only_ the game server with the command `game_server`. The game will wait for the players. Then, you
start your local bot (`LUGO_LOCAL=true npm run start`), and finally start the rest of the players with the
command `docker compose up`