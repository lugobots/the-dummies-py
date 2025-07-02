# Bot Trainer (Reinforcement learning)

# Start the training session

## Start the Game server

You _may_ run the server as a container, but it will be considerably slower than running the binary.

### Using the binary

You may download the game server binary from https://hub.docker.com/repository/docker/lugobots/server/general (the 
links are on the description session).

!!**IMPORTANT**!! Download the version `v2.4-rc.1` or greater!!

Save the binary anywhere, and execute it passing `gym` as a param:
```
# On Linux
./LugoServer_v2.4-rc.1_Linux-amd64 gym
```

### Using the container

Start the server using a Container:
!!**IMPORTANT**!! Download the version `v2.4-rc.1` or greater!!

`docker run -p 5000:5000 -p 8080:8080 lugobots/server:v2.4-rc.2 gym`

## Start the training session

1. Create the virtual environment using the setup script (see bot readme)
2. Install the dependencies: `venv/bin/pip install -r requirements.txt`
   This step will take a while, go watch a 3 hours movie or a match of Cricket
3. Start the training:
   `venv/bin/python3.9 -m src.rl.train`