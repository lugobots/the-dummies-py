# Lugo - The Dummies Py

The Dummies PY is a Python implementation of a player (bot) for [Lugo](https://lugobots.dev) game.

This bot was made using the [Python Client Player](https://github.com/lugobots/lugo4py).

Use this bot as a starting point to a new one. 

## Dependencies

* Docker ([https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/))
* Docker Compose ([https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/))


### (optional) Dependencies for IDE intellisense 

You must install the projects requirements if you want to have the IDE intellisense working correctly in your environment.

### On Windows
1. Download the Python 3.9 installer [https://www.python.org/downloads/release/python-3912/](https://www.python.org/downloads/release/python-3912/)
2. On the Python installing wizard, remember to check the option to install the **Pip** tool
3. On the project directory, run:
```
pip install virtualenv
python.exe -m venv venv
pip install -r requirements.txt

```

### On Linux or Mac
```shell
cd /path/to/your/project
sudo apt install python3.9-venv
python3.9 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

### Configure VS Code

1. `ctrl + p`
2. "Python: Create Environment"
3. Venv
4. Select Python3.9 

#### Configure IntellyJ IDE family (PyCharm, Idea, and others)

(see [https://www.jetbrains.com/help/idea/configuring-local-python-interpreters.html](https://www.jetbrains.com/help/idea/configuring-local-python-interpreters.html))

1. Click on File
2. Project Structure
3. Click on Project
4. Select Python3.9 in the SDK list

The IDE will ask you if you want to install the dependencies. 

## Are you familiar with Lugo? 
If not, before continuing, please visit [the project website](https://lugobots.dev) and read about the game.

## Quick setup (if you do not want to download or clone the code)

You may use the [SetupEnvPy](https://hub.docker.com/r/lugobots/setup-env-py) Docker image to set up the environment for you:

## How to use this source code
1. (optional to speed up next steps) Download the images that you will need
   ```shell
   docker pull lugobots/server
   docker pull lugobots/the-dummies-go:latest
   docker pull python:3.9-slim-buster
   ```
2. Run the builder service that will install the depencencies you need (**wait for the service to finish**):
   ```sell 
   docker compose up builder
   ```
3. **Test it out**: Before any change, make the Dummies Py play to ensure you are not working on a broken code.

   ```shell 
   docker compose up
   ```
   and open [http://localhost:8080/](http://localhost:8080/) to watch the game.
4. **Now, make your changes**: (see :question:[How to change the bot](#how-to-edit-the-bot))
5. Play again to see your changes results: 

   ```sh 
   docker compose up
   ```
6. **Are you ready to compete? Build your Docker image:** 
    
    ```sh 
   docker build -f .lugo/Dockerfile -t repo.lugobots.ai/[bot handle]:[version] .
   ```

## How to edit the bot   

### Main file [main.py](src/main.py)

You will not change this file. It only initializes the bot.

### Settings file [settings.py](src/settings.py)

Settings file only stores configurations that will affect the player behaviour, e.g. positions, tactic, etc.

### My bot [my_bot.py](src/my_bot.py)

:eyes: This is the most important file!

There will be 5 important methods that you must edit to change the bot behaviour.

```python
    def on_disputing(self, inspector: GameSnapshotInspector) -> List[Order]:
        # on_disputing is called when no one has the ball possession
        pass

    @abstractmethod
    def on_defending(self, inspector: GameSnapshotInspector) -> List[Order]:
        # OnDefending is called when an opponent player has the ball possession
        pass

    @abstractmethod
    def on_holding(self, inspector: GameSnapshotInspector) -> List[Order]:
        # OnHolding is called when this bot has the ball possession
        pass

    @abstractmethod
    def on_holding(self, inspector: GameSnapshotInspector) -> List[Order]:
        # OnSupporting is called when a teammate player has the ball possession
        pass

    @abstractmethod
    def as_goalkeeper(self, inspector: GameSnapshotInspector, state: PLAYER_STATE) -> List[Order]:
        # AsGoalkeeper is only called when this bot is the goalkeeper (number 1). This method is called on every turn,
        # and the player state is passed at the last parameter.
        pass

    @abstractmethod
    def getting_ready(self, inspector: GameSnapshotInspector):
        # getting_ready will be called before the game starts and after a goal event. You will only need to implement
        # this method in very rare cases.
        pass
```

## Running directly in your machine (:ninja: advanced) 

If you want to run the Python code in your machine instead of inside the container, you definitely can do this.

The command to start locally is `BOT_TEAM=home BOT_NUMBER=1 python3.9 main.py`. However, when you run the Docker compose 
file, all players from both teams will start. Then, if you run another bot directly from your machine, it will not
be allowed to join the game.

But you also cannot start your bot before the game server has started.

You have two options to run your bot locally.

### Option 1 - comment out the bot from the Docker compose file

You can edit the file `docker-compose.yml` and comment out the player 2 of the home team.

The game server will wait all 11 players from both teams to connect before starting the game.

### Option 2 - starting the game server first

You can start _only_ the game server with the command `docker compose up -d game_server`. The game will wait for the players. Then, you
start your local bot (`BOT_TEAM=home BOT_NUMBER=1 python3.9 main.py`), and finally start the rest of the players with the
command `docker compose up`