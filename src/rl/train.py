import os
import signal
import threading
import sys

from lugo4py import TeamSide
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ..my_bot import MyBot
from .training_function import my_training_function
from lugo4py.rl import ThreadPoolExecutor, Gym

from .bot_trainer import MyBotTrainer

grpc_address = "localhost:5000"
slow_speed = False

stop = threading.Event()

if __name__ == "__main__":
    gym_executor = ThreadPoolExecutor()

    # Now we can create the Gym, which will control all async work and allow us to focus on the learning part
    gym = Gym(gym_executor, grpc_address)

    bot = MyBotTrainer(5, gym.remote)
    # gym.create_team_bots(TeamSide.HOME, lambda conf: MyBot(
    #     conf.get_bot_team_side(),
    #     conf.get_bot_number(),
    #     conf.get_initial_position(),
    #     conf.get_mapper()
    # ))

    # gym.create_team_bots(TeamSide.AWAY, lambda conf: MyBot(
    #     conf.get_bot_team_side(),
    #     conf.get_bot_number(),
    #     conf.get_initial_position(),
    #     conf.get_mapper()
    # ))

    gym.start(bot, my_training_function, slow_speed)

    def signal_handler(_, __):
        print("Stop requested\n")
        stop.set()
        gym_executor.shutdown(wait=True, cancel_futures=True)
        print("All stopped\n")

    signal.signal(signal.SIGINT, signal_handler)
    stop.wait()
